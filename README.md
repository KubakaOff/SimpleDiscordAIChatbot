# REWRITE DONE
## **For people that update from version older than from 29 Feb 2024:**
**Please delete the `channels.json` file in the directory same as `main.py`.**

Last `config.py` change: 20 April 2024

# Simple Discord AI Chatbot
This Chatbot uses [Groq](https://console.groq.com) API to generate responses.

If you want an always free AI, use the [pawan](https://github.com/KubakaOff/SimpleDiscordAIChatbot/tree/pawan) branch.

Running instance: https://discord.com/oauth2/authorize?client_id=921730426047954965&permissions=274881154048&scope=bot (running on the [pawan](https://github.com/KubakaOff/SimpleDiscordAIChatbot/tree/pawan) branch)

The bot is really simple and customizable.

## Features:
- Context when running in a dedicated channel
- Asynchronous generation
- Option to run in dedicated channels (`ai!chatbotchannel (channel)`)
- Proper permissions
- Custom prompts for a channel, server, or for the whole bot! (can be disabled in config) (`ai!setprompt`)
- Customizable (both by the server admins and the instance admin)
- Separate model and context length for chatting without context
- Token counter and token limiter

### Setup instructions:
1. Get a [Groq key](https://console.groq.com/keys)
2. Copy the key to config.py
3. Install py-cord, tiktoken and openai (`python -m pip install py-cord tiktoken openai`)
Note: You can also use discord.py, but i won't provide support since this bot is made for py-cord
4. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and generate a bot token
5. Copy the token to config.py
6. Uncomment one of the models in the config.py file
7. Configure rest of the stuff in the config.py, the comments are there to explain everything
8. Done!

### FAQ

**Q:** I want to use Pawan instead

**A:** Use the [pawan](https://github.com/KubakaOff/SimpleDiscordAIChatbot/tree/pawan) branch.
