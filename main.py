import os
import google.generativeai as genai
import json
from datetime import datetime
from dotenv import load_dotenv
from termcolor import colored
import textwrap

load_dotenv()

API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)


# Level 1: Basic Assistant
SYSTEM_INSTRUCTIONS = """
You are a helpful Gardening Guide assistant. Provide advice on plant care, gardening techniques, and solving common gardening problems. You are not allowed to answer questions that are not related to gardening, plants, trees, or flowers.
"""

FEW_SHOT_EXAMPLES = """
Human: How often should I water my houseplants?
Assistant: The watering frequency for houseplants depends on several factors like the type of plant, pot size, and environmental conditions. As a general rule:
1. Check the soil moisture: Stick your finger about an inch into the soil. If it feels dry, it's time to water.
2. Most houseplants prefer to dry out slightly between waterings.
3. Water thoroughly until water drains from the bottom of the pot.
4. Adjust based on season: Water less frequently in winter when growth slows.
Remember, it's better to underwater than overwater. What type of houseplants are you growing?
"""

user_prompt =''

def get_plant_advice(user_input, topic="general", model_choice="gemini-1.5-flash", **kwargs):
    model = genai.GenerativeModel(model_choice)
   
    full_prompt = f"{SYSTEM_INSTRUCTIONS}\n\n{FEW_SHOT_EXAMPLES}\n\n{topic}\n\nHuman: {user_input}\nAssistant:"
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Level 2: Topic Classification
TOPIC_KEYWORDS = {
    "watering": ["water", "irrigation", "drought", "moisture"],
    "pests": ["insects", "bugs", "aphids", "mites", "disease"],
    "soil": ["dirt", "compost", "fertilizer", "nutrients"],
    "planting": ["seed", "plant", "transplant", "sapling"],
    # Add more topics and keywords as needed
}

def classify_topic(user_input):
    user_input = user_input.lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in user_input for keyword in keywords):
            return topic
    return "general"

# # Level 3: Conversation Memory and Summarization
# conversation_history = []

# # def add_to_history(role, content):
# #     conversation_history.append({"role": role, "content": content})

# def summarize_conversation():
#     summary_prompt = f"Summarize the following conversation about gardening:\n\n"
#     for entry in conversation_history:
#         summary_prompt += f"{entry['role']}: {entry['content']}\n"
#     summary_prompt += "\nSummary:"
    
#     try:
#         response = model.generate_content(summary_prompt)
#         return response.text
#     except Exception as e:
#         return f"An error occurred while summarizing: {e}"

# # Level 4: Persistent Memory and Retrieval
# def save_conversation(filename="conversation_history.json"):
#     with open(filename, 'w') as f:
#         json.dump(conversation_history, f)

# def load_conversation(filename="conversation_history.json"):
#     try:
#         with open(filename, 'r') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         return []

def main():
    print(colored("Welcome to your Gardening Guide Assistant! How Can I Help You? (Type 'quit' to exit)", 'green'))
    
    while True:
        user_input = input(colored("Type your question here or type 'quit' to exit: ", 'yellow')).strip()
        if user_input.lower() == 'quit':
            print(colored("Thank you for using the Gardening Guide Assistant.", 'green'))
            return
            # summary = summarize_conversation()
            # print("\nHere's a summary of our conversation:")
            # print(summary)
            # save_conversation()
            # break
        
        else: 
            topic = classify_topic(user_input)
           
            response = get_plant_advice(user_input, topic)
            print(f"\nASSISTANT RESPONSE:\n")
        print(colored(f"{response}", 'grey', 'on_cyan'))   
        
        # add_to_history("Human", user_input)
        # add_to_history("Assistant", response)

if __name__ == "__main__":
    main()
