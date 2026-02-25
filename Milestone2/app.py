import streamlit as st
from datetime import datetime
from prompt_builder import build_prompt
from model_api import query_model, test_api_connection

st.set_page_config(
    page_title="FIT Plan AI - Milestone 2",
    page_icon="💪",
    layout="centered"
)

# Helper function to verify workout plan - MUST be defined before it's used
def verify_workout_plan(plan_text):
    """Check if the workout plan contains all 5 days"""
    if not plan_text or plan_text.startswith("Error"):
        return False, "No valid plan generated"
    
    days_present = []
    for i in range(1, 6):
        if f"Day {i}" in plan_text:
            days_present.append(i)
    
    if len(days_present) == 5:
        return True, "Complete 5-day plan"
    else:
        missing_days = set(range(1,6)) - set(days_present)
        return False, f"Missing day(s): {', '.join(map(str, missing_days))}"

st.title("💪 FIT Plan AI – Personalized Fitness Profile")
st.markdown("---")

# Test API connection on startup
if "api_status" not in st.session_state:
    with st.spinner("Checking API connection..."):
        api_ok, api_message = test_api_connection()
        st.session_state.api_status = api_ok
        st.session_state.api_message = api_message

# Show API status in sidebar
with st.sidebar:
    st.header("🔧 System Status")
    if st.session_state.get("api_status", False):
        st.success("✅ API Connected")
    else:
        st.error(f"❌ API Error: {st.session_state.get('api_message', 'Unknown error')}")
        st.info("Please set your HF_TOKEN environment variable")

# Initialize session state
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Profile"

# Create tabs for different sections
tab1, tab2 = st.tabs(["📋 Profile Setup", "🏋️ Workout Plan"])

