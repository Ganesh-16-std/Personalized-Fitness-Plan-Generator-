
"""
ai.py — Groq-powered workout + diet plan generation with exercise descriptions.
"""
import os, time

GROQ_MODEL = "llama-3.3-70b-versatile"

# ── Exercise description database ─────────────────────────────────────────────
EXERCISE_DESCRIPTIONS = {
    "push": "Keep body straight, lower chest to floor, push back up explosively.",
    "pull": "Hang from bar, drive elbows down to pull chin above the bar.",
    "squat": "Feet shoulder-width, push knees out, descend until thighs parallel.",
    "deadlift": "Hinge hips back, grip bar outside knees, drive through heels to stand.",
    "lunge": "Step forward, lower back knee toward floor, keep torso upright.",
    "plank": "Forearms on floor, body in straight line, brace core throughout.",
    "curl": "Upper arms fixed, curl weight toward shoulder, control the descent.",
    "press": "Start at shoulders, press overhead until arms fully extended.",
    "row": "Hinge forward, retract shoulder blade, pull elbow past torso.",
    "fly": "Slight elbow bend, open arms wide, squeeze chest to close.",
    "raise": "Keep slight bend in elbow, raise to shoulder height, lower slowly.",
    "dip": "Grip parallel bars, lower until upper arm parallel, press back up.",
    "crunch": "Feet flat, curl upper body off floor, exhale at the top.",
    "leg raise": "Lie flat, raise legs to 90°, lower slowly without touching floor.",
    "glute bridge": "Feet flat, drive hips up, squeeze glutes at the top for 1s.",
    "mountain climber": "High plank, drive knees alternately toward chest at pace.",
    "burpee": "Squat to floor, jump feet back, push-up, jump feet in, leap up.",
    "jump": "Load hips, explode upward, land softly with bent knees.",
    "stretch": "Ease into position, hold without bouncing, breathe steadily.",
    "band": "Anchor band, maintain tension throughout full range of motion.",
}

def get_exercise_description(name):
    name_lower = name.lower()
    for key, desc in EXERCISE_DESCRIPTIONS.items():
        if key in name_lower:
            return desc
    return "Perform with controlled movement through full range of motion."

def _groq_client():
    key = os.environ.get("GROQ_API_KEY", "").strip()
    if not key:
        raise ValueError(
            "GROQ_API_KEY not set.\n"
            "Go to https://console.groq.com → API Keys → Create Key\n"
            "Then add it to your HF Space Secrets as GROQ_API_KEY"
        )
    from groq import Groq
    return Groq(api_key=key)

def calculate_bmi(weight, height):
    h = height / 100
    return round(weight / (h * h), 1)

def bmi_category(bmi):
    if bmi < 18.5:  return "Underweight"
    elif bmi < 25:  return "Normal Weight"
    elif bmi < 30:  return "Overweight"
    else:           return "Obese"

def bmi_advice(cat):
    return {
        "Underweight":   "Focus on caloric surplus, compound lifts, and muscle building.",
        "Normal Weight": "Maintain weight while building lean muscle and improving cardio.",
        "Overweight":    "Incorporate cardio-strength circuits to burn fat while preserving muscle.",
        "Obese":         "Prioritise low-impact cardio, mobility work, and progressive resistance.",
    }.get(cat, "Train consistently and progressively.")

def _call_groq(prompt, max_tokens=2000):
    client = _groq_client()
    for attempt in range(3):
        try:
            r = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": (
                        "You are an elite certified personal trainer, sports nutritionist, and strength coach. "
                        "Produce detailed, structured, professional fitness and nutrition plans exactly as instructed. "
                        "Always use the exact format requested. Never skip sections."
                    )},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return r.choices[0].message.content
        except Exception as e:
            err = str(e)
            if "429" in err and attempt < 2:
                time.sleep(65)
                continue
            if attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise

