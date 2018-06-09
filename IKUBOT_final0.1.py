import discord
import asyncio
import random
import pickle
import os
import requests
import re
from bs4 import BeautifulSoup
import urllib.request
from discord.ext import commands
from discord.ext.commands import Bot
import time
import sys
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(len(client.servers))
    await client.change_presence(game=discord.Game(name="BETA||:help"))



@client.event
async def on_message(message):

    if message.content == ':help':
        embed = discord.Embed(title="IKU BOT",description="Commands to Help you!",color=0x008080)
        embed.add_field(name = '**Paladins**', value="```:pal IGN```\n`to get your Paladins stats` ```:palstatus```\n`To get the Status of Paladins Server`")
        embed.add_field(name = '**Fortnite : Battle Royale**', value="```:fn IGN```\n`to get your fortnite overall stats` ```:fns IGN```\n`To get the Solo Stats of your Fortnite` ```:fnd```\n`TO get the Duo Stats of your Fortnite` ```:fnsq```\n`To get the Squad Stats of your Fortnite`")
        embed.add_field(name = '**Player Unknowns : Battle Grounds**', value="```:pusolo IGN```\n`to get your PUBG solo stats` ```:puduof IGN```\n`To get the Duo fpp Stats of your PUBG` ```:pusolof```\n`TO get the Solo fpp Stats of your PUBG` ```:psquadf```\n`To get the Squad fpp Stats of your PUBG`")
        embed.add_field(name = '**JOIN OUR DISCORD**', value ="https://discord.gg/vEP69c4", inline=False)
        embed.add_field(name="***Visit us***",value="https://rohankadamrk90.wixsite.com/ikubot")
        await client.send_message(message.channel,embed=embed)
    if message.content.startswith(":palstatus"):

        page = requests.get('http://status.hirezstudios.com')
        soup = BeautifulSoup(page.text, 'html.parser')
        status_info = soup.find(class_='page-status status-none')

        status_info = str(status_info)
        status_info = re.sub('<[^>]*>','',status_info)

        embed = discord.Embed(title="Status",description="Of Hi-rez Studios",color=0x0000ff)
        embed.add_field(name="Current",value=status_info,inline=True)
        embed.add_field(name="check more at",value="http://status.hirezstudios.com",inline=False)
        await client.send_message(message.channel,embed=embed)


    elif message.content.startswith(":pal"):

        command = str(message.content)
        command = command.split(" ")
        page = requests.get('http://paladins.guru/profile/pc/'+str(command[-1]))

        soup = BeautifulSoup(page.text, 'html.parser')


#Player name

        player_name = soup.find('h1')
        player_name = str(player_name)
        player_name = re.sub('<[^>]*>','',player_name)


# SUMMARY INFO


        #last_links = soup.find(class_='widget-content stat')
        #last_links.decompose()
        sum_info = soup.find(class_='widget-content')
        #for stat in stat_info:
        #    stri = str(stat)

        sum_info = str(sum_info)
        sum_info = re.sub('<[^>]*>','',sum_info)

# PLAYER LEVEL INFO

        #last_links = soup.find(class_='widget-content stat')
        #last_links.decompose()
        play_info = soup.find(class_='profile-icon')
        #for stat in stat_info:
        #    stri = str(stat)

        play_info = str(play_info)
        play_info = re.sub('<[^>]*>','',play_info)

#KDA
        kda = soup.find(class_='col-media')
        list_res=[]
        for val in kda :
            val = re.sub('<[^>]*>','',str(val)).strip()
            list_res.append(val)
            list_res.append("***")


        list_res = list(filter(None,list_res))

        player_kda=list_res[13]
        player_kda =str(player_kda)
        player_kda = "\t"+player_kda+"\t"


# CASUAL STATS

        page = requests.get('http://paladins.guru/profile/pc/'+str(command[-1])+'/casual')
        if page is None :
            await client.send_message(message.channel,"Player NOT FOUND")
        soup = BeautifulSoup(page.text, 'html.parser')
        #last_links = soup.find(class_='widget-content stat')
        #last_links.decompose()
        stat_info = soup.find(class_='widget-content')
        #for stat in stat_info:
        #    stri = str(stat)

        stat_info = str(stat_info)
        stat_info = re.sub('<[^>]*>','',stat_info)

