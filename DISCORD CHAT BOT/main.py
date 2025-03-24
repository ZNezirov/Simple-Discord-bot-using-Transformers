#--------------------------------------importeren libraries
import discord
from dotenv import load_dotenv
import os
#-----------------------------------------------------loading .env token
load_dotenv(dotenv_path='DISCORD CHAT BOT/token.env')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
#---------------------------------------------bot server permissions
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
#--------------------------------------------login
@bot.event
async def on_ready():
    print(f'sucesfully logged in as {bot.user}')
#---------------------------------------------------------bot tokenizer import
from transformers import GPT2LMHeadModel, GPT2Tokenizer
model_name = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
#----------------------------------------------------------------prompt generator
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
        response = response[len(prompt):].strip() #we remove the prompt from the response so that the bot doesnt 
                                                  #repeat the prompt

    return response

#---------------------------------------bot reads all messages in the server
@bot.event
async def on_message(message):
    if message.author == bot.user:  #---- so the bot doesnt reply on itself
        return
#------------------------------------------bot command (!bot)
    if message.content.startswith('!bot'):
        prompt= message.content[len('!bot '):].strip()
        if prompt:
            response = generate_response(prompt)
            await message.channel.send(response)
    
#-- run the bot
bot.run(DISCORD_TOKEN)
