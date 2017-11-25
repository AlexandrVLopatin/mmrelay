# MMRelay

It's just and example how to handle [Mattermost](https://mattermost.com) WebSocket [events](https://api.mattermost.com/#tag/WebSocket) and relay them to your backend.

## Requirements:
python 3.5+

## Installation:
```bash
git clone https://github.com/AlexandrVLopatin/mmrelay.git
cd mmrelay
pip install -r requirements.txt
```

## Configuration
There are several options defined by consts in `mmreplay.py`:

* `MM_URL`: Mattermost API endpoint
* `MM_WSURL`: Mattermost WebSocket endpoint
* `MM_LOGIN`: Mattermost admin username
* `MM_PASSWORD`: Mattermost admin password
* `CALLBACK_URL`: Your API endpoint
* `CALLBACK_TIMEOUT`: Your API request timeout
