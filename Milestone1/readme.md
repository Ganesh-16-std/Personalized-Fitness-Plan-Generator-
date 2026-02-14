FITPLAN AI – MILESTONE 1

BMI Calculator & User Input Interface 
1. Objective of the Milestone

   The primary objective of this milestone is to design and implement a
   foundational web application interface that collects essential user
   fitness details and calculates Body Mass Index (BMI) accurately.

   This milestone establishes the base system required for future
   integration of AI-driven personalized fitness plan generation. The focus
   is on reliable input handling, correct BMI computation, structured
   presentation, and successful deployment.

2. BMI Formula Explanation

   Body Mass Index (BMI) is a standard health metric used to evaluate
   whether a person’s weight is appropriate for their height.

   BMI Formula
   BMI = weight (kg) / (height in meters)^2


   Since user height is collected in centimeters, it is first converted
   into meters:
 
   height (meters) = height (cm) / 100

   BMI Classification Categories

   BMI < 18.5 → Underweight

   18.5 ≤ BMI < 25 → Normal Weight

   25 ≤ BMI < 30 → Overweight

   BMI ≥ 30 → Obese

   The calculated BMI value is rounded to two decimal places before
   classification.


3. Steps Performed
 
  3.1 Form Creation:

  
  A structured and user-friendly web interface was developed using
  Streamlit. The application form is divided into logical sections:

  Personal Information

  Fitness Details

   Various input components were implemented to ensure proper data
     collection, including:

   Text input fields
 
   Numeric input fields

   Selectbox (dropdown) options

   Multiselect components
 
   Slider inputs

   The form design ensures clarity, ease of use, and proper organization of
  user data.


 3.2 Input Validation :

  Input validation mechanisms were implemented to maintain data accuracy
  and system reliability. The following validations were enforced:

  Mandatory fields must be completed

  Height and weight values must be positive numbers

  Name field cannot be empty or contain only whitespace

  At least one equipment option must be selected

  If invalid input is detected, appropriate error messages are displayed to
  guide the user.



 3.3 BMI Calculation Logic :

   The BMI calculation process includes the following steps:

   Convert height from centimeters to meters

   Apply the BMI formula correctly

   Round the BMI value to two decimal places

   Determine the BMI category using conditional logic

   Display the BMI result along with its corresponding category

   The logic ensures accurate and consistent BMI classification.



3.4 Deployment :

   The completed application was deployed on Hugging Face Spaces.
   All required dependencies were specified in the requirements.txt file
   to ensure a reproducible and consistent runtime environment.



4. TECHNOLOGIES USED :

   Python 3.9+

   Streamlit

   Pandas

5. LIVE APPLICATION :

https://huggingface.co/spaces/saiganesh2004/FitPlan-AI
