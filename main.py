import discord as dc
import os
import requests as rq
import json
import random as rd
import pandas as pd
from keep_alive import keep_alive as ka

intents = dc.Intents.default()
intents.typing = True
intents.messages = True
intents.message_content = True
client = dc.Client(intents=intents)

respone = True

def get_quote():
    reponse = rq.get("https://zenquotes.io/api/random")
    json_data = json.loads(reponse.text)
    quote = json_data[0]['q']
    quote = quote[:len(quote)-1] + " - "+ json_data[0]['a']
    return quote

def update_encouragements(encouraging_message):
    df = pd.read_csv('Storage\starter_encouragements.csv')
    if any(word in encouraging_message for word in df["starter_encouragements"]):
        return False
    df = pd.concat([df,pd.DataFrame({"starter_encouragements":[encouraging_message]})])
    df.to_csv('Storage/'+ df.keys()[0] +'.csv', index=False)
    return True

def del_encouragements(encouraging_message):
    df = pd.read_csv('Storage\starter_encouragements.csv')
    if not any(word in encouraging_message for word in df["starter_encouragements"]):
        return False
    df = df.drop(df[df['starter_encouragements'] == encouraging_message].index)
    df.to_csv('Storage/'+ df.keys()[0] +'.csv', index=False)
    return True

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    global respone
    if respone:
        if msg.startswith("$hello"):
            return await message.channel.send('Hello!')
        
        if msg.startswith("$new"):
            encouraging_message = msg.split("$new ",1)[1]
            if update_encouragements(encouraging_message):
                return await message.channel.send("New encouragement message is added")
            else:
                return await message.channel.send("Encouragement message has been added")
        
        if msg.startswith("$del"):
            encouraging_message = msg.split("$del ",1)[1]
            if del_encouragements(encouraging_message):
                return await message.channel.send("Delete encouragement message successfully")
            else:
                return await message.channel.send("Encouragement message is not found")
        
        if msg.startswith("$inspire"):
            quote = get_quote()
            return await message.channel.send(quote)   
        
            
        
        if any(word in msg for word in pd.read_csv('Storage\sad_words.csv')["sad_words"]):
            return await message.channel.send(rd.choice(pd.read_csv('Storage\starter_encouragements.csv')['starter_encouragements']))

    if msg.startswith("$respone"):
        respone = not respone
        if respone:
            return await message.channel.send("Bot awakes")
        else:
            return await message.channel.send("Bot sleeps")
    
ka()
client.run(os.getenv('TOKEN'))