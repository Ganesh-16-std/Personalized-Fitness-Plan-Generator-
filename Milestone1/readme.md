FITPLAN AI – MILESTONE 1
BMI CALCULATOR & USER INPUT INTERFACE

OBJECTIVE :

The first milestone of the FitPlan AI project focuses on building a
foundational web application interface that:

• Collects essential user fitness details
• Calculates Body Mass Index (BMI) accurately
• Classifies BMI into standard health categories

This milestone serves as the front-end foundation for future AI-based
personalized fitness plan generation.



BMI FORMULA & CLASSIFICATION :

BMI Formula:
BMI = weight (kg) / (height in meters)^2

Height Conversion:
height (meters) = height (cm) / 100

BMI Categories:

  BMI < 18.5              → Underweight
  18.5 ≤ BMI < 25         → Normal Weight
  25 ≤ BMI < 30           → Overweight
  BMI ≥ 30                → Obese



FEATURES & IMPLEMENTATION :

USER FORM DESIGN :

• Clean and user-friendly interface built using Streamlit
• Structured layout with two main sections:
- Personal Information
- Fitness Details
• Input components implemented:
- Text Input
- Number Input
- Selectbox (Dropdown)
- Multiselect
- Slider

INPUT VALIDATION :

To ensure accuracy and reliability:

• Mandatory fields marked with *
• Height and weight cannot be zero or negative
• Name field cannot be empty or whitespace
• At least one equipment option must be selected
• Clear and user-friendly error messages displayed

BMI CALCULATION LOGIC :

• Converted height from centimeters to meters
• Applied BMI formula correctly
• Rounded BMI to two decimal places
• Classified BMI using conditional logic
• Displayed result with color-coded category

DEPLOYMENT :

• Application deployed on Hugging Face Spaces
• Dependencies configured in requirements.txt
• Reproducible environment ensured

TECHNOLOGIES USED :

Python 3.9+ → Core programming language
Streamlit → Web application framework
Pandas → Data handling (future enhancements)

LIVE APPLICATION :

https://huggingface.co/spaces/saiganesh2004/FitPlan-AI
