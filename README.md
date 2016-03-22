# telegramLoggerNetworkBot

Well, this is a bot that is "constantly" making maps (with some time before petitions), to see who is online in a local network and which ports has open. If a new ip is being used or another one stops being used, or if an known host closes or opens a port, it sends a message to your telegram conversation with the new info.

## How to use

- `git clone https://github.com/adanto/telegramLoggerNetworkBot.git & cd telegramLoggerNetworkBot`
- `touch log`
- Enter your bot api's in line 129 and conversation id in 130
- `python logger.py`
