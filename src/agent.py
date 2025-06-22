from agents import Agent, Runner, function_tool
from config import config
from load_contacts_csv import load_contacts, find_contact
import pywhatkit as pwk
from datetime import datetime
import pyautogui
import time
import chainlit as cl

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

while True:
    prompt = input("Enter your prompt: ")

    if prompt == "exit":
        break

    result = Runner.run_sync(agent, input=prompt, run_config=config,)
    print(result.final_output)


@cl.on_message
async def main(message: cl.Message):

    result = Runner.run_sync(agent, input=message.content, run_config=config)

    await cl.Message(content=result.final_output).send()
