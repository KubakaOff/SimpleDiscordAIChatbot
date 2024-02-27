# BOT SETUP
# 1. GO TO discord.pawan.krd and join the server
# 2. Verify (if you have to) and go to the channel "#bot"
# 3. Type in /key
# 4. Copy the key here
openai_api_key = "KEY FROM discord.pawan.krd"
# 5. Install discord.py, tiktoken and openai (python -m pip install discord tiktoken openai)
# 6. Go to the Discord Developer Portal and Generate a bot token
# 7. Enter the token below
discord_token = "TOKEN FROM DISCORD DEV PORTAL"
#
# ====================================================================
# MAKE SURE TO DO THIS ONE CORRECTLY
# 
# 8. Uncomment one of the models with the usage below the instruction 
# ====================================================================
#
# 9. Configure rest of the stuff, the comments are there to explain everything
# 10. Done!
# IMPORTANT! IF YOU GET ANY ERRORS WHEN GENERATING A RESPONSE, RUN /resetip IN THE #bot CHANNEL IN THE PAWAN SERVER YOU JOINED EARLIER
#
# Here you can change the model to (comment the current model and usage and uncomment the new model and usage to change it):
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
response_length = 250
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
#
# If you don't want to use Pawans API, change this to the base_url you want, and set "status_command" to False
openai_base_url = "https://api.pawan.krd/v1/"
