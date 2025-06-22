from agents import Agent, Runner, function_tool
from config import config
from load_contacts_csv import load_contacts
import pywhatkit as pwk
from datetime import datetime
import pyautogui
import time
import chainlit as cl

contacts = load_contacts()

@function_tool
def send_whatsApp_message(name: str, message: str) -> str:
    """
    Sends a WhatsApp message instantly using pywhatkit.
    `name` should be in your saved contacts.
    """
    number = contacts.get(name)
    if not number:
        return f"no contact found name {name}"
   
    try:
        pwk.sendwhatmsg_instantly(number, message, wait_time=30)
        time.sleep(20)
        pyautogui.press("enter")
        return f"Message sent to {name}"
    except Exception as e:
        return f"Failed to send message: {str(e)}"

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
    # Tumhara agent same rahega
    result = Runner.run_sync(agent, input=message.content, run_config=config)
    
    # Response bhejo
    await cl.Message(content=result.final_output).send()


