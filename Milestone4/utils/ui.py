
"""
ui.py — Expert-level dark design system with fixed calendar + vivid components.
"""

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:       #07070f;
  --bg2:      #0d0d1a;
  --bg3:      #13132a;
  --bg4:      #1a1a35;
  --border:   rgba(120,119,198,0.18);
  --border2:  rgba(120,119,198,0.35);
  --accent:   #7c7cf7;
  --accent2:  #a78bfa;
  --green:    #10d9a0;
  --amber:    #f59e0b;
  --red:      #f43f5e;
  --text:     #eeeeff;
  --text2:    rgba(238,238,255,0.75);
  --muted:    rgba(238,238,255,0.45);
  --muted2:   rgba(238,238,255,0.25);
  --muted3:   rgba(238,238,255,0.12);
  --radius:   14px;
  --radius-sm:9px;
  --font-head:'Syne', sans-serif;
  --font-body:'DM Sans', sans-serif;
  --font-mono:'JetBrains Mono', monospace;
}

#MainMenu,footer,header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] { display:none!important; }

html,body { background:#07070f!important; }

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"]>section {
  background:#07070f!important;
  color:#eeeeff!important;
  font-family:'DM Sans',sans-serif!important;
}

[data-testid="stAppViewContainer"]>section>div.block-container {
  max-width:1220px!important;
  margin:0 auto!important;
  padding:0 28px 100px!important;
  background:transparent!important;
}

h1,h2,h3,h4 { font-family:'Syne',sans-serif!important; color:#eeeeff!important; }

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
.stTextInput>label, .stNumberInput>label,
.stSelectbox>label, .stMultiSelect>label,
.stCheckbox>label, .stRadio>label {
  color:rgba(238,238,255,0.55)!important;
  font-size:0.70rem!important; font-weight:600!important;
  letter-spacing:1.8px!important; text-transform:uppercase!important;
}

div[data-baseweb="input"]>div,
div[data-baseweb="textarea"]>div {
  background:#0f0f22!important;
  border:1.5px solid rgba(120,119,198,0.22)!important;
  border-radius:9px!important; transition:all 0.2s!important;
}
div[data-baseweb="input"]:focus-within>div,
div[data-baseweb="textarea"]:focus-within>div {
  border-color:#7c7cf7!important;
  box-shadow:0 0 0 3px rgba(124,124,247,0.15)!important;
  background:#13132a!important;
}
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
  background:transparent!important; color:#eeeeff!important;
  font-family:'DM Sans',sans-serif!important; font-size:0.92rem!important;
}
div[data-baseweb="input"] input::placeholder { color:rgba(238,238,255,0.22)!important; }

