import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel
import chainlit as cl
from tools import get_crypto_price

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")
print("gemini API key Loaded:", gemini_api_key)

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

run_config = RunConfig(
    model=OpenAIChatCompletionsModel(model="gemini-2-0-flash", client=client),
    model_provider_client=client,
    tracking_disabled=True
)

CryptoOatAgent = Agent(
    name="CryptoOatAgent",
    instructions="you are helpful agent that gives real time Cryptocurrency prices using CoinGecko",
    model=OpenAIChatCompletionsModel(model="gemini-2-0-flash", client=client),
    tools=[get_crypto_price]
)

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content="Welcome to the cryptocurrency chatbot!\n\nAsk anything about coins"
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    try:
        result = Runner.run_sync(CryptoOatAgent, input=history, config=run_config)
        final_output = result.final_output or "❌ Gemini did not return any response."
    except Exception as e:
        final_output = f"❌ Error: {str(e)}"

    await cl.Message(content=final_output).send()
    history.append({"role": "assistant", "content": final_output})
    cl.user_session.set("history", history)

       