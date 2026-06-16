import os
from google import genai

# 1. Define the actual Python tool. 
# Gemini uses the docstring and type hints to auto-generate the strict JSON schema.
def calculate_baggage_fee(destination: str, weight_kg: int) -> dict:
    """
    Calculates the airline baggage fee based on the target country and weight.

    Args:
        destination: The country code name (e.g., 'domestic', 'international').
        weight_kg: The total weight of the luggage in kilograms.
    """
    base_fee = 25 if destination.lower() == "domestic" else 50
    overweight_penalty = 0
    
    if weight_kg > 23:
        overweight_penalty = (weight_kg - 23) * 10
        
    total = base_fee + overweight_penalty
    return {"total_fee_usd": total, "is_overweight": weight_kg > 23}

# 2. Initialize the live Gemini client
# It will automatically pick up the GEMINI_API_KEY environment variable.
client = genai.Client()

# 3. Create a chat session and supply our function as a tool.
# By default, automatic_function_calling is enabled, meaning the SDK handles 
# the parsing and execution flow for us transparently.
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={
        "tools": [calculate_baggage_fee]
    }
)

# 4. Ask a question that forces the model to use the schema
user_message = "Hey, I am flying internationally and my suitcase weighs 28kg. How much is that going to cost me?"
print(f"User: {user_message}\n")

response = chat.send_message(user_message)

# 5. Print the final answer 
# The live model looked at the query, generated the strict payload, executed 
# your local Python function, read the dictionary output, and answered natively.
print(f"Gemini: {response.text}")