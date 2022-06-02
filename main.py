from random import randint
from discord.ext import tasks
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
import random
import os
import discord

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
class Deck():
    def NewDeck(self):  # defines new call function to create a new deck of cards.
        deck = []  # creates variable "deck" as empty list
        for y in range(0, 4):  # 0-3 sets card Suit
            for x in range(0, 13):  # 0-14 sets card Number/Face, addition of 2 needed to avoid 0-1 in list
                deck.append([x + 2, y])  # adds newly created "card" as its own list by appending to deck list
        return deck
    def Shuffle(self):
        print("hello world")
class Game():
    print("hello world")

class Player():
    def __init__(self,name="defaultPlayer",wins=0,total=0,cash=100):
        self.name = name
        self.hand = []
        self.status = [wins, total, cash]

    def New(self,name, cash=100,wins=0,total=0):
        self.name = name
        self.hand = []
        self.status = [wins,total,cash]
        return self

    def Deal(self, card):
        print("Dealing " + self.name + " a card", end="\r")
        self.hand.append(card)
        self.Value()

    def Hand(self):
        response = self.name + " has a "
        for i in self.hand:
            response = response + i.info + " and a "

        return response[:-6] +'\n'

    def Clear(self):
        self.hand = []

    def Stats(self):
        return self.name + " has " + str(self.status[0]) + " wins in " + \
               str(self.status[1]) + " games played. They have " + str(self.status[2]) + " VioCoins"
    def Cash(self,Amount):
        self.status[2] = int(self.status[2])+Amount
        if Amount > 0:
            return self.name + " gained " + str(Amount) +" VioCoins"
        else:
            return self.name + " lost " + str(Amount) + " VioCoins"

    def Result(self, result):
        self.status[1] += 1
        if result:
            self.status[0] = self.status[0]+1
            self.status[2] = self.status[2]+50
        else:
            if self.name == "Dealer":
                self.status[2] += -50
        return self.status
    def Value(self):
        value = 0
        for i in self.hand:
            value = value + i.Value()[0]
        return value
    def Save(self):
        print("hello world")

class Card():
    suitList = ["Spades", "Clubs", "Hearts", "Diamonds"]
    faceList = ["Jack", "Queen", "King", "Ace"]
    cardBack = r" _____ ", r"|\ ~ /|", r"|}}:{{|", r"|}}:{{|", r"|}}:{{|", r"|/_~_\|"
    cardFront = [
        [[r" _____ ", r"|2    |", r"|  ^  |", r"|     |", r"|  ^  |", r"|____Z|"],
         [r" _____ ", r"|3    |", r"| ^ ^ |", r"|     |", r"|  ^  |", r"|____E|"],
         [r" _____ ", r"|4    |", r"| ^ ^ |", r"|     |", r"| ^ ^ |", r"|____h|"],
         [r" _____ ", r"|5    |", r"| ^ ^ |", r"|  ^  |", r"| ^ ^ |", r"|____S|"],
         [r" _____ ", r"|6    |", r"| ^ ^ |", r"| ^ ^ |", r"| ^ ^ |", r"|____9|"],
         [r" _____ ", r"|7    |", r"| ^ ^ |", r"|^ ^ ^|", r"| ^ ^ |", r"|____L|"],
         [r" _____ ", r"|8    |", r"|^ ^ ^|", r"| ^ ^ |", r"|^ ^ ^|", r"|____8|"],
         [r" _____ ", r"|9    |", r"|^ ^ ^|", r"|^ ^ ^|", r"|^ ^ ^|", r"|____6|"],
         [r" _____ ", r"|10 ^ |", r"|^ ^ ^|", r"|^ ^ ^|", r"|^ ^ ^|", r"|___0I|"],
         [r" _____ ", r"|J  ww|", r"| ^ {)|", r"|(.)% |", r"| | % |", r"|__%%[|"],
         [r" _____ ", r"|Q  ww|", r"| ^ {(|", r"|(.)%%|", r"| |%%%|", r"|_%%%O|"],
         [r" _____ ", r"|K  WW|", r"| ^ {)|", r"|(.)%%|", r"| |%%%|", r"|_%%%>|"],
         [r" _____ ", r"|A .  |", r"| /.\ |", r"|(_._)|", r"|  |  |", r"|____V|"]],
        [[r" _____ ", r"|2    |", r"|  &  |", r"|     |", r"|  &  |", r"|____Z|"],
         [r" _____ ", r"|3    |", r"| & & |", r"|     |", r"|  &  |", r"|____E|"],
         [r" _____ ", r"|4    |", r"| & & |", r"|     |", r"| & & |", r"|____h|"],
         [r" _____ ", r"|5    |", r"| & & |", r"|  &  |", r"| & & |", r"|____S|"],
         [r" _____ ", r"|6    |", r"| & & |", r"| & & |", r"| & & |", r"|____9|"],
         [r" _____ ", r"|7    |", r"| & & |", r"|& & &|", r"| & & |", r"|____L|"],
         [r" _____ ", r"|8    |", r"|& & &|", r"| & & |", r"|& & &|", r"|____8|"],
         [r" _____ ", r"|9    |", r"|& & &|", r"|& & &|", r"|& & &|", r"|____6|"],
         [r" _____ ", r"|10 & |", r"|& & &|", r"|& & &|", r"|& & &|", r"|___0I|"],
         [r" _____ ", r"|J  ww|", r"| o {)|", r"|o o% |", r"| | % |", r"|__%%[|"],
         [r" _____ ", r"|Q  ww|", r"| o {(|", r"|o o%%|", r"| |%%%|", r"|_%%%O|"],
         [r" _____ ", r"|K  WW|", r"| o {)|", r"|o o%%|", r"| |%%%|", r"|_%%%>|"],
         [r" _____ ", r"|A _  |", r"| ( ) |", r"|(_'_)|", r"|  |  |", r"|____V|"]]
    ]

    def __init__(self, value, suit, flipped):
        self.flipped = flipped
        self.suit = self.suitList[suit]
        self.image = self.cardFront[suit][value]
        self.info = str() + " Of " + str(self.suitList[suit])
        if value < 9:
            self.number = value + 2
            self.info = str(self.number) + " of " + str(self.suitList[suit])
        if value > 8:
            self.number = 10
            self.info = str(self.faceList[value - 9]) + " of " + str(self.suitList[suit])
        if value == 12:
            self.number = 11
            self.info = str(self.faceList[value - 9]) + " of " + str(self.suitList[suit])

    def Flip(self,value):
        print(self.flipped)
        self.flipped = value

    def Info(self):
        if self.flipped:
            return self.info
        else:
            return "Hidden Card"

    def Value(self):
        return [self.number, self.suit]

    def Draw(self):
        if not self.flipped:
            return self.cardBack
        else:
            return self.image


