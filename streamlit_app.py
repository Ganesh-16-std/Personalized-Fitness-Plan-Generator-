import streamlit as st

st.set_page_config(
    page_title="FIT Plan AI - Milestone 1",
    page_icon="💪",
    layout="centered"
)

st.title("💪 FIT Plan AI – Personalized Fitness Profile")
st.markdown("---")

if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

with st.form("fitness_profile_form"):
    st.header("📋 Your Fitness Profile")

    st.subheader("👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name *")
        height = st.number_input("Height (cm) *", min_value=1.0, max_value=300.0, value=170.0, step=0.1)

    with col2:
        age = st.number_input("Age", min_value=10, max_value=120, value=25, step=1)
        weight = st.number_input("Weight (kg) *", min_value=1.0, max_value=500.0, value=70.0, step=0.1)

    st.subheader("🎯 Fitness Details")

    goal = st.selectbox(
        "Fitness Goal *",
        options=[
            "Weight Loss",
            "Build Muscle",
            "Strength Gain",
            "Abs Building",
            "Flexibility"
        ],
        index=0
    )

    equipment = st.multiselect(
        "Available Equipment *",
        options=[
            "Dumbbells",
            "Resistance Bands",
            "Barbell",
            "Pull-up Bar",
            "Treadmill",
            "Kettlebells",
            "Jump Rope",
            "Yoga Mat",
            "No Equipment (Bodyweight only)"
        ],
        default=["No Equipment (Bodyweight only)"]
    )

    fitness_level = st.select_slider(
        "Fitness Level *",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Beginner"
    )

    st.markdown("---")
    st.caption("* Required fields")

    submitted = st.form_submit_button("Generate My Plan", use_container_width=True)

if submitted:
    errors = []

    if not name or name.strip() == "":
        errors.append("❌ Name is required")

    if height <= 0:
        errors.append("❌ Height must be greater than zero")

    if weight <= 0:
        errors.append("❌ Weight must be greater than zero")

    if not equipment:
        errors.append("❌ Please select at least one equipment option")

    if errors:
        for error in errors:
            st.error(error)
        st.stop()

    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
        bmi_color = "#3498db"
    elif bmi < 25:
        bmi_status = "Normal"
        bmi_color = "#2ecc71"
    elif bmi < 30:
        bmi_status = "Overweight"
        bmi_color = "#f39c12"
    else:
        bmi_status = "Obese"
        bmi_color = "#e74c3c"

    st.session_state.form_submitted = True
    st.session_state.name = name
    st.session_state.bmi = bmi
    st.session_state.bmi_status = bmi_status
    st.session_state.bmi_color = bmi_color
    st.session_state.age = age
    st.session_state.goal = goal
    st.session_state.equipment = equipment
    st.session_state.fitness_level = fitness_level
    st.session_state.height = height
    st.session_state.weight = weight

