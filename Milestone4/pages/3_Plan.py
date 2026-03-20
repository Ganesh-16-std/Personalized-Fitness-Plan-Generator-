
import streamlit as st
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.auth import load_latest_workout, load_profile, load_tracking
from utils.ai import calculate_bmi, bmi_category, get_exercise_description
from utils.ui import inject_css, section_header, badge, exercise_card

st.set_page_config(page_title="FitPro AI — My Plan", page_icon="⚡", layout="wide")
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

inject_css()
username    = st.session_state.get("username", "")
profile     = load_profile(username)
tracking    = load_tracking(username)
workout_rec = load_latest_workout(username)

# Topnav
c1, c2, c3 = st.columns([4, 4, 2])
with c1:
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.45rem;font-weight:800;
      background:linear-gradient(135deg,#6366f1,#a78bfa);-webkit-background-clip:text;
      -webkit-text-fill-color:transparent;padding:16px 0 14px;
      border-bottom:1px solid var(--border);margin-bottom:26px">⚡ FitPro AI</div>""",
      unsafe_allow_html=True)
with c2:
    st.markdown('<div style="padding:16px 0 14px;border-bottom:1px solid var(--border);margin-bottom:26px;text-align:center"><span style="font-size:0.62rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border:1px solid rgba(99,102,241,0.32);border-radius:100px;color:#818cf8;background:rgba(99,102,241,0.06)">MY PLAN</span></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div style="padding:10px 0 4px;border-bottom:1px solid var(--border);margin-bottom:26px">', unsafe_allow_html=True)
    if st.button("🏠 Dashboard", key="back_dash", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")
    st.markdown("</div>", unsafe_allow_html=True)

if not workout_rec:
    st.markdown("""
    <div style="text-align:center;padding:80px 24px;animation:fadeSlideUp 0.4s ease">
      <div style="font-size:3.5rem;margin-bottom:18px">🎯</div>
      <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;
        color:var(--text);margin-bottom:10px">No Plan Generated Yet</div>
      <div style="font-size:0.92rem;color:var(--muted);max-width:380px;margin:0 auto">
        Create your personalised AI-powered plan to get started.</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button("⚡ Create My Plan", use_container_width=False, key="go_create"):
        st.switch_page("pages/4_Create_Plan.py")
    st.stop()

plan_text = workout_rec["plan_text"]
diet_text = ""
if "##DIET##" in plan_text:
    parts = plan_text.split("##DIET##", 1)
    plan_text = parts[0].strip()
    diet_text = parts[1].strip()

# Profile hero
if profile:
    bmi     = calculate_bmi(profile["weight"], profile["height"])
    bmi_cat = bmi_category(bmi)
    name    = profile.get("name", username)
    level   = profile.get("level", "")
    goal    = profile.get("goal", "")
    bmi_color = {"Underweight":"#f59e0b","Normal Weight":"#10d9a0","Overweight":"#f97316","Obese":"#f43f5e"}.get(bmi_cat,"#6366f1")

    # Progress
    done_count = sum(1 for v in tracking.values() if v.get("status") == "done")
    total_days = workout_rec["days_total"]
    pct = int(done_count / total_days * 100) if total_days else 0

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(99,102,241,0.12),rgba(139,92,246,0.06));
      border:1px solid rgba(99,102,241,0.24);border-radius:var(--radius);
      padding:28px 32px;margin-bottom:28px;position:relative;overflow:hidden;
      animation:fadeSlideUp 0.35s ease">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;
        background:linear-gradient(90deg,#6366f1,#a78bfa,transparent)"></div>
      <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:16px">
        <div>
          <div style="font-size:0.58rem;font-weight:700;letter-spacing:4px;text-transform:uppercase;
            color:rgba(99,102,241,0.75);margin-bottom:8px">Personalised AI Fitness Plan</div>
          <div style="font-family:'Syne',sans-serif;font-size:clamp(1.6rem,3vw,2.4rem);
            font-weight:800;color:var(--text);margin-bottom:10px;line-height:1">{name.upper()}'S PLAN</div>
          <div style="display:flex;gap:12px;flex-wrap:wrap">
            <span style="font-size:0.78rem;color:var(--muted)">🎯 {goal}</span>
            <span style="color:rgba(99,102,241,0.3)">·</span>
            <span style="font-size:0.78rem;color:var(--muted)">📊 {level}</span>
            <span style="color:rgba(99,102,241,0.3)">·</span>
            <span style="font-size:0.78rem;color:{bmi_color}">⚖️ BMI {bmi} · {bmi_cat}</span>
            <span style="color:rgba(99,102,241,0.3)">·</span>
            <span style="font-size:0.78rem;color:var(--muted)">📅 {total_days} days</span>
          </div>
        </div>
        <div style="text-align:center">
          <div style="font-size:0.58rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
            color:var(--muted);margin-bottom:6px">Progress</div>
          <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#6366f1">{pct}%</div>
          <div style="font-size:0.68rem;color:var(--muted)">{done_count}/{total_days} done</div>
        </div>
      </div>
      <div style="margin-top:16px;height:5px;background:rgba(255,255,255,0.05);border-radius:100px;overflow:hidden">
        <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#6366f1,#a78bfa);border-radius:100px;box-shadow:0 0 10px rgba(99,102,241,0.40)"></div>
      </div>
    </div>""", unsafe_allow_html=True)

# Parse day blocks
lines = plan_text.split("\n")
day_blocks, current = [], []
for line in lines:
    s = line.strip()
    if (re.match(r"^#{1,3}\s*day\s*\d", s, re.I) or re.match(r"^day\s*\d", s, re.I)) and current:
        day_blocks.append("\n".join(current)); current = [line]
    else:
        current.append(line)
if current:
    day_blocks.append("\n".join(current))

SECTION_ICONS = {
    "warm": ("🔥","Warm-Up"), "main": ("💪","Main Workout"),
    "cool": ("🧊","Cool-Down"), "stretch": ("🧘","Stretching"),
    "cardio": ("🏃","Cardio"), "rest": ("😴","Rest"), "note": ("📝","Notes"),
}
EX_ICONS = ["🏋️","💪","🔄","⬆️","🦵","🤸","🏃","🥊","🧗","🚴","🔥","⚡","🎯","🌀"]

def detect_section(text):
    t = text.lower()
    for key, (icon, label) in SECTION_ICONS.items():
        if key in t:
            return icon, label
    return "📋", text.strip("*# ").title()

def parse_ex_line(raw):
    s = re.sub(r"^[-•*\d\.]+\s*", "", raw).strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    m = re.search(r"(\d+)\s*(?:sets?|×|x)[,\s]?\s*(\d+(?:[-–]\d+)?)\s*(?:reps?)?\s*(?:.*?rest\s*(\d+)\s*s)?", s, re.I)
    if m:
        name = re.split(r"[\-—–:,]|\d+\s*(?:set|rep|x|X|×)", s)[0].strip() or s[:40]
        return name, m.group(1), m.group(2), (m.group(3)+"s" if m.group(3) else "—")
    m2 = re.search(r"(\d+)\s*[xX×]\s*(\d+)", s)
    if m2:
        name = re.split(r"[\-—–:]|\d+\s*[xX×]", s)[0].strip() or s[:40]
        return name, m2.group(1), m2.group(2), "—"
    return None

def render_block_html(text):
    html = ""
    lines_ = text.split("\n")
    in_list = False
    ex_idx  = 0
    for line in lines_:
        s = line.strip()
        if not s:
            if in_list: html += "</div>"; in_list = False
            continue
        if re.match(r"^#{1,3}\s*day\s*\d", s, re.I) or re.match(r"^day\s*\d", s, re.I):
            if in_list: html += "</div>"; in_list = False
            clean = re.sub(r"^#+\s*", "", s)
            html += f"""<div style="font-family:'Syne',sans-serif;font-size:1.45rem;font-weight:800;
              color:var(--text);margin:0 0 18px;padding-bottom:14px;
              border-bottom:1px solid rgba(99,102,241,0.16)">{clean.upper()}</div>"""
        elif re.match(r"^#{2,}", s) or (s.startswith("**") and s.endswith("**")):
            if in_list: html += "</div>"; in_list = False
            clean = re.sub(r"[*#]", "", s).strip()
            if clean:
                icon, label = detect_section(clean)
                html += f"""<div style="font-size:0.60rem;font-weight:700;letter-spacing:3px;
                  text-transform:uppercase;color:rgba(99,102,241,0.75);margin:22px 0 10px;
                  display:flex;align-items:center;gap:8px">
                  <span>{icon}</span><span>{label}</span>
                  <div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(99,102,241,0.18),transparent)"></div>
                </div>"""
        elif re.match(r"^[-•*]\s+", s) or re.match(r"^\d+\.\s+", s):
            parsed = parse_ex_line(s)
            if parsed:
                name, sets, reps, rest = parsed
                icon = EX_ICONS[ex_idx % len(EX_ICONS)]
                desc = get_exercise_description(name)
                if not in_list:
                    html += "<div style='display:flex;flex-direction:column;gap:0'>"; in_list = True
                html += exercise_card(icon, name, sets, reps, rest, ex_idx, desc)
                ex_idx += 1
            else:
                if in_list: html += "</div>"; in_list = False
                content = re.sub(r"^[-•*\d\.]+\s*", "", s)
                content = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", content)
                html += f'<p style="font-size:0.86rem;color:var(--muted);padding:3px 0;line-height:1.7">{content}</p>'
        else:
            if in_list: html += "</div>"; in_list = False
            clean = re.sub(r"\*\*(.+?)\*\*", r"<strong style=color:var(--text)>\1</strong>", s)
            html += f'<p style="font-size:0.86rem;color:var(--muted);line-height:1.7;margin:4px 0">{clean}</p>'
    if in_list: html += "</div>"
    return html

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_workout, tab_diet = st.tabs(["💪 Workout Plan", "🥗 Nutrition Plan"])

with tab_workout:
    st.markdown(section_header(f"Your {workout_rec['days_total']}-Day Workout Plan",
        "Tap any day tab to view exercises"), unsafe_allow_html=True)

    if len(day_blocks) >= 2:
        labels = []
        for i, blk in enumerate(day_blocks):
            fl = blk.strip().split("\n")[0]
            fl = re.sub(r"^#+\s*", "", fl).strip()
            dm = re.search(r"day\s*(\d+)", fl, re.I)
            day_num = dm.group(1) if dm else str(i+1)
            # Get tracking status for this day
            day_key = None
            for k, v in tracking.items():
                if v.get("day_idx") == i:
                    day_key = k
                    break
            status_emoji = ""
            if day_key:
                s = tracking[day_key].get("status","")
                status_emoji = " ✅" if s=="done" else (" ⏭️" if s=="skipped" else "")
            labels.append(f"Day {day_num}{status_emoji}")

        tabs_list = st.tabs(labels)
        for tab, blk in zip(tabs_list, day_blocks):
            with tab:
                st.markdown(f"""
                <div style="background:var(--bg2);border:1px solid var(--border);
                  border-radius:var(--radius);padding:28px 32px;
                  animation:fadeSlideUp 0.3s ease">
                  {render_block_html(blk)}
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:var(--bg2);border:1px solid var(--border);
          border-radius:var(--radius);padding:28px 32px;animation:fadeSlideUp 0.3s ease">
          {render_block_html(plan_text)}
        </div>""", unsafe_allow_html=True)

with tab_diet:
    if not diet_text:
        st.markdown("""
        <div style="text-align:center;padding:48px;animation:fadeSlideUp 0.35s ease">
          <div style="font-size:2.5rem;margin-bottom:14px">🥗</div>
          <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;
            color:var(--text);margin-bottom:8px">No Nutrition Plan</div>
          <div style="font-size:0.90rem;color:var(--muted);max-width:380px;margin:0 auto">
            Create a new plan and check "Include Nutrition Plan" to get diet recommendations.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("⚡ Create New Plan with Diet", key="regen_diet"):
            st.switch_page("pages/4_Create_Plan.py")
    else:
        st.markdown(section_header("Your Personalised Nutrition Plan",
            "Tailored to your goal and BMI"), unsafe_allow_html=True)

        def render_diet(text):
            html = ""
            for line in text.split("\n"):
                s = line.strip()
                if not s: html += "<div style='height:6px'></div>"; continue
                if s.startswith("## "):
                    clean = s[3:]
                    html += f"""<div style="font-family:'Syne',sans-serif;font-size:1.05rem;
                      font-weight:700;color:var(--text);margin:22px 0 10px;padding-bottom:8px;
                      border-bottom:1px solid rgba(99,102,241,0.15)">{clean}</div>"""
                elif s.startswith("**") and s.endswith("**"):
                    clean = s[2:-2]
                    html += f"""<div style="font-size:0.76rem;font-weight:700;letter-spacing:1.5px;
                      text-transform:uppercase;color:rgba(99,102,241,0.75);margin:14px 0 6px">{clean}</div>"""
                elif re.match(r"^[-•*]\s+", s) or re.match(r"^\d+\.\s+", s):
                    content = re.sub(r"^[-•*\d\.]+\s*", "", s)
                    content = re.sub(r"\*\*(.+?)\*\*", r"<strong style='color:var(--text)'>\1</strong>", content)
                    html += f"""<div style="display:flex;align-items:flex-start;gap:9px;
                      padding:5px 0;font-size:0.86rem;color:var(--muted);line-height:1.65">
                      <span style="color:rgba(99,102,241,0.60);margin-top:1px;flex-shrink:0">▸</span>
                      <span>{content}</span></div>"""
                else:
                    clean = re.sub(r"\*\*(.+?)\*\*", r"<strong style='color:var(--text)'>\1</strong>", s)
                    html += f'<p style="font-size:0.86rem;color:var(--muted);line-height:1.7;margin:4px 0">{clean}</p>'
            return html

        st.markdown(f"""
        <div style="background:var(--bg2);border:1px solid var(--border);
          border-radius:var(--radius);padding:28px 32px;animation:fadeSlideUp 0.35s ease">
          {render_diet(diet_text)}
        </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
if st.button("⚡ Generate New Plan", key="gen_new"):
    st.switch_page("pages/4_Create_Plan.py")
