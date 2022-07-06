import contextlib

from telethon.errors import (
    BadRequestError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)
from telethon.utils import get_display_name

from userbot import legend

from ..core.data import _sudousers_list
from ..core.logger import logging
from ..core.managers import eod, eor
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.globals import gvarstatus
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, ban_pic, demote_pic, mute_pic, promote_pic

# =================== STRINGS ============
PP_TOO_SMOL = "`The image is too small`"
PP_ERROR = "`Failure while processing the image`"
NO_ADMIN = "`I am not an admin nub nibba!`"
NO_PERM = "`I don't have sufficient permissions! This is so sed. Alexa play despacito`"
CHAT_PP_CHANGED = "`Chat Picture Changed`"
INVALID_MEDIA = "`Invalid Extension`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

ADMIN_PIC = gvarstatus("ADMIN_PIC")
if ADMIN_PIC:
    prmt_pic = ADMIN_PIC
else:
    prmt_pic = promote_pic

if ADMIN_PIC:
    bn_pic = ADMIN_PIC
else:
    bn_pic = ban_pic

if ADMIN_PIC:
    dmt_pic = ADMIN_PIC
else:
    dmt_pic = demote_pic

if ADMIN_PIC:
    mt_pic = ADMIN_PIC
else:
    mt_pic = mute_pic


LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

menu_category = "admin"
# ================================================
from telethon.tl.types import ChannelParticipantsAdmins as admin
from telethon.tl.types import ChannelParticipantsKicked as banned


