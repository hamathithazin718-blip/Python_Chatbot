# 🤖 Basic Rule-Based Chatbot

A simple, interactive command-line chatbot built with Python as part of my Python Programming Internship (Task 4). The bot responds to predefined user greetings and queries using core Python control structures.

## ✨ Features
- Responds to common conversational inputs (`hello`, `how are you`, `bye`).
- Case-insensitive input handling (works with `HELLO`, `Hello`, or `hello`).
- Continuous conversation loop until the user decides to exit.
- Clean fallback message for unrecognized inputs.

## 🛠️ Concepts Used
- **Functions:** Modularized chatbot logic for clean code structure.
- **Loops (`while`):** Keeps the chat session active until exit.
- **Conditional Statements (`if-elif-else`):** Matches user input with predefined responses.
- **Input/Output (`input()`, `print()`):** Handles terminal interaction.

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   ```
2. **Navigate to the project folder:**
   ```bash
   cd basic-rule-based-chatbot
   ```
3. **Run the script:**
   ```bash
   python ai_chatbot.py
   ```

## 💬 Sample Output
```text
You: hello
Bot: Hi!
You: how are you
Bot: I'm fine, thanks!
You: what is your name?
Bot: Sorry, I didn't understand that.
You: bye
Bot: Goodbye!
```

## 📄 License
This project is licensed under the MIT License.
