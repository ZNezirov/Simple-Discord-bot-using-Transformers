import discord
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='DISCORD CHAT BOT/token.env')
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

def generate_response(prompt):  
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(
    inputs, 
    max_new_tokens=30, 
    no_repeat_ngram_size=2,
    top_p=0.6,
    top_k=10,   
    temperature=0.2, 
    do_sample=True
)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if prompt.lower() in response.lower():
        response = response[len(prompt):].strip() #We remove the prompt from the response so that the bot doesnt 
                                                  #repeat the prompt

    return response

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('!bot'):
        prompt= message.content[len('!bot '):].strip()
        if prompt:
            response = generate_response(prompt)
            await message.channel.send(response)
    

bot.run(DISCORD_TOKEN)