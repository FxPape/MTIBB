# MTIBB
Matrix to IRC Bridge Bot. For the use cases where matrix-appservice-irc does not work (or rather: is banned)

Simply connect two channels - one in matrix, one in irc - via relaying messages without puppeting or anything nice something like ``matrix-appservice-irc`` would do.

Why? Because matrix-appservice-irc is banned on hackint.

## 1. Prerequisites
* Python 3 and packages:
    * matrix-nio
    * irc
    * aiogram
    
## 2. Install
Install the Prerequisites (via pip).

Copy ``mtibb.example.yaml`` to ``mtibb.yaml`` and adapt the values to your setup.

???

``python mtibb.py`` and profit.

## 3. TODO
* IRC Nickserv support
* Telegram support
* Matrix e2e encryption support
* Add some kind of logger
* Callbacks and conversions for matrix message types != plain text
    * Images
    * Emojis
    * Videos
    * everything else matrix-nio supports in RoomMessages
* Commands
    * accepted via channel or query
    * answers via query/notice only (to not spam the channel)
    * ``?users`` to get users active in the respective other channel
    * ``?ignoreme`` to not be relayed
    * ``?relayme`` to be relayed (again)