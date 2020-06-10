# MTIBB
Matrix to IRC Bridge Bot. For the use cases where matrix-appservice-irc does not work (or rather: is banned)

Simply connect two channels - one in matrix, one in irc - via relaying messages without puppeting or anything nice something like ``matrix-appservice-irc`` would do.

Why? Because matrix-appservice-irc is banned on hackint.

## 1. Prerequisites
* Python 3 and packages:
    * matrix-nio
    * irc
    * aiogram (for telegram bridging, unfinished)
    
## 2. Install
Install the Prerequisites (via pip).

Copy ``mtibb.example.yaml`` to ``mtibb.yaml`` and adapt the values to your setup.

???

``python mtibb.py`` and profit.

## 3. TODO
* Sort todos by importance
* Check message lengths and split accordingly (by protocol)
* Matrix: sending multiple messages to it fast mixes up order.
* IRC Nickserv support
* Telegram support
* Matrix e2e encryption support
* Add some kind of logger
* Callbacks and conversions for matrix message types != plain text
    * Images
    * Emojis
    * Videos
    * everything else matrix-nio supports in RoomMessages
* Message Handling in separate Thread (?)
    * ooor maybe not: the race conditions
* Commands
    * make command handler classes singletons to enable multiple commands being handled by the same object
    * config changes due to commands can be saved in config file (e.g. op/deop)
    * answers via query/notice only (to not spam the channel)
    * ``?op`` / ``?deop`` to become bot-admin
    * ``?list`` list all commands
    * give commands a neccesary \_\_str\_\_ for their description (e.g. for ``?list``)
    * ``?users`` to get users active in the other channel/s
    * ``?ignoreme`` to not be relayed
    * ``?relayme`` to be relayed (again)