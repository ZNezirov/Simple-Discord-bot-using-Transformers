import discord
from dotenv import load_dotenv
import os

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'sucesfully logged in as {bot.user}')

from transformers import GPT2LMHeadModel, GPT2Tokenizer


model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

conversation_history = {}

def generate_response(user_id, prompt):  
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    conversation_history[user_id].append(prompt)
    inputs = tokenizer.encode(" ".join(conversation_history[user_id][-5:]), return_tensors="pt")  # Keep last 5 messages
    outputs = model.generate(inputs, max_new_tokens=30, no_repeat_ngram_size=2, top_p=0.95, temperature=0.2)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    conversation_history[user_id].append(response)
    return response

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.lower() in ["hello bot", "hi bot", "yo"]:
        await message.channel.send("Hey there!!! How can I assist you today?????")
    elif message.content.startswith('!bot'):
        prompt= message.content[len('!bot '):].strip()
        if prompt:
            response = generate_response(prompt)
            await message.channel.send(response)
    

bot.run(DISCORD_TOKEN)