# telegram-msg

Interactively sends messages (or optionally an image) to a specified group in Telegram.

Copyright (C) 2020 Denis Meyer

## Prerequisites

* Python 3
* Windows
  * Add Python to PATH variable in environment

## TODO before using

* Create a token
** https://t.me/botfather ( https://core.telegram.org/bots#6-botfather )
* Get chat ID
** Add the Telegram bot to the group
** Get the list of updates for your BOT: https://api.telegram.org/bot<botToken>/getUpdates
** Look for the "chat" object
* Fill in the token and chat ID in Main.py

## Usage

* Start shell
  * Windows
    * Start shell as administrator
    * `Set-ExecutionPolicy Unrestricted -Force`
* Create a virtual environment
  * `python -m venv venv`
* Activate the virtual environment
  * Mac/Linux
    * `source venv/bin/activate`
  * Windows
    * `.\venv\scripts\activate`
* Install the required libraries
  * `pip install -r requirements.txt`
* Run the app
  * `python Main.py`
