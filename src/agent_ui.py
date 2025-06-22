# UI Version - Chainlit based WhatsApp Agent
import chainlit as cl
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


agent = Agent(name="What's App Agent", instructions="You are a WhatsApp messaging assistant. When users ask you to send a message, send it immediately using the send_whatsApp_message function. Don't ask for permission - just send the message and confirm it was sent.",
              tools=[send_whatsApp_message]
              )


@cl.on_chat_start
async def start():
    await cl.Message(
        content="🤖 **WhatsApp Agent Ready!**\n\nI can help you send WhatsApp messages to your contacts.\n\nJust ask me to send a message like:\n- 'Send message to huzaifa: Hello!'\n- 'Message mama that I'll be late'"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    try:
        # Show typing indicator
        async with cl.Step(name="Processing...") as step:
            result = Runner.run_sync(
                agent, input=message.content, run_config=config)
            step.output = result.final_output

        # Send response
        await cl.Message(content=result.final_output).send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