# RANKED STATS

        page = requests.get('http://paladins.guru/profile/pc/'+str(command[-1])+'/ranked')
        if page is None :
            await client.send_message(message.channel,"Player Not Found")
        soup = BeautifulSoup(page.text, 'html.parser')
        #last_links = soup.find(class_='widget-content stat')
        #last_links.decompose()
        rank_info = soup.find(class_='widget-content')
        #for stat in stat_info:
        #    stri = str(stat)

        rank_info = str(rank_info)
        rank_info = re.sub('<[^>]*>','',rank_info)

 # FINAL EMBED FOR PALADINS
        embed = discord.Embed(title="IKU IS HERE",description="Paladins Stats",color=0x00ff00)
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/pp-xC5yYk2XzwKQFkx5i5LXVdyo9H-oMO6ZdLdopC9QiuhK0NAarrNkfAzvmqaLwRcZ9=w300")
        embed.add_field(name="Player name",value=player_name,inline=True)
        embed.add_field(name="Global KDA",value=player_kda,inline=False)
        embed.add_field(name="Player Level",value=play_info,inline=True)
        embed.add_field(name="Summary",value=sum_info,inline=True)
        embed.add_field(name="Ranked",value=rank_info,inline=True)
        embed.add_field(name="Casual",value=stat_info,inline=True)
        embed.add_field(name="**More Info**",value="http://paladins.guru/",inline=True)
        await client.send_message(message.channel,embed=embed)



#Pubg Status

    if message.content.startswith(":pu"):
        command = str(message.content)
        command = command.split(" ")
        list_fort = []
        page = requests.get('https://masterpubg.com/profile/pc/'+str(command[-1]))
        if page is None :
            await client.send_message(message.channel,value="Player Not Found")
        soup = BeautifulSoup(page.text, 'html.parser')
        stat_info = soup.find('h1')
        stat_info = str(stat_info)
        name = re.sub('<[^>]*>','',stat_info)


        val = "data-mode-cards"
        stat_info = soup.find(class_='data-mode-cards')

            #for stat in stat_info:
            #    stri = str(stat)
        stat_info = str(stat_info)
        stat_info = re.sub('<[^>]*>','',stat_info)
        stat_info = stat_info.splitlines()
        stat_info = list(filter(None,stat_info))
        #stat_info.remove("(adsbygoogle = window.adsbygoogle || []).push({});")

        for items in stat_info :
            items = items.strip()
            list_fort.append(items)
        stat_info = list(filter(None,list_fort))



        squad_fpp = stat_info[0:36:]
        solo_fpp = list(stat_info[36:72:])
        duo_fpp = list(stat_info[72:108:])
        solo = list(stat_info[108::])



        def print_maker(stat_info):
            embed = discord.Embed(title="IKU IS HERE",description="PUB Stats",color=0x00ff00)
            embed.set_thumbnail(url="https://i-cdn.phonearena.com/images/article/100331-image/Check-out-the-official-trailer-for-PlayerUnknowns-Battlegrounds-mobile-version-PUBG-with-style.jpg")
            embed.add_field(name="Player name",value=name,inline=True)
            embed.add_field(name="Matches Played",value=stat_info[1],inline=True)
            embed.add_field(name="KDA",value=stat_info[2],inline=True)
            embed.add_field(name="Winrate",value=stat_info[4],inline=True)
            embed.add_field(name="Top 10",value=stat_info[6],inline=True)
            embed.add_field(name="Rating",value=stat_info[8],inline=True)
            embed.add_field(name="Rank",value=stat_info[10],inline=True)
            embed.add_field(name="Gmaes Played",value=stat_info[12],inline=True)
            embed.add_field(name="Wins",value=stat_info[14],inline=True)
            embed.add_field(name="Top 10s",value=stat_info[16],inline=True)
            embed.add_field(name="Most Kills",value=stat_info[18],inline=True)
            embed.add_field(name="Assists",value=stat_info[20],inline=True)
            embed.add_field(name="Total kills",value=stat_info[22],inline=True)
            embed.add_field(name="Headshot Kills",value=stat_info[24],inline=True)
            embed.add_field(name="Headshot KDA",value=stat_info[26],inline=True)
            embed.add_field(name="Time Survived",value=stat_info[28],inline=True)
            embed.add_field(name="Damage",value=stat_info[34],inline=True)
            embed.add_field(name = "**Find more**",value="https://masterpubg.com/",inline=True)
            return embed


    if message.content.startswith(":pu"):

        if message.content.startswith(":pusolo"):
            await client.send_message(message.channel,embed=print_maker(solo))

        elif message.content.startswith(":pusolof"):
            await client.send_message(message.channel,embed=print_maker(solo_fpp))

        elif message.content.startswith(":puuduof"):
            await client.send_message(message.channel,embed=print_maker(duo_fpp))

        elif message.content.startswith(":pusquadf"):
            await client.send_message(message.channel,embed=print_maker(squad_fpp))



        elif message.content.startswith(":pu"):
            stat_info = soup.find(class_='data-lifetime-stats widget widget-table')
            stat_info = str(stat_info)
            stat_info = re.sub('<[^>]*>','',stat_info)
            stat_info = stat_info.splitlines()
            stat_info = list(filter(None,stat_info))
            for items in stat_info :
                items = items.strip()
                list_fort.append(items)
            stat_info = list(filter(None,list_fort))
            embed = discord.Embed(title="IKU IS HERE",description="STATS OF PUBG",color=0x00ff00)
            embed.set_thumbnail(url="https://i-cdn.phonearena.com/images/article/100331-image/Check-out-the-official-trailer-for-PlayerUnknowns-Battlegrounds-mobile-version-PUBG-with-style.jpg")
            embed.add_field(name="Player name",value=name,inline=True)
            embed.add_field(name="Matches Played",value=stat_info[2],inline=True)
            embed.add_field(name="Total Kills",value=stat_info[6],inline=True)
            embed.add_field(name="Total Wins",value=stat_info[4],inline=True)
            embed.add_field(name="weapons Acquired",value=stat_info[18],inline=True)
            embed.add_field(name="Boosts",value=stat_info[16],inline=True)
            embed.add_field(name="Heals",value=stat_info[14],inline=True)
            embed.add_field(name="Revives",value=stat_info[12],inline=True)
            embed.add_field(name="Assists",value=stat_info[10],inline=True)
            embed.add_field(name="Headshot Kills",value=stat_info[8],inline=True)
            embed.add_field(name="Time Survived",value=stat_info[-1],inline=True)
            embed.add_field(name="Distance Travelled",value=stat_info[-3],inline=True)
            await client.send_message(message.channel,embed=embed)

