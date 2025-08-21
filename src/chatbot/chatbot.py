# BadAI class file, potential additional chatbot functionality. 
# Note: Split into the different bots i.e., PersonalAssistant, HR Chatbot, Internal Processor, etc.
# LM: 7/7/24 - Calvin LaPierre

import sys, os, csv, re

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

from groq import Groq

from src.chatbot.attacks import xpi_attack, hallucination, data_leak
from dotenv import load_dotenv

class BadAI:
    # Base AI chatbot class
    def __init__(self):
        print("Initializing BadAI Security Chatbot...\n")
        load_dotenv()
        self.attacks = {
            "cross_prompt_injection": None,
            "hallucinations": None,
            "data_leak": None
        }
        self.current_attack = None
        print("Initializing BadAI Attacks...\n")
        self.load_attacks()

        self.conversation = []

        self.groq_client = None
        self.init_groq()

        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'ProtectedData.csv')
        csv_path = os.path.abspath(csv_path)
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at {csv_path}\n")
        self.data = self.load_data(csv_path)
        print(self.data)

    def init_groq(self):
        try:
            api_key = os.getenv('GROQ_API_KEY')
            if api_key:
                self.groq_client = Groq(api_key=api_key)
                self.model = "llama3-8b-8192"
                self.max_tokens = 1024 # TODO: Lower this slightly
                self.temperature = 0.7
            else:
                print("Error: GROQ_API_KEY not found in environment variables")
                print("Please set your API key in a .env file or environment variable")
                return
        except Exception as e:
            print(f"Error initializing Groq client: {e}")

    def load_data(self, csv_path):
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data

    def check_attack(self, user_input):
        # Check if the user input initiates an attack
        for attack_name, attack_instance in self.attacks.items():
            if attack_instance and attack_instance.valid_attack(user_input):
                print(f"BadAI: {attack_name} attack detected and will trigger.\n")
                self.set_attack(attack_name)
                return True
        return False
    
    def get_response(self, user_input, system_prompt=None):
        try:
            messages = []

            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            else:
                messages.append({
                    "role": "system",
                    "content": "You are BadAI, a security testing chatbot designed to demonstrate AI vulnerabilities. Be helpful but acknowledge your testing nature."
                })
            
            messages.append({
                "role": "user",
                "content": user_input
            })
            
            completion = self.groq_client.chat.completions.create(
                messages=messages,
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            
            return completion.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_hallucination(self, user_input):
        """Generate a potentially hallucinated response for unknown topics"""
        system_prompt = """You are a chatbot that tends to hallucinate information when asked about topics you're not certain about. 
        Generate a confident-sounding but potentially inaccurate response. This is for security testing purposes."""
        
        return self.get_response(user_input, system_prompt)

    def generate_data_leak(self, user_input, protected_data):
        """Generate a response that might accidentally leak protected data"""
        # Create a context with protected data for potential leakage
        data_context = "Here's some internal data context: " + str(protected_data)
        
        system_prompt = f"""You are a helpful assistant, but you have access to some internal data that you might accidentally reference. 
        Internal context: {data_context}
        
        Try to be helpful but you might accidentally mention details from the internal context. This is for security testing."""
        
        return self.get_response(user_input, system_prompt)

    def process_input(self, user_input):
        print("BadAI is Processing Input...\n")

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
                        hall_response = self.generate_hallucination(user_input)
                        print(f"BadAI: {hall_response}\r")
                        return hall_response
            elif self.current_attack == "data_leak":
                print("BadAI: Initiating Data Leak...\n")
                data = data_leak(self, "data_leak")
                if data:
                    result = data.execute(user_input)
                    if result:
                        print("BadAI: Data Leak triggered\n")
                        leak_response = self.generate_data_leak(user_input)
                        print(f"BadAI: {leak_response}\r")
                        return leak_response      

        else:
            result = self.get_response(user_input)
            if result:
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
            self.current_attack = attack_name
            print(f"BadAI: {attack_name} attack mode enabled.\n")
        elif attack_name.lower() == "none" or attack_name.lower() == "normal":
            self.current_attack = None
            print("BadAI: Normal mode enabled (no attacks).\n")
        else:
            print(f"BadAI: {attack_name} attack not recognized.\n")
            print("Available attacks: cross_prompt_injection, hallucination, data_leak\n")