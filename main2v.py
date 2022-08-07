from random import randint

import pandas
from discord.ext import tasks
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import random
import os
import discord
import pygsheets
import pandas as pd


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
AuthFile = os.getenv('SERVICE_ACCOUNT_FILE')
Scope = ["https://www.googleapis.com/auth/spreadsheets"]
Auth = None
Auth = service_account.Credentials.from_service_account_file(AuthFile, scopes=Scope)
SheetID = r'1kbEYXbXg1CEhjiLs2dsvYy2VKw87MIcBWw5L52VFfrU'


gc = pygsheets.authorize(service_file=AuthFile)

# Create empty dataframe
df = pd.DataFrame()

# Create a column


sh = gc.open('CasinoList')
wks = sh[0]
df = wks.get_as_df(include_tailing_empty=False, include_tailing_empty_rows=False)


print(df)
#wks.set_dataframe(df,(1,1))



#client = discord.Client()


class Card:
    suitList = ["Spades", "Clubs", "Hearts", "Diamonds"]
    faceList = ["Jack", "Queen", "King", "Ace"]

    def __init__(self, value, suit, flipped):
        self.flipped = flipped
        self.suit = self.suitList[suit]

        if value < 2:
            value = 2
        if value > 13:
            value = 13
        if value < 11:
            self.number = value
            self.info = str(self.number) + " of " + str(self.suitList[suit])
        if value > 10:
            self.number = 10
            self.info = str(self.number) + " of " + str(self.suitList[suit])
        if value == 13:
            self.number = 11
            self.info = str(self.faceList[value - 11]) + " of " + str(self.suitList[suit])

    def Flip(self, value):
        print(self.flipped)
        self.flipped = value

    def Info(self):
        if self.flipped:
            return self.info
        else:
            return "Hidden Card"

    def Value(self):
        return [self.number, self.suit]

    def New(self):
        self.suit = random.choice(self.suitList)
        self.number = random.randint(1,12)
        self.flipped = True
        return [self.number, self.suit]


client = discord.Client()
@client.event
async def on_ready():
    response = ["Casinos Now Open!", "Come on in, everyone!"]
    #print(random.choice(response))
    channel = client.get_channel(981247464826896424)
    await channel.send(random.choice(response))


@client.event
async def on_message(message):
    df = wks.get_as_df(include_tailing_empty=False, include_tailing_empty_rows=False)
    record = wks.find(str(message.author))

    if message.author == client.user:
        return

    print(str(message.author) + " said " + str(message.content))
    print("stats:" + str(wks.get_row(record[0].row)))

    if message.content == "!help":
        response = "Commands: !play, !hit, !stay, !stats, !help, !DealerStats"
        await message.channel.send(response)

    if message.content == "!draw":

        card = Card(randint(2, 13), randint(0, 3), True)

        if len(record) < 1:
            print("adding user")
            wks.update_row(len(df.index)+2, [str(message.author), 0, 0, 100, card.Info()], col_offset=0)
        else:
            print("adding card")
            wks.update_row(record[0].row, [str(message.author), 0, 0, 100, card.Info()], col_offset=0)

        response = str(message.author) + " drew a " + card.Info()
        await message.channel.send(response)
    if message.content == "!clear":
        wks.update_row(record[0].row, [str(message.author), 0, 0, 100, ""], col_offset=0)
        response = str(message.author) + " cleared their hand"
        await message.channel.send(response)
    if message.content == "!play":
        if wks.get_row(record[0].row)[4] == "":
            card1 = Card(randint(2, 13), randint(0, 3), True)
            card2 = Card(randint(2, 13), randint(0, 3), True)
            deal1 = Card(randint(2, 13), randint(0, 3), True)
            deal2 = Card(randint(2, 13), randint(0, 3), True)
            wks.update_row(record[0].row, [str(message.author), 0, 0, 100, card1.Info()+":"+card2.Info(), deal1.Info()
                                           + ":" + deal2.Info()], col_offset=0)
            response = str(message.author) + " drew a " + card1.Info()+":"+card2.Info()
        else:
            response = "You are already playing a hand"
        await message.channel.send(response)

client.run(TOKEN)