div[data-baseweb="select"]>div {
  background:#0f0f22!important;
  border:1.5px solid rgba(120,119,198,0.22)!important;
  border-radius:9px!important; color:#eeeeff!important; transition:all 0.2s!important;
}
div[data-baseweb="select"]>div:focus-within {
  border-color:#7c7cf7!important; box-shadow:0 0 0 3px rgba(124,124,247,0.15)!important;
}
div[data-baseweb="select"] span { color:#eeeeff!important; }
div[data-baseweb="popover"] {
  background:#0d0d1a!important;
  border:1px solid rgba(120,119,198,0.28)!important;
  border-radius:12px!important; box-shadow:0 24px 64px rgba(0,0,0,0.85)!important;
}
li[role="option"] {
  color:rgba(238,238,255,0.45)!important;
  font-family:'DM Sans',sans-serif!important;
  border-radius:6px!important; margin:2px 6px!important;
}
li[role="option"]:hover { background:rgba(124,124,247,0.18)!important; color:#eeeeff!important; }
li[aria-selected="true"] { background:rgba(124,124,247,0.25)!important; color:#eeeeff!important; }

div[data-baseweb="multi-select"]>div {
  background:#0f0f22!important;
  border:1.5px solid rgba(120,119,198,0.22)!important;
  border-radius:9px!important; min-height:46px!important;
}
span[data-baseweb="tag"] {
  background:rgba(124,124,247,0.20)!important;
  border:1px solid rgba(124,124,247,0.38)!important; border-radius:5px!important;
}
span[data-baseweb="tag"] span { color:#eeeeff!important; font-size:0.80rem!important; }

[data-testid="stCheckbox"] label {
  color:rgba(238,238,255,0.75)!important; font-size:0.88rem!important;
  letter-spacing:0!important; text-transform:none!important; font-weight:400!important;
}

.stButton>button {
  background:linear-gradient(135deg,#5b5bd6,#7c3aed)!important;
  border:none!important; color:#fff!important; border-radius:9px!important;
  font-family:'DM Sans',sans-serif!important; font-size:0.87rem!important;
  font-weight:600!important; padding:11px 22px!important;
  letter-spacing:0.3px!important; transition:all 0.2s ease!important;
  box-shadow:0 4px 18px rgba(91,91,214,0.35)!important;
}
.stButton>button:hover {
  transform:translateY(-2px)!important;
  box-shadow:0 10px 34px rgba(91,91,214,0.56)!important;
  filter:brightness(1.10)!important;
}
.stButton>button:active { transform:translateY(0)!important; }

.stTabs [data-baseweb="tab-list"] {
  background:#0d0d1a!important; border-radius:9px!important;
  padding:4px!important; gap:3px!important;
  border:1px solid rgba(120,119,198,0.18)!important;
}
.stTabs [data-baseweb="tab"] {
  background:transparent!important; color:rgba(238,238,255,0.45)!important;
  border-radius:6px!important; font-family:'DM Sans',sans-serif!important;
  font-size:0.84rem!important; font-weight:500!important;
  border:none!important; padding:9px 18px!important; transition:all 0.2s!important;
}
.stTabs [aria-selected="true"] {
  background:linear-gradient(135deg,#5b5bd6,#7c3aed)!important;
  color:#fff!important; box-shadow:0 2px 14px rgba(91,91,214,0.45)!important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display:none!important; }

.stProgress>div>div {
  background:linear-gradient(90deg,#5b5bd6,#a78bfa)!important; border-radius:100px!important;
}
.stProgress>div { background:rgba(255,255,255,0.06)!important; border-radius:100px!important; }

.stAlert { border-radius:9px!important; font-size:0.88rem!important; }
hr { border-color:rgba(120,119,198,0.14)!important; margin:20px 0!important; }

::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:#07070f; }
::-webkit-scrollbar-thumb { background:rgba(124,124,247,0.30); border-radius:100px; }
::-webkit-scrollbar-thumb:hover { background:rgba(124,124,247,0.55); }

@keyframes fadeUp {
  from { opacity:0; transform:translateY(10px); }
  to   { opacity:1; transform:translateY(0); }
}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(BASE_CSS, unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────────────────
# COMPONENTS
# ──────────────────────────────────────────────────────────────────────────────

def stat_card(icon, label, value, sub="", accent="#7c7cf7", glow=True):
    r, g, b = _hex_to_rgb_tuple(accent)
    glow_css = f"box-shadow:0 0 28px rgba({r},{g},{b},0.22);" if glow else ""
    return f"""
<div style="background:#0f0f22;border:1px solid rgba({r},{g},{b},0.25);
  border-radius:14px;padding:22px 16px;text-align:center;position:relative;
  overflow:hidden;animation:fadeUp 0.4s ease;{glow_css}">
  <div style="position:absolute;top:0;left:15%;right:15%;height:2px;
    background:linear-gradient(90deg,transparent,{accent},transparent);opacity:0.8"></div>
  <div style="font-size:1.55rem;margin-bottom:10px;line-height:1">{icon}</div>
  <div style="font-family:'Syne',sans-serif;font-size:2.1rem;font-weight:800;
    color:{accent};line-height:1;letter-spacing:-1.5px">{value}</div>
  <div style="font-size:0.59rem;font-weight:700;letter-spacing:2.5px;
    text-transform:uppercase;color:rgba(238,238,255,0.38);margin-top:8px">{label}</div>
  {f'<div style="font-size:0.72rem;color:rgba(238,238,255,0.22);margin-top:3px">{sub}</div>' if sub else ''}
</div>"""


def section_header(title, sub="", icon=""):
    return f"""
<div style="display:flex;align-items:center;gap:13px;margin:30px 0 16px;animation:fadeUp 0.35s ease">
  <div style="width:3px;height:22px;background:linear-gradient(180deg,#5b5bd6,#a78bfa);
    border-radius:2px;flex-shrink:0"></div>
  <div>
    <div style="font-family:'Syne',sans-serif;font-size:1.08rem;font-weight:700;
      color:#eeeeff;line-height:1.15">{icon+' ' if icon else ''}{title}</div>
    {f'<div style="font-size:0.74rem;color:rgba(238,238,255,0.42);margin-top:3px">{sub}</div>' if sub else ''}
  </div>
</div>"""


def badge(text, color="#7c7cf7"):
    return (f'<span style="display:inline-flex;align-items:center;background:{color}1a;'
            f'border:1px solid {color}44;border-radius:5px;padding:2px 10px;'
            f'font-size:0.70rem;font-weight:700;color:{color}">{text}</span>')


def exercise_card(icon, name, sets, reps, rest, idx=0, desc=""):
    desc_html = (f'<div style="font-size:0.70rem;color:rgba(238,238,255,0.30);'
                 f'margin-top:3px;line-height:1.5">{desc}</div>') if desc else ""
    sets_reps = (f'<span style="background:rgba(124,124,247,0.14);border:1px solid rgba(124,124,247,0.26);'
                 f'border-radius:6px;padding:3px 10px;font-size:0.70rem;font-weight:700;'
                 f'color:#a78bfa">{sets}x{reps}</span>') if sets else ""
    rest_badge = (f'<span style="background:rgba(245,158,11,0.10);border:1px solid rgba(245,158,11,0.22);'
                  f'border-radius:6px;padding:3px 10px;font-size:0.70rem;font-weight:600;'
                  f'color:#f59e0b">{rest}</span>') if rest and rest != "." else ""
    return f"""
<div style="display:flex;align-items:center;gap:12px;padding:10px;
  border-radius:9px;background:rgba(255,255,255,0.025);
  border:1px solid rgba(120,119,198,0.10);margin-bottom:5px">
  <div style="width:34px;height:34px;border-radius:8px;flex-shrink:0;
    background:rgba(124,124,247,0.12);border:1px solid rgba(124,124,247,0.22);
    display:flex;align-items:center;justify-content:center;font-size:0.85rem">{icon}</div>
  <div style="flex:1;min-width:0">
    <div style="font-size:0.85rem;font-weight:600;color:#eeeeff;
      white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{name}</div>
    {desc_html}
  </div>
  <div style="display:flex;gap:5px;flex-shrink:0">{sets_reps}{rest_badge}</div>
</div>"""


def progress_ring(pct, size=80, stroke=6, color="#7c7cf7"):
    r = (size - stroke) // 2
    circ = 2 * 3.14159 * r
    offset = circ * (1 - pct / 100)
    return f"""
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <circle cx="{size//2}" cy="{size//2}" r="{r}"
    fill="none" stroke="rgba(124,124,247,0.12)" stroke-width="{stroke}"/>
  <circle cx="{size//2}" cy="{size//2}" r="{r}"
    fill="none" stroke="{color}" stroke-width="{stroke}"
    stroke-dasharray="{circ:.1f}" stroke-dashoffset="{offset:.1f}"
    stroke-linecap="round" transform="rotate(-90 {size//2} {size//2})"/>
  <text x="50%" y="50%" text-anchor="middle" dominant-baseline="central"
    font-family="Syne,sans-serif" font-size="{size//5}" font-weight="800"
    fill="{color}">{pct}%</text>
</svg>"""


def calendar_widget(tracking, num_days, today_str):
    """
    Monthly calendar view showing full current month.
    Each cell displays the date number clearly, colored by workout status.
    """
    from datetime import date, timedelta
    import calendar as cal_mod

    today     = date.today()
    year      = today.year
    month     = today.month
    month_name = today.strftime("%B %Y")
    days_in_month  = cal_mod.monthrange(year, month)[1]
    first_weekday  = date(year, month, 1).weekday()   # 0=Mon … 6=Sun

    # ── Day-of-week header ────────────────────────────────────────────────────
    day_hdrs = "".join(
        f'<div style="text-align:center;font-size:0.63rem;font-weight:700;'
        f'letter-spacing:1px;text-transform:uppercase;'
        f'color:rgba(238,238,255,0.35);padding-bottom:6px">{d}</div>'
        for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    )

    # ── Blank leading cells ───────────────────────────────────────────────────
    cells = "".join('<div></div>' for _ in range(first_weekday))

    # ── Day cells ─────────────────────────────────────────────────────────────
    for day_num in range(1, days_in_month + 1):
        d  = date(year, month, day_num)
        ds = d.isoformat()
        s  = tracking.get(ds, {}).get("status", "none")
        is_today  = (d == today)
        is_future = (d > today)

        # colors
        if is_future:
            bg      = "rgba(255,255,255,0.03)"
            num_col = "rgba(238,238,255,0.18)"
            bdr     = "rgba(255,255,255,0.05)"
        elif s == "done":
            bg      = "#3d3d9e"
            num_col = "#ffffff"
            bdr     = "#5b5bd6"
        elif s == "skipped":
            bg      = "rgba(245,158,11,0.22)"
            num_col = "#f5c842"
            bdr     = "rgba(245,158,11,0.50)"
        elif d < today:                        # missed
            bg      = "rgba(244,63,94,0.10)"
            num_col = "rgba(244,63,94,0.55)"
            bdr     = "rgba(244,63,94,0.22)"
        else:                                  # today, pending
            bg      = "rgba(124,124,247,0.20)"
            num_col = "#c4b5fd"
            bdr     = "rgba(124,124,247,0.60)"

        today_ring = (
            "box-shadow:0 0 0 2px #7c7cf7,0 0 14px rgba(124,124,247,0.40);"
        ) if is_today else ""

        # small status dot below number
        dot = ""
        if s == "done":
            dot = '<div style="width:4px;height:4px;border-radius:50%;background:rgba(255,255,255,0.65);margin:2px auto 0"></div>'
        elif s == "skipped":
            dot = '<div style="width:4px;height:4px;border-radius:50%;background:#f59e0b;margin:2px auto 0"></div>'

        cells += f"""<div title="{ds}"
  style="background:{bg};border:1px solid {bdr};border-radius:7px;
  min-height:40px;display:flex;flex-direction:column;align-items:center;
  justify-content:center;cursor:pointer;padding:4px 2px;{today_ring}
  transition:transform 0.15s,opacity 0.15s"
  onmouseover="this.style.transform='scale(1.08)'"
  onmouseout="this.style.transform='scale(1)'">
  <span style="font-size:0.84rem;font-weight:700;color:{num_col};line-height:1">{day_num}</span>
  {dot}
</div>"""

    # ── Legend + container ────────────────────────────────────────────────────
    return f"""
<div>
  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
    <span style="font-family:'Syne',sans-serif;font-size:0.90rem;font-weight:700;color:#eeeeff">{month_name}</span>
    <div style="display:flex;gap:12px">
      <span style="display:flex;align-items:center;gap:5px;font-size:0.62rem;color:rgba(238,238,255,0.40)">
        <span style="width:9px;height:9px;border-radius:2px;background:#3d3d9e;display:inline-block"></span>Done
      </span>
      <span style="display:flex;align-items:center;gap:5px;font-size:0.62rem;color:rgba(238,238,255,0.40)">
        <span style="width:9px;height:9px;border-radius:2px;background:rgba(245,158,11,0.55);display:inline-block"></span>Skipped
      </span>
      <span style="display:flex;align-items:center;gap:5px;font-size:0.62rem;color:rgba(238,238,255,0.40)">
        <span style="width:9px;height:9px;border-radius:2px;background:rgba(244,63,94,0.40);display:inline-block"></span>Missed
      </span>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-bottom:4px">
    {day_hdrs}
  </div>
  <div style="display:grid;grid-template-columns:repeat(7,1fr);gap:4px">
    {cells}
  </div>
</div>"""


# ── internal helpers ──────────────────────────────────────────────────────────
def _hex_to_rgb_tuple(hex_color):
    h = hex_color.lstrip('#')
    try:
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except Exception:
        return 124, 124, 247

def _hex_to_rgb(hex_color):
    r, g, b = _hex_to_rgb_tuple(hex_color)
    return f"{r},{g},{b}"
