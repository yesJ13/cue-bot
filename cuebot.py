import os
import discord
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta
import json

#__BOT SETUP__
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

#creating bot instance 
bot = commands.Bot(command_prefix='!', intents=intents)

stopwatch_starts = {} #dict stores stopwatch start times fro each users; key = user ID, start time

#--To-Do List--
TODO_FILE = "todo_lists.json"

def load_todos(): #loads to-do lists from a JSON file
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} #if file is empty or corrupt, return a new dict
    return {} #if file doesn't exist, return a new dict

def save_todos(data): #saves data to the to-do JSON file
    with open(TODO_FILE, 'w') as f:
        json.dump(data, f, indent=4)

todo_lists = load_todos() #;oad todo lists on startup; use str(user_id) as JSON key        


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

#-to do-
@bot.group(name='todo', invoke_without_command= True, help="Shows your to-do lists. Use !todo add <task> to add.")
async def todo(ctx):
    user_id = str(ctx.author.id)
    if user_id not in todo_lists or not todo_lists[user_id]:
        await ctx.send(f"{ctx.author.mention}, your to-do list is empty! Add taks with `!todo add <task>`.")
        return
    
    embed = discord.Embed(title=f"📝{ctx.author.mention}'s To-Do List", color=discord.Color.blue())
    task_list = ""
    for i, item in enumerate(todo_lists[user_id]):
        status = "✅" if item["done"] else "☐"
        task_list += f"**{i + 1}.** {status} {item['task']}\n"

    embed.description = task_list
    embed.set_footer(text="Use `!todo done <number>` to check off a task.")
    await ctx.send(embed=embed)

@todo.command(name='add', help="Adds a new task to your to-do list. Usage: !todo add <task>")
async def add_task(ctx, *, task: str): #adds a task to the user's list
    user_id = str(ctx.author.id) 
    if user_id not in todo_lists:
        todo_lists[user_id] = []
    
    todo_lists[user_id].append({"task": task, "done": False})
    save_todos(todo_lists) #saves to file
    await ctx.send(f"✅ {ctx.author.mention}, added task: **'{task}'**")

@todo.command(name='done', aliases=['complete', 'check'], help="Marks a task as complete. Usage: !tdod done <task number>")
async def done_task(ctx, task_number: int): #marks a task as done
    user_id = str(ctx.author.id)

    if user_id not in todo_lists or not todo_lists[user_id]:
        await ctx.send(f"{ctx.author.mention}, your to-to list is empty.")
        return
    
    try: 
        task_index = task_number - 1
        if 0 <= task_index < len(todo_lists[user_id]):
            if todo_lists[user_id][task_index]["done"]:
                await ctx.send(f"{ctx.author.mention}, task **{tassk_number}** is already marked as done.")
            else:
                todo_lists[user_id][task_index]["done"] = True
                save_todos(todo_lists) #save to file
                await ctx.send(f"✅{ctx.author.mention}, marked tass **{task_number}** as complete!")
        else:
            await ctx.send(f"{ctx.author.mention}, invalid task number. YOu have {len(todo_lists[user_id])} tasks.")
    except ValueError:
        await ctx.send("Please provid a valid task number.")

@todo.command(name='remove', aliases=['rm', 'del'], help='Removes a task from your list. Usage: !todo remove <task number>')
async def remove_task(ctx, task_number: int): #removes a task from the list
    user_id = str(ctx.author.id)

    if user_id not in todo_lists or not todo_lists[user_id]:
        await ctx.send(f"{ctx.author.mention}, your to-do list is empty.")
        return

    try:
        task_index = task_number - 1
        if 0 <= task_index < len(todo_lists[user_id]):
            removed_task = todo_lists[user_id].pop(task_index)
            save_todos(todo_lists) # Save to file
            await ctx.send(f"🗑️ {ctx.author.mention}, removed task: **'{removed_task['task']}'**")
        else:
            await ctx.send(f"{ctx.author.mention}, invalid task number.")
    except ValueError:
        await ctx.send("Please provide a valid task number.")

@todo.command(name='clear', help='Clears your entire to-do list.')
async def clear_tasks(ctx): #clear all task for the user
    user_id = str(ctx.author.id)
    if user_id in todo_lists and todo_lists[user_id]:
        todo_lists[user_id] = []
        save_todos(todo_lists)
        await ctx.send(f"✨ {ctx.author.mention}, your to-do list has been cleared!")
    else:
        await ctx.send(f"{ctx.author.mention}, your to-do list is already empty.")


#__RUN THE CUE BOT__
bot.run('os.getenv('DISCORD_TOKEN')')
