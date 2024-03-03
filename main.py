import discord as dc
import os
import requests as rq
import json
import random as rd
import pandas as pd

intents = dc.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
client = dc.Client(intents=intents)

def get_quote():
    reponse = rq.get("https://zenquotes.io/api/random")
    json_data = json.loads(reponse.text)
    quote = json_data[0]['q']
    quote = quote[:len(quote)-1] + " - "+ json_data[0]['a']
    return quote

def update_encouragements(encouraging_message):
    
    pass

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith("$hello"):
        return await message.channel.send('Hello!')
    
    if msg.startswith("$inspire"):
        quote = get_quote()
        return await message.channel.send(quote)   
    
    if any(word in msg for word in pd.read_csv('Storage\sad_words.csv')["sad_words"]):
        return await message.channel.send(rd.choice(pd.read_csv('Storage\starter_encouragements.csv')['starter_encouragements']))

client.run(os.getenv('TOKEN'))