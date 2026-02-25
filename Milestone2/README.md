💪 FIT Plan AI - Milestone 2

https://img.shields.io/badge/Python-3.9+-blue.svg

https://img.shields.io/badge/Streamlit-1.28+-red.svg

https://img.shields.io/badge/%F0%9F%A4%97-Hugging%2520Face-yellow.svg

https://img.shields.io/badge/Mistral-7B--Instruct-purple.svg


📋 Live Demo

https://huggingface.co/spaces/saiganesh2004/FitPlan-AI-module2


🎯 Objective of the Milestone
The primary objective of Milestone 2 is to develop an interactive web application that generates personalized 5-day workout plans using a Large Language Model (LLM). The application takes user inputs such as age, gender, height, weight, fitness goals, available equipment, and fitness level to create customized fitness recommendations.

Key Goals:
Collect comprehensive user fitness data through an intuitive form

Calculate BMI and provide health category classification

Generate structured, professional workout plans using Mistral-7B

Ensure plans are safe and appropriate for the user's fitness level

Provide downloadable workout plans and profile reports

Implement a clean, user-friendly interface with tabbed navigation

🤖 Model Name Used
Model: mistralai/Mistral-7B-Instruct-v0.2

Model Specifications:
Architecture: Mistral-7B-v0.2 (Decoder-only Transformer)

Parameters: 7 billion

Context Length: 32,768 tokens

Specialization: Instruction-following and conversational tasks

Fine-tuning: Instruction-tuned version for better prompt adherence

Why Mistral-7B?
Excellent balance between performance and computational efficiency

Strong instruction-following capabilities

Can generate detailed, structured responses

Available for free via Hugging Face Inference API

Suitable for fitness plan generation with proper prompting

📝 Prompt Design Explanation
The prompt engineering strategy focuses on creating structured, safe, and personalized workout plans through careful instruction design.

Prompt Structure:
text
You are a certified professional fitness trainer. Create a comprehensive 5-day workout plan.

USER PROFILE:
- Name: {name}
- Age: {age} years
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- BMI: {bmi:.2f} ({bmi_status})
- Goal: {goal}
- Fitness Level: {fitness_level}
- Available Equipment: {equipment_list}

[Age-specific considerations based on user age]

SPECIFIC FOCUS: {goal_specific_instruction}

REQUIREMENTS:
- Complete 5-day structure with "Day 1" through "Day 5" headers
- 4-6 exercises per day with sets, reps, and rest periods
- Warm-up and cool-down recommendations
- Intensity adjustments based on BMI and fitness level
- Safety considerations for beginners and age groups
Key Prompt Engineering Elements:
Element	Purpose	Example
System Role	Establish expertise	"You are a certified professional fitness trainer"
User Profile	Personalize the response	Includes all user metrics and goals
Age Considerations	Safety modifications	Under 18: avoid heavy lifting; Over 50: joint-friendly exercises
Goal-Specific Focus	Targeted recommendations	Weight Loss: cardio intervals; Muscle Building: hypertrophy focus
Structured Requirements	Ensure consistent output	Clear day headers, exercise details, rest periods
Equipment Awareness	Practicality	Modifies exercises based on available equipment
BMI-Based Intensity	Health-appropriate scaling	Adjusts weights and intensity based on BMI category
BMI Categories and Their Impact:
Underweight (<18.5): Focus on strength building, proper form

Normal (18.5-24.9): Balanced approach based on goal

Overweight (25-29.9): Include cardio, gradual intensity

Obese (≥30): Low-impact exercises, focus on mobility

⚙️ Steps Performed
1. Model Loading
python
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=HF_TOKEN
)
Loaded Mistral-7B-Instruct via Hugging Face Inference API

Implemented error handling and connection testing

Set up environment variable for secure token management

2. Prompt Creation
Developed build_prompt() function in prompt_builder.py

Integrated BMI calculation and categorization

Added conditional logic for age-specific considerations

Created goal-specific instructions for each fitness objective

Formatted equipment list for natural language processing

3. Inference Testing
Tested with various user profiles (different ages, goals, fitness levels)

Verified token limits (2500 tokens) for complete 5-day plans

Implemented response verification to ensure all 5 days are present

Added retry logic for incomplete responses

