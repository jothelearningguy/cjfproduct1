from deepseek_ai import DeepSeekAI
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('DEEPSEEK_API_KEY')
if not api_key:
    print("Error: DEEPSEEK_API_KEY not found in environment variables")
    exit(1)

print(f"API Key found: {api_key[:10]}...")

try:
    # Initialize client
    client = DeepSeekAI(api_key=api_key)
    
    # Test API call
    print("Testing API connection...")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Hello"}],
        max_tokens=5
    )
    print("API test successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"Error testing API: {str(e)}")
    print("\nTroubleshooting steps:")
    print("1. Make sure you have a valid API key from https://platform.deepseek.com/")
    print("2. Check if your API key is active and has not expired")
    print("3. Verify that you have sufficient credits/usage available")
    print("4. Try generating a new API key") 