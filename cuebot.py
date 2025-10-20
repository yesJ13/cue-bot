import discord
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta

#__BOT SETUP__
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

#creating bot instance 
bot = commands.Bot(command_prefix='!', intents=intents)

stopwatch_starts = {} #dict stores stopwatch start times fro each users; key = user ID, start time

#__EVENTS__
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}.')
    print('Bot is ready for commands!')

#__COMMANDS__
#-stopwatch-
@bot.command(name='start', help='Starts a personal stopwatch.')
async def start_stopwatch(ctx):
    user_id = ctx.author.id
    if user_id in stopwatch_starts:
        await ctx/send("Stopwatch is already running...")
    else:
        stopwatch_starts[user_id] = datetime.now()
        await ctx.send(f"{ctx.author.mention}, stopwatch started! Use '!stop' to end.")

@bot.command(name='stop', help='Stops the personal stopwatch and shows elapsed time.')
async def stop_stopwatch(ctx):
    user_id = ctx.author.id
    if user_id not in stopwatch_starts:
        await ctx.send("You don't have a stopwatch running. Use '!start' to begin.")
    else:
        start_time = stopwatch_starts.pop(user_id)
        end_time = datetime.now()
        elapsed_time = end_time - start_time

        seconds = elapsed_time.total_seconds() #formatted timedelta object into readable string
        await ctx.send(f"{ctx.author.mention}, your stopwatch has been stopped! **Elapsed time: {seconds:.2f} seconds**.")

#-reminder-
@bot.command(name='remindme', aliases=['remind'], help='Sets a reminder. Usage: !remindme <time> <message>')
async def remind_me(ctx, time: str, *, message: str): #!reminder 10m check oven; supported time unit: s, m, h, d
    user = ctx.author
    time_unit = time[-1].lower()

    try:
        duration = int(time[:-1])
    except ValueError:
        await ctx.send("Invalid tiem fromat. Please use a number followed by 's', 'm', 'h', or 'd'.")
        return
    
    if time_unit == 's':
        seconds =  duration
    elif time_unit == 'm':
        seconds = duration * 60
    elif time_unit == 'h':
        seconds = duration * 3600
    elif time_unit == 'd':
        seconds = duration * 86400
    else:
        await ctx.send("Invalid time unit. Please use 's', 'm', 'h', or 'd'.")
        return
    
    await asyncio.sleep(seconds) #wait for the specified duration

    await ctx.send(f"🕰️ Reminder for {user.mention}! You asked me to remind you about: **'{message}'**") #sends reminder

#-timer-
@bot.command(name='timer', help='Sets a timer. Usage: !timer <time> [title]')
async def timer(ctx, time: str, *, title: str = "Timer"): #same as reminder
    user = ctx.author
    time_unit = time[-1].lower()

    try:
        duration = int(time[:-1])
    except ValueError:
        await ctx.send("Invalid time format. Please use 's', 'm', or 'h'.")
        return
    
    if time_unit == 's':
        seconds =  duration
    elif time_unit == 'm':
        seconds = duration * 60
    elif time_unit == 'h':
        seconds = duration * 3600
    else:
        await ctx.send("Invalid time unit. Please use 's', 'm', 'h', or 'd'.")
        return
    
    await ctx.send(f"✅ Okay, {user.mention}! Your timer for **'{title}'** is set for {duration}{time_unit}.")

    await asyncio.sleep(seconds) #wait for the specified diration

    await ctx.send(f"⌛ **Time's up!! {user.mention}!**")


#__RUN THE CUE BOT__
bot.run('os.getenv('DISCORD_TOKEN')')
