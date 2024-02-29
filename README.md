# REWRITE DONE
## **For people that update from version older than from 29 Feb 2024:**
**Please delete the `channels.json` file in the directory same as `main.py`.**

# Simple Discord AI Chatbot
This Chatbot uses [Pawans](https://discord.pawan.krd) API to generate responses for free.

Running instance: https://discord.com/oauth2/authorize?client_id=921730426047954965&permissions=274881154048&scope=bot

The bot is really simple and customizable.

## Features:
- Context when running in a dedicated channel
- Asynchronous generation
- Option to run in dedicated channels (`ai!chatbotchannel (channel)`)
- Proper permissions
- API Key status for the whole bot (`ai!status`) (can be turned off in config.py)
- Enable roleplay mode for a channel, server, or the whole bot! (can be disabled in config) (`ai!switchmodel`)
- Custom prompts for a channel, server, or for the whole bot! (can be disabled in config) (`ai!setprompt`)
- Customizable (both by the server admins and the instance admin)
- Separate model and context length for chatting without context
- Token counter and token limiter

## Setup instructions:
1. Join [Pawan's Discord Server](https://discord.pawan.krd)
2. Verify (if you have to) and go to the channel "#bot"
3. Type in /key
4. Copy the key to config.py
5. Install py-cord, tiktoken and openai (`python -m pip install py-cord tiktoken openai`)
Note: You can also use discord.py, but i won't provide support since this bot is made for py-cord
6. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and generate a bot token
7. Copy the token to config.py
8. Uncomment one of the models in the config.py file
9. Configure rest of the stuff in the config.py, the comments are there to explain everything
10. Done!

**IMPORTANT! IF YOU GET ANY ERRORS WHEN GENERATING A RESPONSE, RUN /resetip IN THE #bot CHANNEL IN THE PAWAN SERVER YOU JOINED EARLIER**
