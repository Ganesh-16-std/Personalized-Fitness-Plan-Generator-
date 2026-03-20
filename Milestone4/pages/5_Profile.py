
import streamlit as st
import sys, os, re
from datetime import date, timedelta, datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import (
    load_profile, save_profile, load_latest_workout, load_tracking,
    get_water_today, add_water, reset_water, set_water_goal,
    get_water_history, log_diet, get_diet_today, get_diet_totals,
    delete_diet_entry, log_weight, get_weight_history, get_latest_weight,
)
from utils.ai  import calculate_bmi, bmi_category
from utils.ui  import inject_css, section_header, stat_card

st.set_page_config(page_title="FitPro AI — Profile", page_icon="👤", layout="wide")
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

inject_css()

username  = st.session_state.get("username", "")
profile   = load_profile(username)
today_str = date.today().isoformat()

# ── TOPNAV ─────────────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([4, 4, 2])
with c1:
    st.markdown("""<div style="font-family:'Syne',sans-serif;font-size:1.45rem;font-weight:800;
      background:linear-gradient(135deg,#5b5bd6,#a78bfa);-webkit-background-clip:text;
      -webkit-text-fill-color:transparent;padding:16px 0 14px;
      border-bottom:1px solid rgba(120,119,198,0.14);margin-bottom:26px">⚡ FitPro AI</div>""",
      unsafe_allow_html=True)
with c2:
    st.markdown("""<div style="padding:16px 0 14px;border-bottom:1px solid rgba(120,119,198,0.14);
      margin-bottom:26px;text-align:center">
      <span style="font-size:0.62rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;
        padding:4px 14px;border:1px solid rgba(120,119,198,0.32);border-radius:100px;
        color:#a78bfa;background:rgba(124,124,247,0.06)">MY PROFILE</span></div>""",
      unsafe_allow_html=True)
