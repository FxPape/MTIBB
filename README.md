# MTIBB
Matrix to IRC Bridge Bot. For the use cases where matrix-appservice-irc does not work (or rather: is banned)

Simply connect two channels - one in matrix, one in irc - via relaying messages without puppeting or anything nice something like ``matrix-appservice-irc`` would do.

Why? Because matrix-appservice-irc is banned on hackint.

## Prerequisites
* Python 3 and packages:
    * matrix-nio
    * irc
    * aiogram (for telegram bridging, unfinished)
    
## Install
1. Install the Prerequisites (via pip).
2. ``git clone`` this repository
3. Copy ``mtibb.example.yaml`` to ``mtibb.yaml`` and adapt the values to your setup.
4. ???
5.  and profit.

## Usage
Currently just run: ``python mtibb.py``

Takes not parameters and is only configured via ``mtibb.yaml``

## Restrictions
1. No Matrix e2e Support

This bride would weaken the secrecy to a non e2e encrypted channel anyway.
So better don't use bot bridges to less secure messengeres for secrecys sake.

## Things in development
Or: the neverending feature creep. 

Things in **Bold** are currently being worked on.
### Lowest importance
* Rename this project

### Low importance
* \_\_str\_\_ for connections
* IRC Nickserv support
* Telegram: Initial support
    * Callbacks for multiple message types
    * aiogram or python-telegram-bot?
* Matrix: Callbacks and conversions for matrix message types != plain text
    * Images
    * Emojis
    * Videos
    * everything else matrix-nio supports in RoomMessages

### Medium importance
* Check message lengths and split accordingly (by protocol)
* Add some kind of logger
* Configuration class
    * Currently configuration is a single huge layered dict passed from one class to the other
    * config changes (e.g. due to commands) can be saved in config file
    * save admins and mutes.
* Support for private messages (optional per connection)
    * rework 'sender' property of message
        * Display name can differ from username (e.g. in matrix)
        * Replace by some 'user' class
    * commands should be able to answer via pm
* Commands
    * ``?users`` to get users active in the other channel/s
    * ``?op`` / ``?deop`` to become bot-admin
* Write more user documentation/usage info

### High importance
* Matrix: sending multiple messages to it fast mixes up order.
* **Message Handling in separate Thread**
    * fixin' all the race conditions
    * currently: message handling can block the thread of the connection (matrix) which does not allow sending to the same connection
    * fix matrix out of order issues


