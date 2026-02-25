def calculate_bmi(weight, height):
    """
    Calculate BMI from weight (kg) and height (cm)
    """
    height_m = height / 100
    return weight / (height_m ** 2)

def bmi_category(bmi):
    """
    Categorize BMI value
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal Weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def build_prompt(name, age, gender, height, weight, goal, fitness_level, equipment):
    """
    Build a prompt for the AI model including all user parameters
    """
    bmi = calculate_bmi(weight, height)
    bmi_status = bmi_category(bmi)

    equipment_list = ", ".join(equipment) if equipment else "No Equipment"
    
    # Age-specific considerations
    age_considerations = ""
    if age < 18:
        age_considerations = "\n⚠️ Note: User is under 18. Focus on proper form and bodyweight exercises. Avoid heavy lifting."
    elif age > 50:
        age_considerations = "\n⚠️ Note: User is over 50. Focus on joint-friendly exercises, mobility work, and lower impact activities."
    
    # Goal-specific instructions
    goal_instructions = {
        "Weight Loss": "Focus on compound exercises and include cardio intervals. Higher reps with moderate weight.",
        "Build Muscle": "Focus on hypertrophy with moderate weights and higher reps. Include progressive overload.",
        "Strength Gain": "Focus on lower reps with heavier weights. Include compound lifts.",
        "Abs Building": "Include core-specific exercises along with full-body compound movements.",
        "Flexibility": "Include dynamic and static stretching, yoga poses, and mobility work."
    }
    
    specific_instruction = goal_instructions.get(goal, "Balance cardio and strength training.")

    prompt = f"""You are a certified professional fitness trainer. Create a comprehensive 5-day workout plan.

USER PROFILE:
- Name: {name}
- Age: {age} years
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- BMI: {bmi:.2f} ({bmi_status})
- Primary Goal: {goal}
- Fitness Level: {fitness_level}
- Available Equipment: {equipment_list}
{age_considerations}

SPECIFIC FOCUS: {specific_instruction}

REQUIREMENTS FOR THE WORKOUT PLAN:
1. Create a COMPLETE 5-day workout plan with clear "Day 1" through "Day 5" headers
2. For each day, include 4-6 exercises
3. For EVERY exercise, specify:
   - Exercise name
   - Number of sets and reps (e.g., "3 sets of 12 reps")
   - Rest period between sets (e.g., "Rest 60 seconds")
4. Include a brief warm-up recommendation for each day
5. Include a cool-down/stretch recommendation
6. Adjust exercise intensity based on:
   - BMI category ({bmi_status})
   - Fitness level ({fitness_level})
   - Age considerations
7. Ensure all exercises are safe and appropriate for a {fitness_level}
8. Modify exercises based on available equipment: {equipment_list}

Please provide a well-structured, easy-to-follow 5-day workout plan that addresses the user's specific goal of {goal}.
"""

    return prompt, bmi, bmi_status
