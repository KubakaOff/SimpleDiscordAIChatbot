# BOT SETUP
# 1. GO TO discord.pawan.krd and join the server
# 2. Verify (if you have to) and go to the channel "#bot"
# 3. Type in /key
# 4. Copy the key here
api_key = "KEY FROM groqcloud.com"
# 5. Install py-cord, tiktoken and openai (python -m pip install py-cord tiktoken openai)
# 6. Go to the Discord Developer Portal and Generate a bot token
# 7. Enter the token below
discord_token = "TOKEN FROM DISCORD DEV PORTAL"
# 8. Uncomment one of the models with the usage below the instruction
# 9. Configure rest of the stuff, the comments are there to explain everything
# 10. Done!
# IMPORTANT! IF YOU GET ANY ERRORS WHEN GENERATING A RESPONSE, RUN /resetip IN THE #bot CHANNEL IN THE PAWAN SERVER YOU JOINED EARLIER
#
# Do you want to show the currently used model when running the "status" command?
show_currently_used_model = True
# Prefix for commands in the bot
command_prefix = "ai!"
#
#
# Prompt for the AI to follow (as system message). Set to None for no prompt
prompt = None
#
# Prompt for the AI to follow without context (as system message). Set to None, prompt or a string.
nocontext_prompt = prompt
#
# Can server admins/mods change the prompts for their server?
prompt_change = True
#
# This is the max context, you get 250 credits daily, pai-001-light models use 0.25 credits per 1000, and pai-001 use 0.5 per 1000
max_context = 8000
#
# Amount of messages to get, if I were you, I would just set it to max_context / 200 or max_context / 150, maybe even max_context / 100
num_messages = int(round(max_context / 100))
#
# Length of response, one token is around 3-4 characters, so the max is around 500-600, I would recommend something like 200, depends on use case
response_length = 2000
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
# If the bot is repeating itself with context, you should set the normal temperature higher, and this one lower
# Keep in mind that it will make the bot less "intelligent".
nocontext_temperature = None
#
# If you don't want the "status" command, change it to False.
status_command = True
#
# If you don't want to use Pawans API, change this to the base_url you want, and set "status_command" to False
openai_base_url = "https://api.groq.com/openai/v1"
#
# Filenames/paths for saving settings:
channels_filename = "channels.json"
variants_filename = "variants.json"
prompts_filename = "prompts.json"
#
# Help commands contents:
help_command = f"""
**AI Bot Help**
```{command_prefix}help - You are here
{command_prefix}chat [message] - Send a message to the bot
{command_prefix}status - Show remaining credits for today for the whole bot```
**Admin Commands**
```{command_prefix}chatbotchannel [channel] - Add/remove a channel where the AI can chat.
{command_prefix}switchmodel (channel) - Switch to/from roleplay to generic models.
{command_prefix}setprompt [prompt] (channel) - Set prompt to prompt for the whole server or only for one channel.```

You can host your own AI Discord Bot from here: https://github.com/KubakaOff/SimpleDiscordAIChatbot
You can also [add the main instance to your own Discord server](https://discord.com/oauth2/authorize?client_id=921730426047954965&permissions=274881154048&scope=bot)!
"""