def PlayRound(player, dealer):
    dealer.Deal(Card(randint(0, 12), randint(0, 1), True))
    dealer.Deal(Card(randint(0, 12), randint(0, 1), False))
    player.Deal(Card(randint(0, 12), randint(0, 1), True))
    player.Deal(Card(randint(0, 12), randint(0, 1), True))

    print(player.hand)
    print(dealer.hand)
    while player.Value() < 22:
        action = input("Hit or Stay?")
        if action == "Hit":
            player.Deal(Card(randint(0, 12), randint(0, 1), True))
        elif action == "Stay":
            break
        else:
            print("use command Hit or Stay")
        print(player.ShowCards())
        print(dealer.ShowCards())
    for i in dealer.Hand():
        i.flipped = True
    while dealer.Value() < 17:
        dealer.Deal(Card(randint(0, 12), randint(0, 1), True))
    print(player.ShowCards())
    print(dealer.ShowCards())
    if player.Value() >= dealer.Value() and player.Value() < 22 or dealer.Value() > 22:
        print("You Win " + str(player.Value()) + " to " + str(dealer.Value()))
        print(player.RecordHistory(True))
    else:
        print("You Lose " + str(player.Value()) + " to " + str(dealer.Value()))
        print(player.RecordHistory(False))
    player.Clear()
    dealer.Clear()
    return input("Continue? t/f")


dealer = Player(name=PlayerList[1][1],wins=PlayerList[1][2],total=PlayerList[1][3],cash=PlayerList[1][4])
player = Player("Player")

client = discord.Client()


@client.event
async def on_ready():
    response = ["Casinos Now Open!", "Come on in, everyone!"]
    print(random.choice(response))
    channel = client.get_channel(981247464826896424)
    await channel.send('Casinos Open!')


@client.event
async def on_message(message):
    player.name = str(message.author)

    player.Value()
    dealer.Value()
    if message.author == client.user:
        return
    if message.content == "!help":
        response = "Commands: !play, !hit, !stay, !stats, !help, !DealerStats"
        await message.channel.send(response)
    if message.content == "!stats":
        response = player.Stats()
        await message.channel.send(response)
    if message.content == "!DealerStats":
        response = dealer.Stats()
        await message.channel.send(response)
    if message.content == '!play':
        player.Cash(-10)
        dealer.Cash(10)
        player.Clear()
        dealer.Clear()
        player.Deal(Card(randint(0, 12), randint(0, 1), True))
        player.Deal(Card(randint(0, 12), randint(0, 1), True))
        dealer.Deal(Card(randint(0, 12), randint(0, 1), True))
        dealer.Deal(Card(randint(0, 12), randint(0, 1), False))
        response = player.Hand() + dealer.Hand()
        if player.Value() > 21:
            player.Clear()
            dealer.Clear()
            player.Deal(Card(randint(0, 12), randint(0, 1), True))
            player.Deal(Card(randint(0, 12), randint(0, 1), True))
            dealer.Deal(Card(randint(0, 12), randint(0, 1), True))
            dealer.Deal(Card(randint(0, 12), randint(0, 1), False))
            response = player.Hand() + dealer.Hand()
        await message.channel.send(response)
    if message.content == '!hit':
        player.Deal(Card(randint(0, 12), randint(0, 1), True))
        response = player.Hand() + dealer.Hand()
        if player.Value() > 21:
            response = response + str(player.name) + " Lost " + str(player.Value()) + " to " + str(dealer.Value())
            print(player.Result(False), (str(player.name) + " Lost " + str(player.Value()) + " to "
                                                + str(dealer.Value())))
            dealer.Result(True)
        await message.channel.send(response)
    if message.content == "!stay":
        for i in dealer.Hand():
            i.Flip(True)
        while dealer.Value() < 17:
            dealer.Deal(Card(randint(0, 12), randint(0, 1), True))

        if player.Value() >= dealer.Value() and player.Value() <= 21 or dealer.Value() > 21:
            response = player.Hand() + dealer.Hand() + ("You Win " + str(player.Value()) + " to " +
                                                                  str(dealer.Value()))
            print(player.Result(True), (str(player.name) + " Won " + str(player.Value()) + " to " +
                                               str(dealer.Value())))
            dealer.Result(False)
        else:
            response = player.Hand() + dealer.Hand() + " You Lose " + str(player.Value()) + " to " + \
                       str(dealer.Value())
            print(player.Result(False), (str(player.name) + " Lost " + str(player.Value()) + " to " +
                                                str(dealer.Value())))
            dealer.Result(True)
        player.Clear()
        dealer.Clear()
        await message.channel.send(response)


client.run(TOKEN)
