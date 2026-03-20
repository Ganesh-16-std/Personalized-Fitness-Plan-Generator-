
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.auth import initiate_signup, complete_signup, login

st.set_page_config(
    page_title="FitPro AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if st.session_state.get("logged_in"):
    st.switch_page("pages/2_Dashboard.py")

for k, v in [("mode","landing"),("signup_step","form"),
              ("pending_email",""),("login_err",""),
              ("signup_err",""),("otp_err","")]:
    if k not in st.session_state:
        st.session_state[k] = v

login_err     = st.session_state.pop("login_err",  "")
signup_err    = st.session_state.pop("signup_err", "")
otp_err       = st.session_state.pop("otp_err",    "")
mode          = st.session_state.mode
step          = st.session_state.signup_step
pending_email = st.session_state.get("pending_email","")

# ── GLOBAL STYLES ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&display=swap');

/* ── strip ALL streamlit chrome ── */
#MainMenu, footer, header,
[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stToolbarActions"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stSidebarNav"],
[data-testid="collapsedControl"], [data-testid="baseButton-header"],
.stDeployButton, button[kind="header"],
section[data-testid="stSidebar"] {
  display:none!important; visibility:hidden!important;
  height:0!important; overflow:hidden!important;
  position:absolute!important; pointer-events:none!important;
}

/* ── page background ── */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section {
  background: #07070f !important;
  color: #eeeeff !important;
  font-family: 'DM Sans', sans-serif !important;
  margin: 0 !important;
  padding: 0 !important;
}

/* ── kill ALL default block-container padding ── */
[data-testid="stAppViewContainer"] > section > div.block-container {
  padding: 0 !important;
  margin: 0 !important;
  max-width: 100% !important;
  width: 100% !important;
}

/* ── kill vertical gaps between streamlit elements ── */
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="element-container"] { margin: 0 !important; padding: 0 !important; }
div[data-testid="stHorizontalBlock"] { gap: 0 !important; }

/* ── INPUT FIELDS ── */
div[data-baseweb="input"] > div {
  background: #0f0f22 !important;
  border: 1.5px solid rgba(120,119,198,0.28) !important;
  border-radius: 10px !important;
  transition: all 0.2s !important;
}
div[data-baseweb="input"]:focus-within > div {
  border-color: #7c7cf7 !important;
  box-shadow: 0 0 0 3px rgba(124,124,247,0.14) !important;
}
div[data-baseweb="input"] input {
  background: transparent !important;
  color: #eeeeff !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.95rem !important;
  height: 48px !important;
}
div[data-baseweb="input"] input::placeholder { color: rgba(238,238,255,0.25) !important; }