@legend.legend_cmd(
    pattern="demoteall$",
    command=("demoteall", menu_category),
    info={
        "header": "To Demote all members whom u have promoted ",
        "description": "It Help U to demote all those member whom u have promoted in this chat",
        "usage": [
            "{tr}demall",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def shj(e):
    sr = await e.client.get_participants(e.chat.id, filter=admin)
    et = 0
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "????"
    for i in sr:
        try:
            await e.client(EditAdminRequest(e.chat_id, i.id, newrights, rank))
            et += 1
        except BadRequestError:
            return await eod(e, NO_PERM)
    await eor(e, f"Demoted {et} admins !")


@legend.legend_cmd(
    pattern="getbanned$",
    command=("getbanned", menu_category),
    info={
        "header": "To Get List Of Banned User",
        "description": "It Help U to get list of all user banned in group /nNote: u must be have proper right",
        "usage": [
            "{tr}getbanned",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def getbaed(event):
    try:
        users = await event.client.get_participants(event.chat_id, filter=banned)
    except Exception as e:
        return await eor(event, f"ERROR - {str(e)}")
    if len(users) > 0:
        msg = f"✓ **List of banned member in this group** !!\n✓ Total : __{len(users)}__\n\n"
        for user in users:
            if not user.deleted:
                msg += f"🛡 __[{user.first_name}]({user.id})__\n"
            else:
                msg += "☠️ __ Deleted Account__\n"
        await eor(event, msg)
    else:
        await eod(event, "No Banned Users !!")


@legend.legend_cmd(
    pattern="gpic( -s| -d)$",
    command=("gpic", menu_category),
    info={
        "header": "For changing group display pic or deleting display pic",
        "description": "Reply to Image for changing display picture",
        "flags": {
            "-s": "To set group pic",
            "-d": "To delete group pic",
        },
        "usage": [
            "{tr}gpic -s <reply to image>",
            "{tr}gpic -d",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):  # sourcery no-metrics
    "header": "For changing group dp",
    type = (event.pattern_match.group(1)).strip()
    if type == "-s":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await eod(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await bot.send_file(
                    event.chat_id,
                    help_pic,
                    caption=f"⚜ `Group Profile Pic Changed` ⚜\n🔰Chat ~ {gpic.chat.title}",
                )
            except PhotoCropSizeSmallError:
                return await eod(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await eod(event, PP_ERROR)
            except Exception as e:
                return await eod(event, f"**Error : **`{str(e)}`")
            process = "updated"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await eod(event, f"**Error : **`{e}`")
        process = "deleted"
        await eod(event, "```successfully group profile pic deleted.```")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#GROUPPIC\n"
            f"Group profile pic {process} successfully "
            f"CHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@legend.legend_cmd(
    pattern="promote(?:\s|$)([\s\S]*)",
    command=("promote", menu_category),
    info={
        "header": "To give admin rights for a person",
        "description": "Provides admin rights to the person in the chat\
            \nNote : You need proper rights for this",
        "usage": [
            "{tr}promote <userid/username/reply>",
            "{tr}promote <userid/username/reply> <custom title>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def promote(event):
    "To promote a person in chat"
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(event, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "ℓєgєи∂"
    if not user:
        return
    legendevent = await eor(event, "`Promoting...`")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await legendevent.edit(NO_PERM)
    await event.client.send_file(
        event.chat_id,
        prmt_pic,
        caption=f"**⚜Promoted ~** [{user.first_name}](tg://user?id={user.id})⚜\n**Successfully In** ~ `{event.chat.title}`!! \n**Admin Tag ~**  `{rank}`",
    )
    await event.delete()
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PROMOTE\
            \nUSER: [{user.first_name}](tg://user?id={user.id})\
            \nCHAT: {get_display_name(await event.get_chat())} (`{event.chat_id}`)",
        )


@legend.legend_cmd(
    pattern="demote(?:\s|$)([\s\S]*)",
    command=("demote", menu_category),
    info={
        "header": "To remove a person from admin list",
        "description": "Removes all admin rights for that peron in that chat\
            \nNote : You need proper rights for this and also u must be owner or admin who promoted that guy",
        "usage": [
            "{tr}demote <userid/username/reply>",
            "{tr}demote <userid/username/reply> <custom title>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    "To demote a person in group"
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(event, NO_ADMIN)
        return
    user, _ = await get_user_from_event(event)
    if not user:
        return
    legendevent = await eor(event, "`Demoting...`")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "????"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await legendevent.edit(NO_PERM)
    await legendevent.delete()
    await event.client.send_file(
        event.chat_id,
        dmt_pic,
        caption=f"Demoted Successfully\nUser:[{user.first_name}](tg://{user.id})\n Chat: {event.chat.title}",
    )


@legend.legend_cmd(
    pattern="ban(?:\s|$)([\s\S]*)",
    command=("ban", menu_category),
    info={
        "header": "Will ban the guy in the group where you used this command.",
        "description": "Permanently will remove him from this group and he can't join back\
            \nNote : You need proper rights for this.",
        "usage": [
            "{tr}ban <userid/username/reply>",
            "{tr}ban <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _ban_person(event):
    "To ban a person in group"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == event.client.uid:
        return await eod(event, "__You cant ban yourself.__")
    legendevent = await eor(event, "`Whacking the pest!`")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await legendevent.edit(NO_PERM)
    reply = await event.get_reply_message()
    await legendevent.delete()
    if reason:
        await event.client.send_file(
            event.chat_id,
            bn_pic,
            caption=f"{_format.mentionuser(user.first_name ,user.id)}` is banned !!`\n**Reason : **`{reason}`",
        )
    else:
        await event.client.send_file(
            event.chat_id,
            bn_pic,
            caption=f"{_format.mentionuser(user.first_name ,user.id)} `is banned !!`",
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#BAN\
                \nUSER: [{user.first_name}](tg://user?id={user.id})\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \nREASON : {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#BAN\
                \nUSER: [{user.first_name}](tg://user?id={user.id})\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )
        try:
            if reply:
                await reply.forward_to(BOTLOG_CHATID)
                await reply.delete()
        except BadRequestError:
            return await legendevent.edit(
                "`I dont have message nuking rights! But still he is banned!`"
            )


@legend.legend_cmd(
    pattern="unban(?:\s|$)([\s\S]*)",
    command=("unban", menu_category),
    info={
        "header": "Will unban the guy in the group where you used this command.",
        "description": "Removes the user account from the banned list of the group\
            \nNote : You need proper rights for this.",
        "usage": [
            "{tr}unban <userid/username/reply>",
            "{tr}unban <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    "To unban a person"
    user, _ = await get_user_from_event(event)
    if not user:
        return
    legendevent = await eor(event, "`Unbanning...`")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await legendevent.edit(
            f"{_format.mentionuser(user.first_name ,user.id)} `is Unbanned Successfully. Granting another chance.`"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await legendevent.edit("`Uh oh my unban logic broke!`")
    except Exception as e:
        await legendevent.edit(f"**Error :**\n`{e}`")


@legend.legend_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@legend.legend_cmd(
    pattern="mute(?:\s|$)([\s\S]*)",
    command=("mute", menu_category),
    info={
        "header": "To stop sending messages from that user",
        "description": "If is is not admin then changes his permission in group,\
            if he is admin or if you try in personal chat then his messages will be deleted\
            \nNote : You need proper rights for this.",
        "usage": [
            "{tr}mute <userid/username/reply>",
            "{tr}mute <userid/username/reply> <reason>",
        ],
    },  # sourcery no-metrics
)
async def startmute(event):
    "To mute a person in that paticular chat"
    if event.is_private:
        replied_user = await event.client.get_entity(event.chat_id)
        if is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "`This user is already muted in this chat ~~lmfao sed rip~~`"
            )
        if event.chat_id == legend.uid:
            return await eod(event, "`You cant mute yourself`")
        try:
            mute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**Error **\n`{e}`")
        else:
            await event.edit("`Successfully muted that person.\n**｀-´)⊃━☆ﾟ.*･｡ﾟ **`")
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_MUTE\n"
                f"**User :** [{replied_user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            return await eor(
                event, "`You can't mute a person without admin rights niqq.` ಥ﹏ಥ  "
            )
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == legend.uid:
            return await eor(event, "`Sorry, I can't mute myself`")
        if is_muted(user.id, event.chat_id):
            return await eor(
                event, "`This user is already muted in this chat ~~lmfao sed rip~~`"
            )
        result = await event.client.get_permissions(event.chat_id, user.id)
        try:
            if result.participant.banned_rights.send_messages:
                return await eor(
                    event,
                    "`This user is already muted in this chat ~~lmfao sed rip~~`",
                )
        except AttributeError:
            pass
        except Exception as e:
            return await eor(event, f"**Error : **`{e}`", 10)
        try:
            await event.client(EditBannedRequest(event.chat_id, user.id, MUTE_RIGHTS))
        except UserAdminInvalidError:
            if "admin_rights" in vars(chat) and vars(chat)["admin_rights"] is not None:
                if chat.admin_rights.delete_messages is not True:
                    return await eor(
                        event,
                        "`You can't mute a person if you dont have delete messages permission. ಥ﹏ಥ`",
                    )
            elif "creator" not in vars(chat):
                return await eor(
                    event, "`You can't mute a person without admin rights niqq.` ಥ﹏ಥ  "
                )
            mute(user.id, event.chat_id)
        except Exception as e:
            return await eor(event, f"**Error : **`{e}`", 10)
    await event.delete()
    if reason:
        await event.client.send_file(
            event.chat_id,
            mt_pic,
            caption=f"{_format.mentionuser(user.first_name ,user.id)} `is muted in {get_display_name(await event.get_chat())}`\n`Reason:`{reason}",
        )
    else:
        await event.client.send_file(
            event.chat_id,
            mt_pic,
            caption=f"{_format.mentionuser(user.first_name ,user.id)} `is muted in {get_display_name(await event.get_chat())}`\n",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#MUTE\n"
                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@legend.legend_cmd(
    pattern="unmute(?:\s|$)([\s\S]*)",
    command=("unmute", menu_category),
    info={
        "header": "To allow user to send messages again",
        "description": "Will change user permissions ingroup to send messages again.\
        \nNote : You need proper rights for this.",
        "usage": [
            "{tr}unmute <userid/username/reply>",
            "{tr}unmute <userid/username/reply> <reason>",
        ],
    },
)
async def endmute(event):
    "To mute a person in that paticular chat"
    if event.is_private:
        replied_user = await event.client.get_entity(event.chat_id)
        if not is_muted(event.chat_id, event.chat_id):
            return await event.edit(
                "`__This user is not muted in this chat__\n（ ^_^）o自自o（^_^ ）`"
            )
        try:
            unmute(event.chat_id, event.chat_id)
        except Exception as e:
            await event.edit(f"**Error **\n`{e}`")
        else:
            await event.edit(
                "`Successfully unmuted that person\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍`"
            )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#PM_UNMUTE\n"
                f"**User :** [{replied_user.first_name}](tg://user?id={event.chat_id})\n",
            )
    else:
        user, _ = await get_user_from_event(event)
        if not user:
            return
        try:
            if is_muted(user.id, event.chat_id):
                unmute(user.id, event.chat_id)
            else:
                result = await event.client.get_permissions(event.chat_id, user.id)
                if result.participant.banned_rights.send_messages:
                    await event.client(
                        EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS)
                    )
        except AttributeError:
            return await eor(
                event,
                "`This user can already speak freely in this chat ~~lmfao sed rip~~`",
            )
        except Exception as e:
            return await eor(event, f"**Error : **`{e}`")
        await eor(
            event,
            f"{_format.mentionuser(user.first_name ,user.id)} `is unmuted in {get_display_name(await event.get_chat())}\n乁( ◔ ౪◔)「    ┑(￣Д ￣)┍`",
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#UNMUTE\n"
                f"**User :** [{user.first_name}](tg://user?id={user.id})\n"
                f"**Chat :** {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@legend.legend_cmd(
    pattern="kick(?:\s|$)([\s\S]*)",
    command=("kick", menu_category),
    info={
        "header": "To kick a person from the group",
        "description": "Will kick the user from the group so he can join back.\
        \nNote : You need proper rights for this.",
        "usage": [
            "{tr}kick <userid/username/reply>",
            "{tr}kick <userid/username/reply> <reason>",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def kick(event):
    "use this to kick a user from chat"
    user, reason = await get_user_from_event(event)
    if not user:
        return
    legendevent = await eor(event, "`Kicking...`")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await legendevent.edit(f"{NO_PERM}\n{e}")
    if reason:
        await event.client.send_file(
            event.chat_id,
            help_pic,
            caption=f"Kicked` [{user.first_name}](tg://user?id={user.id})`!`\nReason: {reason}",
        )
    else:
        await event.client.send_file(
            event.chat_id,
            help_pic,
            caption=f"`Kicked` [{user.first_name}](tg://user?id={user.id})`!`",
        )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#KICK\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\n",
        )


@legend.legend_cmd(
    pattern="pin( loud|$)",
    command=("pin", menu_category),
    info={
        "header": "For pining messages in chat",
        "description": "reply to a message to pin it in that in chat\
        \nNote : You need proper rights for this if you want to use in group.",
        "options": {"loud": "To notify everyone without this it will pin silently"},
        "usage": [
            "{tr}pin <reply>",
            "{tr}pin loud <reply>",
        ],
    },
)
async def pin(event):
    "To pin a message in chat"
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await eod(event, "`Reply to a message to pin it.`", 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await eod(event, NO_PERM, 5)
    except Exception as e:
        return await eod(event, f"`{e}`", 5)
    await eod(event, "`Pinned Successfully!`", 3)
    if event.sender_id in sudo_users:
        with contextlib.suppress(BadRequestError):
            await event.delete()
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#PIN\
                \n__successfully pinned a message in chat__\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \nLOUD: {is_silent}",
        )


@legend.legend_cmd(
    pattern="unpin( all|$)",
    command=("unpin", menu_category),
    info={
        "header": "For unpining messages in chat",
        "description": "reply to a message to unpin it in that in chat\
        \nNote : You need proper rights for this if you want to use in group.",
        "options": {"all": "To unpin all messages in the chat"},
        "usage": [
            "{tr}unpin <reply>",
            "{tr}unpin all",
        ],
    },
)
async def unpin(event):
    "To unpin message(s) in the group"
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "all":
        return await eod(
            event,
            "__Reply to a message to unpin it or use __`.unpin all`__ to unpin all__",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "all":
            await event.client.unpin_message(event.chat_id)
        else:
            return await eod(
                event, "`Reply to a message to unpin it or use .unpin all`", 5
            )
    except BadRequestError:
        return await eod(event, NO_PERM, 5)
    except Exception as e:
        return await eod(event, f"`{e}`", 5)
    await eod(event, "`Unpinned Successfully!`", 3)
    sudo_users = _sudousers_list()
    if event.sender_id in sudo_users:
        with contextlib.suppress(BadRequestError):
            await event.delete()
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#UNPIN\
                \n__successfully unpinned message(s) in chat__\
                \nCHAT: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@legend.legend_cmd(
    pattern="undlt( -u)?(?: |$)(\d*)?",
    command=("undlt", menu_category),
    info={
        "header": "To get recent deleted messages in group",
        "description": "To check recent deleted messages in group, by default will show 5. you can get 1 to 15 messages.",
        "flags": {
            "u": "use this type to upload media to chat else will just show as media."
        },
        "usage": [
            "{tr}undlt <count>",
            "{tr}undlt -u <count>",
        ],
        "examples": [
            "{tr}undlt 7",
            "{tr}undlt -u 7 (this will reply all 7 messages to this message",
        ],
    },
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):  # sourcery no-metrics
    "To check recent deleted messages in group"
    legendevent = await eor(event, "`Searching recent actions .....`")
    type = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        lim = min(lim, 15)
        if lim <= 0:
            lim = 1
    else:
        lim = 5
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"⚜ **Recent {lim} Deleted message(s) in this group are:~** ⚜"
    if not type:
        for msg in adminlog:
            sweet = await event.client.get_entity(msg.old.from_id)
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n\n✓ {_format.mentionuser(sweet.first_name ,sweet.id)} : __{msg.old.message}__"
            else:
                deleted_msg += f"\n\n✓ {_format.mentionuser(sweet.first_name ,sweet.id)} :  __{_media_type}__"
            await eor(legendevent, deleted_msg)
    else:
        main_msg = await eor(legendevent, deleted_msg)
        for msg in adminlog:
            sweet = await event.client.get_entity(msg.old.from_id)
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"✓ {_format.mentionuser(sweet.first_name ,sweet.id)} : __{msg.old.message}__"
                )
            else:
                await main_msg.reply(
                    f"✓ {_format.mentionuser(sweet.first_name ,sweet.id)} : __{msg.old.message}__",
                    file=msg.old.media,
                )
