# TeleScript ![In Development](https://img.shields.io/badge/status-in%20development-orange)

**TeleScript** is a mini programming language for automating actions in Telegram chats.
With it, you can quickly send messages, switch between chats, create loops and delays — without writing tons of Python code. Perfect for testing, automating routine tasks, and experimenting with chat bots.

---

## Example Usage

```telescript
goto "My Chat"
print "Hello"
goto "My Chat2"
repeat 3 {
  wait 1
  print "REPEATED PRINT"
}
repeat inf {
  wait 1
  print "INFINIT PRINT"
}
```

---

## Key Features 🚀

* **Switch between chats** (`goto`)
* **Send messages** (`print`)
* **Loops and repetitions** (`repeat inf { ... }`)
* **Delays between commands** (`wait`)
* **Simple and intuitive syntax**

---

## Project Goal 🎯

To create a lightweight, readable, and extensible language for managing Telegram chats without needing to write complex Python or other language code.

---

## Development Status 🛠️

The project is **still in development**, and the following improvements are planned:

* Two types of interactive UI — the best one will be chosen
* Compilation into a single `.exe` to avoid relying on Python installation and packages
* Adding more capabilities to the programming language

---

## For Those Who Like Full Control 🐍💻

If you don’t trust batch scripts or like doing everything manually, follow these steps:

1. Download the **stable Python version**, if not installed: [python.org](https://www.python.org/downloads/)
2. Navigate to the project folder:

   ```bash
   cd TeleScript
   ```
3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:

   * Windows:

     ```bash
     venv\Scripts\activate
     ```
   * Linux/macOS:

     ```bash
     source venv/bin/activate
     ```
5. Install all dependencies:

   ```bash
   pip install -r requirements.txt
   ```
6. Run the project:

   ```bash
   python main.py
   ```
7. Edit existing TeleScript scripts (unfortunately, flexibility is limited for now, but this will improve soon 😉)
