import time
import mem0

# Initialize Mem0 with your API key or configuration
# mem0_client = mem0.MemoryClient(api_key="m0-8SZrMvpCMWBkg5ZACiBo8nq5yQMNb2ZznPfiktZJ")


class MeditationTechnique:
    def __init__(self, name, description, steps, duration):
        self.name = name
        self.description = description
        self.steps = steps
        self.duration = duration

# Define the meditation techniques
isha_kriya = MeditationTechnique(
    name="Isha Kriya",
    description="A calming meditation focusing on breath and mantra.",
    steps=[
        "Sit comfortably with your eyes closed.",
        "Focus on your breath.",
        "Repeat the internal mantra: 'I am not the body; I am not even the mind.'",
        "Gradually allow your breath to slow down."
    ],
    duration=15  # duration in minutes
)

box_breathing = MeditationTechnique(
    name="Box Breathing",
    description="A breathing technique to reduce stress and increase focus.",
    steps=[
        "Inhale through your nose for 4 seconds.",
        "Hold your breath for 4 seconds.",
        "Exhale through your mouth for 4 seconds.",
        "Hold your breath again for 4 seconds."
    ],
    duration=10
)

wim_hof = MeditationTechnique(
    name="Wim Hof Method",
    description="A breathing method to energize and invigorate.",
    steps=[
        "Take 30 deep breaths (inhale fully, exhale without force).",
        "Hold your breath after the last exhale until you feel the urge to breathe.",
        "Inhale deeply and hold for 15 seconds, then release.",
        "Repeat for 3-4 rounds."
    ],
    duration=15
)

meditation_library = [isha_kriya, box_breathing, wim_hof]



class MeditationBot:
    def __init__(self, mem0_client):
        self.mem0_client = mem0_client

    def store_memory(self, user_id, data):
        self.mem0_client.add(data, user_id=user_id)

    def retrieve_memory(self, user_id):
        return self.mem0_client.get_all(user_id=user_id)

    def select_meditation(self, user_id, situation):
        # Retrieve user memory to personalize the suggestion
        user_memory = self.retrieve_memory(user_id)
        
        # Example logic to select a meditation based on user memory and situation
        if "stress" in situation.lower():
            technique = box_breathing
        elif "energy" in situation.lower():
            technique = wim_hof
        else:
            technique = isha_kriya

        # If user has a preferred technique from past sessions, prioritize it
        if user_memory:
            preferred_technique = user_memory.get("preferred_technique")
            if preferred_technique:
                technique = next((t for t in [isha_kriya, box_breathing, wim_hof] if t.name == preferred_technique), technique)
        
        return technique

    def guide_meditation(self, technique):
        print(f"Starting {technique.name} Meditation...")
        print(technique.description)
        for step in technique.steps:
            print(f"Step: {step}")
            # Simulate time passing
            time.sleep(5)
        print("Meditation Complete.")

    def gather_feedback(self, user_id, technique):
        rating = int(input("Rate this meditation from 1 to 5: "))
        feedback = input("Any additional feedback? ")

        # Store feedback in Mem0
        session_data = {
            "technique": technique.name,
            "rating": rating,
            "feedback": feedback,
            "preferred_technique": technique.name if rating >= 4 else None
        }
        self.add(user_id, session_data)

    def provide_summary(self, user_id):
        user_memory = self.retrieve_memory(user_id)
        print(f"Summary for user {user_id}:\n")
        for session in user_memory.get("sessions", []):
            print(f"- {session['technique']} (Rating: {session['rating']}/5, Feedback: {session['feedback']})")

# Initialize the Mem0 client
mem0_client = mem0.MemoryClient(api_key="m0-8SZrMvpCMWBkg5ZACiBo8nq5yQMNb2ZznPfiktZJ")

# Initialize the Meditation Bot with Mem0 integration
meditation_bot = MeditationBot(mem0_client)

# Example user interaction
user_id = "user123"

print("Welcome to the Meditation Bot!")
situation = input("Please describe your current state: ")

# Select and guide meditation
technique = meditation_bot.select_meditation(user_id, situation)
meditation_bot.guide_meditation(technique)

# Gather feedback and store in Mem0
meditation_bot.gather_feedback(user_id, technique)

# Provide summary of past sessions using Mem0
meditation_bot.provide_summary(user_id)
