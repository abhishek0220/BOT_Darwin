import os
#BOT TOKEN
try:
    botToken = os.environ['TOKEN']
    meme_hook = os.environ['webhook']
except:
    f = open("token.txt","r")
    botToken = f.readline().rstrip()
    meme_hook = f.readline().rstrip()
    f.close()
#DISCORD CHANNELS
channels={}
channels["#general"] = "664156473944834082" 
channels["#core"] = "664156536821776384"  
channels["#bot_testing"] = "690605490123571320"
channels["#bot-functionalities"] = "690616698675527782"
channels["#memes"] = "721268921692323851"

insults_arr = []
abuse_mode = False

author = "690599381304606741" #this id can be obtained from DM channel link

#libraries
import discord
import time
import urllib.request
import codecs
import csv
import requests 
import random
from discord.ext import commands
from discord.ext.commands import CommandNotFound


bot = commands.Bot(
        command_prefix='$Darwin ',
        description='Coding Club IIT Jammu Discord BOT',
        case_insensitive=True    
    )
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    with open('assets/insults.txt', 'r') as file:
        for line in file:
            insults_arr.append(line)
    print('--list loaded----')

@bot.command()
async def greet(ctx):   #basic command to greet
    await ctx.send(":smiley: :wave: Hello, I am Darwin...")

@bot.command()
async def about(ctx):   #About command
    msg = "I am **Darwin v1.0** Coding Club IIT Jammu`s Discord BOT.\n $Darwin member abc : to get details of members name starting with abc.\n $Darwin post <channel> <msg> : to post message as bot in specified channel.\n $Darwin events : To find details about upcoming events.\n Currently Supported Command"
    await ctx.send(msg)

@bot.command()
async def post(ctx, a : str , b: str):  #command to post to specific channel
    channelspermited = [channels["#core"], channels["#bot_testing"]]
    #in case developer needs to communicate directely
    if(str(ctx.message.channel.id) == author):
        if(a in channels):
            channel = bot.get_channel(int(channels[a]))
            await channel.send(b)
            print("Msg posted from author")
    elif(str(ctx.message.channel.id) in channelspermited):
        ch_code = a[2:-1]
        channel = bot.get_channel(int(ch_code))
        await channel.send(b)
        print("Msg posted from coreteam")
    else:
        await ctx.send("Sorry you can`t use this command:rolling_eyes:.")

@bot.command()
async def member(ctx, a: str):
    channelspermited = [author, channels["#core"], channels["#bot_testing"], channels["#bot-functionalities"]]
    if(str(ctx.message.channel.id) not in channelspermited):
        await ctx.send("Sorry you can`t use this command:rolling_eyes:.")
        return
    if(len(a)<3):
        await ctx.send("Oops:confused: pls send minimum 3 letters.")
        return
    match = a.upper()
    found = set()
    with open('assets/members.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            name = row[0]
            name = name[0:len(match)]
            if(name.upper() == match):
                tem = (row[0], row[1].lower(), row[3])
                found.add(tem)
    output = "Found "+str(len(found))+" Students\n\n"
    for i in found:
        na = "**Name** : "+i[0]
        em = "**Email** : "+i[1]
        opt = "**Deparment** : "+i[2]
        tem = na+"\n"+em+"\n"+opt+"\n"
        output = output + tem + "\n"
    await ctx.send(output)

@bot.command()
async def dep_members(ctx, a: str):
    channelspermited = [author, channels["#core"], channels["#bot_testing"], channels["#bot-functionalities"]]
    if(str(ctx.message.channel.id) not in channelspermited):
        await ctx.send("Sorry you can`t use this command:rolling_eyes:.")
        return
    if(len(a)<3):
        await ctx.send("Oops:confused: Department code must be of 3 letters.")
        return
    match = a.upper()
    found = {}
    with open('assets/members.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            dep_code = row[1]
            dep_code = dep_code[4:7]
            if(dep_code.upper() == match):
                year = row[1]
                name = row[0]
                found[name] = year[:4]

    no_stu_found = len(found)
    output = "Found {} Students in {} branch\n\n".format(no_stu_found, a.upper())
    i = 1
    for name, year in found.items():
        opt = str(i) + ". " + str(name) + ' ' +str(year)
        #opt = "{}. {}".format((i+1), found[i]) 
        i += 1
        output = output + opt + "\n"
    await ctx.send(output)


@bot.command()
async def events(ctx):
    event_list = []
    with open('assets/upcoming_events.csv', 'r') as file:
        csvfile = csv.reader(file)
        i = 0
        for line in csvfile:
            if(i == 0):
                header = line
                i +=1
                continue
            event_list.append(line)
    output = "Found "+str(len(event_list))+" Events\n\n"
    for i in event_list:
        tem = ""
        for j in range(len(header)):
            tem = tem + "**" + header[j] + "** : " + i[j] + "\n"
        output = output + tem + "\n"
    await ctx.send(output)

@bot.command()
async def Corona(ctx):
    URL = "https://corona.lmao.ninja/v2/countries/India"
    r = requests.get(url = URL) 
    data = r.json() 
    da = ['country','cases','todayCases','deaths','todayDeaths','recovered','active','critical','casesPerOneMillion','testsPerOneMillion']
    out = ""
    for i in da:
        out = out + i + " : " + str(data[i])+"\n"
    time_got = int(data['updated'])//1000 + 19800
    curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_got))
    last_updated = "\nLast Updated : " + curr_time
    out = out + last_updated
    out = out + "\nSource: NovelCOVID API"
    await ctx.send(out)

@bot.command()
async def abuse(ctx, val):
    global abuse_mode
    channelspermited = [author, channels["#core"], channels["#bot_testing"]]
    if(str(ctx.message.channel.id) not in channelspermited):
        await ctx.send("Sorry you can`t use this command:rolling_eyes:.")
        return
    if(val == '1'):
        abuse_mode = True
    else:
        abuse_mode = False
    out = "Updated abuse mode to " + str(abuse_mode)
    await ctx.send(out)

#API taken from Advice Slip JSON API website https://api.adviceslip.com/
@bot.command()
async def advice(ctx):
    URL = "https://api.adviceslip.com/advice" 
    r = requests.get(url = URL) 
    data = r.json() 
    out = data['slip']['advice']
    await ctx.send(out)

@bot.command()
@commands.cooldown(1, 30, commands.BucketType.guild)
async def titan(ctx):
    channelspermited = [author, channels["#memes"]]
    if(str(ctx.message.channel.id) not in channelspermited):
        await ctx.send("Sorry you can`t use this command here:rolling_eyes:.")
        return
    data = {
        "webhook" : meme_hook
    }
    URL = "http://discord-meme.azurewebsites.net/api/sendmeme?code=fOozheVSUeip5uq36nNaJtTyoYABhYQ42nWqLIa8g763XeAcUQ3xEw=="
    r = requests.post(url = URL, json= data) 


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = 'This command is ratelimited, please try again in {:.2f}s'.format(error.retry_after)
        await ctx.send(msg)
    if isinstance(error, CommandNotFound):
        user_m = '{0.author.mention} '.format(ctx)
        if(abuse_mode):
            if(user_m.strip() == "<@664161180121825301>"):
                msg_s = "Sorry sir, you haven`t developed that feature."
            else:
                msg_s = random.choice(insults_arr)
        else:
            msg_s = "Invalid Command"
        msg_s = user_m + msg_s
        await ctx.send(msg_s)
    else:
        raise error
bot.run(botToken)
