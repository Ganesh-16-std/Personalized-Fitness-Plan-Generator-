
import sqlite3, hashlib, secrets, time, random, json, os
import urllib.request, urllib.error, urllib.parse

BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
EMAIL_SENDER  = os.environ.get("EMAIL_SENDER", "noreply@fitpro.app")
SENDER_NAME   = "FitPro AI"
DB_PATH       = "/tmp/fitpro.db"

_conn = None

def _db():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY, email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL, token TEXT,
                created_at REAL, last_login REAL);
            CREATE TABLE IF NOT EXISTS otps (
                key TEXT PRIMARY KEY, otp TEXT NOT NULL,
                expires_at REAL NOT NULL,
                username TEXT, password_hash TEXT);
            CREATE TABLE IF NOT EXISTS profiles (
                username TEXT PRIMARY KEY, name TEXT, age INTEGER, gender TEXT,
                height REAL, weight REAL, goal TEXT, level TEXT,
                equipment TEXT, updated_at REAL);
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL,
                plan_text TEXT, days_total INTEGER, created_at REAL);
            CREATE TABLE IF NOT EXISTS tracking (
                username TEXT NOT NULL, date TEXT NOT NULL, day_idx INTEGER,
                status TEXT DEFAULT 'pending', PRIMARY KEY (username, date));
            CREATE TABLE IF NOT EXISTS water_intake (
                username TEXT NOT NULL, date TEXT NOT NULL,
                amount_ml INTEGER DEFAULT 0,
                goal_ml INTEGER DEFAULT 2500,
                PRIMARY KEY (username, date));
            CREATE TABLE IF NOT EXISTS diet_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL, date TEXT NOT NULL,
                meal_name TEXT NOT NULL,
                calories REAL DEFAULT 0, protein REAL DEFAULT 0,
                carbs REAL DEFAULT 0, fats REAL DEFAULT 0,
                fiber REAL DEFAULT 0, logged_at REAL);
            CREATE TABLE IF NOT EXISTS weight_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL, date TEXT NOT NULL,
                weight REAL NOT NULL, note TEXT DEFAULT '',
                logged_at REAL);
        """)
        # Upgrade older schemas safely
        for col_sql in [
            "ALTER TABLE otps ADD COLUMN username TEXT",
            "ALTER TABLE otps ADD COLUMN password_hash TEXT",
        ]:
            try:
                _conn.execute(col_sql); _conn.commit()
            except Exception:
                pass
    return _conn

def _hash(pw):  return hashlib.sha256(pw.encode()).hexdigest()
def _token():   return secrets.token_hex(32)
def _otp():     return str(random.randint(100000, 999999))

# ── User ops ──────────────────────────────────────────────────────────────────
def get_user(username_or_email):
    v = username_or_email.strip().lower()
    c = _db().execute(
        "SELECT * FROM users WHERE lower(username)=? OR lower(email)=?", (v, v)
    ).fetchone()
    return dict(c) if c else None

def get_user_by_username(username):
    c = _db().execute(
        "SELECT * FROM users WHERE lower(username)=?",
        (username.strip().lower(),)
    ).fetchone()
    return dict(c) if c else None

def get_user_by_email(email):
    c = _db().execute(
        "SELECT * FROM users WHERE lower(email)=?",
        (email.strip().lower(),)
    ).fetchone()
    return dict(c) if c else None

def create_user(username, email, password_hash_or_plain, already_hashed=False):
    token = _token()
    pw = password_hash_or_plain if already_hashed else _hash(password_hash_or_plain)
    _db().execute(
        "INSERT INTO users (username,email,password,token,created_at) VALUES (?,?,?,?,?)",
        (username.strip(), email.strip().lower(), pw, token, time.time())
    )
    _db().commit()
    return token

def update_user_token(username, token):
    _db().execute(
        "UPDATE users SET token=?,last_login=? WHERE lower(username)=?",
        (token, time.time(), username.lower())
    )
    _db().commit()

def logout_user(username):
    _db().execute(
        "UPDATE users SET token=NULL WHERE lower(username)=?", (username.lower(),)
    )
    _db().commit()

# ── Profile ops ───────────────────────────────────────────────────────────────
def save_profile(username, data: dict):
    _db().execute("""
        INSERT INTO profiles (username,name,age,gender,height,weight,goal,level,equipment,updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(username) DO UPDATE SET
          name=excluded.name, age=excluded.age, gender=excluded.gender,
          height=excluded.height, weight=excluded.weight, goal=excluded.goal,
          level=excluded.level, equipment=excluded.equipment, updated_at=excluded.updated_at
    """, (
        username, data.get("name",""), data.get("age",25), data.get("gender","Male"),
        data.get("height",170), data.get("weight",70), data.get("goal","Build Muscle"),
        data.get("level","Beginner"), json.dumps(data.get("equipment",[])), time.time()
    ))
    _db().commit()

def load_profile(username):
    c = _db().execute("SELECT * FROM profiles WHERE username=?", (username,)).fetchone()
    if not c:
        return None
    d = dict(c)
    try:
        d["equipment"] = json.loads(d.get("equipment") or "[]")
    except Exception:
        d["equipment"] = []
    return d

# ── Workout ops ───────────────────────────────────────────────────────────────
def save_workout(username, plan_text, days_total):
    _db().execute(
        "INSERT INTO workouts (username,plan_text,days_total,created_at) VALUES (?,?,?,?)",
        (username, plan_text, days_total, time.time())
    )
    _db().commit()

def load_latest_workout(username):
    c = _db().execute(
        "SELECT * FROM workouts WHERE username=? ORDER BY created_at DESC LIMIT 1",
        (username,)
    ).fetchone()
    return dict(c) if c else None

# ── Tracking ops ──────────────────────────────────────────────────────────────
def save_tracking(username, date_str, day_idx, status):
    _db().execute("""
        INSERT INTO tracking (username,date,day_idx,status) VALUES (?,?,?,?)
        ON CONFLICT(username,date) DO UPDATE SET
          status=excluded.status, day_idx=excluded.day_idx
    """, (username, date_str, day_idx, status))
    _db().commit()

def load_tracking(username):
    rows = _db().execute(
        "SELECT date,day_idx,status FROM tracking WHERE username=?", (username,)
    ).fetchall()
    return {r["date"]: {"day_idx": r["day_idx"], "status": r["status"]} for r in rows}

def delete_tracking(username):
    _db().execute("DELETE FROM tracking WHERE username=?", (username,))
    _db().commit()

# ── Water intake ops ──────────────────────────────────────────────────────────
def get_water_today(username, date_str):
    c = _db().execute(
        "SELECT amount_ml, goal_ml FROM water_intake WHERE username=? AND date=?",
        (username, date_str)
    ).fetchone()
    return dict(c) if c else {"amount_ml": 0, "goal_ml": 2500}

def add_water(username, date_str, amount_ml):
    _db().execute("""
        INSERT INTO water_intake (username, date, amount_ml, goal_ml)
        VALUES (?, ?, ?, 2500)
        ON CONFLICT(username, date) DO UPDATE SET
          amount_ml = amount_ml + ?
    """, (username, date_str, amount_ml, amount_ml))
    _db().commit()

def set_water_goal(username, date_str, goal_ml):
    _db().execute("""
        INSERT INTO water_intake (username, date, amount_ml, goal_ml)
        VALUES (?, ?, 0, ?)
        ON CONFLICT(username, date) DO UPDATE SET goal_ml=?
    """, (username, date_str, goal_ml, goal_ml))
    _db().commit()

def reset_water(username, date_str):
    _db().execute(
        "UPDATE water_intake SET amount_ml=0 WHERE username=? AND date=?",
        (username, date_str)
    )
    _db().commit()

def get_water_history(username, days=14):
    rows = _db().execute("""
        SELECT date, amount_ml, goal_ml FROM water_intake
        WHERE username=? ORDER BY date DESC LIMIT ?
    """, (username, days)).fetchall()
    return [dict(r) for r in rows]

# ── Diet log ops ──────────────────────────────────────────────────────────────
def log_diet(username, date_str, meal_name, calories=0, protein=0, carbs=0, fats=0, fiber=0):
    _db().execute("""
        INSERT INTO diet_log (username, date, meal_name, calories, protein, carbs, fats, fiber, logged_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, date_str, meal_name, calories, protein, carbs, fats, fiber, time.time()))
    _db().commit()

