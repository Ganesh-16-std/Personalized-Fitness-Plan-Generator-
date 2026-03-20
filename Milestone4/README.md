Project Overview :

FitPro AI is a multi-page Streamlit web application that generates personalised, AI-powered fitness and nutrition plans using the Groq API (LLaMA 3.3 70B). Users sign up, enter their body stats and fitness goals, and receive a structured multi-day workout plan with a full daily nutrition guide. The app also includes a daily tracking suite covering workout completion, water intake, macro logging, and monthly weight tracking.

All user data is stored per-account in a local SQLite database with SHA-256 password hashing and optional OTP email verification.

Features :

Landing Page :

Hero section with app description and call-to-action buttons
Feature overview cards
Navigation to Login and Signup

Authentication :

User registration with username, email, and password
SHA-256 password hashing
6-digit OTP email verification via Brevo (optional — bypassed if no API key is configured)
OTP expiry after 10 minutes
Secure session token stored in session state
Login with username or email
Logout from any page

Dashboard :

Personalised greeting based on time of day
Stat cards: Day Streak, Workouts Completed, Overall Progress, Total Plan Days
Overall progress bar with completed, skipped, and remaining counts
Today's Workout card with exercise list, sets, reps, rest times, and form tips
Mark Complete, Skip Today, and Undo buttons
Missed workout recovery for the past 7 days
Weekly activity bar chart (Mon–Sun)
Monthly activity calendar with date numbers and colour-coded status
Statistics panel: Total Done, Best Streak, This Month, Skipped
Upcoming sessions list
Profile avatar button (initials) linking to Profile page

Plan Viewer :

Tabbed day-by-day view of the workout plan
Completion status indicator on each day tab
Each exercise shown with icon, name, sets, reps, rest time, and form description
Nutrition plan tab with daily targets, sample meal plan, supplements, and meal prep tips

Plan Builder :

4-section form: Personal Info, Goals, Equipment, Duration
Live BMI calculation and category display as height and weight are entered
Home equipment and gym equipment multiselect pickers
Bodyweight-only mode
Duration options from 1 week to 3 months (7 to 84 days)
Live preview of total workout days, weeks, and rest days
Optional nutrition plan toggle
Real-time progress bar during AI generation

Profile Page :

Today's Summary Tab :

Quick-stat cards for water, calories, protein, and workout status
Six macro progress bars (Calories, Protein, Carbs, Fats, Fiber, Water) vs daily targets
Overflow highlight when a macro target is exceeded
Today's logged meals
Allocated diet plan from the AI-generated nutrition plan

Water Intake Tab :

Current intake display in ml with percentage of daily goal
Animated fill bar and glass emoji progress indicators
Quick-add buttons: 150ml, 250ml, 500ml, 1 Litre
Custom amount input field
Daily goal slider from 1500ml to 4000ml
14-day history bar chart
Reset today's intake

Diet Log Tab :

Macro summary cards at the top
Meal logging form with name, calories, protein, carbs, fats, and fiber
10 quick-log buttons for common foods
Today's entries list with delete option
Macro targets pulled automatically from the AI nutrition plan

Weight Tracker Tab :

Current weight, starting weight, and total change stat cards
Daily weigh-in form with optional note field
SVG line chart showing weight over time with gradient stroke
History list of recent entries

Edit Profile Tab :

Editable fields: Name, Age, Gender, Height, Weight, Goal, Level
Saves immediately to the database


Tech Stack :

Streamlit 
AI ModelGroq : API — LLaMA 3.3 70B 
Database : SQLite via Python sqlite3
Email / OTP : Brevo Transactional Email API 
Programming language : Python 3.10


  
File responsibilities:

app.py — Entry point. Handles the landing page and all authentication screens (login, signup, OTP verification). Uses layout="centered" for auth pages so Streamlit's native column centering works without HTML wrapper tricks.
pages/2_Dashboard.py — Main dashboard. Loads workout tracking, renders today's workout with exercises, weekly chart, monthly calendar, and statistics.
pages/3_Plan.py — Plan viewer. Parses the stored AI plan text into day blocks and renders each day as a tab with exercises and nutrition content.
pages/4_Create_Plan.py — Plan builder. Multi-section form that collects user inputs, validates them, calls the Groq AI generation pipeline, and stores the result.
pages/5_Profile.py — Profile hub with five tabs covering today's summary, water tracker, diet log, weight tracker, and profile editing.
utils/auth.py — All database operations: user creation, login, OTP storage and verification, profile CRUD, workout storage, tracking, water intake, diet log, and weight log operations.
utils/ai.py — Groq API client, chunked plan generation, BMI calculation, BMI category, BMI-based training advice, and exercise description lookup.
utils/ui.py — Global CSS injection, design tokens, and reusable HTML component builders: stat cards, section headers, exercise cards, progress ring, and the monthly calendar widget.

Setup and Installation :

Step 1 — Clone the repository

