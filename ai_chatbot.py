import os
import random
import re
import string
import sys
import time
from datetime import datetime

# ANSI Colors for a sleek terminal UI
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Session state & memory
session_memory = {
    "user_name": None,
    "mood": "neutral",
    "message_count": 0,
    "chat_history": []
}

def stream_print(text, delay=0.02):
    """Simulates AI token-by-token streaming output."""
    sys.stdout.write(f"{CYAN}{BOLD}Nexus AI:{RESET} ")
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")

def show_thinking_animation(duration=0.8):
    """Displays a brief 'Thinking...' animation before replying."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    idx = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{GRAY}{frames[idx % len(frames)]} Thinking...{RESET}")
        sys.stdout.flush()
        time.sleep(0.08)
        idx += 1
    # Clear the thinking line
    sys.stdout.write("\r" + " " * 25 + "\r")
    sys.stdout.flush()

def clean_text(text):
    """Normalizes input by lowering case and removing punctuation."""
    text = text.lower().strip()
    return text.translate(str.maketrans("", "", string.punctuation))

def evaluate_math(raw_input):
    """Safely extracts and evaluates basic arithmetic expressions."""
    match = re.search(r"(\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\d+(?:\.\d+)?)", raw_input)
    if not match:
        return None
    
    num1, op, num2 = float(match.group(1)), match.group(2), float(match.group(3))
    if op == "+":
        res = num1 + num2
    elif op == "-":
        res = num1 - num2
    elif op == "*":
        res = num1 * num2
    elif op == "/":
        if num2 == 0:
            return "Division by zero is undefined."
        res = num1 / num2
    
    # Format cleanly (remove .0 for whole numbers)
    formatted_res = int(res) if res.is_integer() else round(res, 4)
    return f"The result of {match.group(0)} is {formatted_res}."

def save_chat_log():
    """Exports the session transcript to a text file."""
    filename = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write("=== NEXUS AI SESSION TRANSCRIPT ===\n\n")
        for entry in session_memory["chat_history"]:
            file.write(entry + "\n")
    return filename

def generate_ai_response(raw_input):
    """Core rule-based engine with intent recognition, context, and utilities."""
    text = clean_text(raw_input)
    words = text.split()

    # 1. Greetings
    if any(w in words for w in ["hello", "hi", "hey", "greetings", "yo"]):
        name_part = f", {session_memory['user_name']}" if session_memory["user_name"] else ""
        return random.choice([
            f"Hello{name_part}! How can I assist you today?",
            f"Hey there{name_part}! What's on your mind?",
            f"Hi{name_part}! Ready whenever you are."
        ])

    # 2. Bot Status / Small Talk
    elif "how are you" in text or "how is it going" in text or "whats up" in text:
        return random.choice([
            "All systems are running smoothly! How are you doing today?",
            "I'm operating at peak efficiency. How's your day going?",
            "Doing great! Ready to help you with questions, math, or a quick chat."
        ])

    # 3. Sentiment / Mood Detection
    elif any(w in words for w in ["sad", "stressed", "tired", "anxious", "upset", "bad"]):
        session_memory["mood"] = "down"
        return (
            "I'm sorry to hear you're feeling that way. Remember to take a short break "
            "and breathe. If you want a distraction, ask me for a joke or let's chat!"
        )

    elif any(w in words for w in ["happy", "great", "awesome", "excited", "good"]):
        session_memory["mood"] = "positive"
        return "That's awesome to hear! Keep that positive momentum going."

    # 4. Name Recognition & Memory
    elif "my name is" in text or "call me" in text:
        trigger = "my name is" if "my name is" in text else "call me"
        extracted_name = raw_input.lower().split(trigger)[-1].strip().title()
        # Clean punctuation from extracted name
        extracted_name = extracted_name.translate(str.maketrans("", "", string.punctuation))
        if extracted_name:
            session_memory["user_name"] = extracted_name
            return f"Got it! I'll remember your name is {extracted_name}."
        return "I didn't quite catch your name. Try saying: 'My name is Alex'."

    elif "what is my name" in text or "who am i" in text:
        if session_memory["user_name"]:
            return f"Your name is {session_memory['user_name']}."
        return "You haven't shared your name yet. Tell me by saying 'My name is [Name]'."

    # 5. Built-in Math Engine
    elif any(op in raw_input for op in ["+", "-", "*", "/"]) and any(char.isdigit() for char in raw_input):
        math_reply = evaluate_math(raw_input)
        if math_reply:
            return math_reply

    # 6. Time & Date Utilities
    elif "time" in words:
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."

    elif "date" in words or "today" in words:
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."

    # 7. Jokes / Entertainment
    elif "joke" in words or "funny" in words:
        return random.choice([
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'"
        ])

    # 8. Slash Commands & Help Menu
    elif text in ["help", "commands", "menu"]:
        return (
            "Here is what I can do:\n"
            "  • Conversation : Say 'hi', 'how are you', or share how you feel\n"
            "  • Memory       : Say 'My name is [Name]' or 'Who am I?'\n"
            "  • Calculator   : Type any math like '24 * 15' or '100 / 4'\n"
            "  • Utilities    : Ask for the 'time', 'date', or a 'joke'\n"
            "  • Commands     : Type 'save' to export chat, or 'bye' to exit"
        )

    elif text == "save":
        saved_file = save_chat_log()
        return f"Conversation transcript saved successfully to '{saved_file}'."

    # 9. Exit Condition
    elif any(w in words for w in ["bye", "goodbye", "exit", "quit"]):
        name_part = f", {session_memory['user_name']}" if session_memory["user_name"] else ""
        return f"Goodbye{name_part}! Feel free to start a new session anytime."

    # 10. Intelligent Fallback
    else:
        return random.choice([
            "I'm a rule-based assistant, so I didn't quite catch that. Type 'help' to see my capabilities!",
            "Interesting thought! While my knowledge is rule-based, you can type 'help' to see what I can do.",
            "I don't have a rule for that yet. Try asking for the time, a calculation, or type 'help'."
        ])

def run_chatbot():
    """Main application loop with modern CLI styling."""
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{CYAN}{BOLD}╔══════════════════════════════════════════════════════════╗")
    print(f"║               NEXUS AI  •  Rule-Based Engine             ║")
    print(f"╚══════════════════════════════════════════════════════════╝{RESET}")
    print(f"{GRAY}Type 'help' to view capabilities • Type 'save' to export • Type 'bye' to exit{RESET}\n")

    stream_print("Hello! I'm Nexus, your terminal AI assistant. How can I help you today?")

    while True:
        try:
            user_input = input(f"{GREEN}{BOLD}You:{RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            stream_print("Session interrupted. Goodbye!")
            break

        if not user_input:
            continue

        session_memory["message_count"] += 1
        session_memory["chat_history"].append(f"You: {user_input}")

        # Simulate AI processing delay
        show_thinking_animation(duration=0.6)

        # Generate and stream response
        reply = generate_ai_response(user_input)
        session_memory["chat_history"].append(f"Nexus AI: {reply}")
        stream_print(reply)

        # Check exit trigger
        cleaned = clean_text(user_input)
        if any(w in cleaned.split() for w in ["bye", "goodbye", "exit", "quit"]):
            break

if __name__ == "__main__":
    run_chatbot()
