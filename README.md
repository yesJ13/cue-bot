# Cue Bot - Discord bot

Cue Bot features:
1. ⏱Stopwatch
2. ⌛Timer
3. 🕒Reminder
4. ✅To-do List

You can run the file locally with Discord Token.

## Run your own Instance

### 1. Prerequisites

* [Python 3.10+](https://www.python.org/downloads).
* Discord account and server you have admin rights.

### 2.  Setup

1. **Clone or Download the Respository**

2. **Create the Discord Bot**
   - Got to the [*Discord Developer Portal*](https://discord.com/developers/applications).
   - Create a *New Application* and give it a name.
   - Go to the **Bot** tab and click on *'Add Bot'*.
   - In **'Token'** click on ***Reset Token***. Copy the token and save it secret.
   - Scroll down to **'Privileged Gateway Intents'** and *enable* both **SERVER MEMBER INTENT** and **MESSAGE CONTENT INTENT**.

3. **Install Dependencies**
   Open terminal in the project folder. Run:
   ```bash
      pip install -r requirements.txt
   ```

   Install dicord depenedencies if not. Run:
   ```bash
      pip install discord.py
   ```

4. **Set Your Bot Token**
   * **Windows (Command Prompt):** `set DISCORD_TOKEN=YOUR_TOKEN_HERE` .
    * **Windows (PowerShell):** `$env:DISCORD_TOKEN = "YOUR_TOKEN_HERE"` .
    * **macOS/Linux:** `export DISCORD_TOKEN="YOUR_TOKEN_HERE"` .

    *(Alternatively, for testing only, you can replace `os.getenv('DISCORD_TOKEN')` at the bottom of `cuebot.py` with your actual token in quotes.)*

5. **Run the Bot**
   ```bash
      python FILE_NAME.py
   ```

### 3. Invite the Bot to Your Server

- In the [*Discord Developer Portal*](https://discord.com/developers/applications), go to **'OAuth2'** -> **'OAuth2 URL Generator'**.
- Under **'bot' Scopes**, select checkboxes for:
  - Read Messages
  - Send Messages
  - Embed Links
- Copy the url from **'Generate URL'**. Paste it into your browswer and select the server in discord to add the bot.

### 4. Command List

#### Stopwatch
* `!start` : Starts your personal time.
* `!stop` : Stops your stop watch and shows the elapsed time.

#### TImer
* `!timer <time> [title]`
    - egs:- `!timer 5m` or `!timer 20m Team is ready`.

#### Reminder
* `!remindme <time> <message>`
    - egs:- `!remindme 2h Check on member roles` - must mention <'message'>.

#### To-do
* `!todo` : Shows your current to-do list.
* `!todo add <task>` : Adds a new task.
* `!todo done <task_number>` : Marks a task as complete.
* `!todo remove <task_number>` : Deletes a task.
* `!todo clear` : Clear the entire list.
____