/* hide the baseweb "label" text inside inputs so only our custom label shows */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span {
  color: rgba(238,238,255,0.50) !important;
  font-size: 0.70rem !important;
  font-weight: 600 !important;
  letter-spacing: 1.8px !important;
  text-transform: uppercase !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: linear-gradient(135deg,#5b5bd6,#7c3aed) !important;
  border: none !important;
  color: #fff !important;
  border-radius: 10px !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.95rem !important;
  font-weight: 600 !important;
  padding: 13px 28px !important;
  width: 100% !important;
  box-shadow: 0 4px 20px rgba(91,91,214,0.32) !important;
  transition: all 0.2s !important;
  cursor: pointer !important;
}
.stButton > button:hover {
  opacity: 0.88 !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 28px rgba(91,91,214,0.50) !important;
}

.ghost-btn .stButton > button {
  background: transparent !important;
  border: 1.5px solid rgba(120,119,198,0.35) !important;
  color: rgba(238,238,255,0.60) !important;
  box-shadow: none !important;
}
.ghost-btn .stButton > button:hover {
  border-color: #a78bfa !important;
  color: #eeeeff !important;
  background: rgba(124,124,247,0.08) !important;
  box-shadow: none !important;
  transform: translateY(-1px) !important;
}

/* ── ALERTS ── */
.stAlert { border-radius: 10px !important; font-size: 0.88rem !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════════════════════
if mode == "landing":

    # ── Topnav ─────────────────────────────────────────────────────────────────
    nav_l, nav_r = st.columns([6, 2])
    with nav_l:
        st.markdown("""
        <div style="padding:22px 40px 18px">
          <span style="font-family:'Syne',sans-serif;font-size:1.55rem;font-weight:800;
            background:linear-gradient(135deg,#5b5bd6,#a78bfa);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:1px">
            ⚡ FitPro AI</span>
        </div>""", unsafe_allow_html=True)
    with nav_r:
        st.markdown("<div style='padding:14px 40px 0;display:flex;gap:10px;justify-content:flex-end'>",
                    unsafe_allow_html=True)
        nb1, nb2 = st.columns(2)
        with nb1:
            st.markdown("<div class='ghost-btn'>", unsafe_allow_html=True)
            if st.button("Sign In", key="nav_signin"):
                st.session_state.mode = "login"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        with nb2:
            if st.button("Get Started", key="nav_start"):
                st.session_state.mode = "signup"
                st.session_state.signup_step = "form"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin:0;border-color:rgba(120,119,198,0.12)'>", unsafe_allow_html=True)

    # ── Hero ───────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding:80px 40px 56px;text-align:center;
      background:radial-gradient(ellipse 55% 60% at 10% 20%,rgba(91,91,214,0.13) 0%,transparent 55%),
                radial-gradient(ellipse 45% 50% at 90% 80%,rgba(124,124,247,0.10) 0%,transparent 55%)">
      <div style="font-size:0.60rem;font-weight:700;letter-spacing:5px;text-transform:uppercase;
        color:#a78bfa;margin-bottom:18px;display:flex;align-items:center;justify-content:center;gap:10px">
        <span style="width:28px;height:1px;background:rgba(124,124,247,0.40);display:inline-block"></span>
        AI-Powered Personal Training
        <span style="width:28px;height:1px;background:rgba(124,124,247,0.40);display:inline-block"></span>
      </div>
      <h1 style="font-family:'Syne',sans-serif;font-size:clamp(2.8rem,5vw,4.8rem);font-weight:800;
        line-height:0.94;letter-spacing:-1.5px;margin:0 0 22px">
        <span style="background:linear-gradient(135deg,#fff,rgba(255,255,255,0.75));
          -webkit-background-clip:text;-webkit-text-fill-color:transparent">TRAIN SMARTER.</span><br>
        <span style="background:linear-gradient(135deg,#5b5bd6,#a78bfa);
          -webkit-background-clip:text;-webkit-text-fill-color:transparent">GET REAL RESULTS.</span>
      </h1>
      <p style="font-size:1.05rem;color:rgba(238,238,255,0.45);font-weight:300;
        max-width:500px;margin:0 auto 44px;line-height:1.8">
        Your AI coach builds a fully personalised workout &amp; nutrition plan
        tailored to your body, goals and equipment — in seconds.
      </p>
    </div>""", unsafe_allow_html=True)

    _, cta_l, cta_r, _ = st.columns([2, 1.2, 1.2, 2])
    with cta_l:
        if st.button("⚡ Start for Free", key="hero_start", use_container_width=True):
            st.session_state.mode = "signup"; st.session_state.signup_step = "form"; st.rerun()
    with cta_r:
        st.markdown("<div class='ghost-btn'>", unsafe_allow_html=True)
        if st.button("Sign In →", key="hero_signin", use_container_width=True):
            st.session_state.mode = "login"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Feature cards ──────────────────────────────────────────────────────────
    st.markdown("<hr style='border-color:rgba(120,119,198,0.10);margin:44px 0 32px'>",
                unsafe_allow_html=True)
    st.markdown("""<div style="text-align:center;font-size:0.60rem;font-weight:700;letter-spacing:3px;
      text-transform:uppercase;color:rgba(238,238,255,0.22);margin-bottom:22px">
      Everything you need</div>""", unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3, gap="medium")
    for col, icon, title, desc in [
        (f1,"🤖","AI-Generated Plans",
         "Groq LLaMA 3.3 generates your full workout + diet plan in under 60 seconds, personalised to your stats, goals and equipment."),
        (f2,"📊","Progress Tracking",
         "Track daily workouts, build streaks, visualise your weekly activity and calendar — mark sessions complete from the dashboard."),
        (f3,"🥗","Nutrition & Wellness",
         "Full macro breakdown, water intake tracker, meal logger, weight tracker — everything to keep you on track every single day."),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:#0d0d1a;border:1px solid rgba(120,119,198,0.14);
              border-radius:16px;padding:28px 24px;height:100%;margin:0 6px">
              <div style="font-size:1.8rem;margin-bottom:14px">{icon}</div>
              <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;
                color:#eeeeff;margin-bottom:8px">{title}</div>
              <div style="font-size:0.82rem;color:rgba(238,238,255,0.38);line-height:1.7">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# AUTH PAGES  (login / signup / OTP)
# ══════════════════════════════════════════════════════════════════════════════
else:
    # Minimal header
    st.markdown("""
    <div style="padding:20px 32px 16px;border-bottom:1px solid rgba(120,119,198,0.10)">
      <span style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;
        background:linear-gradient(135deg,#5b5bd6,#a78bfa);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent">⚡ FitPro AI</span>
    </div>""", unsafe_allow_html=True)

    # ── centered layout: narrow column ────────────────────────────────────────
    _, mid, _ = st.columns([1, 1.6, 1])

    with mid:
        # ── Back button ──────────────────────────────────────────────────────
        st.markdown("<div style='padding:16px 0 0'>", unsafe_allow_html=True)
        back_col, _ = st.columns([1, 3])
        with back_col:
            st.markdown("<div class='ghost-btn'>", unsafe_allow_html=True)
            if st.button("← Home", key="back_home"):
                st.session_state.mode = "landing"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Auth card ─────────────────────────────────────────────────────────
        st.markdown("""
        <div style="background:#0c0c1e;border:1px solid rgba(120,119,198,0.28);
          border-radius:20px;padding:36px 36px 28px;margin:16px 0 20px;
          position:relative;overflow:hidden;
          box-shadow:0 32px 80px rgba(0,0,0,0.60),0 0 0 1px rgba(120,119,198,0.06)">
          <div style="position:absolute;top:0;left:0;right:0;height:2px;
            background:linear-gradient(90deg,transparent,#5b5bd6 30%,#a78bfa 60%,transparent)"></div>
        """, unsafe_allow_html=True)

        # ════════════════════════════════════════════════════════════════
        # LOGIN
        # ════════════════════════════════════════════════════════════════
        if mode == "login":
            st.markdown("""
            <div style="margin-bottom:22px">
              <div style="font-size:0.58rem;font-weight:700;letter-spacing:4px;
                text-transform:uppercase;color:#a78bfa;margin-bottom:6px">Welcome back</div>
              <div style="font-family:'Syne',sans-serif;font-size:2.0rem;font-weight:800;
                color:#eeeeff;line-height:1">Sign In</div>
            </div>""", unsafe_allow_html=True)

            if login_err:
                st.error(login_err)

            with st.form("login_form", clear_on_submit=False):
                li_u = st.text_input("Email or Username", placeholder="your@email.com")
                li_p = st.text_input("Password", type="password", placeholder="••••••••")
                sub  = st.form_submit_button("Sign In →", use_container_width=True)

            if sub:
                if not li_u.strip() or not li_p:
                    st.error("Please fill all fields.")
                else:
                    ok, token, real_u, msg = login(li_u.strip(), li_p)
                    if ok:
                        st.session_state.update(logged_in=True, username=real_u, auth_token=token)
                        st.switch_page("pages/2_Dashboard.py")
                    else:
                        st.error(msg)

            st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
            st.markdown("""<div style="text-align:center;font-size:0.84rem;
              color:rgba(238,238,255,0.32);margin-bottom:10px">New here?</div>""",
              unsafe_allow_html=True)
            if st.button("Create an account →", key="to_signup", use_container_width=True):
                st.session_state.mode = "signup"; st.session_state.signup_step = "form"; st.rerun()

        # ════════════════════════════════════════════════════════════════
        # OTP
        # ════════════════════════════════════════════════════════════════
        elif mode == "signup" and step == "otp":
            st.markdown(f"""
            <div style="margin-bottom:22px">
              <div style="font-size:0.58rem;font-weight:700;letter-spacing:4px;
                text-transform:uppercase;color:#a78bfa;margin-bottom:6px">Almost there</div>
              <div style="font-family:'Syne',sans-serif;font-size:2.0rem;font-weight:800;
                color:#eeeeff;line-height:1">Verify Email</div>
            </div>
            <div style="background:rgba(124,124,247,0.08);border:1px solid rgba(124,124,247,0.22);
              border-radius:10px;padding:14px;text-align:center;margin-bottom:20px">
              <div style="font-size:0.84rem;color:rgba(238,238,255,0.45)">6-digit code sent to</div>
              <div style="font-weight:700;color:#a78bfa;margin-top:3px">{pending_email}</div>
            </div>""", unsafe_allow_html=True)

            if otp_err:
                st.error(otp_err)

            with st.form("otp_form", clear_on_submit=False):
                otp_val = st.text_input("Verification Code", placeholder="000000", max_chars=6)
                sub = st.form_submit_button("Verify & Create Account →", use_container_width=True)

            if sub:
                if len(otp_val.strip()) < 6:
                    st.error("Please enter the 6-digit code.")
                else:
                    ok, token, result = complete_signup(pending_email, otp_val.strip())
                    if ok:
                        st.session_state.update(
                            logged_in=True, username=result, auth_token=token,
                            mode="landing", signup_step="form", pending_email=""
                        )
                        st.switch_page("pages/2_Dashboard.py")
                    else:
                        st.error(result)

            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
            if st.button("← Wrong email? Go back", key="back_otp", use_container_width=True):
                st.session_state.signup_step = "form"; st.rerun()

        # ════════════════════════════════════════════════════════════════
        # SIGNUP
        # ════════════════════════════════════════════════════════════════
        else:
            st.markdown("""
            <div style="margin-bottom:22px">
              <div style="font-size:0.58rem;font-weight:700;letter-spacing:4px;
                text-transform:uppercase;color:#a78bfa;margin-bottom:6px">Get started free</div>
              <div style="font-family:'Syne',sans-serif;font-size:2.0rem;font-weight:800;
                color:#eeeeff;line-height:1">Create Account</div>
            </div>""", unsafe_allow_html=True)

            if signup_err:
                st.error(signup_err)

            with st.form("signup_form", clear_on_submit=False):
                su_u = st.text_input("Username", placeholder="yourname")
                su_e = st.text_input("Email Address", placeholder="your@email.com")
                pc1, pc2 = st.columns(2)
                with pc1: su_p  = st.text_input("Password", type="password", placeholder="min 6 chars")
                with pc2: su_p2 = st.text_input("Confirm Password", type="password", placeholder="repeat")
                sub = st.form_submit_button("Create Account →", use_container_width=True)

            if sub:
                err = ""
                if not su_u.strip() or not su_e.strip() or not su_p or not su_p2:
                    err = "Please fill all fields."
                elif "@" not in su_e:
                    err = "Enter a valid email address."
                elif su_p != su_p2:
                    err = "Passwords don't match."
                elif len(su_p) < 6:
                    err = "Password must be at least 6 characters."
                if err:
                    st.error(err)
                else:
                    ok, mode_flag, token = initiate_signup(su_u.strip(), su_e.strip(), su_p)
                    if ok and mode_flag == "__DIRECT__":
                        st.session_state.update(
                            logged_in=True, username=su_u.strip(), auth_token=token,
                            mode="landing", signup_step="form", pending_email=""
                        )
                        st.switch_page("pages/2_Dashboard.py")
                    elif ok and mode_flag == "__OTP__":
                        st.session_state.pending_email = su_e.strip()
                        st.session_state.signup_step   = "otp"
                        st.rerun()
                    else:
                        st.error(mode_flag)

            st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
            st.markdown("""<div style="text-align:center;font-size:0.84rem;
              color:rgba(238,238,255,0.32);margin-bottom:10px">Already have an account?</div>""",
              unsafe_allow_html=True)
            if st.button("Sign in →", key="to_login", use_container_width=True):
                st.session_state.mode = "login"; st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)  # close auth card
