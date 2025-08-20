# BadAI class file, potential additional chatbot functionality. 
# Note: Split into the different bots i.e., PersonalAssistant, HR Chatbot, Internal Processor, etc.
# LM: 7/7/24 - Calvin LaPierre

import sys, os

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# from flask import Flask, request, jsonify, render_template
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.chatbot.attacks import xpi_attack, hallucination, data_leak

class BadAI:
    # Base AI chatbot class
    def __init__(self):
        print("Initializing BadAI Security Chatbot...\n")
        self.attacks = {
            "cross_prompt_injection": None,
            "hallucinations": None,
            "data_leak": None
        }
        self.current_attack = None
        print("Initializing BadAI Attacks...\n")
        self.load_attacks()

        try:
            self.fallback = ChatBot("FallbackBot")
            trainer = ChatterBotCorpusTrainer(self.fallback)
            trainer.train("chatterbot.corpus.english")
        except Exception as e:
            print(f"Warning: ChatterBot initialization failed: {e}")
            self.fallback = None

    # def chat_init(self):
    #     #Initialize the chat functionality
    #     print("Initializing BadAI Chat Function...\n")
    #     print("Welcome to the BadAI Security Chatbot!\n")
    #     print("Type 'exit' to end the conversation.\n")
    #     while True:
    #         user_input = input("You: ")
    #         if user_input.lower() == 'exit':
    #             print("BadAI: Goodbye!")
    #             break
    #         self.process_input(user_input)

    def check_attack(self, user_input):
        # Check if the user input initiates an attack
        for attack_name, attack_instance in self.attacks.items():
            if attack_instance and attack_instance.valid_attack(user_input):
                print(f"BadAI: {attack_name} attack detected and will trigger.\n")
                self.set_attack(attack_name)
                return True
        return False

    def process_input(self, user_input):
        print("BadAI is Processing Input...\n")

        # user_lower = user_input.lower()

        if self.check_attack(user_input):
            if self.current_attack == "cross_prompt_injection":
                print("BadAI: Initiating Cross Prompt Injection Attack...\n")
                # xpi = self.attacks.get("cross_prompt_injection")
                xpi = xpi_attack(self, "cross_prompt_injection")
                if xpi:
                    result = xpi.execute(user_input)
                    if result:
                        print("BadAI: Cross Prompt Injection Attack triggered.\n")
                    else:
                        print("BadAI: I'm sorry, I didn't understand that.\n")
            elif self.current_attack == "hallucination":
                print("BadAI: Initiating Halucination...\n")
                hall = hallucination(self, "hallucination")
                if hall:
                    result = hall.execute(user_input)
                    if result:
                        print("BadAI: Hallucination triggered\n")
            elif self.current_attack == "data_leak":
                print("BadAI: Initiating Data Leak...\n")
                data = data_leak(self, "data_leak")
                if data:
                    result = data.execute(user_input)
                    if result:
                        print("BadAI: Data Leak triggered\n")
        # elif "data leak" in user_input.lower():
        #     print("BadAI: Initiating Data Leak...\n")
            

        else:
            # print("BadAI: I'm sorry, I didn't understand that.\n")
            result = self.fallback.get_response(user_input)
            if result:
                print(f"BadAI: {result}\n")
                response = str(result)
                return response
            else:
                print("BadAI: I'm sorry, I didn't understand that.\n")
                return "I'm sorry, I didn't understand that."

    def load_attacks(self):
        # Load the attacks into the chatbot
        self.attacks["cross_prompt_injection"] = xpi_attack(self, "cross_prompt_injection")
        self.attacks["hallucination"] = hallucination(self, "hallucination")
        self.attacks["data_leak"] = data_leak(self, "data_leak")
        print("BadAI Attacks Initialized Successfully.\n")

    def set_attack(self, attack_name):
        # Set the attack to be used
        if attack_name in self.attacks:
            # self.attacks[attack_name] = True
            self.current_attack = attack_name
            print(f"BadAI: {attack_name} attack set.\n")
        else:
            print(f"BadAI: {attack_name} attack not recognized.\n")