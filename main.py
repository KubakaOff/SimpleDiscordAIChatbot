import asyncio,discord,json,tiktoken,openai,requests
from discord.ext import commands
from config import *

enc = tiktoken.get_encoding("cl100k_base")
intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.remove_command('help')

# Load everything into memory
try:
    with open(channels_filename, 'r') as f:
        channels = json.load(f)
except FileNotFoundError:
    channels = {}

try:
    with open(prompts_filename, 'r') as f:
        prompts = json.load(f)
except FileNotFoundError:
    prompts = {}

def get_role(author) -> str:
    if author == bot.user:
        return "assistant"
    else:
        return "user"

async def generate_response(messages, temperature, max_tokens):
    return await openai.AsyncOpenAI(api_key=api_key, base_url=openai_base_url).chat.completions.create(
        model = model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens,
        stream = False)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def chat(ctx, *, args):
    global prompts
    if not args:
        await ctx.send("No input was provided.")
        return
    messages = []
    server_id = str(ctx.guild.id)

    if server_id in prompts:
        if "global" in prompts[server_id]:
            messages.append({"role": "system", "content": prompts[server_id]["global"]})

    messages.append({"role": "user", "content": args})
    async with ctx.channel.typing():
        response = await asyncio.wait_for(generate_response(messages, temperature, response_length), None)
        await ctx.reply(response.choices[0].message.content[:2000])
        
@bot.command()
async def chatbotchannel(ctx, channel: discord.TextChannel = None):
    global channels
    if channel is None:
        await ctx.send("No channel was provided.")
        return
    
    # Check if the user has the 'Manage Channels' permission
    if ctx.message.author.guild_permissions.manage_channels:
        # Get the server ID and the channel ID
        server_id = str(ctx.guild.id)
        channel_id = str(channel.id)

        if server_id not in channels:
            channels[server_id] = []

        if channel_id not in channels[server_id]:
            channels[server_id].append(channel_id)
            await ctx.send(f"Channel {channel.mention} added.")
        else:
            channels[server_id].remove(channel_id)
            await ctx.send(f"Channel {channel.mention} removed.")

        # Save the updated channels back to the JSON file
        with open(channels_filename, 'w') as f:
            json.dump(channels, f)

    else:
        await ctx.send("You do not have the 'Manage Channels' permission.")

@bot.command()
async def setprompt(ctx, *args):
    global prompts
    server_id = str(ctx.guild.id)
    channel_id = None
    args = list(args)
    if args[-1].startswith("<#") and args[-1].endswith(">"):
        channel_id = str(args[-1])
        channel_id = channel_id.replace("<", "").replace("#", "").replace(">", "")
        args.pop()
    input = ' '.join(map(str, args))
    if not args:
        ctx.send("Please include the prompt in your message.")
    if channel_id != None and ctx.message.author.guild_permissions.manage_channels:
        if server_id not in prompts:
            prompts[server_id] = {}
        
        prompts[server_id][channel_id] = input
        
        await ctx.send(f"Prompt set for channel <#{channel_id}>.")
        with open(prompts_filename, 'w') as f:
            json.dump(prompts, f)
    elif ctx.message.author.guild_permissions.manage_guild:
        if server_id not in prompts:
            prompts[server_id] = {}
        prompts[server_id]['global'] = input
        with open(prompts_filename, 'w') as f:
            json.dump(prompts, f)
        await ctx.send(f"Prompt set globally.")
    else:
        await ctx.send("Please make sure you have the `Manage Channels` permission when modifying a channel, or the `Manage Server` permission when modifying globally.")

@bot.command()
async def help(ctx): await ctx.reply(help_command)

@bot.event
async def on_message(msg):
    global channels
    if msg.author == bot.user: return

    server_id = str(msg.guild.id)
    if server_id in channels and str(msg.channel.id) in channels[server_id]:
        channel_id = str(msg.channel.id)
        limit = num_messages
        messages = [message async for message in msg.channel.history(limit=limit)]
        message_count = len(messages)
        list_of_messages = []

        for i in range(message_count):
            role = get_role(messages[message_count - i - 1].author)
            info = {"role": role, "content": messages[message_count - i - 1].content}
            list_of_messages.append(info)
        
        if server_id in prompts:
            if channel_id in prompts[server_id]:
                actual_prompt = prompts[server_id][channel_id]
            elif "global" in prompts[server_id]:
                actual_prompt = prompts[server_id]["global"]
        else:
            actual_prompt = prompt
        if actual_prompt != None: list_of_messages.append({"role": "system", "content": actual_prompt})
        
        list_of_messages.reverse()
        total_tokens = 0
        truncated_messages = []
        max_tokens = max_context
        for message in list_of_messages:
            tokens = list(enc.encode(str(message['content'])))
            num_tokens = len(tokens)
            if total_tokens + num_tokens <= max_tokens:
                truncated_messages.append(message)
                total_tokens += num_tokens
            else: break

        truncated_messages.reverse()
        if prompt != None:
            truncated_messages.pop()
            truncated_messages.insert(0, {"role": "system", "content": actual_prompt})
        
        async with msg.channel.typing():
            response = await asyncio.wait_for(generate_response(truncated_messages, temperature, response_length), None)
            await msg.reply(response.choices[0].message.content[:2000])
    else:
        await bot.process_commands(msg)

bot.run(discord_token)
