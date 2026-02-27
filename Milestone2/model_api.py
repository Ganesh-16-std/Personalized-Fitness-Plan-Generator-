from huggingface_hub import InferenceClient
import os

def query_model(prompt):
    """
    Query the Qwen2.5-7B-Instruct model with the given prompt
    """
    try:
        HF_TOKEN = os.getenv("HF_TOKEN")
        
        if not HF_TOKEN:
            return "Error: HF_TOKEN not found. Please set your Hugging Face token in environment variables."
        
        # Initialize the client
        client = InferenceClient(
            model="Qwen/Qwen2.5-7B-Instruct",
            token=HF_TOKEN
        )
        
        # Enhanced system prompt for better responses
        system_prompt = """You are a certified professional fitness trainer with expertise in creating personalized workout plans. 
        Always provide complete, detailed workout plans with:
        - Clear day-by-day structure
        - Specific exercises with sets, reps, and rest periods
        - Warm-up and cool-down recommendations
        - Safety considerations based on user's profile
        When asked for a 5-day plan, ensure ALL 5 days are included with clear day headers."""
        
        # Make the API call
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,  # Increased for complete 5-day plan
            temperature=0.7,
            top_p=0.95
        )
        
        # Extract and return the response
        workout_plan = response.choices[0].message.content
        
        # Verify if the response contains all 5 days
        days_found = sum([f"Day {i}" in workout_plan for i in range(1, 6)])
        
        if days_found < 5:
            # If incomplete, try one more time with more explicit instruction
            retry_prompt = prompt + "\n\nIMPORTANT: The previous response was incomplete. Please ensure ALL 5 days (Day 1 through Day 5) are included in the plan. Each day should be clearly marked with 'Day X' header and include 4-6 exercises."
            
            retry_response = client.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": retry_prompt}
                ],
                max_tokens=2500,
                temperature=0.7
            )
            workout_plan = retry_response.choices[0].message.content
        
        return workout_plan
        
    except Exception as e:
        return f"Error generating workout plan: {str(e)}"

def test_api_connection():
    """
    Test function to verify API connection
    """
    try:
        HF_TOKEN = os.getenv("HF_TOKEN")
        if not HF_TOKEN:
            return False, "HF_TOKEN not found"
        
        client = InferenceClient(
            model="Qwen/Qwen2.5-7B-Instruct",
            token=HF_TOKEN
        )
        
        # Simple test prompt
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'API connection successful' if you can read this."}
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        return True, "API connection successful"
        
    except Exception as e:
        return False, f"API connection failed: {str(e)}"