# Tab 1: Profile Setup
with tab1:
    with st.form("fitness_profile_form"):
        st.header("Your Fitness Profile")
        st.subheader("👤 Personal Information")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name *")
            height = st.number_input("Height (cm) *", min_value=1.0, max_value=300.0, value=170.0)

        with col2:
            age = st.number_input("Age *", min_value=10, max_value=120, value=25)
            weight = st.number_input("Weight (kg) *", min_value=1.0, max_value=500.0, value=70.0)

        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        st.subheader("🎯 Fitness Details")

        goal = st.selectbox(
            "Fitness Goal *",
            ["Weight Loss", "Build Muscle", "Strength Gain", "Abs Building", "Flexibility"]
        )

        equipment = st.multiselect(
            "Available Equipment *",
            [
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
        submit = st.form_submit_button("Save Profile", use_container_width=True)

    if submit:
        if not name:
            st.error("Please enter your name.")
            st.stop()

        if not equipment:
            st.error("Please select at least one equipment option.")
            st.stop()

        # Build prompt using the imported function
        prompt, bmi, bmi_status = build_prompt(
            name=name,
            age=age,
            gender=gender,
            height=height,
            weight=weight,
            goal=goal,
            fitness_level=fitness_level,
            equipment=equipment
        )

        st.success("✅ Profile Saved Successfully!")

        st.session_state.update({
            "form_submitted": True,
            "name": name,
            "bmi": bmi,
            "bmi_status": bmi_status,
            "age": age,
            "goal": goal,
            "equipment": equipment,
            "fitness_level": fitness_level,
            "height": height,
            "weight": weight,
            "gender": gender,
            "prompt": prompt
        })

    # Show profile summary if form is submitted
    if st.session_state.form_submitted:
        st.markdown("---")
        st.success(f"Welcome, **{st.session_state.name}**!")

        col1, col2, col3 = st.columns(3)
        col1.metric("📊 BMI", f"{st.session_state.bmi:.2f}")
        col2.metric("🏷 Category", st.session_state.bmi_status)
        col3.metric("🏋️ Level", st.session_state.fitness_level)
        
        # Quick action button to switch to workout plan tab
        if st.button("👉 Go to Workout Plan Tab", type="primary", use_container_width=True):
            st.session_state.active_tab = "Workout Plan"
            st.rerun()

        # Profile Report Section
        st.markdown("---")
        with st.expander("📄 View Profile Report"):
            report_text = f"""
FIT PLAN AI - PROFILE REPORT
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Name: {st.session_state.name}
Age: {st.session_state.age}
Gender: {st.session_state.gender}
Height: {st.session_state.height} cm
Weight: {st.session_state.weight} kg

BMI: {st.session_state.bmi:.2f}
Category: {st.session_state.bmi_status}

Goal: {st.session_state.goal}
Level: {st.session_state.fitness_level}
Equipment: {', '.join(st.session_state.equipment)}

Go to the Workout Plan tab to generate your personalized 5-day workout plan!
"""

            st.download_button(
                "📥 Download Profile Report",
                data=report_text,
                file_name=f"FITPlanAI_{st.session_state.name}_Profile.txt",
                mime="text/plain",
                use_container_width=True
            )

# Tab 2: Workout Plan
with tab2:
    st.header("🏋️ Your Personalized Workout Plan")
    
    # Check if profile is submitted
    if not st.session_state.form_submitted:
        st.warning("⚠️ Please set up your profile first in the 'Profile Setup' tab!")
        if st.button("Go to Profile Setup"):
            st.session_state.active_tab = "Profile"
            st.rerun()
    else:
        # Check API status
        if not st.session_state.get("api_status", False):
            st.error("⚠️ API is not connected. Please check your HF_TOKEN environment variable.")
            st.stop()
        
        # Show profile summary
        with st.container():
            st.markdown("### Profile Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Name", st.session_state.name)
            col2.metric("Age", st.session_state.age)
            col3.metric("BMI", f"{st.session_state.bmi:.1f}")
            col4.metric("Goal", st.session_state.goal)
        
        st.markdown("---")
        
        # Generate Workout Plan Button
        st.subheader("Generate Your 5-Day Workout Plan")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Generate Workout Plan", type="primary", use_container_width=True):
                with st.spinner("Creating your personalized workout plan... This may take a moment."):
                    # Call the model API from model_api.py
                    workout_plan = query_model(st.session_state.prompt)
                    st.session_state.workout_plan = workout_plan
                    st.rerun()
                
        # Display workout plan if generated
        if st.session_state.workout_plan:
            st.markdown("---")
            st.subheader("📋 Your 5-Day Workout Plan")
            
            # Check if plan is complete - Now verify_workout_plan is defined
            is_complete, message = verify_workout_plan(st.session_state.workout_plan)
            if not is_complete:
                st.warning(f"⚠️ {message}. You can regenerate the plan if needed.")
            
            # Display the workout plan
            with st.container():
                st.markdown(st.session_state.workout_plan)
            
            st.markdown("---")
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Download button for workout plan
                workout_text = f"""
FIT PLAN AI - PERSONALIZED WORKOUT PLAN
Generated for: {st.session_state.name}
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

PROFILE SUMMARY:
- Age: {st.session_state.age}
- BMI: {st.session_state.bmi:.2f} ({st.session_state.bmi_status})
- Goal: {st.session_state.goal}
- Level: {st.session_state.fitness_level}
- Equipment: {', '.join(st.session_state.equipment)}

{st.session_state.workout_plan}

---
Stay consistent and trust the process!
Generated by FIT Plan AI
"""
                
                st.download_button(
                    "📥 Download Plan",
                    data=workout_text,
                    file_name=f"FITPlanAI_{st.session_state.name}_Workout.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                if st.button("🔄 Regenerate Plan", use_container_width=True):
                    with st.spinner("Regenerating your workout plan..."):
                        workout_plan = query_model(st.session_state.prompt)
                        st.session_state.workout_plan = workout_plan
                        st.rerun()
            
            with col3:
                if st.button("✏️ Edit Profile", use_container_width=True):
                    st.session_state.active_tab = "Profile"
                    st.rerun()
        
        # Tips section
        with st.expander("💡 Workout Tips & Guidelines"):
            st.markdown("""
            ### 📌 Tips for Best Results:
            1. **Warm-up** before each workout (5-10 minutes of light cardio and dynamic stretches)
            2. **Stay hydrated** during your workout
            3. **Maintain proper form** over lifting heavy weights
            4. **Rest adequately** between sets as specified
            5. **Cool down** and stretch after each session
            6. **Be consistent** - follow the plan regularly
            7. **Listen to your body** and adjust intensity if needed
            
            ### ⚠️ Safety First:
            - Consult with a healthcare professional before starting any new exercise program
            - Stop immediately if you feel sharp pain or discomfort
            - Start with lighter weights to master the form
            """)

# Footer
st.markdown("---")
st.caption("FIT Plan AI - Milestone 2 | Powered by Mistral-7B")
