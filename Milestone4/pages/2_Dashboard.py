import streamlit as st
import sys, os, re
from datetime import date, timedelta, datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth import (load_profile, load_tracking, delete_tracking,
                         logout_user, save_profile, load_latest_workout,
                         save_tracking, _db)
from utils.ai import calculate_bmi, bmi_category, get_exercise_description
from utils.ui import (inject_css, section_header, stat_card, exercise_card,
                      progress_ring, calendar_widget, badge)

st.set_page_config(page_title="FitPro AI — Dashboard", page_icon="⚡",
                   layout="wide", initial_sidebar_state="expanded")

if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

inject_css()
username    = st.session_state.get("username", "Athlete")
profile     = load_profile(username)
tracking    = load_tracking(username)
today_str   = date.today().isoformat()
workout_rec = load_latest_workout(username)
plan_text   = workout_rec["plan_text"] if workout_rec else ""
days_total  = workout_rec["days_total"] if workout_rec else 0

# ── Parse day blocks ───────────────────────────────────────────────────────────
day_blocks, current = [], []
for line in plan_text.split("\n"):
    s = line.strip()
    if (re.match(r"^#{1,3}\s*day\s*\d", s, re.I) or re.match(r"^day\s*\d", s, re.I)) and current:
        day_blocks.append("\n".join(current)); current = [line]
    else:
        current.append(line)
if current and plan_text:
    day_blocks.append("\n".join(current))

num_days      = len(day_blocks) if day_blocks else max(days_total, 1)
done_count    = sum(1 for v in tracking.values() if v.get("status") == "done")
skipped_count = sum(1 for v in tracking.values() if v.get("status") == "skipped")
pct           = int(done_count / num_days * 100) if num_days else 0

# Streak calculation
streak = 0
check  = date.today()
for _ in range(365):
    if tracking.get(check.isoformat(), {}).get("status") == "done":
        streak += 1; check -= timedelta(days=1)
    else:
        break

today_idx    = done_count % num_days if num_days else 0
today_block  = day_blocks[today_idx] if day_blocks else ""
today_status = tracking.get(today_str, {}).get("status", "pending")

def get_day_title(blk):
    for line in blk.split("\n"):
        s = line.strip()
        if s:
            return re.sub(r"^#+\s*", "", s).upper()
    return "WORKOUT"

def parse_exercises(block):
    exs, idx = [], 0
    ICONS = ["🏋️","💪","🔄","🦵","⬆️","🤸","🏃","🥊","🧗","🚴","🔥","⚡","🎯","🌀"]
    for line in block.split("\n"):
        s = line.strip()
        if not s or re.match(r"^#+", s): continue
        if re.match(r"^[-•*]\s+", s) or re.match(r"^\d+\.\s+", s):
            content = re.sub(r"^[-•*\d\.]+\s*", "", s)
            content = re.sub(r"\*\*(.+?)\*\*", r"\1", content)
            m = re.search(r"(\d+)\s*[xX×]\s*(\d+(?:[-–]\d+)?)\s*(?:reps?)?\s*(?:.*?rest\s*(\d+)\s*s)?", content, re.I)
            if m:
                sets, reps = m.group(1), m.group(2)
                rest = (m.group(3)+"s") if m.group(3) else "60s"
            else:
                m2 = re.search(r"(\d+)\s*[xX×]\s*(\d+)", content)
                sets, reps, rest = (m2.group(1), m2.group(2), "60s") if m2 else (None, None, None)
            name = re.split(r"[\-—–:,]|\d+\s*[xX×]", content)[0].strip() or content[:40]
            desc = get_exercise_description(name)
            exs.append({"icon": ICONS[idx % len(ICONS)], "name": name,
                        "sets": sets, "reps": reps, "rest": rest, "desc": desc})
            idx += 1
    return exs