def get_diet_today(username, date_str):
    rows = _db().execute("""
        SELECT * FROM diet_log WHERE username=? AND date=? ORDER BY logged_at ASC
    """, (username, date_str)).fetchall()
    return [dict(r) for r in rows]

def delete_diet_entry(entry_id):
    _db().execute("DELETE FROM diet_log WHERE id=?", (entry_id,))
    _db().commit()

def get_diet_totals(username, date_str):
    c = _db().execute("""
        SELECT
            COALESCE(SUM(calories),0) as calories,
            COALESCE(SUM(protein),0)  as protein,
            COALESCE(SUM(carbs),0)    as carbs,
            COALESCE(SUM(fats),0)     as fats,
            COALESCE(SUM(fiber),0)    as fiber
        FROM diet_log WHERE username=? AND date=?
    """, (username, date_str)).fetchone()
    return dict(c) if c else {"calories":0,"protein":0,"carbs":0,"fats":0,"fiber":0}

# ── Weight log ops ────────────────────────────────────────────────────────────
def log_weight(username, date_str, weight_kg, note=""):
    # upsert — one entry per day
    _db().execute("""
        INSERT INTO weight_log (username, date, weight, note, logged_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT DO NOTHING
    """, (username, date_str, weight_kg, note, time.time()))
    # if already exists, update it
    _db().execute("""
        UPDATE weight_log SET weight=?, note=?, logged_at=?
        WHERE username=? AND date=?
    """, (weight_kg, note, time.time(), username, date_str))
    _db().commit()