if st.session_state.form_submitted:
    st.markdown("---")
    st.success(f" Welcome, **{st.session_state.name}**! Your personalized fitness profile is ready.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="📊 BMI", value=st.session_state.bmi)

    with col2:
        st.markdown(
            f"""
            <div style="background-color: {st.session_state.bmi_color}; 
                        padding: 10px; 
                        border-radius: 10px; 
                        text-align: center;
                        color: white;">
                <span style="font-size: 0.9rem;">BMI Category</span><br>
                <span style="font-size: 1.4rem; font-weight: bold;">{st.session_state.bmi_status}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.metric(label="🏋️ Level", value=st.session_state.fitness_level)

    st.subheader("📌 Your Complete Profile")

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:
        st.markdown("**Personal Details:**")
        st.write(f"• **Name:** {st.session_state.name}")
        st.write(f"• **Age:** {st.session_state.age} years")
        st.write(f"• **Height:** {st.session_state.height} cm")
        st.write(f"• **Weight:** {st.session_state.weight} kg")

    with profile_col2:
        st.markdown("**Fitness Preferences:**")
        st.write(f"• **Goal:** {st.session_state.goal}")
        st.write(f"• **Fitness Level:** {st.session_state.fitness_level}")
        st.write(f"• **Equipment:** {', '.join(st.session_state.equipment)}")

    with st.expander("Understanding Your BMI"):
        st.markdown("""
        **Body Mass Index (BMI) Categories:**

        - **Underweight (< 18.5):** You may need to gain some weight. Focus on nutrient-rich foods and strength training.
        - **Normal (18.5 - 24.9):** You are in a healthy weight range. Maintain with balanced diet and regular exercise.
        - **Overweight (25 - 29.9):** Consider incorporating more cardio and a slight caloric deficit.
        - **Obese (≥ 30):** Consult with a healthcare provider for a personalized weight management plan.

        *Note: BMI is a screening tool, not a diagnostic tool. Individual factors like muscle mass and body composition matter.*
        """)

    st.subheader("Personalized Tips")

    tip_col1, tip_col2 = st.columns(2)

    with tip_col1:
        st.info(f"**Based on your BMI ({st.session_state.bmi_status})**\n\n" + 
                {
                    "Underweight": "Focus on calorie surplus with protein-rich foods and strength training to build muscle.",
                    "Normal": "Great job maintaining! Combine cardio and strength training for overall fitness.",
                    "Overweight": "Combine cardio workouts with strength training and maintain a slight calorie deficit.",
                    "Obese": "Start with low-impact cardio (walking, swimming) and consult a nutritionist."
                }.get(st.session_state.bmi_status, "Keep moving consistently!"))

    with tip_col2:
        st.success(f"**Based on your goal ({st.session_state.goal})**\n\n" + 
                  {
                      "Weight Loss": "Focus on calorie deficit, cardio, and whole foods. Stay consistent!",
                      "Build Muscle": "Prioritize protein intake and progressive overload in strength training.",
                      "Strength Gain": "Focus on compound lifts with lower reps and heavier weights.",
                      "Abs Building": "Reduce body fat through diet and cardio, plus core-specific exercises.",
                      "Flexibility": "Incorporate daily stretching, yoga, or pilates for best results."
                  }.get(st.session_state.goal, "Stay consistent with your routine!"))

    st.markdown("---")

    report_text = f"""
    ════════════════════════════════════════
              FIT PLAN AI - PROFILE REPORT
    ════════════════════════════════════════

    Generated on: {st.session_state.get('timestamp', 'N/A')}

    👤 PERSONAL INFORMATION
    ──────────────────────────────────────
    Name: {st.session_state.name}
    Age: {st.session_state.age} years
    Height: {st.session_state.height} cm
    Weight: {st.session_state.weight} kg

    📊 BODY MASS INDEX (BMI)
    ──────────────────────────────────────
    BMI Value: {st.session_state.bmi}
    Category: {st.session_state.bmi_status}
    Health Range: {
        '< 18.5' if st.session_state.bmi_status == 'Underweight' else
        '18.5 - 24.9' if st.session_state.bmi_status == 'Normal' else
        '25 - 29.9' if st.session_state.bmi_status == 'Overweight' else
        '≥ 30'
    }

    🎯 FITNESS PROFILE
    ──────────────────────────────────────
    Primary Goal: {st.session_state.goal}
    Experience Level: {st.session_state.fitness_level}
    Available Equipment: {', '.join(st.session_state.equipment)}

    💡 QUICK TIP
    ──────────────────────────────────────
    {
        "Focus on calorie surplus with protein-rich foods and strength training." if st.session_state.bmi_status == "Underweight" else
        "Maintain your healthy weight with balanced diet and regular exercise." if st.session_state.bmi_status == "Normal" else
        "Aim for gradual weight loss through diet and increased physical activity." if st.session_state.bmi_status == "Overweight" else
        "Consult healthcare provider for personalized weight management plan."
    }

    ════════════════════════════════════════
    Stay consistent, stay hydrated, and trust the process!
    """

    st.download_button(
        label="Download Complete Profile Report",
        data=report_text,
        file_name=f"FITPlanAI_{st.session_state.name}_Profile.txt",
        mime="text/plain",
        use_container_width=True
    )

st.markdown("---")
st.caption("FIT Plan AI - Milestone 1 | BMI Calculator & Profile Generator")