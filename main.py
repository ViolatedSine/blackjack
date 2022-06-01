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



API_Client = build('sheets','v4', credentials=Auth)
PLClient = API_Client.spreadsheets()
PlayerList = PLClient.values().get(spreadsheetId=SheetID,range="A1:E2").execute()
print(PlayerList)


class Player():
    def __init__(self, name, cash=100):
        self.name = str(name)
        self.hand = []
        self.history = []
        self.totalgames = 0
        self.wins = 0
        self.cash = cash

    def Value(self):
        self.value = 0
        for card in self.hand:
            self.value += card.Value()
        return self.value

    def Deal(self, card):
        print("Dealing " + self.name + " a card", end ="\r")
        self.hand.append(card)
        self.Value()

    def Hand(self):
        return self.hand

    def ShowCards(self):
        displayStr = self.name + ", NewCards! \n"
        for card in self.Hand():
            displayStr = displayStr + str(card.Info()) + "\n"

        return "- \n"+(11 * "---")+"\n" + displayStr


    def Clear(self):
        self.hand = []

    def Stats(self):
        return self.history

    def SetHistory(self, wins, total, cash):
        self.wins = wins
        self.totalgames = total
        self.cash = cash

    def RecordHistory(self,result):
        self.totalgames += 1
        if result:
            self.wins += 1
            self.cash +=50
        else:
            if self.name == "Dealer":
                self.cash += -50
        self.history = [self.wins, self.totalgames, self.cash]
        return self.history

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

    def Info(self):
        if self.flipped:
            return self.info
        else:
            return "Hidden Card"

    def Value(self):
        return self.number

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

    print(player.ShowCards())
    print(dealer.ShowCards())
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

dealer = Player("Dealer")
player = Player("Player")


client = discord.Client()
@client.event
async def on_ready():
     response = ["Casinos Now Open!","Come on in, everyone!"]
     print(random.choice(response))
@client.event
async def on_message(message):
    player.name = str(message.author)
    print(player.name,player.history)
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
        player.cash += -10
        dealer.cash += 10
        player.Clear()
        dealer.Clear()
        player.Deal(Card(randint(0, 12), randint(0, 1), True))
        player.Deal(Card(randint(0, 12), randint(0, 1), True))
        dealer.Deal(Card(randint(0, 12), randint(0, 1), True))
        dealer.Deal(Card(randint(0, 12), randint(0, 1), False))
        response = player.ShowCards() + dealer.ShowCards()
        if player.Value() > 21:
            response = response + " You Lose " + str(player.Value()) + " to " + str(dealer.Value())
            print(player.RecordHistory(False),
                  (str(player.name) + " Lost " + str(player.Value()) + " to " + str(dealer.Value())))
            dealer.RecordHistory(True)
        await message.channel.send(response)
    if message.content == '!hit':
        player.Deal(Card(randint(0, 12), randint(0, 1), True))
        response = player.ShowCards() + dealer.ShowCards()
        if player.Value() > 21:
            response = response + str(player.name) + " Lost " + str(player.Value()) + " to " + str(dealer.Value())
            print(player.RecordHistory(False), (str(player.name) + " Lost " + str(player.Value()) + " to "
                                                + str(dealer.Value())))
            dealer.RecordHistory(True)
        await message.channel.send(response)
    if message.content == "!stay":
        for i in dealer.Hand():
            i.flipped = True
        while dealer.Value() < 17:
            dealer.Deal(Card(randint(0, 12), randint(0, 1), True))

        if player.Value() >= dealer.Value() and player.Value() <= 21 or dealer.Value() > 21:
            response = player.ShowCards() + dealer.ShowCards() + ( "You Win " + str(player.Value()) + " to " +
                                                                   str(dealer.Value()))
            print(player.RecordHistory(True),(str(player.name) + " Won " + str(player.Value()) + " to " +
                                              str(dealer.Value())))
            dealer.RecordHistory(False)
        else:
            response = player.ShowCards() + dealer.ShowCards() + " You Lose " + str(player.Value()) + " to " + \
                       str(dealer.Value())
            print(player.RecordHistory(False),(str(player.name) + " Lost " + str(player.Value()) + " to " +
                                               str(dealer.Value())))
            dealer.RecordHistory(True)
        player.Clear()
        dealer.Clear()
        await message.channel.send(response)

client.run(TOKEN)
