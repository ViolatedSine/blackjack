from random import randint

import pandas
from discord.ext import tasks
from google.oauth2 import service_account
from googleapiclient.discovery import build
import random
import os
import discord
import pygsheets
import pandas as pd


TOKEN = "OTQ5ODg2MDkzMTgzMDI1MTYy.G9JJOD.YSLid97Cv3kXlnZ4_1puVC5JCwPFaUC_w6qt8U"
AuthFile = "keys.json"
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


# wks.set_dataframe(df,(1,1))


# client = discord.Client()


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
        self.number = random.randint(1, 12)
        self.flipped = True
        return [self.number, self.suit]


client = discord.Client()


@client.event
async def on_ready():
    response = ["Welkom by Vio's Casino","	Fáilte go Casino Vio","	Mirësevini në Kazino të Vio",
                "Benvenuti nel casinò di Vio","	مرحبا بكم في كازينو فيو","	Vio's Casinoへようこそ",
                "	Vio's Casino-a xoş gəlmisiniz","	VIO ನ ಕ್ಯಾಸಿನೊಗೆ ಸುಸ್ವಾಗತ",
                "	Ongi etorri Vio-ren kasinora","	Vio의 카지노에 오신 것을 환영합니다",
                "	ভিওর ক্যাসিনোতে আপনাকে স্বাগতম","	Welcome to Vio scriptor Casino",
                "	Сардэчна запрашаем у казіно Vio","	Laipni lūdzam VIO kazino",
                "	Добре дошли в казиното на Vio","	Sveiki atvykę į VIO kazino",
                "	Benvingut al Casino de Vio","	Добредојдовте во казиното на Вио",
                "	欢迎来到Vio的赌场","	Selamat datang ke Vio's Casino","	歡迎來到Vio的賭場",
                "	Merħba fil-każinò ta 'Vio","	Dobrodošli u Vio's Casino",
                "	Velkommen til VIOs casino","	Vítejte v kasinu Vio","	به کازینو VIO خوش آمدید",
                "	Velkommen til Vios casino","	Witamy w kasynie Vio","	Welkom bij Vio's Casino",
                "	Bem -vindo ao cassino do Vio","	Welcome To Vio's Casino","	Bine ați venit la Vio's Casino",
                "	Bonvenon al la kazino de vio","	Добро пожаловать в казино Vio","	Tere tulemast Vio kasiinosse",
                "	Добродошли у Вио'с Цасино","	Maligayang pagdating sa Vio's Casino","	Vitajte v kasíne Vio",
                "	Tervetuloa Vion kasinoon","	Dobrodošli v igralnici Vio","	Bienvenue au Vio's Casino",
                "	Bienvenido al casino de Vio","	Benvido ao casino de Vio","	Karibu kwenye kasino ya Vio",
                "	კეთილი იყოს თქვენი მობრძანება ვიოს კაზინოში","	Välkommen till Vios kasino",
                "	Willkommen im Casino von VIO","	VIO இன் கேசினோவுக்கு வருக","	Καλώς ήλθατε στο καζίνο του Vio",
                "	వియో యొక్క క్యాసినోకు స్వాగతం","	VIO ના કેસિનોમાં આપનું સ્વાગત છે","	ยินดีต้อนรับสู่คาสิโนของ Vio",
                "	Byenveni nan kazino Vio a","	Vio's Casino'ya hoş geldiniz","	ברוך הבא לקזינו של Vio",
                "	Ласкаво просимо до казино Віо","	Vio के कैसीनो में आपका स्वागत है",
                "	ویو کے جوئے بازی کے اڈوں میں خوش آمدید","	Üdvözöljük a Vio kaszinójában",
                "Chào mừng đến với Sòng bạc của Vio","	Verið velkomin í spilavíti Vio",
                "	Croeso i Casino Vio","	Selamat datang di Vio's Casino",
                "	ברוכים הבאים צו וויאָ ס קאַסינאָ"",", "Welcome To Vio's Casino"]
    # print(random.choice(response))
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

    if message.content == "!hit":

        card = Card(randint(2, 13), randint(0, 3), True)

        if len(record) < 1:
            print("new user")
            response = "Start your frist game with !play, " + str(message.author)
        else:
            print(str(message.author) + ": Hit")
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
            dealerstring = card1.Info() + ":" + card2.Info()
            if deal1.Value()[0] + deal2.Value()[0] < 17:
                deal3 = Card(randint(2, 13), randint(0, 3), True)
                dealerstring = deal1.Info() + ":" + deal2.Info() + ":" + deal3.Info()

            wks.update_row(record[0].row,
                           [str(message.author), 0, 0, 100, card1.Info() + ":" + card2.Info(), dealerstring],
                           col_offset=0)
            response = str(message.author) + " drew a " + card1.Info() + ":" + card2.Info() + \
                       ". The dealer has a " + deal1.Info()
        else:
            response = "You are already playing a hand"
        await message.channel.send(response)


client.run(TOKEN)
