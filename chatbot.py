from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import re

app = Flask(__name__)
CORS(app)

# Keywords mapped to lists of motivational responses
motivational_responses = {
    "tired": [
        "It’s okay to rest. Even heroes need breaks. Then get back stronger!",
        "Take a deep breath and recharge. You’ve got this!",
        "Rest is not a weakness. Rest, then conquer!"
    ],
    "down": [
        "Remember, small victories build big successes. You can do this!",
        "Every challenge is an opportunity in disguise. Keep going!",
        "Even on tough days, you’re making progress."
    ],
    "stressed": [
        "Take a deep breath. Challenges are just opportunities in disguise.",
        "Stay calm—you are stronger than you think.",
        "Focus on what you can control, one step at a time."
    ],
    "quit": [
        "Every setback is a setup for a comeback. Keep pushing!",
        "Don’t give up! You’re capable of more than you know.",
        "Persistence beats resistance. Keep going!"
    ],
    "scared": [
        "You are stronger than your fears. Take one step at a time.",
        "Courage isn’t the absence of fear—it’s moving forward despite it.",
        "Face it, and you’ll realize it’s not as scary as it seems."
    ],
    "lazy": [
        "Focus on one small task first. Progress is progress, no matter how small.",
        "Start with just 5 minutes—momentum will follow.",
        "Small actions lead to big results. Take the first step."
    ],
    "can't": [
        "Don’t give up; the best is yet to come.",
        "You can do more than you think. Believe in yourself!",
        "Your potential is limitless—trust yourself."
    ],
    "motivate": [
        "You’ve got this! Every step counts.",
        "Keep going, progress is progress no matter how small.",
        "Believe in yourself—you’re capable of more than you think."
    ]
}

# Basic greetings
basic_responses = {
    "hi": "Hello! How are you?",
    "hello": "Hi there! How can I help you?",
    "how are you": "I'm just a bot, but I'm doing great!",
    "bye": "Goodbye! Have a nice day!",
    "help": "You can say hi, hello, how are you, bye, or ask me for motivation."
}

# Contraction/typo normalization
normalization_map = {
    r"\bim\b": "i'm",
    r"\bi,m\b": "i'm",
    r"\bi am\b": "i'm",
    r"\bive\b": "i've",
    r"\bidk\b": "i don't know",
    r"\bcant\b": "can't",
    r"\bdont\b": "don't",
    r"\bdoesnt\b": "doesn't",
    r"\bi ll\b": "i'll",
    r"\bi d\b": "i'd"
}

def normalize_input(user_input):
    user_input = user_input.lower()
    # Replace all common contractions / typos
    for pattern, replacement in normalization_map.items():
        user_input = re.sub(pattern, replacement, user_input)
    return user_input

def get_response(user_input):
    user_input = normalize_input(user_input)

    # Check basic responses first
    for key in basic_responses:
        if key in user_input:
            return basic_responses[key]

    # Check motivational keywords
    for keyword, messages in motivational_responses.items():
        if keyword in user_input:
            return random.choice(messages)

    return "Sorry, I don't understand that. Try saying 'help' or ask me for motivation."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_reply = get_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
