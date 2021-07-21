from bot.util import *

import bot.cmd.info
import bot.cmd.ball
import bot.cmd.help
import bot.cmd.avatar
import bot.cmd.sad
import bot.cmd.ping
import bot.cmd.serverinfo
import bot.cmd.hd
import bot.cmd.cat
import bot.cmd.sauce
import bot.cmd.say
import bot.database
import bot.cmd.img
import bot.cmd.hentai

commands["info"]["func"]        = bot.cmd.info
commands["8ball"]["func"]       = bot.cmd.ball
commands["help"]["func"]        = bot.cmd.help
commands["avatar"]["func"]      = bot.cmd.avatar
commands["sad"]["func"]         = bot.cmd.sad
commands["ping"]["func"]        = bot.cmd.ping
commands["serverinfo"]["func"]  = bot.cmd.serverinfo
commands["hd"]["func"]          = bot.cmd.hd
commands["cat"]["func"]         = bot.cmd.cat
commands["sauce"]["func"]       = bot.cmd.sauce
commands["say"]["func"]         = bot.cmd.say

commands["shop"]["func"]        = bot.database
commands["buy"]["func"]         = bot.database
commands["level"]["func"]       = bot.database
commands["bet"]["func"]         = bot.database
commands["balance"]["func"]     = bot.database
commands["daily"]["func"]       = bot.database

commands["bonk"]["func"]        = bot.cmd.img
commands["watchmojo"]["func"]   = bot.cmd.img
commands["toro"]["func"]        = bot.cmd.img
commands["lgbt"]["func"]        = bot.cmd.img

commands["hentai"]["func"]      = bot.cmd.hentai