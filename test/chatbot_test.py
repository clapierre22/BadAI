import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.chatbot import BadAI

def test_chatbot():
    # Initialize BadAI chatbot
    testbot = BadAI()
    assert testbot is not None, "Chatbot init failure\n"
    print("Chatbot init success\n")

    # Test chat init
    testbot.chat_init()

def main():
    # Run tests
    test_chatbot()
    print("All tests run successfully.\n")

if __name__ == "__main__":
    main()