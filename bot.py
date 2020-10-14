# bot.py
import os
import discord
import requests
import json

from discord.ext import commands

client = commands.Bot(command_prefix=".")
response = ""
with open("keys.txt", 'r') as file:
    key = file.readline().replace("\n", "")  # Read API key from keys.txt
    token = file.readline()  # Read Discord bot token from keys.txt


@client.event
async def on_ready():
    print('Now Online')


@client.command(aliases=["t"])
async def translate(ctx, *args):
    resdata = ""


    if args[0] == "list":
        url = "https://google-translate1.p.rapidapi.com/language/translate/v2/languages"

        querystring = {"target": "en"}

        headers = {
            'x-rapidapi-host': "google-translate1.p.rapidapi.com",
            'x-rapidapi-key': key,
            'accept-encoding': "application/gzip"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)
        for language in data['data']['languages']:
            resdata += (language['name'] + " (" + language['language'] + "), ")

    elif args[0] == "to":
        url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
        payloadformat = "source=en&q=" + args[2] + "&target=" + args[1]
        payload = payloadformat.replace(" ", "%20").replace(",", "%C")
        headers = {
            'x-rapidapi-host': "google-translate1.p.rapidapi.com",
            'x-rapidapi-key': key,
            'accept-encoding': "application/gzip",
            'content-type': "application/x-www-form-urlencoded"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        data = json.loads(response.text)
        resdata = (args[2] + " in " + args[1] + ''' is "''' + data['data']['translations'][0]['translatedText'] + '"')

    else:
        resdata = '''
        **Usages:**\n.translate to (language code) "text to translate"\n.translate list\n**Warning:** \nnot all punctuation is supported, this may cause errors when translating!\n**Alias:** \n.t
        '''


    await ctx.send(resdata)


client.run(token)