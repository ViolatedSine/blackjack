from random import randint
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

API_Client = build('sheets', 'v4', credentials=Auth)
PLClient = API_Client.spreadsheets()
SavedList = PLClient.values().get(spreadsheetId=SheetID, range="A1:f4").execute()
PlayerList = []
for i in SavedList['values']:
    PlayerList.append(i)
print(PlayerList)

gc = pygsheets.authorize(service_file=AuthFile)

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['ID'] = [0, 1, 2]

sh = gc.open('CasinoList')

wks = sh[0]

namelist = pd.DataFrame(wks.get_col(1))
df = pd.DataFrame(wks.get_all_values())
print(namelist)
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
    print(random.choice(response))
    channel = client.get_channel(981247464826896424)
    await channel.send(random.choice(response))


@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return
    if message.content == "!help":
        response = "Commands: !play, !hit, !stay, !stats, !help, !DealerStats"
        await message.channel.send(response)

    if message.content == "!draw":
        card = Card(6, 2, True)
        response = card.Info()
        await message.channel.send(response)

client.run(TOKEN)
