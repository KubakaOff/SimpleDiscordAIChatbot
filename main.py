import asyncio,discord,json,tiktoken,openai,requests
from discord.ext import commands
from config import *

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

async def generate_response(model, messages, temperature, max_tokens):
    return await openai.AsyncOpenAI(api_key=openai_api_key, base_url=openai_base_url).chat.completions.create(
        model = model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens,
        stream = False)

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

    messages = [{"role": "user", "content": input}]
    async with ctx.channel.typing():
        response = await asyncio.wait_for(generate_response(selected_model, messages, temperature, actual_response_length), None)
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
        response = requests.get('https://api.pawan.krd/info', headers={'Authorization': openai_api_key})
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
            response = await asyncio.wait_for(generate_response(model, truncated_messages, temperature, response_length), None)
            await msg.reply(response.choices[0].message.content[:2000])
    else:
        await bot.process_commands(msg)

bot.run(discord_token)
