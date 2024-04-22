# BOT SETUP
# 1. Go to console.groq.com and get an API key.
api_key = "KEY FROM console.groq.com"
# 2. Install py-cord, tiktoken and openai (python -m pip install py-cord tiktoken openai)
# 3. Go to the Discord Developer Portal and Generate a bot token
# 4. Enter the token below
discord_token = "TOKEN FROM DISCORD DEV PORTAL"
# 5. Uncomment one of the models with the usage below the instruction
# 6. Configure rest of the stuff, the comments are there to explain everything
# 7. Done!
# IMPORTANT! IF YOU GET ANY ERRORS WHEN GENERATING A RESPONSE, RUN /resetip IN THE #bot CHANNEL IN THE PAWAN SERVER YOU JOINED EARLIER
#
# Prefix for commands in the bot
command_prefix = "ai!"
#
# If you don't want to use Groq cloud, change this to the OpenAI compatible base_url you want.
openai_base_url = "https://api.groq.com/openai/v1"
#
# Enter the default model you want to use here.
model = "llama3-70b-8192"
# Enter models you want to allow usage of (NOT DONE YET)
# Billing limit is tokens per month (in tokens)
# The settings below are PER MODEL
# None: fallback to global values
# actual_model = Actual model used to generate the response. Can be set to None.
allowed_models = {"llama3-70b-8192": {"actual_model": None, "prompt": None, "max_context": 8192, "billing_limit": None, "default_temperature": None, "response_length": None}, 
                  "llama3-8b-8192": {"actual_model": None, "prompt": None, "max_context": 8192, "billing_limit": None, "default_temperature": None, "response_length": None}, 
                  "llama2-70b-4096": {"actual_model": None, "prompt": None, "max_context": 4096, "billing_limit": None, "default_temperature": None, "response_length": None}, 
                  "mixtral-8x7b-32768": {"actual_model": None, "prompt": None, "max_context": 32768, "billing_limit": None, "default_temperature": None, "response_length": None}, 
                  "gemma-7b-it": {"actual_model": None, "prompt": None, "max_context": 8192, "billing_limit": None, "default_temperature": None, "response_length": None},
                 }
# Use as much as you can afford (and as much as the model supports)
max_context = 8192
# Length of response, one token is around 3-4 characters, so the max is around 500-600, I would recommend something like 200, depends on use case
response_length = 600
#
#
# Prompt for the AI to follow (as system message). Set to None for no prompt
prompt = None
#
# Do you want to enable the stats command? (COMING SOON)
stats = True
#
# Prompt for the AI to follow without context (as system message). Set to None, prompt or a string.
nocontext_prompt = prompt
#
# Can server admins/mods change the prompts for their server?
prompt_change = True
#
#
# Amount of messages to get, if I were you, I would just set it to max_context / 200 or max_context / 150, maybe even max_context / 100
num_messages = int(round(max_context / 250))
#
# If the bot should repeat more, but be more intelligent, or repeat less, but be less inteligent, the starting point is 0.7, play with it until
# you get the desired intelligence to repetition ratio
temperature = 0.7
#
# If you want a different response length for chatting without context, enter it here as an integer
nocontext_response_length = None
#
# If the bot is repeating itself with context, you should set the normal temperature higher, and this one lower
# Keep in mind that it will make the bot less "intelligent".
nocontext_temperature = None
#
# Filenames/paths for saving settings:
channels_filename = "channels.json"
prompts_filename = "prompts.json"
# COMING SOON
temperature_filename = "temperature.json"
models_filename = "models.json"
#
# Help commands contents:
help_command = f"""
**AI Bot Help**
```{command_prefix}help - You are here
{command_prefix}chat [message] - Send a message to the bot```
**Admin Commands**
```{command_prefix}chatbotchannel [channel] - Add/remove a channel where the AI can chat.
{command_prefix}setprompt [prompt] (channel) - Set prompt to prompt for the whole server or only for one channel.```

You can host your own AI Discord Bot from here: https://github.com/KubakaOff/SimpleDiscordAIChatbot
You can also [add the main instance to your own Discord server](https://discord.com/oauth2/authorize?client_id=921730426047954965&permissions=274881154048&scope=bot)
"""