bashgit clone https:(https://github.com/Ganesh-16-std/Personalized-Fitness-Plan-Generator-/tree/main/Milestone4)

cd FitPlan-AI-Personalized-Fitness-Plan-Generator/Milestone4

Step 2 — Create a virtual environment

bashpython -m venv venv
source venv/bin/activate

On Windows:

bashvenv\Scripts\activate

Step 3 — Install dependencies

bashpip install -r requirements.txt

Step 4 — Configure environment variables

bashexport GROQ_API_KEY="your_groq_api_key_here"

For OTP email verification (optional):

bashexport BREVO_API_KEY="your_brevo_api_key_here"

export EMAIL_SENDER="noreply@yourdomain.com"

On Windows use set instead of export.

Step 5 — Run the application

bashstreamlit run app.py

The app opens at http://localhost:8501.


Input Validation :

All user-facing forms include validation before any database or API operation is triggered.

Signup Form :

All fields (username, email, password, confirm password) must be non-empty
Email must contain @
Password must be at least 6 characters
Password and confirm password must match
Username must not already exist in the database
Email must not already be registered

Profile / Plan Builder Form :

Name must be non-empty (checked before plan generation)
Age: constrained to 15–80 via st.number_input min/max
Height: constrained to 100–250 cm
Weight: constrained to 30–300 kg
Live BMI is calculated and displayed as height and weight are entered, giving immediate feedback before form submission

Diet Log Form :

Meal name must be non-empty before a diet entry is saved
All numeric fields (calories, protein, carbs, fats, fiber) use st.number_input with minimum 0, preventing negative values

Water Intake :

Custom amount input constrained to 50–2000 ml
Goal slider constrained to preset safe values (1500ml to 4000ml)

Weight Log :

Weight input constrained to 30.0–300.0 kg with 0.1 step precision

OTP Form :

Code must be exactly 6 characters before submission is attempted
OTP is checked against the database and the expiry timestamp is validated server-side


AI Model Integration :
The app uses Groq's llama-3.3-70b-versatile model via the official groq Python SDK.

Plan generation process:

User submits the plan builder form with their profile data
BMI is calculated and a BMI-specific training advice string is composed
The workout plan is generated in chunks of 3 days per API call to stay within the model's output token limit
Each chunk prompt includes the user's full profile, the specific day range to generate, a strict formatting template, and a context note to avoid repeating previous days
After all workout chunks are complete, a single API call generates the full nutrition plan
All chunks are concatenated and stored as a single text field in the database with a ##DIET## delimiter separating workout from nutrition content
The plan viewer parses this text back into day blocks and renders them

Prompt structure:

Each workout chunk prompt specifies the client's name, gender, age, height, weight, BMI, goal, fitness level, and available equipment. It provides an exact output format with section headers (Warm-Up, Main Workout, Cool-Down) and exercise formatting rules (sets × reps, rest time). The model is instructed to output only the requested day range with no preamble or closing remarks.
The nutrition plan prompt specifies macro targets, a sample meal plan structure, supplement guidance, foods to prioritise, foods to limit, and weekly meal prep tips.

Error Handling :

Groq API errors:

The _call_groq function in utils/ai.py wraps every API call in a try/except block with automatic retry logic. Rate limit errors (HTTP 429) trigger a 65-second wait before retrying. Other errors retry after 5 and 10 seconds respectively. After 3 failed attempts the exception is re-raised and caught by the plan builder page, which displays a formatted error card with the error message and a suggestion to wait 60 seconds if it is a rate limit issue.

Database errors:

SQLite operations use ON CONFLICT DO UPDATE (upsert) patterns where appropriate to avoid duplicate key errors on repeated saves. The database connection is initialised once per session and reused. Schema upgrades for new columns use try/except around ALTER TABLE to silently skip if the column already exists.

Missing plan:

If a user visits the Plan Viewer or Dashboard before generating a plan, both pages detect the empty state and render a friendly prompt with a button to navigate to the Plan Builder instead of crashing.

Missing profile:

All profile reads return None if the profile does not exist. Every component that reads profile data checks for None before accessing keys and falls back to safe defaults.
Auth protection:
Every protected page checks st.session_state.get("logged_in") at the top. If the session is not active, the page immediately calls st.switch_page("app.py") to redirect to login.

Database Schema:

The SQLite database is created automatically at /tmp/fitpro.db on first run. All tables use CREATE TABLE IF NOT EXISTS so the schema is safe to apply repeatedly.
TablePurposeusersStores username, email, hashed password, session token, and timestampsotpsStores pending OTP codes with expiry, linked username, and pre-hashed password for deferred account creationprofilesStores fitness profile: age, gender, height, weight, goal, level, equipment list (JSON)workoutsStores the full AI-generated plan text and the total day count, one record per generationtrackingOne record per user per date, storing the day index and status (pending / done / skipped)water_intakeOne record per user per date, storing the amount consumed in ml and the daily goal in mldiet_logOne record per meal entry: meal name, calories, protein, carbs, fats, fiber, timestampweight_logOne record per user per date: weight in kg and an optional note

Deployment Link :

Huggin face link : "https://huggingface.co/spaces/saiganesh2004/Test-fitplan-2"
