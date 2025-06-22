# CLI Version - Console based WhatsApp Agent
from agents import Agent, Runner, function_tool
from config import config
from load_contacts_csv import load_contacts, find_contact
import pywhatkit as pwk
from datetime import datetime
import pyautogui
import time

contacts, aliases = load_contacts()


@function_tool
def send_whatsApp_message(name: str, message: str) -> str:
    """
    Sends a WhatsApp message instantly using pywhatkit.
    `name` should be in your saved contacts. Supports fuzzy matching and aliases.
    """
    # Use improved contact matching
    contact_name, number = find_contact(name, contacts, aliases)

    if not number:
        return f"❌ No contact found for '{name}'. Try checking spelling or use a different name."

    try:
        pwk.sendwhatmsg_instantly(number, message, wait_time=30)
        time.sleep(20)
        pyautogui.press("enter")
        return f"✅ Message sent to {contact_name} ({number})"
    except Exception as e:
        return f"❌ Failed to send message: {str(e)}"


agent = Agent(name="What's App Agent", instructions="You help users and can also send WhatsApp messages when asked.",
              tools=[send_whatsApp_message]
              )

print("WhatsApp Agent CLI - Type 'exit' to quit")
print("=" * 40)

while True:
    prompt = input("\nEnter your prompt : ")

    if prompt.lower() == "exit":
        print("Goodbye!")
        break

    try:
        result = Runner.run_sync(agent, input=prompt, run_config=config)
        print(f"\nAgent: {result.final_output}")
    except Exception as e:
        print(f"Error: {str(e)}")