Tested edge cases (minimum age, maximum weight, no equipment)

4. Streamlit Integration
Built multi-tab interface with Profile Setup and Workout Plan views

Implemented session state management for data persistence

Created download functionality for reports and workout plans

Added real-time BMI calculation and display

Integrated API status checking in sidebar

📊 Sample Generated Outputs
Sample Profile 1: Beginner Weight Loss
User Profile:

Name: Sarah

Age: 28

Gender: Female

Height: 165 cm

Weight: 80 kg

BMI: 29.4 (Overweight)

Goal: Weight Loss

Level: Beginner

Equipment: Dumbbells, Yoga Mat

Generated Output:

text
🏋️ YOUR 5-DAY WEIGHT LOSS WORKOUT PLAN

DAY 1: Full Body & Cardio
Warm-up: 5 min jumping jacks, arm circles, leg swings

1. Bodyweight Squats
   - 3 sets of 15 reps
   - Rest: 45 seconds
   - Focus on form, keep chest up

2. Push-ups (Knee-supported if needed)
   - 3 sets of 10-12 reps
   - Rest: 45 seconds
   - Keep core engaged throughout

3. Dumbbell Rows (5-8 kg each)
   - 3 sets of 12 reps per arm
   - Rest: 60 seconds
   - Maintain flat back position

4. Plank
   - 3 sets of 30-second holds
   - Rest: 30 seconds
   - Progress to 45 seconds if comfortable

5. Jump Rope (or high knees)
   - 3 sets of 1 minute
   - Rest: 30 seconds between sets

Cool-down: 5 min full body stretching

DAY 2: Lower Body & Core
Warm-up: 5 min leg swings, hip circles, bodyweight squats

1. Goblet Squats (hold one dumbbell)
   - 3 sets of 12 reps
   - Rest: 60 seconds
   - Keep weight in heels, chest up

2. Lunges (alternating legs)
   - 3 sets of 10 reps per leg
   - Rest: 45 seconds
   - Step forward, lower back knee toward ground

3. Glute Bridges
   - 3 sets of 15 reps
   - Rest: 30 seconds
   - Squeeze glutes at the top

4. Dumbbell Deadlifts (light weight)
   - 3 sets of 12 reps
   - Rest: 60 seconds
   - Hinge at hips, keep back straight

5. Bicycle Crunches
   - 3 sets of 20 reps (10 per side)
   - Rest: 30 seconds
   - Slow and controlled movement

Cool-down: 5 min lower body stretching

DAY 3: Active Recovery & Cardio
Warm-up: 5 min dynamic stretching

1. Brisk Walking or Treadmill
   - 30 minutes at moderate pace
   - Maintain conversation pace

2. Full Body Stretching
   - 15 minutes of gentle stretching
   - Hold each stretch 20-30 seconds

3. Yoga Flow (Sun Salutations)
   - 10-15 minutes
   - Focus on breath and movement

Cool-down: Deep breathing, 5 min

DAY 4: Upper Body & Core
Warm-up: 5 min arm circles, band pull-aparts, push-up preparation

1. Dumbbell Shoulder Press
   - 3 sets of 10-12 reps
   - Rest: 60 seconds
   - Use 4-6 kg dumbbells

2. Bent-Over Dumbbell Rows
   - 3 sets of 12 reps per arm
   - Rest: 60 seconds
   - Support with opposite hand on bench

3. Dumbbell Bicep Curls
   - 3 sets of 12 reps
   - Rest: 45 seconds
   - Keep elbows pinned to sides

4. Tricep Dips (using chair/bench)
   - 3 sets of 10 reps
   - Rest: 45 seconds
   - Walk feet out for more challenge

5. Russian Twists (with or without weight)
   - 3 sets of 20 reps (10 per side)
   - Rest: 30 seconds
   - Keep feet elevated for more difficulty

Cool-down: 5 min upper body stretching

DAY 5: Full Body & HIIT
Warm-up: 5 min jumping jacks, dynamic stretches

1. Burpees (modified: step back instead of jump)
   - 3 sets of 8-10 reps
   - Rest: 60 seconds
   - Maintain steady pace

2. Dumbbell Thrusters
   - 3 sets of 10 reps
   - Rest: 60 seconds
   - Combine squat with overhead press

