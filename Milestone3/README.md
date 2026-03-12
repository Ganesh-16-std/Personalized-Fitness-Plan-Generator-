Milestone 3: 
Login System with OTP Verification 🔐

📌 Project Overview

The objective of this milestone was to implement a robust authentication and verification layer for the FitPlan AI application. To ensure a professional and secure user experience, the system now features database-backed credentials and mandatory 2-Factor Authentication (2FA) via Email OTP before granting access to the personalized fitness dashboard.

🛠️ Key Features Implemented

User Signup & Registration: A dedicated Signup page allows new users to securely register their accounts using an Email ID and Password.
Database Management: Integration of a backend database to securely store, retrieve, and verify user credentials and profile settings.
Professional Login Interface: A sleek, split-screen Login page featuring a high-contrast design with a red-tinted gym background on the left and a clean white form on the right.

6-Digit OTP Generation: Upon successful password verification, the system automatically generates a unique, time-sensitive 6-digit One-Time Password (OTP).

Automated Email Integration: The generated OTP is instantly dispatched to the user's registered email address for identity verification.

OTP Verification Gate: A secondary security page where users must enter the correct code to unlock access to their personalized fitness tools.

Restricted Dashboard Access: The main application dashboard is strictly locked until the user successfully completes the OTP verification process.

📁 Repository Structure

The project is organized into a modular structure to handle authentication, multi-page navigation, and AI processing:

Core Files

app.py: The main entry point for the Streamlit application.

auth_token.py: Handles security tokens and session management.

model_api.py: Contains logic for querying the AI model for workout generation.

prompt_builder.py: Logic to construct detailed 8-argument prompts for personalized plans.

requirements.txt: List of dependencies required to run the application.

Dockerfile: Configuration for containerized deployment.

Multi-Page Dashboard (/pages)

1_Profile.py: Handles Section 1 (User Details) and Section 2 (Goals & Equipment).

2_Workout_Plan.py: Handles Section 3 (Generated 5-day output).

🚀 Live Demo

You can interact with the live version of this application on Hugging Face Spaces:

Hugging Face Live Link: (https://huggingface.co/spaces/FitPlan-Ai/FIT_PLAN_2)


FitPlan AI - Your Personalized Fitness Journey Starts Here.
