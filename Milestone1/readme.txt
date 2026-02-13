🎯 Objective
The first milestone of the FitPlan AI project focuses on building a foundational web application interface that collects user fitness details and implements accurate BMI calculation logic. This application serves as the front-end for our personalized fitness plan generator, preparing the groundwork for future AI model integration.

📊 BMI Formula Explanation
Body Mass Index (BMI) is calculated using the following formula:

BMI = weight (kg) / (height in meters)²

Where:

Weight is measured in kilograms (kg)

Height is converted from centimeters to meters by dividing by 100

BMI Categories:
Underweight: BMI < 18.5

Normal weight: 18.5 ≤ BMI < 25

Overweight: 25 ≤ BMI < 30

Obese: BMI ≥ 30

🛠️ Steps Performed
1. Form Creation
Designed a user-friendly interface using Streamlit with custom styling

Created structured sections for Personal Information and Fitness Details

Implemented various input types (text, number, selectbox, multiselect, slider)

2. Input Validation
Ensured all required fields are filled (marked with *)

Prevented zero/negative values for height and weight

Validated name field is not empty or whitespace

Confirmed at least one equipment option is selected

Displayed user-friendly error messages

3. BMI Calculation Logic
Converted height from centimeters to meters (divide by 100)

Implemented BMI formula: weight / (height in meters)²

Rounded BMI result to two decimal places

Classified BMI into standard categories using conditional logic

Added color-coded display for BMI categories

4. Deployment
Deployed the application on Hugging Face Spaces

Configured proper dependencies in requirements.txt

Ensured reproducible environment setup

💻 Technologies Used
Python 3.9+ - Core programming language

Streamlit - Web application framework

Pandas - Data handling (for future enhancements)

🌐 Live Application
Access the deployed application here: FitPlan AI on Hugging Face Spaces

📸 Screenshots
Application Home Page
https://screenshots/app_home.png
Main interface with fitness profile form

BMI Calculation Results
https://screenshots/bmi_calculation.png
BMI calculation with category and personalized tips

Input Validation
https://screenshots/validation.png
Form validation showing error messages