today_title     = get_day_title(today_block) if today_block else f"DAY {today_idx+1}"
today_exercises = parse_exercises(today_block)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
      display:block!important;
      background:#070710!important;
      border-right:1px solid rgba(99,102,241,0.14)!important;
      min-width:268px!important; max-width:288px!important;
    }
    section[data-testid="stSidebar"] > div { padding:0!important; }
    [data-testid="collapsedControl"] { display:none!important; }
    </style>""", unsafe_allow_html=True)

    name_d   = profile.get("name", username) if profile else username
    age_v    = profile.get("age", "—") if profile else "—"
    weight_v = profile.get("weight", "—") if profile else "—"
    height_v = profile.get("height", "—") if profile else "—"
    goal_v   = profile.get("goal", "—") if profile else "—"
    level_v  = profile.get("level", "—") if profile else "—"
    bmi_v = bmi_cat_v = "—"
    if profile and profile.get("weight") and profile.get("height"):
        bmi_v     = calculate_bmi(profile["weight"], profile["height"])
        bmi_cat_v = bmi_category(bmi_v)
    bmi_color = {"Underweight":"#f59e0b","Normal Weight":"#10d9a0",
                 "Overweight":"#f97316","Obese":"#f43f5e"}.get(bmi_cat_v,"#6366f1")

    # Avatar & name
    initials = "".join(w[0].upper() for w in name_d.split()[:2]) or "FP"
    st.markdown(f"""
    <div style="padding:28px 18px 18px;border-bottom:1px solid rgba(99,102,241,0.10)">
      <div style="width:62px;height:62px;border-radius:50%;
        background:linear-gradient(135deg,#6366f1,#a78bfa);
        display:flex;align-items:center;justify-content:center;
        font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;
        color:#fff;margin:0 auto 12px;
        box-shadow:0 0 0 3px rgba(99,102,241,0.20),0 0 20px rgba(99,102,241,0.25)">{initials}</div>
      <div style="text-align:center">
        <div style="font-family:'Syne',sans-serif;font-size:1.0rem;font-weight:700;
          color:#f0eeff">{name_d}</div>
        <div style="font-size:0.62rem;color:rgba(240,238,255,0.30);margin-top:3px;
          letter-spacing:1.5px;text-transform:uppercase">@{username}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # BMI display
    if bmi_v != "—":
        st.markdown(f"""
        <div style="margin:14px 18px 0;padding:12px;background:{bmi_color}12;
          border:1px solid {bmi_color}30;border-radius:12px;text-align:center">
          <div style="font-size:0.55rem;letter-spacing:2.5px;text-transform:uppercase;
            color:{bmi_color};font-weight:700;margin-bottom:4px">BMI Score</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
            color:{bmi_color};line-height:1">{bmi_v}</div>
          <div style="font-size:0.68rem;color:{bmi_color};opacity:0.75;margin-top:2px">{bmi_cat_v}</div>
        </div>""", unsafe_allow_html=True)

    # Profile stats
    st.markdown("""<div style="padding:14px 18px 0">
      <div style="font-size:0.55rem;font-weight:700;letter-spacing:2.5px;
        text-transform:uppercase;color:rgba(240,238,255,0.22);margin-bottom:10px">
        Profile Stats</div>""", unsafe_allow_html=True)

    def _srow(label, val, unit=""):
        return f"""<div style="display:flex;justify-content:space-between;align-items:center;
          padding:7px 10px;background:rgba(255,255,255,0.025);border-radius:8px;margin-bottom:4px">
          <span style="font-size:0.73rem;color:rgba(240,238,255,0.35)">{label}</span>
          <span style="font-size:0.82rem;font-weight:600;color:#f0eeff">{val}{' '+unit if unit else ''}</span>
        </div>"""

    st.markdown(
        _srow("Age", age_v, "yrs") +
        _srow("Height", height_v, "cm") +
        _srow("Weight", weight_v, "kg") +
        _srow("Goal", goal_v) +
        _srow("Level", level_v),
        unsafe_allow_html=True
    )

    # Recent activity
    st.markdown("""<div style="margin-top:14px;font-size:0.55rem;font-weight:700;letter-spacing:2.5px;
      text-transform:uppercase;color:rgba(240,238,255,0.22);margin-bottom:8px">
      Recent Activity</div>""", unsafe_allow_html=True)

    recent = sorted(tracking.keys(), reverse=True)[:5]
    if recent:
        for d in recent:
            s = tracking[d].get("status", "pending")
            ic = "✅" if s=="done" else ("⏭️" if s=="skipped" else "⏳")
            cl = "#10d9a0" if s=="done" else ("#f59e0b" if s=="skipped" else "#6366f1")
            try: df = datetime.strptime(d, "%Y-%m-%d").strftime("%b %d")
            except: df = d
            st.markdown(f"""<div style="display:flex;align-items:center;gap:8px;
              padding:6px 8px;background:rgba(255,255,255,0.025);border-radius:7px;margin-bottom:4px">
              <span style="font-size:0.80rem">{ic}</span>
              <span style="flex:1;font-size:0.75rem;color:#f0eeff">{df}</span>
              <span style="font-size:0.58rem;color:{cl};font-weight:700;
                text-transform:uppercase;letter-spacing:1px">{s}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:0.73rem;color:rgba(240,238,255,0.22);text-align:center;padding:10px 0">No activity yet</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(99,102,241,0.10);margin:12px 0'>", unsafe_allow_html=True)
    st.markdown("<div style='padding:8px 18px 16px;display:flex;flex-direction:column;gap:5px'>", unsafe_allow_html=True)

    if st.button("✏️ Edit Profile", use_container_width=True, key="edit_p"):
        st.session_state.show_edit = True
    if st.button("📋 Full Plan", use_container_width=True, key="full_p"):
        st.switch_page("pages/3_Plan.py")
    if st.button("⚡ New Plan", use_container_width=True, key="new_p"):
        st.switch_page("pages/4_Create_Plan.py")
    st.markdown("</div>", unsafe_allow_html=True)

# ── TOPNAV ─────────────────────────────────────────────────────────────────────
hour  = datetime.now().hour
greet = "Good Morning" if hour < 12 else ("Good Afternoon" if hour < 18 else "Good Evening")

st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
  padding:18px 0 14px;border-bottom:1px solid rgba(99,102,241,0.12);margin-bottom:30px">
  <div style="font-family:'Syne',sans-serif;font-size:1.50rem;font-weight:800;
    background:linear-gradient(135deg,#6366f1,#a78bfa);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-0.5px">
    ⚡ FitPro AI</div>
  <div style="font-size:0.92rem;color:rgba(240,238,255,0.50)">
    {greet}, <strong style="color:#f0eeff;font-weight:700">{username}</strong> 👋
  </div>
  <div style="font-size:0.62rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
    padding:5px 14px;border:1px solid rgba(99,102,241,0.28);border-radius:100px;
    color:#818cf8;background:rgba(99,102,241,0.06)">Dashboard</div>
</div>
""", unsafe_allow_html=True)

_, prof_col, so_col = st.columns([5, 1, 1])
with prof_col:
    # Profile avatar button — click to open profile page
    initials_top = "".join(w[0].upper() for w in (profile.get("name", username) if profile else username).split()[:2]) or "FP"
    st.markdown(f"""
    <style>
    div[data-testid="stButton"] button[kind="secondary"]#prof_avatar_btn {{
      background:linear-gradient(135deg,#5b5bd6,#7c3aed)!important;
      border-radius:50%!important;width:42px!important;height:42px!important;
      padding:0!important;font-size:0.80rem!important;font-weight:800!important;
    }}
    </style>""", unsafe_allow_html=True)
    if st.button(initials_top, key="prof_btn", use_container_width=True,
                  help=f"View {profile.get('name', username) if profile else username}'s profile"):
        st.switch_page("pages/5_Profile.py")
with so_col:
    if st.button("🚪 Sign Out", key="so", use_container_width=True):
        logout_user(username)
        for k in ["logged_in", "username", "auth_token"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")

# ── Edit profile ───────────────────────────────────────────────────────────────
if st.session_state.get("show_edit"):
    st.markdown(section_header("Edit Profile", "Update your fitness details"), unsafe_allow_html=True)
    with st.form("edit_form"):
        ec1, ec2 = st.columns(2)
        with ec1:
            ep_name   = st.text_input("Full Name", value=profile.get("name","") if profile else "")
            ep_age    = st.number_input("Age", 15, 80, value=int(profile.get("age",25)) if profile else 25)
            ep_gender = st.selectbox("Gender", ["Male","Female","Other"],
                        index=["Male","Female","Other"].index(profile.get("gender","Male")) if profile else 0)
        with ec2:
            ep_h = st.number_input("Height (cm)", 100, 250, value=int(profile.get("height",170)) if profile else 170)
            ep_w = st.number_input("Weight (kg)", 30, 300, value=int(profile.get("weight",70)) if profile else 70)
            goals = ["Build Muscle","Weight Loss","Strength Gain","Abs Building","Flexibility & Mobility","General Fitness"]
            ep_g = st.selectbox("Goal", goals,
                    index=goals.index(profile.get("goal","Build Muscle")) if profile and profile.get("goal") in goals else 0)
        ep_l = st.selectbox("Level", ["Beginner","Intermediate","Advanced"],
                index=["Beginner","Intermediate","Advanced"].index(profile.get("level","Beginner")) if profile else 0)
        sc1, sc2 = st.columns(2)
        with sc1: save_btn = st.form_submit_button("💾 Save Changes", use_container_width=True)
        with sc2: cancel_btn = st.form_submit_button("Cancel", use_container_width=True)
    if save_btn:
        save_profile(username, {"name":ep_name,"age":ep_age,"gender":ep_gender,
            "height":ep_h,"weight":ep_w,"goal":ep_g,"level":ep_l,
            "equipment": profile.get("equipment",[]) if profile else []})
        st.session_state.show_edit = False; st.success("✅ Profile updated!"); st.rerun()
    if cancel_btn:
        st.session_state.show_edit = False; st.rerun()
    st.markdown("<hr>", unsafe_allow_html=True)

# ── STAT CARDS ─────────────────────────────────────────────────────────────────
st.markdown(section_header("Overview", "Your fitness snapshot"), unsafe_allow_html=True)
s1, s2, s3, s4 = st.columns(4)
with s1: st.markdown(stat_card("🔥", "Day Streak", streak, "consecutive", "#f59e0b"), unsafe_allow_html=True)
with s2: st.markdown(stat_card("✅", "Completed", done_count, f"of {num_days}", "#10d9a0"), unsafe_allow_html=True)
with s3: st.markdown(stat_card("📊", "Progress", f"{pct}%", "overall", "#6366f1"), unsafe_allow_html=True)
with s4: st.markdown(stat_card("📅", "Plan Days", num_days, "total", "#a78bfa"), unsafe_allow_html=True)

# ── Progress bar ──
if num_days:
    st.markdown(f"""
    <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);
      padding:18px 22px;margin:4px 0 28px;animation:fadeSlideUp 0.4s ease">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
        <div>
          <span style="font-size:0.70rem;font-weight:700;letter-spacing:1.5px;
            text-transform:uppercase;color:var(--muted)">Overall Progress</span>
          <span style="font-size:0.72rem;color:var(--muted2);margin-left:10px">
            {done_count} completed · {skipped_count} skipped · {num_days-done_count-skipped_count} remaining</span>
        </div>
        <span style="font-family:'Syne',sans-serif;font-size:1.2rem;
          color:#6366f1;font-weight:800">{pct}%</span>
      </div>
      <div style="height:8px;background:rgba(255,255,255,0.05);border-radius:100px;overflow:hidden;position:relative">
        <div style="height:100%;width:{pct}%;
          background:linear-gradient(90deg,#6366f1,#a78bfa);border-radius:100px;
          box-shadow:0 0 12px rgba(99,102,241,0.50);transition:width 0.8s ease"></div>
        {f'<div style="position:absolute;top:0;left:{int(skipped_count/num_days*100)}%;height:100%;width:{int(skipped_count/num_days*100)}%;background:rgba(245,158,11,0.40);border-radius:100px"></div>' if skipped_count else ''}
      </div>
    </div>""", unsafe_allow_html=True)

# ── MAIN LAYOUT ────────────────────────────────────────────────────────────────
left, right = st.columns([6, 4], gap="large")

# ── LEFT COLUMN ───────────────────────────────────────────────────────────────
with left:
    st.markdown(section_header("Today's Workout", date.today().strftime("%A, %B %d")), unsafe_allow_html=True)

    if not day_blocks:
        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(99,102,241,0.10),rgba(139,92,246,0.05));
          border:1px solid rgba(99,102,241,0.22);border-radius:var(--radius);
          padding:52px;text-align:center;animation:fadeSlideUp 0.4s ease">
          <div style="font-size:3rem;margin-bottom:16px">🎯</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;
            color:var(--text);margin-bottom:8px">No Workout Plan Yet</div>
          <div style="font-size:0.88rem;color:var(--muted);line-height:1.7">
            Create your personalised AI plan to get started on your fitness journey.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("⚡ Create My Workout Plan", use_container_width=True, key="create_hero"):
            st.switch_page("pages/4_Create_Plan.py")
    else:
        chip_c = {"done":"#10d9a0","skipped":"#f59e0b","pending":"#6366f1"}[today_status]
        chip_t = {"done":"✅ Completed","skipped":"⏭️ Skipped","pending":"⚡ Today"}[today_status]

        # Day header card
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(99,102,241,0.10),rgba(139,92,246,0.05));
          border:1px solid rgba(99,102,241,0.20);border-radius:var(--radius);padding:22px 24px;
          position:relative;overflow:hidden;margin-bottom:12px;animation:fadeSlideUp 0.35s ease">
          <div style="position:absolute;top:0;left:0;right:0;height:2px;
            background:linear-gradient(90deg,#6366f1,#a78bfa,transparent)"></div>
          <div style="display:flex;align-items:flex-start;justify-content:space-between;
            flex-wrap:wrap;gap:10px">
            <div>
              <div style="font-size:0.58rem;font-weight:700;letter-spacing:3px;
                text-transform:uppercase;color:rgba(99,102,241,0.70);margin-bottom:5px">
                Day {today_idx+1} of {num_days}</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.45rem;font-weight:800;
                color:var(--text);line-height:1.1">{today_title}</div>
              <div style="font-size:0.75rem;color:var(--muted);margin-top:5px">
                {len(today_exercises)} exercises planned</div>
            </div>
            <div style="display:inline-flex;align-items:center;padding:6px 15px;
              background:{chip_c}14;border:1px solid {chip_c}38;border-radius:100px;
              font-size:0.70rem;font-weight:700;color:{chip_c};letter-spacing:0.5px">{chip_t}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Exercise list with descriptions
        if today_exercises:
            st.markdown('<div style="animation:fadeSlideUp 0.4s ease">', unsafe_allow_html=True)
            for i, ex in enumerate(today_exercises[:8]):
                st.markdown(exercise_card(
                    ex["icon"], ex["name"],
                    ex.get("sets",""), ex.get("reps",""),
                    ex.get("rest","—"), i,
                    ex.get("desc","")
                ), unsafe_allow_html=True)
            if len(today_exercises) > 8:
                st.markdown(f'<div style="font-size:0.68rem;color:var(--muted2);'
                            f'text-align:center;padding:8px">+{len(today_exercises)-8} more in full plan</div>',
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Action buttons
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if today_status == "pending":
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("✅ Mark Complete", use_container_width=True, key="done_btn"):
                    save_tracking(username, today_str, today_idx, "done"); st.rerun()
            with b2:
                if st.button("⏭️ Skip Today", use_container_width=True, key="skip_btn"):
                    save_tracking(username, today_str, today_idx, "skipped"); st.rerun()
            with b3:
                if st.button("📋 Full Plan", use_container_width=True, key="plan_btn"):
                    st.switch_page("pages/3_Plan.py")
        else:
            # Show completion message
            if today_status == "done":
                st.markdown(f"""
                <div style="background:rgba(16,217,160,0.08);border:1px solid rgba(16,217,160,0.25);
                  border-radius:var(--radius-sm);padding:14px 18px;margin-bottom:10px;
                  display:flex;align-items:center;gap:12px">
                  <span style="font-size:1.2rem">🎉</span>
                  <div>
                    <div style="font-size:0.86rem;font-weight:600;color:#10d9a0">Great work today!</div>
                    <div style="font-size:0.72rem;color:var(--muted)">Workout marked as complete. Keep the streak going!</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1:
                if st.button("↩️ Undo", use_container_width=True, key="undo_btn"):
                    _db().execute("DELETE FROM tracking WHERE username=? AND date=?",
                                  (username, today_str)); _db().commit(); st.rerun()
            with b2:
                if st.button("📋 Full Plan", use_container_width=True, key="plan2_btn"):
                    st.switch_page("pages/3_Plan.py")

    # ── Missed workouts ──────────────────────────────────────────────────────
    missed = [date.today()-timedelta(days=i+1) for i in range(30)
              if tracking.get((date.today()-timedelta(days=i+1)).isoformat(),{}).get("status","pending")=="pending"
              and (date.today()-timedelta(days=i+1)) >= date.today()-timedelta(days=7)][:3]

    if missed:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(section_header("Missed Workouts", "Log these recent sessions"), unsafe_allow_html=True)
        for md in missed:
            st.markdown(f"""
            <div style="background:rgba(244,63,94,0.06);border:1px solid rgba(244,63,94,0.18);
              border-radius:var(--radius-sm);padding:12px 16px;margin-bottom:8px;
              display:flex;align-items:center;gap:10px">
              <span style="font-size:1rem">📅</span>
              <span style="flex:1;font-size:0.84rem;color:var(--text2)">{md.strftime("%A, %b %d, %Y")}</span>
            </div>""", unsafe_allow_html=True)
            mc1, mc2 = st.columns(2)
            with mc1:
                if st.button(f"✅ Done", key=f"md_{md.isoformat()}"):
                    save_tracking(username, md.isoformat(), 0, "done"); st.rerun()
            with mc2:
                if st.button(f"⏭️ Skip", key=f"ms_{md.isoformat()}"):
                    save_tracking(username, md.isoformat(), 0, "skipped"); st.rerun()

# ── RIGHT COLUMN ──────────────────────────────────────────────────────────────
with right:
    # ── Weekly bar chart ──
    st.markdown(section_header("This Week", "Daily activity"), unsafe_allow_html=True)
    week_start = date.today() - timedelta(days=date.today().weekday())
    DAYS  = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    bars  = "<div style='display:grid;grid-template-columns:repeat(7,1fr);gap:6px;align-items:end;height:80px;margin-bottom:7px'>"
    done_wk = 0
    for i in range(7):
        d  = week_start + timedelta(days=i)
        s  = tracking.get(d.isoformat(), {}).get("status", "pending")
        it = d == date.today()
        if s=="done":     h,bg,done_wk = 72,"linear-gradient(180deg,#6366f1,rgba(99,102,241,0.40))",done_wk+1
        elif s=="skipped": h,bg = 28,"rgba(245,158,11,0.50)"
        elif d < date.today(): h,bg = 10,"rgba(244,63,94,0.28)"
        else:              h,bg = 8,"rgba(255,255,255,0.05)"
        lc = "#818cf8" if it else "rgba(240,238,255,0.22)"
        border = "box-shadow:0 0 0 2px #6366f1;" if it else ""
        bars += (f"<div style='display:flex;flex-direction:column;align-items:center;gap:4px;height:100%'>"
                 f"<div style='flex:1;display:flex;align-items:flex-end;width:100%'>"
                 f"<div style='width:100%;height:{h}px;background:{bg};border-radius:5px 5px 0 0;{border}'></div></div>"
                 f"<div style='font-size:0.50rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:{lc}'>{DAYS[i]}</div>"
                 f"</div>")
    bars += "</div>"

    st.markdown(f"""
    <div style="background:var(--bg2);border:1px solid var(--border);
      border-radius:var(--radius);padding:18px 20px;margin-bottom:22px;
      animation:fadeSlideUp 0.4s ease">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
        <span style="font-size:0.70rem;font-weight:600;color:var(--muted)">Weekly Activity</span>
        <span style="font-family:'Syne',sans-serif;font-size:1.2rem;color:#6366f1;font-weight:800">{done_wk}/7</span>
      </div>
      {bars}
      <div style="display:flex;gap:14px;margin-top:8px">
        <div style="display:flex;align-items:center;gap:5px;font-size:0.60rem;color:var(--muted2)">
          <div style="width:8px;height:8px;border-radius:2px;background:#6366f1"></div>Done</div>
        <div style="display:flex;align-items:center;gap:5px;font-size:0.60rem;color:var(--muted2)">
          <div style="width:8px;height:8px;border-radius:2px;background:rgba(245,158,11,0.55)"></div>Skipped</div>
        <div style="display:flex;align-items:center;gap:5px;font-size:0.60rem;color:var(--muted2)">
          <div style="width:8px;height:8px;border-radius:2px;background:rgba(244,63,94,0.40)"></div>Missed</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Workout Calendar ──
    st.markdown(section_header("Activity Calendar", "Last 5 weeks"), unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:var(--bg2);border:1px solid var(--border);
      border-radius:var(--radius);padding:18px 20px;margin-bottom:22px;
      animation:fadeSlideUp 0.45s ease">
      {calendar_widget(tracking, num_days, today_str)}
    </div>""", unsafe_allow_html=True)

    # ── Workout Statistics ──
    st.markdown(section_header("Statistics", "All-time performance"), unsafe_allow_html=True)

    total_workouts = done_count
    completion_rate = int(done_count / max(done_count + skipped_count + 1, 1) * 100) if (done_count + skipped_count) > 0 else 0

    # This month
    month_start = date.today().replace(day=1).isoformat()
    done_month = sum(1 for k, v in tracking.items() if k >= month_start and v.get("status") == "done")

    st.markdown(f"""
    <div style="background:var(--bg2);border:1px solid var(--border);
      border-radius:var(--radius);padding:18px 20px;margin-bottom:22px;
      animation:fadeSlideUp 0.50s ease">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
        <div style="text-align:center;padding:14px;background:rgba(16,217,160,0.07);
          border:1px solid rgba(16,217,160,0.18);border-radius:var(--radius-sm)">
          <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#10d9a0">{total_workouts}</div>
          <div style="font-size:0.62rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);margin-top:4px">Total Done</div>
        </div>
        <div style="text-align:center;padding:14px;background:rgba(245,158,11,0.07);
          border:1px solid rgba(245,158,11,0.18);border-radius:var(--radius-sm)">
          <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#f59e0b">{streak}</div>
          <div style="font-size:0.62rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);margin-top:4px">Best Streak</div>
        </div>
        <div style="text-align:center;padding:14px;background:rgba(99,102,241,0.07);
          border:1px solid rgba(99,102,241,0.18);border-radius:var(--radius-sm)">
          <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#818cf8">{done_month}</div>
          <div style="font-size:0.62rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);margin-top:4px">This Month</div>
        </div>
        <div style="text-align:center;padding:14px;background:rgba(167,139,250,0.07);
          border:1px solid rgba(167,139,250,0.18);border-radius:var(--radius-sm)">
          <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:#a78bfa">{skipped_count}</div>
          <div style="font-size:0.62rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);margin-top:4px">Skipped</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Upcoming sessions ──
    if day_blocks:
        st.markdown(section_header("Upcoming", "Next sessions"), unsafe_allow_html=True)
        WICONS = ["🏋️","💪","🏃","🥊","🧗","🚴","🤸","⚡"]
        shown = 0
        for i in range(min(5, num_days)):
            if i == 0 and today_status in ("done", "skipped"):
                continue
            if shown >= 3: break
            di    = (today_idx + i) % num_days
            blk   = day_blocks[di] if day_blocks else ""
            title = get_day_title(blk)[:28] if blk else f"Day {di+1}"
            n_ex  = len(parse_exercises(blk))
            icon  = WICONS[di % len(WICONS)]
            nd    = date.today() + timedelta(days=i)
            lbl   = "Today" if i==0 else ("Tomorrow" if i==1 else nd.strftime("%b %d"))
            lbl_color = "#6366f1" if i==0 else "var(--muted2)"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:12px 14px;
              background:rgba(255,255,255,0.02);border:1px solid rgba(99,102,241,0.12);
              border-radius:var(--radius-sm);margin-bottom:8px;
              animation:fadeSlideUp 0.4s {shown*0.06:.2f}s ease both">
              <div style="width:38px;height:38px;border-radius:9px;flex-shrink:0;
                background:rgba(99,102,241,0.10);border:1px solid rgba(99,102,241,0.20);
                display:flex;align-items:center;justify-content:center;font-size:0.95rem">{icon}</div>
              <div style="flex:1;min-width:0">
                <div style="font-size:0.84rem;font-weight:600;color:var(--text);
                  white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{title}</div>
                <div style="font-size:0.65rem;color:var(--muted2);margin-top:2px">
                  {n_ex} exercises · Day {di+1}</div>
              </div>
              <div style="font-size:0.62rem;font-weight:700;color:{lbl_color};white-space:nowrap">{lbl}</div>
            </div>""", unsafe_allow_html=True)
            shown += 1

    # ── Reset tracking ──
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🔄 Reset All Tracking", use_container_width=True, key="rst"):
        delete_tracking(username); st.success("Tracking reset!"); st.rerun()
