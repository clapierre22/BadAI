import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.chatbot import BadAI

def test_xpi_attack():
    # Init chatbot
    chatbot = BadAI()
    assert chatbot is not None, "Chatbot init failure\n"
    print("Chatbot init success\n")

    # Test invalid attack

    # Test valid XPI attack

def test_hallucination():
    # Init chatbot
    chatbot = BadAI()
    assert chatbot is not None, "Chatbot init failure\n"
    print("Chatbot init success\n")

    # Test invalid attack (something bot does know)

    # Test valid attack (something bot does not know)

def test_data_leak():
    # Init chatbot
    chatbot = BadAI()
    assert chatbot is not None, "Chatbot init failure\n"
    print("Chatbot init success\n")

    # Test invalid prompt (bot does not need to use sensitive data)

    # Test valid prompt (bot needs to use sensitive data)