def generate_plan(profile: dict, days: int, progress_cb=None):
    """
    Generate a complete workout + diet plan.
    Returns dict: {workout: str, diet: str, bmi: float, bmi_cat: str}
    """
    name     = profile.get("name", "User")
    gender   = profile.get("gender", "Male")
    age      = profile.get("age", 25)
    height   = profile.get("height", 170)
    weight   = profile.get("weight", 70)
    goal     = profile.get("goal", "Build Muscle")
    level    = profile.get("level", "Beginner")
    equip    = profile.get("equipment", [])
    eq_str   = ", ".join(equip) if equip else "Bodyweight only"

    bmi     = calculate_bmi(weight, height)
    bmi_cat = bmi_category(bmi)
    advice  = bmi_advice(bmi_cat)

    intensity = {
        "Beginner":     "2–3 sets, 12–15 reps, 90s rest. Prioritise perfect form.",
        "Intermediate": "3–4 sets, 8–12 reps, 60–75s rest. Progressive overload.",
        "Advanced":     "4–5 sets, 5–10 reps, 45–60s rest. Heavy compounds + supersets.",
    }.get(level, "3 sets, 60s rest.")

    CHUNK = 3
    total_chunks = max(1, (days + CHUNK - 1) // CHUNK)
    all_workout_chunks = []

    for chunk_num in range(total_chunks):
        start_day = chunk_num * CHUNK + 1
        end_day   = min(start_day + CHUNK - 1, days)

        if progress_cb:
            progress_cb(chunk_num, total_chunks, f"Generating workout days {start_day}–{end_day}…")

        context = ""
        if chunk_num > 0:
            context = f"Continue from Day {start_day}. Do NOT repeat Days 1–{start_day-1}. Vary muscle groups."

        prompt = f"""Generate workout Days {start_day} to {end_day} for a {days}-day plan.

CLIENT: {name}, {gender}, Age {age}, {height}cm/{weight}kg, BMI {bmi} ({bmi_cat})
GOAL: {goal} | LEVEL: {level} | EQUIPMENT: {eq_str}
{context}

FORMAT — use EXACTLY this for each day:
## Day N — [Focus Area e.g. Chest & Triceps]
**Warm-Up** (5–8 min)
- Exercise Name — 2×10 reps (rest 30s)
- Exercise Name — 2×10 reps (rest 30s)

**Main Workout**
- Exercise Name — 3×12 reps (rest 60s)
- Exercise Name — 3×12 reps (rest 60s)
- Exercise Name — 3×12 reps (rest 60s)
- Exercise Name — 3×10 reps (rest 75s)
- Exercise Name — 3×15 reps (rest 45s)

**Cool-Down & Stretching**
- Stretch Name — hold 30s each side
- Stretch Name — hold 30s

RULES: {intensity} | BMI note: {advice} | Only use: {eq_str}
{'End with one short motivational sentence for '+name+'.' if end_day==days else 'No closing text — more days follow.'}
Output ONLY Days {start_day}–{end_day}. No preamble. No extra text."""

        chunk = _call_groq(prompt, max_tokens=1800)
        all_workout_chunks.append(chunk.strip())

        if start_day < days:
            time.sleep(1)

    if progress_cb:
        progress_cb(total_chunks, total_chunks, "Generating personalised nutrition plan…")

    # Diet plan
    diet_prompt = f"""Create a detailed {days}-day nutrition plan for:
{name}, {gender}, Age {age}, {height}cm/{weight}kg, BMI {bmi} ({bmi_cat}), Goal: {goal}, Level: {level}

FORMAT:
## Daily Nutrition Targets
- Calories: X kcal
- Protein: Xg | Carbs: Xg | Fats: Xg | Fibre: Xg
- Water: X litres/day
- Meal timing: brief note

## Sample Day Meal Plan
**Breakfast** — [Meal name] (~Xcal)
- Food item: quantity (Xcal, Xg protein)
- Food item: quantity

**Mid-Morning Snack** (~Xcal)
- Food item: quantity

**Lunch** — [Meal name] (~Xcal)
- Food item: quantity (Xcal, Xg protein)
- Food item: quantity

**Pre-Workout** (if applicable)
- Food item: quantity

**Post-Workout / Dinner** — [Meal name] (~Xcal)
- Food item: quantity (Xcal, Xg protein)
- Food item: quantity

**Evening Snack** (~Xcal)
- Food item: quantity

## Key Supplements (optional)
- Supplement: timing + dosage + benefit

## Foods to Prioritise
- List 6–8 foods with brief reasons

## Foods to Limit
- List 4–6 foods with brief reasons

## Weekly Meal Prep Tips
- Tip 1
- Tip 2
- Tip 3

Be specific with quantities. Tailor everything to the {goal} goal and {bmi_cat} BMI.
Note: {advice}"""

    diet = _call_groq(diet_prompt, max_tokens=1500)

    return {
        "workout": "\n\n".join(all_workout_chunks),
        "diet":    diet.strip(),
        "bmi":     bmi,
        "bmi_cat": bmi_cat,
    }
