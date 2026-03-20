
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth import load_profile, save_profile, save_workout
from utils.ai import generate_plan, calculate_bmi, bmi_category
from utils.ui import inject_css, section_header

st.set_page_config(page_title="FitPro AI — Create Plan", page_icon="⚡", layout="wide")
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

inject_css()
username = st.session_state.get("username", "")
profile  = load_profile(username)

# Topnav
c1, c2, c3 = st.columns([4, 4, 2])
with c1:
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.45rem;font-weight:800;
      background:linear-gradient(135deg,#6366f1,#a78bfa);-webkit-background-clip:text;
      -webkit-text-fill-color:transparent;padding:16px 0 14px;
      border-bottom:1px solid var(--border);margin-bottom:26px">⚡ FitPro AI</div>""",
      unsafe_allow_html=True)
with c2:
    st.markdown('<div style="padding:16px 0 14px;border-bottom:1px solid var(--border);margin-bottom:26px;text-align:center"><span style="font-size:0.62rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border:1px solid rgba(99,102,241,0.32);border-radius:100px;color:#818cf8;background:rgba(99,102,241,0.06)">CREATE PLAN</span></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div style="padding:10px 0 4px;border-bottom:1px solid var(--border);margin-bottom:26px">', unsafe_allow_html=True)
    if st.button("🏠 Dashboard", key="back_db", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")
    st.markdown("</div>", unsafe_allow_html=True)

# Hero header
st.markdown("""
<div style="text-align:center;padding:22px 0 36px;animation:fadeSlideUp 0.35s ease">
  <div style="font-size:0.60rem;font-weight:700;letter-spacing:5px;text-transform:uppercase;
    color:rgba(99,102,241,0.75);margin-bottom:14px">AI-Powered Plan Builder</div>
  <div style="font-family:'Syne',sans-serif;font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;
    color:var(--text);line-height:1;letter-spacing:-1px">
    Build Your <span style="background:linear-gradient(135deg,#6366f1,#a78bfa);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent">Perfect Plan</span></div>
  <div style="font-size:0.88rem;color:var(--muted);margin-top:12px;max-width:480px;margin-left:auto;margin-right:auto">
    Fill in your details and we'll generate a complete workout + nutrition plan tailored just for you.</div>
</div>""", unsafe_allow_html=True)

# ── Step indicator ──────────────────────────────────────────────────────────
steps = ["👤 Personal", "🎯 Goals", "🏋️ Equipment", "📅 Duration"]
st.markdown(f"""
<div style="display:flex;gap:0;margin-bottom:32px;animation:fadeSlideUp 0.4s ease">
  {''.join(f'<div style="flex:1;text-align:center;padding:10px 5px;font-size:0.68rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;border-bottom:2px solid rgba(99,102,241,0.25);color:rgba(240,238,255,0.40)">{s}</div>' for s in steps)}
</div>""", unsafe_allow_html=True)

def _section_card(title, sub, icon):
    return f"""
<div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--radius);
  padding:24px 28px;margin-bottom:16px;animation:fadeSlideUp 0.4s ease">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px">
    <div style="width:36px;height:36px;border-radius:9px;background:rgba(99,102,241,0.12);
      border:1px solid rgba(99,102,241,0.22);display:flex;align-items:center;
      justify-content:center;font-size:1rem;flex-shrink:0">{icon}</div>
    <div>
      <div style="font-family:'Syne',sans-serif;font-size:0.95rem;font-weight:700;color:var(--text)">{title}</div>
      <div style="font-size:0.73rem;color:var(--muted);margin-top:2px">{sub}</div>
    </div>
  </div>"""

# ── Card 1: Personal ────────────────────────────────────────────────────────
st.markdown(_section_card("Personal Information",
    "Used to calculate BMI and calibrate training intensity", "👤"), unsafe_allow_html=True)

with st.container():
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        p_name = st.text_input("Full Name", value=profile.get("name","") if profile else "",
                               placeholder="e.g. Raj Sharma")
    with r1c2:
        gender_opts = ["Male","Female","Other"]
        gender_val  = profile.get("gender","Male") if profile else "Male"
        p_gender = st.selectbox("Gender", gender_opts,
                                index=gender_opts.index(gender_val) if gender_val in gender_opts else 0)

    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        p_age = st.number_input("Age", 15, 80, value=int(profile.get("age",25)) if profile else 25)
    with r2c2:
        p_height = st.number_input("Height (cm)", 100, 250,
                                   value=int(profile.get("height",170)) if profile else 170)
    with r2c3:
        p_weight = st.number_input("Weight (kg)", 30, 300,
                                   value=int(profile.get("weight",70)) if profile else 70)

    if p_height > 0:
        bmi = calculate_bmi(p_weight, p_height)
        bmi_cat = bmi_category(bmi)
        bmi_color = {"Underweight":"#f59e0b","Normal Weight":"#10d9a0",
                     "Overweight":"#f97316","Obese":"#f43f5e"}.get(bmi_cat,"#6366f1")
        st.markdown(f"""
        <div style="display:inline-flex;align-items:center;gap:12px;padding:10px 18px;
          background:{bmi_color}10;border:1px solid {bmi_color}28;border-radius:10px;margin-top:8px">
          <span style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800;color:{bmi_color}">{bmi}</span>
          <span style="font-size:0.72rem;color:{bmi_color};font-weight:600">BMI · {bmi_cat}</span>
        </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Card 2: Goals ────────────────────────────────────────────────────────────
st.markdown(_section_card("Goals & Fitness Level",
    "Shapes exercise selection, rep ranges and weekly structure", "🎯"), unsafe_allow_html=True)

with st.container():
    gc1, gc2 = st.columns(2)
    with gc1:
        goal_opts = ["Build Muscle","Weight Loss","Strength Gain",
                     "Abs Building","Flexibility & Mobility","General Fitness"]
        goal_val  = profile.get("goal","Build Muscle") if profile else "Build Muscle"
        p_goal = st.selectbox("Fitness Goal", goal_opts,
                              index=goal_opts.index(goal_val) if goal_val in goal_opts else 0)
    with gc2:
        level_opts = ["Beginner","Intermediate","Advanced"]
        level_val  = profile.get("level","Beginner") if profile else "Beginner"
        p_level = st.selectbox("Fitness Level", level_opts,
                               index=level_opts.index(level_val) if level_val in level_opts else 0)

    # Level descriptions
    level_desc = {
        "Beginner": "New to training. Focus on form, 2–3 sets, 12–15 reps, longer rests.",
        "Intermediate": "6+ months experience. Progressive overload, 3–4 sets, 8–12 reps.",
        "Advanced": "2+ years training. Heavy compounds, supersets, 4–5 sets, 5–10 reps.",
    }
    st.markdown(f"""
    <div style="background:rgba(99,102,241,0.06);border:1px solid rgba(99,102,241,0.14);
      border-radius:var(--radius-sm);padding:10px 14px;margin-top:6px;
      font-size:0.78rem;color:var(--muted)">
      ℹ️ {level_desc.get(p_level,'')}
    </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Card 3: Equipment ────────────────────────────────────────────────────────
st.markdown(_section_card("Equipment Available",
    "We'll tailor every exercise to what you actually have", "🏋️"), unsafe_allow_html=True)

with st.container():
    HOME_EQUIP = [
        "Dumbbells","Adjustable Dumbbells","Barbell + Plates","Resistance Bands",
        "Pull-up Bar","Kettlebell","Bench (Flat)","Incline/Decline Bench",
        "Yoga Mat","Jump Rope","Foam Roller","TRX / Suspension Trainer",
        "Battle Ropes","Medicine Ball","Dip Bars","Treadmill","Stationary Bike","Rowing Machine",
    ]
    GYM_EQUIP = [
        "Full Commercial Gym Access","Cable Pulley System","Leg Press Machine",
        "Lat Pulldown Machine","Chest Press Machine","Hack Squat Machine",
        "Leg Curl / Extension Machine","Pec Deck / Fly Machine",
        "Seated Row Machine","EZ Curl Bar","Trap Bar / Hex Bar",
    ]

    ec1, ec2 = st.columns(2)
    with ec1:
        prev_home = [e for e in (profile.get("equipment",[]) if profile else []) if e in HOME_EQUIP]
        p_home_equip = st.multiselect("🏠 Home Equipment", HOME_EQUIP,
                                      default=prev_home, placeholder="Select items…")
    with ec2:
        prev_gym = [e for e in (profile.get("equipment",[]) if profile else []) if e in GYM_EQUIP]
        p_gym_equip = st.multiselect("🏋️ Gym / Commercial", GYM_EQUIP,
                                     default=prev_gym, placeholder="Select machines…")

    p_no_equip = st.checkbox("No equipment — bodyweight only", value=False)
    if p_no_equip:
        equipment = ["Bodyweight only"]
    else:
        equipment = p_home_equip + p_gym_equip or ["Bodyweight only"]

    if equipment:
        eq_display = ", ".join(equipment[:4]) + (f" +{len(equipment)-4} more" if len(equipment) > 4 else "")
        st.markdown(f"""
        <div style="margin-top:8px;font-size:0.75rem;color:var(--muted)">
          Selected: <strong style="color:var(--text2)">{eq_display}</strong>
        </div>""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Card 4: Duration ─────────────────────────────────────────────────────────
st.markdown(_section_card("Plan Duration",
    "Choose your commitment level and weekly training frequency", "📅"), unsafe_allow_html=True)

with st.container():
    dc1, dc2 = st.columns(2)
    with dc1:
        p_days_pw = st.selectbox("Training Days / Week",
                                 [3,4,5,6,7], index=2,
                                 format_func=lambda x: f"{x} days/week")
    with dc2:
        duration_options = {
            "1 week  — 7 days":    7,
            "2 weeks — 14 days":   14,
            "3 weeks — 21 days":   21,
            "1 month — 28 days":   28,
            "6 weeks — 42 days":   42,
            "2 months — 56 days":  56,
            "3 months — 84 days":  84,
        }
        duration_choice = st.selectbox("Program Length", list(duration_options.keys()), index=0)
        total_days_raw = duration_options[duration_choice]
        weeks = total_days_raw // 7
        total_days = min(p_days_pw * weeks, total_days_raw)
        total_days = max(total_days, p_days_pw)

    # Duration preview cards
    d1, d2, d3 = st.columns(3)
    with d1:
        st.markdown(f"""
        <div style="background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.20);
          border-radius:var(--radius-sm);padding:14px;text-align:center;margin-top:6px">
          <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#6366f1">{total_days}</div>
          <div style="font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted)">Workout Days</div>
        </div>""", unsafe_allow_html=True)
    with d2:
        st.markdown(f"""
        <div style="background:rgba(167,139,250,0.08);border:1px solid rgba(167,139,250,0.20);
          border-radius:var(--radius-sm);padding:14px;text-align:center;margin-top:6px">
          <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#a78bfa">{weeks}</div>
          <div style="font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted)">Weeks</div>
        </div>""", unsafe_allow_html=True)
    with d3:
        rest_days = (weeks * 7) - total_days
        st.markdown(f"""
        <div style="background:rgba(16,217,160,0.08);border:1px solid rgba(16,217,160,0.20);
          border-radius:var(--radius-sm);padding:14px;text-align:center;margin-top:6px">
          <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;color:#10d9a0">{rest_days}</div>
          <div style="font-size:0.60rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted)">Rest Days</div>
        </div>""", unsafe_allow_html=True)

    include_diet = st.checkbox("🥗 Also generate a Personalised Nutrition Plan", value=True)

st.markdown("</div>", unsafe_allow_html=True)

# ── Generate button ───────────────────────────────────────────────────────────
st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
gen_col1, gen_col2, gen_col3 = st.columns([1, 2, 1])
with gen_col2:
    generate = st.button("⚡ Generate My AI Plan", use_container_width=True,
                         key="gen_plan_btn", type="primary")

if generate:
    if not p_name.strip():
        st.error("⚠️ Please enter your full name.")
        st.stop()

    save_profile(username, {
        "name": p_name.strip(), "age": p_age, "gender": p_gender,
        "height": p_height, "weight": p_weight,
        "goal": p_goal, "level": p_level, "equipment": equipment,
    })

    profile_data = {
        "name": p_name.strip(), "age": p_age, "gender": p_gender,
        "height": p_height, "weight": p_weight,
        "goal": p_goal, "level": p_level, "equipment": equipment,
    }

    n_chunks = max(1, (total_days + 2) // 3)
    est_sec  = n_chunks * 12 + (15 if include_diet else 0)

    st.markdown(f"""
    <div style="text-align:center;padding:24px 0 12px;animation:fadeSlideUp 0.35s ease">
      <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;
        color:var(--text);margin-bottom:6px">⚡ Building Your Plan</div>
      <div style="font-size:0.82rem;color:var(--muted)">
        {total_days}-day programme · est. ~{est_sec}s · Powered by Groq LLaMA 3.3
      </div>
    </div>""", unsafe_allow_html=True)

    prog      = st.progress(0, text="Initialising AI engine…")
    status_ph = st.empty()

    def on_progress(chunk, total, msg):
        pct = min(int(chunk / total * 90), 90) if total else 50
        prog.progress(pct, text=msg)
        status_ph.markdown(
            f'<div style="text-align:center;font-size:0.70rem;color:var(--muted2)">'
            f'Processing chunk {chunk} of {total}</div>', unsafe_allow_html=True)

    try:
        result = generate_plan(profile_data, total_days, progress_cb=on_progress)
        workout_text = result["workout"]
        diet_text_r  = result["diet"] if include_diet else ""
        combined     = workout_text + ("\n\n##DIET##\n\n" + diet_text_r if diet_text_r else "")
        save_workout(username, combined, total_days)

        prog.progress(100, text="✅ Plan ready!")
        status_ph.empty()
        st.success(f"🎉 Your {total_days}-day plan has been generated!")
        st.balloons()

        import time; time.sleep(1.2)
        st.switch_page("pages/3_Plan.py")

    except Exception as e:
        prog.empty(); status_ph.empty()
        err = str(e)
        st.markdown(f"""
        <div style="background:var(--danger-bg);border:1px solid rgba(244,63,94,0.28);
          border-radius:var(--radius);padding:20px 24px;margin-top:16px">
          <div style="font-weight:700;color:#fb7185;margin-bottom:6px">⚠ Generation Failed</div>
          <div style="font-size:0.82rem;color:var(--muted);line-height:1.7">{err}</div>
          <div style="margin-top:12px;font-size:0.72rem;color:var(--muted2)">
            💡 If you see a 429 rate limit error, wait 60 seconds and try again.
            For very long plans, try fewer days/week or a shorter duration first.
          </div>
        </div>""", unsafe_allow_html=True)
