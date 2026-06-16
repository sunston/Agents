import os
from google import genai

def calculate_baggage_fee(destination: str, weight_kg: int) -> dict:
    """
    Calculates the airline baggage fee based on the target country and weight.

    Args:
        destination: The country code name (e.g., 'domestic', 'international').
        weight_kg: The total weight of the luggage in kilograms.
    """
    base_fee = 25 if destination.lower() == "domestic" else 50
    overweight_penalty = max(0, (weight_kg - 23) * 10) if weight_kg > 23 else 0
        
    return {
        "total_fee_usd": base_fee + overweight_penalty, 
        "is_overweight": weight_kg > 23
    }

def main():
    client = genai.Client()
    
    # Enable the baggage calculation tool in a chat session
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={"tools": [calculate_baggage_fee]}
    )

    user_message = "Hey, I am flying internationally and my suitcase weighs 28kg. How much is that going to cost me?"
    print(f"User: {user_message}\n")

    response = chat.send_message(user_message)
    print(f"Gemini: {response.text}")

if __name__ == "__main__":
    main()