# FORTNITE STATS
    if message.content.startswith(":fn"):

        command = str(message.content)
        command = command.split(" ")
        page = requests.get('https://fortnitestats.net/stats/'+str(command[-1]))
        if page is None :
            await client.send_message(message.channel,"Player Not Found")
        soup = BeautifulSoup(page.text, 'html.parser')
        name = soup.find('h1')
        name = str(name)
        name = re.sub('<[^>]*>','',name)

        def cleaner_fn(val):
            stat_info = soup.find(class_=val)
            stat_info = str(stat_info)
            stat_info = re.sub('<[^>]*>','',stat_info)
            stat_info = stat_info.splitlines()
            stat_info = list(filter(None,stat_info))
            return stat_info

        def print_maker(stat_info):
            embed = discord.Embed(title="IKU IS HERE",description="FORTNITE Stats",color=0x00ff00)
            embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/872808170225270784/_ccP8lTm_400x400.jpg")
            embed.add_field(name="Player name",value=name,inline=True)
            embed.add_field(name="Total Kills",value=stat_info[2],inline=True)
            embed.add_field(name="Overall KD",value=stat_info[4],inline=True)
            embed.add_field(name="Total Wins",value=stat_info[0],inline=True)
            embed.add_field(name="Top 5s",value=stat_info[6],inline=True)
            embed.add_field(name="Top 10s",value=stat_info[8],inline=True)
            embed.add_field(name="Top 25s",value=stat_info[10],inline=True)
            embed.add_field(name = "**Find more**",value="https://fortnitestats.net/",inline=True)
            return embed

        main_stat= 'main-stats'
        solo_stat = 'panel-body panel-main'
        duo_stat = 'panel panel-default stat-panel panel-duo'
        squad_stat = 'panel panel-default stat-panel panel-squad'
#FORTNITE Solo Status
        if message.content.startswith(":fns"):
                    val = solo_stat
                    stat_info = cleaner_fn(val)
                    await client.send_message(message.channel,embed=print_maker(stat_info))

#FORTNITE Duo Status
        elif message.content.startswith(":fnd"):
                    val = duo_stat
                    stat_info = cleaner_fn(val)
                    stat_info.pop(0)
                    await client.send_message(message.channel,embed=print_maker(stat_info))
#FORTNITE Squad STATS
        elif message.content.startswith(":fnsq"):
                    val = squad_stat
                    stat_info = cleaner_fn(val)
                    await client.send_message(message.channel,embed=print_maker(stat_info))

        elif message.content.startswith(":fn"):

                    val = main_stat
                    stat_info = cleaner_fn(val)
                    embed = discord.Embed(title="IKU IS HERE",description="FORTNITE Stats",color=0x00ff00)
                    embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/872808170225270784/_ccP8lTm_400x400.jpg")
                    embed.add_field(name="Player name",value=name,inline=True)
                    embed.add_field(name="Total Wins",value=stat_info[6],inline=True)
                    embed.add_field(name="Total Kills",value=stat_info[0],inline=False)
                    embed.add_field(name="Overall KD",value=stat_info[2],inline=True)
                    embed.add_field(name="Overall Winrate",value=stat_info[4],inline=True)
                    embed.add_field(name="Total Matches",value=stat_info[8],inline=True)
                    embed.add_field(name="Hours Played",value=stat_info[10],inline=True)
                    embed.add_field(name = "**Find more**",value="https://fortnitestats.net/",inline=True)
                    await client.send_message(message.channel,embed=embed)




client.run("****************** " ID " ***********************)
