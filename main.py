import asyncio
import discord
import json
import openai
import requests
from discord.ext import commands
from config import *
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=command_prefix, intents=intents)
bot.remove_command('help')

# Load channels and prompts
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

channels = load_data(channels_filename)
prompts = load_data(prompts_filename)

def get_role(author):
    return "assistant" if author == bot.user else "user"

async def generate_response(messages, temperature, max_tokens):
    return await openai.AsyncOpenAI(api_key=api_key, base_url=openai_base_url).chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def chat(ctx, *, args):
    if not args:
        await ctx.send("No input was provided.")
        return

    messages = [{"role": "user", "content": args}]
    server_id = str(ctx.guild.id)

    if server_id in prompts.get(server_id, {}):
        messages.insert(0, {"role": "system", "content": prompts[server_id]["global"]})

    async with ctx.channel.typing():
        response = await asyncio.wait_for(generate_response(messages, temperature, response_length), None)
        await ctx.reply(response.choices[0].message.content[:2000])

@bot.command()
async def chatbotchannel(ctx, channel: discord.TextChannel = None):
    if channel is None:
        await ctx.send("No channel was provided.")
        return

    if ctx.message.author.guild_permissions.manage_channels:
        server_id = str(ctx.guild.id)
        channel_id = str(channel.id)

        channels.setdefault(server_id, [])
        channels[server_id] = list(set(channels[server_id]))  # Remove duplicates

        if channel_id not in channels[server_id]:
            channels[server_id].append(channel_id)
            await ctx.send(f"Channel {channel.mention} added.")
        else:
            channels[server_id].remove(channel_id)
            await ctx.send(f"Channel {channel.mention} removed.")

        with open(channels_filename, 'w') as f:
            json.dump(channels, f)
    else:
        await ctx.send("You do not have the 'Manage Channels' permission.")

@bot.command()
async def setprompt(ctx, *args):
    server_id = str(ctx.guild.id)
    channel_id = None
    args = list(args)

    if args and args[-1].startswith("<#") and args[-1].endswith(">"):
        channel_id = args[-1].strip("<#>")
        args.pop()

    input_prompt = ' '.join(args)

    if not input_prompt:
        ctx.send("Please include the prompt in your message.")
        return

    if channel_id and ctx.message.author.guild_permissions.manage_channels:
        prompts.setdefault(server_id, {})
        prompts[server_id][channel_id] = input_prompt
        await ctx.send(f"Prompt set for channel <#{channel_id}>.")
    elif ctx.message.author.guild_permissions.manage_guild:
        prompts.setdefault(server_id, {})
        prompts[server_id]['global'] = input_prompt
        await ctx.send(f"Prompt set globally.")
    else:
        await ctx.send("Please make sure you have the `Manage Channels` permission when modifying a channel, or the `Manage Server` permission when modifying globally.")

    with open(prompts_filename, 'w') as f:
        json.dump(prompts, f)

@bot.command()
async def help(ctx):
    await ctx.reply(help_command)

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return

    server_id = str(msg.guild.id)
    if server_id in channels and str(msg.channel.id) in channels[server_id]:
        limit = num_messages
        messages = [message async for message in msg.channel.history(limit=limit)]

        list_of_messages = []
        for message in reversed(messages):
            role = get_role(message.author)
            list_of_messages.append({"role": role, "content": message.content})

        actual_prompt = prompts.get(server_id, {}).get(str(msg.channel.id)) or prompts.get(server_id, {}).get('global')

        if actual_prompt:
            list_of_messages.append({"role": "system", "content": actual_prompt})

        total_tokens = 0
        truncated_messages = []
        max_tokens = max_context
        for message in list_of_messages:
            tokens = list(enc.encode(str(message['content'])))
            num_tokens = len(tokens)
            if total_tokens + num_tokens <= max_tokens:
                truncated_messages.append(message)
                total_tokens += num_tokens
            else:
                break

        if prompt:
            truncated_messages.pop()
            truncated_messages.insert(0, {"role": "system", "content": actual_prompt})

        async with msg.channel.typing():
            response = await asyncio.wait_for(generate_response(truncated_messages, temperature, response_length), None)
            await msg.reply(response.choices[0].message.content[:2000])
    else:
        await bot.process_commands(msg)

bot.run(discord_token)