def get_weight_history(username, limit=24):
    rows = _db().execute("""
        SELECT date, weight, note FROM weight_log
        WHERE username=? ORDER BY date ASC LIMIT ?
    """, (username, limit)).fetchall()
    return [dict(r) for r in rows]

def get_latest_weight(username):
    c = _db().execute("""
        SELECT weight, date FROM weight_log WHERE username=?
        ORDER BY date DESC LIMIT 1
    """, (username,)).fetchone()
    return dict(c) if c else None

# ── OTP ops ───────────────────────────────────────────────────────────────────
def store_otp(email, otp, username="", password_plain=""):
    key = f"signup:{email.strip().lower()}"
    pw_hash = _hash(password_plain) if password_plain else ""
    _db().execute("""
        INSERT INTO otps(key,otp,expires_at,username,password_hash)
        VALUES(?,?,?,?,?)
        ON CONFLICT(key) DO UPDATE SET
          otp=excluded.otp, expires_at=excluded.expires_at,
          username=excluded.username, password_hash=excluded.password_hash
    """, (key, otp, time.time() + 600, username, pw_hash))
    _db().commit()

def check_otp(email, otp_input):
    key = f"signup:{email.strip().lower()}"
    c = _db().execute("SELECT * FROM otps WHERE key=?", (key,)).fetchone()
    if not c:
        return False, "Code not found. Please sign up again.", "", ""
    if time.time() > c["expires_at"]:
        _db().execute("DELETE FROM otps WHERE key=?", (key,)); _db().commit()
        return False, "Code expired. Please sign up again.", "", ""
    if c["otp"] != otp_input.strip():
        return False, "Incorrect code. Try again.", "", ""
    username = c["username"] or ""
    pw_hash  = c["password_hash"] or ""
    _db().execute("DELETE FROM otps WHERE key=?", (key,)); _db().commit()
    return True, "OK", username, pw_hash

# ── Email ─────────────────────────────────────────────────────────────────────
def send_otp_email(to_email, otp):
    if not BREVO_API_KEY:
        return True, "__NO_EMAIL__"
    html = f"""<div style="background:#0a0a0f;padding:40px;font-family:system-ui;
      max-width:520px;margin:auto;border-radius:16px">
      <div style="text-align:center;margin-bottom:28px">
        <div style="font-size:28px;font-weight:900;color:#6366f1">FITPRO AI</div>
      </div>
      <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.25);
        border-radius:12px;padding:28px;text-align:center">
        <div style="font-size:48px;font-weight:900;letter-spacing:14px;color:#6366f1">{otp}</div>
      </div>
      <p style="color:rgba(255,255,255,0.4);font-size:12px;text-align:center;margin-top:20px">
        Expires in 10 minutes.</p></div>"""
    payload = json.dumps({
        "sender": {"name": SENDER_NAME, "email": EMAIL_SENDER},
        "to": [{"email": to_email}],
        "subject": f"FitPro AI — Your code: {otp}",
        "htmlContent": html,
    }).encode()
    req = urllib.request.Request(
        "https://api.brevo.com/v3/smtp/email", data=payload,
        headers={"accept":"application/json","api-key":BREVO_API_KEY,
                 "content-type":"application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return (r.status in (200,201,202)), "Sent"
    except Exception as e:
        return False, str(e)

# ── Auth flows ────────────────────────────────────────────────────────────────
def initiate_signup(username, email, password):
    username = username.strip()
    email    = email.strip().lower()
    if get_user_by_username(username):
        return False, "Username already taken.", None
    if get_user_by_email(email):
        return False, "Email already registered.", None
    if len(password) < 6:
        return False, "Password must be at least 6 characters.", None
    if not BREVO_API_KEY:
        token = create_user(username, email, password)
        return True, "__DIRECT__", token
    otp = _otp()
    ok, msg = send_otp_email(email, otp)
    if not ok:
        return False, msg, None
    store_otp(email, otp, username=username, password_plain=password)
    return True, "__OTP__", None

def complete_signup(email, otp_input):
    ok, msg, username, pw_hash = check_otp(email, otp_input)
    if not ok:
        return False, None, msg
    if not username or not pw_hash:
        return False, None, "Session data missing. Please sign up again."
    token = create_user(username, email, pw_hash, already_hashed=True)
    return True, token, username

def login(username_or_email, password):
    u = get_user(username_or_email)
    if not u:
        return False, None, None, "Account not found."
    if u["password"] != _hash(password):
        return False, None, None, "Incorrect password."
    token = _token()
    update_user_token(u["username"], token)
    return True, token, u["username"], "Welcome back!"