3. Mountain Climbers
   - 3 sets of 30 seconds
   - Rest: 30 seconds
   - Keep core tight, hips down

4. Kettlebell Swings (if available) or Dumbbell Swings
   - 3 sets of 12 reps
   - Rest: 45 seconds
   - Hip-driven movement, not arms

5. Plank Jacks
   - 3 sets of 20 seconds
   - Rest: 20 seconds
   - Jump feet in and out while in plank

Cool-down: 10 min full body stretching

IMPORTANT NOTES FOR BEGINNERS:
- Listen to your body and rest when needed
- Focus on form over speed or weight
- Stay hydrated throughout workouts
- Take rest days seriously for recovery
- Progress gradually - increase weights/reps only when comfortable
Sample Profile 2: Intermediate Muscle Building
User Profile:

Name: Mike

Age: 32

Gender: Male

Height: 178 cm

Weight: 75 kg

BMI: 23.7 (Normal)

Goal: Build Muscle

Level: Intermediate

Equipment: Barbell, Dumbbells, Bench, Pull-up Bar

Generated Output:

text
🏋️ YOUR 5-DAY MUSCLE BUILDING WORKOUT PLAN

DAY 1: Chest & Triceps (Push Day)
Warm-up: 5-10 min light cardio, arm circles, band pull-aparts, light push-ups

1. Barbell Bench Press
   - 4 sets of 8-10 reps
   - Rest: 90 seconds
   - Use 70-75% of 1RM, focus on controlled negatives
   - Progress: Add 2.5 kg each week if form remains solid

2. Incline Dumbbell Press
   - 3 sets of 10-12 reps
   - Rest: 60 seconds
   - Set bench at 30-degree angle
   - Focus on stretch at bottom, explosive press

3. Dumbbell Flyes
   - 3 sets of 12-15 reps
   - Rest: 45 seconds
   - Light weight, focus on mind-muscle connection
   - Slight bend in elbows throughout movement

4. Tricep Pushdowns (cable or band)
   - 3 sets of 12-15 reps
   - Rest: 45 seconds
   - Keep elbows locked at sides
   - Squeeze at bottom of movement

5. Close-Grip Bench Press
   - 3 sets of 8-10 reps
   - Rest: 60 seconds
   - Hands shoulder-width apart
   - Keep elbows close to body

6. Diamond Push-ups (to failure)
   - 2 sets to failure
   - Rest: 60 seconds
   - Hands form diamond shape under chest

Cool-down: Chest and tricep stretches, 5-10 min

DAY 2: Back & Biceps (Pull Day)
Warm-up: 5 min band pull-aparts, arm circles, lat activation

1. Pull-ups (or Lat Pulldowns)
   - 4 sets to failure (or 8-12 reps)
   - Rest: 90 seconds
   - Use assist band if needed
   - Focus on pulling with elbows, not arms

2. Barbell Rows
   - 4 sets of 8-10 reps
   - Rest: 75 seconds
   - Bend at hips, keep back straight
   - Pull bar to lower chest

3. Single-Arm Dumbbell Rows
   - 3 sets of 10-12 reps per arm
   - Rest: 60 seconds
   - Support with opposite hand on bench
   - Full range of motion, squeeze at top

4. Face Pulls (band or cable)
   - 3 sets of 15 reps
   - Rest: 45 seconds
   - Great for posture and shoulder health
   - Pull to forehead, external rotation

5. Barbell Bicep Curls
   - 3 sets of 10-12 reps
   - Rest: 45 seconds
   - Keep elbows pinned to sides
   - No swinging, controlled movement

6. Hammer Curls
   - 3 sets of 12 reps
   - Rest: 45 seconds
   - Palms facing each other
   - Hits brachialis for thicker arms

Cool-down: Back and bicep stretches, 5-10 min

DAY 3: Legs & Core
Warm-up: 5-10 min leg swings, bodyweight squats, hip circles, lunges

1. Barbell Squats
   - 4 sets of 8-10 reps
   - Rest: 90 seconds
   - Depth: thighs parallel or below
   - Keep chest up, brace core

2. Romanian Deadlifts
   - 3 sets of 10 reps
   - Rest: 75 seconds
   - Soft knees, hinge at hips
   - Feel hamstring stretch

