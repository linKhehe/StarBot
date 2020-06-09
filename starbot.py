from discord.ext import commands
import subprocess, asyncio, json
from time import sleep

import lib.verificationHandler as verificationHandler
from lib.botController import botControllerClass

bot = commands.Bot(command_prefix = "")
bot.remove_command('help')

sleep(0.1)

try:
    bot.config = json.loads(open("data/config.json", "r").read())
except:
    open("data/config.json", "w").write('{"minecraft":{"email":"","password":"","serverAddress":"creative.starlegacy.net","connectionCooldown":500},"discord":{"token":"","botMaster":0,"botControllers":[0]}}')

bot.botController = botControllerClass()

bot.command_prefix = ">"

@commands.command()
async def help(ctx):
    await ctx.send("""**StarBot v1.0**

Commands:
>playerInfo (>playerinfo / >pi) : Gets details about a player
>nationInfo (>nationinfo / >ni) : Gets details about a nation
>settlementInfo (>settlementinfo / >si) : Gets details about a settlement
>botControl (>botcontrol / >bc) : Restricted Command
>botControl shutdown : Restricted Command - Shuts down the bot
>botControl disable : Restricted Command - Prevents the bot from connecting to minecraft
>botControl enable : Restricted Command - Allows the bot to connect to minecraft

Bot Discord Server: https://discord.gg/cPkrrrj""")

@bot.command(aliases = ["botcontrol", "bc"])
async def botControl(ctx, subcommand):
    if not ctx.message.author.id in bot.config["discord"]["botControllers"] and not ctx.message.author.id == bot.config["discord"]["botMaster"]:
        await ctx.send(f"Access Denied: If you belive this is an error please contact <@{bot.config['discord']['botMaster']}>")
        return
    
    if subcommand == "shutdown" and ctx.message.author.id == bot.config["discord"]["botMaster"]:
        await ctx.send("Shutting Down")
        await ctx.bot.logout()

    elif not ctx.message.author.id == bot.config["discord"]["botMaster"] and subcommand == "shutdown":
        await ctx.send("Access Denied.")

    if subcommand == "disable":
        bot.botController.disabled = True
        bot.botController.disabledBy = ctx.message.author.id

        await ctx.send("Disabled")

    if subcommand == "enable":
        bot.botController.disabled = False
        bot.botController.disabledBy = 0

        await ctx.send("Enabled")

@bot.event
async def on_ready():
    bot.remove_command("help")
    bot.add_command(help)

loop = asyncio.get_event_loop()

loop.create_task(bot.botController.activeCheck())
loop.create_task(verificationHandler.handleExpiredCodes())

bot.load_extension("cogs.utils")

try:
    bot.run(bot.config["discord"]["token"])
except:
    pass