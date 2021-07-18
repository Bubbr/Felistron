from bot.util import *

import bot.info
import bot.ball
import bot.help
import bot.avatar
import bot.sad
import bot.ping
import bot.serverinfo
import bot.hd
import bot.cat
import bot.sauce
import bot.say
import bot.database
import bot.img

commands["info"]["func"]        = bot.info
commands["ball"]["func"]        = bot.ball
commands["help"]["func"]        = bot.help
commands["avatar"]["func"]      = bot.avatar
commands["sad"]["func"]         = bot.sad
commands["ping"]["func"]        = bot.ping
commands["serverinfo"]["func"]  = bot.serverinfo
commands["hd"]["func"]          = bot.hd
commands["cat"]["func"]         = bot.cat
commands["sauce"]["func"]       = bot.sauce
commands["say"]["func"]         = bot.say

commands["shop"]["func"]        = bot.database
commands["buy"]["func"]         = bot.database
commands["level"]["func"]       = bot.database

commands["bonk"]["func"]        = bot.img
commands["watchmojo"]["func"]   = bot.img
commands["toro"]["func"]        = bot.img
commands["lgbt"]["func"]        = bot.img
commands["urss"]["func"]        = bot.img