3. Leg Press (if available) or Goblet Squats
   - 3 sets of 12 reps
   - Rest: 60 seconds
   - Full range of motion
   - Control on way down

4. Walking Lunges (with dumbbells)
   - 3 sets of 12 reps per leg
   - Rest: 60 seconds
   - Keep torso upright
   - Step far enough to feel stretch

5. Calf Raises
   - 4 sets of 15-20 reps
   - Rest: 30 seconds
   - Full range, pause at top

6. Hanging Knee Raises (or Lying Leg Raises)
   - 3 sets of 15 reps
   - Rest: 45 seconds
   - Control movement, no swinging

Cool-down: Quad, hamstring, glute stretches, 5-10 min

DAY 4: Shoulders & Abs
Warm-up: 5 min arm circles, band pull-aparts, face pulls, light lateral raises

1. Overhead Barbell Press (or Dumbbell Press)
   - 4 sets of 8-10 reps
   - Rest: 75 seconds
   - Keep core braced, slight arch
   - Bar path straight up and down

2. Lateral Raises
   - 3 sets of 12-15 reps
   - Rest: 45 seconds
   - Light weight, controlled movement
   - Lead with elbows, slight bend

3. Rear Delt Flyes (bent-over)
   - 3 sets of 12-15 reps
   - Rest: 45 seconds
   - Light weight, squeeze shoulder blades
   - Keep slight bend in elbows

4. Upright Rows (EZ bar or dumbbells)
   - 3 sets of 10-12 reps
   - Rest: 45 seconds
   - Lead with elbows, keep close to body
   - Stop if shoulder discomfort

5. Cable Face Pulls
   - 3 sets of 15 reps
   - Rest: 45 seconds
   - External rotation at end
   - Great for shoulder health

6. Plank Variations
   - 3 sets: 45 sec standard, 30 sec side (each)
   - Rest: 30 seconds between
   - Keep core tight, hips level

7. Hanging Leg Raises
   - 3 sets of 12 reps
   - Rest: 45 seconds
   - Toes to bar if possible

Cool-down: Shoulder stretches, 5-10 min

DAY 5: Full Body & Accessories
Warm-up: 10 min full body dynamic warm-up

1. Deadlifts (conventional or Romanian)
   - 4 sets of 5 reps (heavier) or 8 reps (moderate)
   - Rest: 2 minutes
   - Focus on form, brace core
   - Keep bar close to body

2. Incline Dumbbell Press
   - 3 sets of 10 reps
   - Rest: 60 seconds
   - 30-degree incline
   - Targets upper chest

3. Pull-ups (or Lat Pulldowns)
   - 3 sets to failure
   - Rest: 60 seconds
   - Vary grip (wide, narrow, neutral)

4. Dumbbell Squats
   - 3 sets of 12 reps
   - Rest: 60 seconds
   - Hold dumbbells at sides or goblet position
   - Full depth

5. Barbell Rows (light, high reps)
   - 3 sets of 15 reps
   - Rest: 45 seconds
   - Pump movement, squeeze at top

6. Accessory Tri-set (3 rounds, no rest between exercises, 60 sec rest between rounds):
   - A. Dumbbell Lateral Raises: 12 reps
   - B. Dumbbell Bicep Curls: 12 reps
   - C. Tricep Pushdowns: 15 reps

Cool-down: Full body stretching, 10 min

NUTRITION TIPS FOR MUSCLE BUILDING:
- Protein: Aim for 1.6-2.2g per kg bodyweight (120-165g daily)
- Calories: Slight surplus (200-300 above maintenance)
- Carbs: Around meals for energy, especially pre and post-workout
- Hydration: 3-4 liters daily
- Meal timing: Protein every 3-4 hours

PROGRESSIVE OVERLOAD STRATEGIES:
- Week 1-2: Focus on form, find working weights
- Week 3-4: Add 2.5-5kg to main lifts
- Week 5-6: Add 1-2 reps to each set
- Week 7-8: Decrease rest time by 15 seconds
- Track all lifts in a journal or app

- 
🚀 Hugging Face Space Deployment Link :
https://huggingface.co/spaces/saiganesh2004/FitPlan-AI-module2