with c3:
    st.markdown('<div style="padding:10px 0 4px;border-bottom:1px solid rgba(120,119,198,0.14);margin-bottom:26px">',
                unsafe_allow_html=True)
    if st.button("🏠 Dashboard", key="back_dash", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")
    st.markdown("</div>", unsafe_allow_html=True)

# ── DATA ───────────────────────────────────────────────────────────────────────
name_d   = profile.get("name", username) if profile else username
age_v    = profile.get("age",   "—")    if profile else "—"
weight_v = profile.get("weight","—")    if profile else "—"
height_v = profile.get("height","—")    if profile else "—"
goal_v   = profile.get("goal",  "—")    if profile else "—"
level_v  = profile.get("level", "—")    if profile else "—"
gender_v = profile.get("gender","—")    if profile else "—"

bmi_v = bmi_cat_v = "—"
if profile and profile.get("weight") and profile.get("height"):
    bmi_v     = calculate_bmi(profile["weight"], profile["height"])
    bmi_cat_v = bmi_category(bmi_v)

bmi_color = {"Underweight":"#f59e0b","Normal Weight":"#10d9a0",
             "Overweight":"#f97316","Obese":"#f43f5e"}.get(bmi_cat_v,"#7c7cf7")

initials  = "".join(w[0].upper() for w in name_d.split()[:2]) or "FP"
tracking  = load_tracking(username)
done_count= sum(1 for v in tracking.values() if v.get("status")=="done")

latest_wt    = get_latest_weight(username)
current_wt   = latest_wt["weight"] if latest_wt else (profile.get("weight",70) if profile else 70)

# Diet targets from AI plan
workout_rec  = load_latest_workout(username)
plan_text    = workout_rec["plan_text"] if workout_rec else ""
diet_text    = ""
if plan_text and "##DIET##" in plan_text:
    diet_text = plan_text.split("##DIET##",1)[1].strip()

def _parse_diet_targets(text):
    t = {"calories":2000,"protein":150,"carbs":250,"fats":65,"fiber":30}
    for line in text.split("\n")[:50]:
        s = line.strip().lower()
        for key, pat in [("calories",r"calories[:\s]+(\d+)"),("protein",r"protein[:\s]+(\d+)"),
                         ("carbs",r"carbs[:\s]+(\d+)"),("fats",r"fats?[:\s]+(\d+)"),
                         ("fiber",r"fibre?[:\s]+(\d+)")]:
            m = re.search(pat, s)
            if m: t[key] = int(m.group(1))
    return t

diet_targets = _parse_diet_targets(diet_text) if diet_text else {"calories":2000,"protein":150,"carbs":250,"fats":65,"fiber":30}
cal_target   = diet_targets["calories"]
prot_target  = diet_targets["protein"]
carb_target  = diet_targets["carbs"]
fat_target   = diet_targets["fats"]
fib_target   = diet_targets["fiber"]

# ── PROFILE HERO ───────────────────────────────────────────────────────────────
def _pill(label, value, unit, color):
    return f"""
<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(120,119,198,0.18);
  border-radius:10px;padding:12px 16px;text-align:center;min-width:72px">
  <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:800;color:{color}">{value}</div>
  <div style="font-size:0.59rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;
    color:rgba(238,238,255,0.35);margin-top:3px">{label}</div>
  {f'<div style="font-size:0.62rem;color:{color};opacity:0.65;margin-top:1px">{unit}</div>' if unit else ''}
</div>"""

st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(91,91,214,0.14),rgba(124,124,247,0.05));
  border:1px solid rgba(124,124,247,0.22);border-radius:16px;
  padding:28px 32px;margin-bottom:28px;position:relative;overflow:hidden">
  <div style="position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,#5b5bd6,#a78bfa,transparent)"></div>
  <div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap">
    <div style="width:76px;height:76px;border-radius:50%;flex-shrink:0;
      background:linear-gradient(135deg,#5b5bd6,#7c3aed);
      display:flex;align-items:center;justify-content:center;
      font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;color:#fff;
      box-shadow:0 0 0 3px rgba(124,124,247,0.25),0 0 20px rgba(124,124,247,0.28)">{initials}</div>
    <div style="flex:1;min-width:160px">
      <div style="font-family:'Syne',sans-serif;font-size:1.55rem;font-weight:800;
        color:#eeeeff;line-height:1">{name_d}</div>
      <div style="font-size:0.66rem;color:rgba(238,238,255,0.32);letter-spacing:1.5px;
        text-transform:uppercase;margin-top:4px">@{username}</div>
      <div style="display:flex;gap:10px;margin-top:9px;flex-wrap:wrap">
        <span style="font-size:0.75rem;color:rgba(238,238,255,0.50)">🎯 {goal_v}</span>
        <span style="color:rgba(124,124,247,0.25)">·</span>
        <span style="font-size:0.75rem;color:rgba(238,238,255,0.50)">📊 {level_v}</span>
        <span style="color:rgba(124,124,247,0.25)">·</span>
        <span style="font-size:0.75rem;color:rgba(238,238,255,0.50)">⚥ {gender_v}</span>
      </div>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      {_pill("Age",    str(age_v),    "yrs",  "#a78bfa")}
      {_pill("Height", str(height_v), "cm",   "#38bdf8")}
      {_pill("Weight", str(current_wt)+"kg","latest","#10d9a0")}
      {_pill("BMI",    str(bmi_v),    bmi_cat_v[:10] if bmi_cat_v!="—" else "", bmi_color)}
      {_pill("Done",   str(done_count),"workouts","#f59e0b")}
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_today, tab_water, tab_diet_tab, tab_weight, tab_edit = st.tabs([
    "📋 Today's Summary",
    "💧 Water Intake",
    "🥗 Diet Log",
    "⚖️ Weight Tracker",
    "✏️ Edit Profile",
])

# ─────────────────────────────────────────────────────────────────────────────
# TODAY'S SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
with tab_today:
    st.markdown(section_header("Today's Overview", date.today().strftime("%A, %B %d %Y")),
                unsafe_allow_html=True)

    water_data   = get_water_today(username, today_str)
    w_ml         = water_data["amount_ml"]
    w_goal_ml    = water_data["goal_ml"]
    w_pct        = min(int(w_ml / w_goal_ml * 100), 100) if w_goal_ml else 0
    totals       = get_diet_totals(username, today_str)
    entries_today= get_diet_today(username, today_str)
    w_status     = tracking.get(today_str, {}).get("status", "pending")
    w_icon       = {"done":"✅","skipped":"⏭️","pending":"⏳"}[w_status]
    w_col        = {"done":"#10d9a0","skipped":"#f59e0b","pending":"#7c7cf7"}[w_status]

    s1,s2,s3,s4 = st.columns(4)
    with s1: st.markdown(stat_card("💧","Water",f"{w_ml}ml",f"of {w_goal_ml}ml · {w_pct}%","#38bdf8"), unsafe_allow_html=True)
    with s2: st.markdown(stat_card("🔥","Calories",f"{int(totals['calories'])}",f"/ {cal_target} kcal","#f97316"), unsafe_allow_html=True)
    with s3: st.markdown(stat_card("💪","Protein",f"{int(totals['protein'])}g",f"/ {prot_target}g","#10d9a0"), unsafe_allow_html=True)
    with s4: st.markdown(stat_card(w_icon,"Workout",w_status.capitalize(),"today",w_col), unsafe_allow_html=True)

    # Macro progress bars
    st.markdown(section_header("Nutrition Progress", "Today vs daily target"), unsafe_allow_html=True)

    def _bar(label, consumed, target, color, unit="g"):
        pct  = min(int(consumed / target * 100), 100) if target else 0
        over = consumed > target
        bc   = "#f43f5e" if over else color
        return f"""
<div style="background:#0f0f22;border:1px solid rgba(120,119,198,0.12);
  border-radius:10px;padding:13px 16px;margin-bottom:8px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:7px">
    <span style="font-size:0.82rem;font-weight:600;color:#eeeeff">{label}</span>
    <span style="font-size:0.76rem;color:rgba(238,238,255,0.40)">
      <span style="color:{bc};font-weight:700">{int(consumed)}{unit}</span>
      &nbsp;/&nbsp;{int(target)}{unit}&nbsp;
      <span style="font-size:0.62rem;color:rgba(238,238,255,0.28)">({pct}%)</span>
    </span>
  </div>
  <div style="height:7px;background:rgba(255,255,255,0.06);border-radius:100px;overflow:hidden">
    <div style="height:100%;width:{pct}%;background:{bc};border-radius:100px;transition:width 0.6s ease"></div>
  </div>
</div>"""

    mb1, mb2 = st.columns(2)
    with mb1:
        st.markdown(_bar("🔥 Calories", totals["calories"], cal_target, "#f97316","kcal"), unsafe_allow_html=True)
        st.markdown(_bar("💪 Protein",  totals["protein"],  prot_target,"#10d9a0"), unsafe_allow_html=True)
        st.markdown(_bar("💧 Water",     w_ml, w_goal_ml, "#38bdf8","ml"), unsafe_allow_html=True)
    with mb2:
        st.markdown(_bar("🍞 Carbs",  totals["carbs"], carb_target, "#a78bfa"), unsafe_allow_html=True)
        st.markdown(_bar("🥑 Fats",   totals["fats"],  fat_target,  "#f59e0b"), unsafe_allow_html=True)
        st.markdown(_bar("🌾 Fiber",  totals["fiber"], fib_target,  "#38bdf8"), unsafe_allow_html=True)

    # Today's meals
    if entries_today:
        st.markdown(section_header("Meals Logged", f"{len(entries_today)} items today"), unsafe_allow_html=True)
        for e in entries_today:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:10px 14px;
              background:rgba(255,255,255,0.025);border:1px solid rgba(120,119,198,0.10);
              border-radius:9px;margin-bottom:5px">
              <span style="font-size:0.95rem">🍽️</span>
              <div style="flex:1">
                <div style="font-size:0.85rem;font-weight:600;color:#eeeeff">{e['meal_name']}</div>
                <div style="font-size:0.68rem;color:rgba(238,238,255,0.35);margin-top:2px">
                  {int(e['calories'])} kcal · {int(e['protein'])}g P · {int(e['carbs'])}g C · {int(e['fats'])}g F
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

    # Diet plan excerpt
    if diet_text:
        st.markdown(section_header("Allocated Diet Plan", "From your AI-generated plan"), unsafe_allow_html=True)
        lines = [l.strip() for l in diet_text.split("\n") if l.strip()][:40]
        shown = ""
        for l in lines:
            if l.startswith("##"):
                c = re.sub(r"^#+\s*","",l)
                shown += f'<div style="font-size:0.75rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#a78bfa;margin:12px 0 5px">{c}</div>'
            elif l.startswith("**") and l.endswith("**"):
                shown += f'<div style="font-size:0.82rem;font-weight:700;color:#eeeeff;margin:8px 0 4px">{l[2:-2]}</div>'
            elif re.match(r"^[-•*]\s+", l):
                ct = re.sub(r"^[-•*]+\s*","",l)
                ct = re.sub(r"\*\*(.+?)\*\*",r"<strong>\1</strong>",ct)
                shown += f'<div style="font-size:0.79rem;color:rgba(238,238,255,0.52);padding:2px 0 2px 10px">▸ {ct}</div>'
            else:
                shown += f'<div style="font-size:0.79rem;color:rgba(238,238,255,0.40);padding:2px 0">{l}</div>'
        st.markdown(f"""
        <div style="background:#0f0f22;border:1px solid rgba(120,119,198,0.14);
          border-radius:12px;padding:20px 22px;max-height:320px;overflow-y:auto">{shown}</div>""",
          unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# WATER INTAKE
# ─────────────────────────────────────────────────────────────────────────────
with tab_water:
    water_data = get_water_today(username, today_str)
    w_ml       = water_data["amount_ml"]
    w_goal_ml  = water_data["goal_ml"]
    w_pct      = min(int(w_ml / w_goal_ml * 100), 100) if w_goal_ml else 0
    w_rem      = max(w_goal_ml - w_ml, 0)
    cups       = max(int(w_ml / 250), 0)
    total_cups = max(int(w_goal_ml / 250), 1)

    st.markdown(section_header("💧 Water Intake Tracker", f"Goal: {w_goal_ml}ml per day"),
                unsafe_allow_html=True)

    # Big display
    cup_row = "".join(
        f'<span style="font-size:1.4rem;opacity:{1.0 if i<cups else 0.15}">💧</span>'
        for i in range(min(total_cups, 12))
    )
    goal_reached_html = """
<div style="margin-top:14px;padding:10px 18px;background:rgba(56,189,248,0.14);
  border-radius:8px;font-size:0.82rem;color:#38bdf8;font-weight:700;text-align:center">
  🎉 Daily goal reached! Outstanding hydration!</div>""" if w_pct >= 100 else ""

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(56,189,248,0.10),rgba(14,165,233,0.04));
      border:1px solid rgba(56,189,248,0.24);border-radius:16px;padding:28px;
      margin-bottom:20px;text-align:center;position:relative;overflow:hidden">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;
        background:linear-gradient(90deg,transparent,#38bdf8,transparent)"></div>
      <div style="font-size:0.58rem;font-weight:700;letter-spacing:3px;text-transform:uppercase;
        color:#38bdf8;margin-bottom:10px">Today's Hydration</div>
      <div style="font-family:'Syne',sans-serif;font-size:3.8rem;font-weight:800;
        color:#38bdf8;line-height:1">{w_ml}<span style="font-size:1.1rem;opacity:0.55">ml</span></div>
      <div style="font-size:0.82rem;color:rgba(238,238,255,0.42);margin:6px 0 18px">
        {w_rem}ml remaining · {w_pct}% of daily goal</div>
      <div style="height:10px;background:rgba(255,255,255,0.06);border-radius:100px;
        overflow:hidden;margin-bottom:18px">
        <div style="height:100%;width:{w_pct}%;background:linear-gradient(90deg,#0ea5e9,#38bdf8);
          border-radius:100px;{'box-shadow:0 0 14px rgba(56,189,248,0.50)' if w_pct>=100 else ''}"></div>
      </div>
      <div style="display:flex;justify-content:center;gap:5px;flex-wrap:wrap;margin-bottom:6px">
        {cup_row}
      </div>
      <div style="font-size:0.68rem;color:rgba(238,238,255,0.28)">{cups} of {total_cups} glasses · 250ml each</div>
      {goal_reached_html}
    </div>""", unsafe_allow_html=True)

    # Quick-add buttons
    st.markdown("**Quick Add:**")
    qa1,qa2,qa3,qa4 = st.columns(4)
    for col, (lbl, ml) in zip([qa1,qa2,qa3,qa4],[("💧 150ml",150),("💧 250ml",250),("💧 500ml",500),("💧 1 Litre",1000)]):
        with col:
            if st.button(lbl, use_container_width=True, key=f"wadd_{ml}"):
                add_water(username, today_str, ml); st.rerun()

    ca1, ca2, ca3 = st.columns([3,1,1])
    with ca1:
        custom_ml = st.number_input("Custom amount (ml)",50,2000,200,50,key="cwater")
    with ca2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("➕ Add",use_container_width=True,key="wadd_custom"):
            add_water(username, today_str, custom_ml); st.rerun()
    with ca3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Reset",use_container_width=True,key="wreset"):
            reset_water(username, today_str); st.rerun()

    # Goal slider
    st.markdown("<hr>", unsafe_allow_html=True)
    g1, g2 = st.columns([4,1])
    with g1:
        goal_opts = [1500,1750,2000,2250,2500,2750,3000,3500,4000]
        safe_goal = w_goal_ml if w_goal_ml in goal_opts else 2500
        new_goal  = st.select_slider("Daily Water Goal (ml)", options=goal_opts, value=safe_goal,
            format_func=lambda x: f"{x}ml")
    with g2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Set Goal",use_container_width=True,key="wgoal"):
            set_water_goal(username, today_str, new_goal)
            st.success("Goal updated!"); st.rerun()

    # 14-day history bars
    history = get_water_history(username, 14)
    if len(history) > 1:
        st.markdown(section_header("14-Day History","Daily intake"), unsafe_allow_html=True)
        max_ml = max(r["amount_ml"] for r in history) or 2500
        bhtml  = "<div style='display:flex;align-items:flex-end;gap:5px;height:80px;margin-bottom:6px'>"
        for r in reversed(history):
            h   = max(int(r["amount_ml"]/max_ml*72), 3)
            hit = r["amount_ml"] >= r["goal_ml"]
            bg  = "#38bdf8" if hit else "rgba(56,189,248,0.35)"
            try: dl = datetime.strptime(r["date"],"%Y-%m-%d").strftime("%d")
            except: dl = r["date"][-2:]
            bhtml += (f"<div style='flex:1;display:flex;flex-direction:column;align-items:center;gap:3px'>"
                      f"<div style='width:100%;height:{h}px;background:{bg};border-radius:4px 4px 0 0'></div>"
                      f"<div style='font-size:0.50rem;color:rgba(238,238,255,0.28)'>{dl}</div></div>")
        bhtml += "</div>"
        st.markdown(f"""
        <div style="background:#0f0f22;border:1px solid rgba(120,119,198,0.14);
          border-radius:12px;padding:16px 18px">{bhtml}
          <div style="font-size:0.62rem;color:rgba(238,238,255,0.28);text-align:right;margin-top:4px">
            Bright blue = goal reached</div></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DIET LOG
# ─────────────────────────────────────────────────────────────────────────────
with tab_diet_tab:
    totals  = get_diet_totals(username, today_str)
    entries = get_diet_today(username, today_str)

    st.markdown(section_header("🥗 Diet Log", f"Log & track your meals for {date.today().strftime('%b %d')}"),
                unsafe_allow_html=True)

    t1,t2,t3,t4,t5 = st.columns(5)
    with t1: st.markdown(stat_card("🔥","Calories",f"{int(totals['calories'])}",f"/{cal_target} kcal","#f97316"), unsafe_allow_html=True)
    with t2: st.markdown(stat_card("💪","Protein", f"{int(totals['protein'])}g", f"/{prot_target}g","#10d9a0"), unsafe_allow_html=True)
    with t3: st.markdown(stat_card("🍞","Carbs",   f"{int(totals['carbs'])}g",  f"/{carb_target}g","#a78bfa"), unsafe_allow_html=True)
    with t4: st.markdown(stat_card("🥑","Fats",    f"{int(totals['fats'])}g",   f"/{fat_target}g", "#f59e0b"), unsafe_allow_html=True)
    with t5: st.markdown(stat_card("🌾","Fiber",   f"{int(totals['fiber'])}g",  f"/{fib_target}g", "#38bdf8"), unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Log form
    st.markdown(section_header("Log a Meal","Enter what you ate"), unsafe_allow_html=True)
    with st.form("meal_form", clear_on_submit=True):
        meal_name = st.text_input("Meal / Food Name", placeholder="e.g. Chicken Breast + Rice")
        mf1,mf2,mf3,mf4,mf5 = st.columns(5)
        with mf1: mc  = st.number_input("Calories",0,5000,0,10,key="mc")
        with mf2: mp  = st.number_input("Protein (g)",0.0,500.0,0.0,0.5,key="mp")
        with mf3: mcb = st.number_input("Carbs (g)",  0.0,500.0,0.0,0.5,key="mcb")
        with mf4: mf  = st.number_input("Fats (g)",   0.0,500.0,0.0,0.5,key="mf")
        with mf5: mfb = st.number_input("Fiber (g)",  0.0,100.0,0.0,0.5,key="mfb")
        if st.form_submit_button("➕ Log Meal", use_container_width=True):
            if meal_name.strip():
                log_diet(username, today_str, meal_name.strip(), mc, mp, mcb, mf, mfb)
                st.success(f"✅ '{meal_name}' logged!"); st.rerun()
            else:
                st.error("Enter a meal name.")

    # Quick items
    st.markdown("**Quick Log — common foods:**")
    QUICK = [
        ("🍳 Eggs ×2",    156,13,1,11,0),("🍗 Chicken 100g",165,31,0,4,0),
        ("🍚 Rice 100g",  130,3,28,0,0), ("🥛 Milk 250ml",  122,8,12,5,0),
        ("🍌 Banana",      89,1,23,0,3), ("🥜 Almonds 30g", 174,6,6,15,4),
        ("🥚 Oats 50g",   190,7,32,3,5), ("🧀 Paneer 100g", 265,18,4,20,0),
        ("🍎 Apple",       95,0,25,0,4), ("🥤 Whey Shake",  120,25,4,2,0),
    ]
    qcols = st.columns(5)
    for i,(ql,qcal,qp,qc,qft,qfb) in enumerate(QUICK):
        with qcols[i%5]:
            if st.button(ql,use_container_width=True,key=f"q_{i}"):
                log_diet(username,today_str,ql,qcal,qp,qc,qft,qfb); st.rerun()

    # Logged entries
    if entries:
        st.markdown(section_header("Today's Meals",f"{len(entries)} logged"), unsafe_allow_html=True)
        for e in entries:
            ec1, ec2 = st.columns([5,1])
            with ec1:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.025);border:1px solid rgba(120,119,198,0.10);
                  border-radius:9px;padding:11px 15px;margin-bottom:5px">
                  <div style="font-size:0.86rem;font-weight:600;color:#eeeeff">{e['meal_name']}</div>
                  <div style="display:flex;gap:12px;margin-top:5px;flex-wrap:wrap">
                    <span style="font-size:0.69rem;color:#f97316">🔥 {int(e['calories'])} kcal</span>
                    <span style="font-size:0.69rem;color:#10d9a0">💪 {int(e['protein'])}g P</span>
                    <span style="font-size:0.69rem;color:#a78bfa">🍞 {int(e['carbs'])}g C</span>
                    <span style="font-size:0.69rem;color:#f59e0b">🥑 {int(e['fats'])}g F</span>
                    <span style="font-size:0.69rem;color:#38bdf8">🌾 {int(e['fiber'])}g Fb</span>
                  </div>
                </div>""", unsafe_allow_html=True)
            with ec2:
                if st.button("🗑️",key=f"dd_{e['id']}",help="Delete"):
                    delete_diet_entry(e["id"]); st.rerun()
    else:
        st.markdown("""<div style="text-align:center;padding:32px;font-size:0.86rem;
          color:rgba(238,238,255,0.28)">No meals logged yet. Add one above!</div>""",
          unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# WEIGHT TRACKER
# ─────────────────────────────────────────────────────────────────────────────
with tab_weight:
    st.markdown(section_header("⚖️ Weight Tracker","Log monthly check-ins, track your progress"),
                unsafe_allow_html=True)

    wt_history   = get_weight_history(username, 24)
    start_wt     = float(profile.get("weight",70)) if profile else 70.0
    curr_wt      = latest_wt["weight"] if latest_wt else start_wt
    delta        = round(curr_wt - start_wt, 1)
    delta_sign   = "+" if delta > 0 else ""
    delta_color  = "#f43f5e" if delta > 0 else "#10d9a0" if delta < 0 else "#a78bfa"

    w1,w2,w3 = st.columns(3)
    with w1: st.markdown(stat_card("⚖️","Current",f"{curr_wt}kg","latest entry","#10d9a0"), unsafe_allow_html=True)
    with w2: st.markdown(stat_card("📍","Starting",f"{start_wt}kg","from profile","#a78bfa"), unsafe_allow_html=True)
    with w3: st.markdown(stat_card("📈","Change",f"{delta_sign}{delta}kg","since start",delta_color), unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    st.markdown(section_header("Log Your Weight","Record today's weigh-in"), unsafe_allow_html=True)

    with st.form("wt_form"):
        wf1,wf2 = st.columns([3,2])
        with wf1:
            new_wt = st.number_input("Weight (kg)",30.0,300.0,
                                      value=float(curr_wt),step=0.1,format="%.1f")
        with wf2:
            wt_note = st.text_input("Note (optional)",placeholder="morning / post-workout")
        if st.form_submit_button("💾 Save Weight Entry",use_container_width=True):
            log_weight(username, today_str, new_wt, wt_note)
            st.success(f"✅ {new_wt}kg logged for {today_str}!"); st.rerun()

    # Chart
    if wt_history:
        st.markdown(section_header("Progress Chart",f"{len(wt_history)} entries"), unsafe_allow_html=True)
        weights = [r["weight"] for r in wt_history]
        dates   = [r["date"]   for r in wt_history]
        mn = min(weights)-2; mx = max(weights)+2; rng = mx-mn or 1
        CW = 580; CH = 150; n = len(weights)

        path_d = ""; dots = ""; grid_lines = ""
        for i,(d,w) in enumerate(zip(dates,weights)):
            x = int(40 + (i/max(n-1,1))*(CW-60))
            y = int(CH-20 - ((w-mn)/rng)*(CH-50))
            if i==0: path_d += f"M{x},{y}"
            else:    path_d += f" L{x},{y}"
            is_last = (i==n-1)
            fc = "#10d9a0" if is_last else "#7c7cf7"
            r2 = 6 if is_last else 4
            try: dl = datetime.strptime(d,"%Y-%m-%d").strftime("%b '%y" if n<=8 else "%d/%m")
            except: dl = d[-5:]
            dots += (f'<circle cx="{x}" cy="{y}" r="{r2}" fill="{fc}" stroke="#07070f" stroke-width="2"/>'
                     f'<text x="{x}" y="{y-11}" text-anchor="middle" font-size="9" '
                     f'font-family="DM Sans,sans-serif" fill="rgba(238,238,255,0.55)">{w}kg</text>'
                     f'<text x="{x}" y="{CH-3}" text-anchor="middle" font-size="8" '
                     f'font-family="DM Sans,sans-serif" fill="rgba(238,238,255,0.25)">{dl}</text>')

        for gi in range(4):
            gy = int(20+(gi/3)*(CH-50)); gv = round(mx-(gi/3)*rng,1)
            grid_lines += (f'<line x1="35" y1="{gy}" x2="{CW-10}" y2="{gy}" '
                           f'stroke="rgba(255,255,255,0.06)" stroke-width="1"/>'
                           f'<text x="30" y="{gy+3}" text-anchor="end" font-size="8" '
                           f'font-family="DM Sans,sans-serif" fill="rgba(238,238,255,0.28)">{gv}</text>')

        st.markdown(f"""
        <div style="background:#0f0f22;border:1px solid rgba(120,119,198,0.14);
          border-radius:12px;padding:18px;overflow-x:auto">
          <svg width="100%" viewBox="0 0 {CW} {CH}" style="min-width:300px">
            <defs>
              <linearGradient id="wtg" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stop-color="#7c7cf7"/>
                <stop offset="100%" stop-color="#10d9a0"/>
              </linearGradient>
            </defs>
            {grid_lines}
            <path d="{path_d}" fill="none" stroke="url(#wtg)"
              stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            {dots}
          </svg>
        </div>""", unsafe_allow_html=True)

        # History list
        st.markdown(section_header("Log History","Recent entries"), unsafe_allow_html=True)
        for r in reversed(wt_history[-12:]):
            try: dfmt = datetime.strptime(r["date"],"%Y-%m-%d").strftime("%a, %b %d %Y")
            except: dfmt = r["date"]
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:14px;padding:10px 14px;
              background:rgba(255,255,255,0.025);border:1px solid rgba(120,119,198,0.10);
              border-radius:9px;margin-bottom:5px">
              <span style="font-size:0.78rem;color:rgba(238,238,255,0.38);min-width:140px">{dfmt}</span>
              <span style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:800;
                color:#10d9a0">{r['weight']} kg</span>
              {f'<span style="font-size:0.74rem;color:rgba(238,238,255,0.32);flex:1">{r["note"]}</span>' if r.get("note") else ''}
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style="text-align:center;padding:40px;font-size:0.88rem;
          color:rgba(238,238,255,0.28)">No entries yet. Log your first weigh-in above!</div>""",
          unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# EDIT PROFILE
# ─────────────────────────────────────────────────────────────────────────────
with tab_edit:
    st.markdown(section_header("Edit Profile","Update your personal details"), unsafe_allow_html=True)
    with st.form("edit_form"):
        ep1,ep2 = st.columns(2)
        with ep1:
            ep_name = st.text_input("Full Name", value=profile.get("name","") if profile else "")
            ep_age  = st.number_input("Age",15,80, value=int(profile.get("age",25)) if profile else 25)
            ep_gen  = st.selectbox("Gender",["Male","Female","Other"],
                index=["Male","Female","Other"].index(profile.get("gender","Male")) if profile else 0)
        with ep2:
            ep_h = st.number_input("Height (cm)",100,250, value=int(profile.get("height",170)) if profile else 170)
            ep_w = st.number_input("Weight (kg)",30,300,  value=int(profile.get("weight",70))  if profile else 70)
            goals = ["Build Muscle","Weight Loss","Strength Gain","Abs Building",
                     "Flexibility & Mobility","General Fitness"]
            ep_g = st.selectbox("Goal",goals,
                index=goals.index(profile.get("goal","Build Muscle")) if profile and profile.get("goal") in goals else 0)
        ep_l = st.selectbox("Level",["Beginner","Intermediate","Advanced"],
            index=["Beginner","Intermediate","Advanced"].index(profile.get("level","Beginner")) if profile else 0)
        s1,s2 = st.columns(2)
        with s1: save_btn   = st.form_submit_button("💾 Save Changes", use_container_width=True)
        with s2: cancel_btn = st.form_submit_button("Cancel",          use_container_width=True)

    if save_btn:
        save_profile(username, {"name":ep_name,"age":ep_age,"gender":ep_gen,
            "height":ep_h,"weight":ep_w,"goal":ep_g,"level":ep_l,
            "equipment": profile.get("equipment",[]) if profile else []})
        st.success("✅ Profile updated!"); st.rerun()
