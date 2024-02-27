import discord,json,tiktoken,openai,requests,sys
from discord.ext import commands
usage = None
model = None
# =============================================================================================================================================
# BOT SETUP
# 1. GO TO discord.pawan.krd and join the server
# 2. Verify (if you have to) and go to the channel "#bot"
# 3. Type in /key
# 4. Copy the key here
openai.api_key = "KEY FROM discord.pawan.krd"
# 5. Install discord.py, tiktoken and openai (python -m pip install discord tiktoken openai)
# 6. Go to the Discord Developer Portal and Generate a bot token
# 7. Enter the token below
discord_token = "TOKEN FROM DISCORD DEV PORTAL"
# 8. Uncomment one of the models with the usage below the instruction
# 9. Configure rest of the stuff, the comments are there to explain everything
# 10. Done!
# IMPORTANT! IF YOU GET ANY ERRORS WHEN GENERATING A RESPONSE, RUN /resetip IN THE #bot CHANNEL IN THE PAWAN SERVER YOU JOINED EARLIER
#
# Here you can change the model to:
# PAI-001-LIGHT - Generic model - Uses 0.25 credits per 1000 tokens - Max tokens = 16384
# model = "pai-001-light"
# usage = 0.25
#
# PAI-001-LIGHT-RP - Roleplay model - Uses 0.25 credits per 1000 tokens - Max tokens = 16384
# model = "pai-001-light-rp"
# usage = 0.25
#
# PAI-001 - Generic model - Uses 0.5 credits per 1000 tokens - Max tokens = 32768
# model = "pai-001"
# usage = 0.5
#
# PAI-001-RP - Roleplay model - Uses 0.5 credits per 1000 tokens - Max tokens = 32768
# model = "pai-001-rp"
# usage = 0.5
#
#
# Prefix for commands in the bot
command_prefix = "ai!"
#
# This is the max context, you get 250 credits daily, pai-001-light models use 0.25 credits per 1000, and pai-001 use 0.5 per 1000
max_context = 2000
#
# Amount of messages to get, if I were you, I would just set it to max_context / 200 or max_context / 150, maybe even max_context / 100
num_messages = int(round(max_context / 100))
#
# Length of response, one token is around 3-4 characters, so the max is around 400-500, I would recommend something like 200, depends on use case
response_length = 200
#
# If the bot should repeat more, but be more intelligent, or repeat less, but be less inteligent, the starting point is 0.7, play with it until
# you get the desired inteligence to repetition ratio
temperature = 0.7
#
# If you want to use a different model for chatting without context, enter it here as a string
nocontext_model = None
#
# If you want a different response length for chatting without context, enter it here as an integer
nocontext_response_length = None
#
# If you don't want the "status" command, change it to False.
status_command = True
# =============================================================================================================================================

openai.base_url = "https://api.pawan.krd/v1/"

enc = tiktoken.get_encoding("cl100k_base")
intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.remove_command('help')

# Load the channels into memory when the bot starts up
try:
    with open('channels.json', 'r') as f:
        channels = json.load(f)
except FileNotFoundError:
    channels = {}

def get_role(author) -> str:
    if author == bot.user:
        return "assistant"
    else:
        return "user"

if openai.api_key == None:
    print("You forgot to get the pawan API key, follow the instructions carefully or the bot won't work!")
    sys.exit()

if model == None:
    print("You forgot to uncomment the model below the instructions, the bot won't work without it!")
    sys.exit()

if usage == None:
    print("You forgot to uncomment the usage below the model, the bot won't work without it!")
    sys.exit()
    

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def chat(ctx, *args):
    if not args:
        await ctx.send("No message was provided.")
        return
    
    input = ' '.join(map(str, args))
    if nocontext_model != None:
        selected_model = nocontext_model
    else:
        selected_model = model

    if nocontext_response_length != None:
        actual_response_length = nocontext_response_length
    else:
        actual_response_length = response_length
    async with ctx.channel.typing():
        response = openai.chat.completions.create(
            model = selected_model,
            messages = [{"role": "user", "content": input}],
            temperature = temperature,
            max_tokens = actual_response_length,
            stream = False)
        await ctx.reply(response.choices[0].message.content[:2000])

@bot.command()
async def setchatbotchannel(ctx, channel: discord.TextChannel = None):
    global channels
    if channel is None:
        await ctx.send("No channel was provided.")
        return
    
    # Check if the user has the 'Manage Channels' permission
    if ctx.message.author.guild_permissions.manage_channels:
        # Get the server ID and the channel ID
        server_id = str(ctx.guild.id)
        channel_id = str(channel.id)

        # Load the current channels from the JSON file
        try:
            with open('channels.json', 'r') as f:
                channels = json.load(f)
        except FileNotFoundError:
            channels = {}

        # Update the channels for this server
        channels[server_id] = channel_id

        # Save the updated channels back to the JSON file
        with open('channels.json', 'w') as f:
            json.dump(channels, f)

        await ctx.send(f"Channel set to {channel.mention}")
    else:
        await ctx.send("You do not have the 'Manage Channels' permission.")

@bot.command()
async def status(ctx):
    if status_command:
        response = requests.get('https://api.pawan.krd/info', headers={'Authorization': openai.api_key})
        approx = response.json()['info']['credit']/(max_context*(usage/1000))
        await ctx.reply(f"Credits: `{response.json()['info']['credit']}` (approx. `{round(approx)}` interactions)")

@bot.command()
async def help(ctx):
    if not status_command:
        await ctx.reply(f"**AI Bot Help**\n```{command_prefix}help - You are here\n{command_prefix}chat [message] - Send a message to the bot```\n**Admin Commands**\n```{command_prefix}setchatbotchannel [channel] - Set a channel where the AI can chat```")
    else:
        await ctx.reply(f"**AI Bot Help**\n```{command_prefix}help - You are here\n{command_prefix}chat [message] - Send a message to the bot\n{command_prefix}status - Show remaining credits for today for the whole bot```\n**Admin Commands**\n```{command_prefix}setchatbotchannel [channel] - Set a channel where the AI can chat```")

@bot.event
async def on_message(msg):
    # Don't respond to our own messages
    if msg.author == bot.user:
        return

    # Check if the message was sent in the set channel for this server
    server_id = str(msg.guild.id)
    if server_id in channels and str(msg.channel.id) == channels[server_id]:
        limit = num_messages
        messages = [message async for message in msg.channel.history(limit=limit)]
        message_count = len(messages)
        list_of_messages = []
        for i in range(message_count):
            role = get_role(messages[message_count - i - 1].author)
            info = {"role": role, "content": messages[message_count - i - 1].content}
            list_of_messages.append(info)
        
        to_tokenize = list_of_messages.reverse()
        total_tokens = 0
        truncated_messages = []
        max_tokens = max_context
        for message in list_of_messages:
            tokens = list(enc.encode(str(message)))
            num_tokens = len(tokens)
            if total_tokens + num_tokens <= max_tokens:
                truncated_messages.append(message)
                total_tokens += num_tokens
            else:
                break

        truncated_messages.reverse()

        async with msg.channel.typing():
            response = openai.chat.completions.create(
                model = model,
                messages = truncated_messages,
                temperature = temperature,
                max_tokens = response_length,
                stream = False)
            await msg.reply(response.choices[0].message.content[:2000])
    else:
        await bot.process_commands(msg)

bot.run(discord_token)
