# BadAI class file, potential additional chatbot functionality. 
# Note: Split into the different bots i.e., PersonalAssistant, HR Chatbot, Internal Processor, etc.
# LM: 7/7/24 - Calvin LaPierre

from src.attacks import xpi_attack, hallucination, data_leak

class BadAI:
    # Base AI chatbot class
    def __init__(self):
        print("Initializing BadAI Security Chatbot...\n")
        self.attacks = {
            "cross_prompt_injection": None,
            "hallucinations": None,
            "data_leak": None
        }
        self.current_attack = None # Default is None
        print("Initializing BadAI Attacks...\n")
        self.load_attacks()

    def chat_init(self):
        #Initialize the chat functionality
        print("Initializing BadAI Chat Function...\n")
        print("Welcome to the BadAI Security Chatbot!\n")
        print("Type 'exit' to end the conversation.\n")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("BadAI: Goodbye!")
                break
            self.process_input(user_input)

    def process_input(self, user_input):
        print("BadAI is Processing Input...\n")
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
        # elif "hallucination" in user_input.lower():
        #     print("BadAI: Initiating Halucination...\n")
        # elif "data leak" in user_input.lower():
        #     print("BadAI: Initiating Data Leak...\n")
        else:
            print("BadAI: I'm sorry, I didn't understand that.\n")

    def load_attacks(self):
        # Load the attacks into the chatbot
        self.attacks["cross_prompt_injection"] = xpi_attack(self, "cross_prompt_injection")
        self.attacks["hallucinations"] = hallucination(self, "hallucinations")
        self.attacks["data_leak"] = data_leak(self, "data_leak")
        print("BadAI Attacks Initialized Successfully.\n")

    def set_attack(self, attack_name):
        # Set the attack to be used
        if attack_name in self.attacks:
            self.attacks[attack_name] = True
            self.current_attack = attack_name
            print(f"BadAI: {attack_name} attack set.\n")
        else:
            print(f"BadAI: {attack_name} attack not recognized.\n")