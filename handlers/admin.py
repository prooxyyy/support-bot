from aiogram import types

import kb
from bot import dp, bot
from handlers.fsm import *
from handlers.db import db_profile_access, db_profile_exist, db_profile_updateone, db_profile_exist_usr, db_profile_get_usrname
from configurebot import cfg

errormessage = cfg['error_message']
lvl1name = cfg['1lvl_adm_name']
lvl2name = cfg['2lvl_adm_name']
lvl3name = cfg['3lvl_adm_name']
devid = cfg['dev_id']

def extract_arg(arg):
    return arg.split()[1:]

async def admin_ot(message: types.Message):
    try:
        uid = message.from_user.id

        if(db_profile_access(uid) >= 1):
            args = extract_arg(message.text)
            if len(args) >= 2:
                chatid = str(args[0])
                args.pop(0)
                answer = ""
                for ot in args:
                    answer+=ot+" "
                await message.reply('✅ Вы успешно ответили на вопрос!')
                await bot.send_message(chatid, f"✉ Новое уведомление!\nОтвет от тех.поддержки:\n\n`{answer}`",parse_mode='Markdown')
                return
            else:
                await message.reply('⚠ Укажите аргументы команды\nПример: `/ответ 516712732 Ваш ответ`',parse_mode='Markdown')
                return
        else:
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')

async def admin_giveaccess(message: types.Message):
    try:
        uidown = message.from_user.id

        if (db_profile_access(uidown) >= 3):
            args = extract_arg(message.text)
            if len(args) == 2:
                uid = int(args[0])
                access = int(args[1])
                outmsg = ""      
                if db_profile_exist(uid):
                    if access == 0:
                        outmsg = "✅ Вы успешно сняли все доступы с этого человека!"
                    elif access == 1:
                        outmsg = f"✅ Вы успешно выдали доступ *{lvl1name}* данному человеку!"
                    elif access == 2:
                        outmsg = f"✅ Вы успешно выдали доступ *{lvl2name}* данному человеку!"
                    elif access == 3:
                        outmsg = f"✅ Вы успешно выдали доступ *{lvl3name}* данному человеку!"
                    else:
                        await message.reply('⚠ Максимальный уровень доступа: *3*', parse_mode='Markdown')
                        return
                    db_profile_updateone({'_id': uid}, {"$set": {"access": access}})
                    await message.reply(outmsg, parse_mode='Markdown')
                    return
                else:
                    await message.reply("⚠ Этого пользователя *не* существует!",parse_mode='Markdown')
                    return
            else:
                await message.reply('⚠ Укажите аргументы команды\nПример: `/доступ 516712372 1`',
                                    parse_mode='Markdown')
                return

        else:
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')

async def admin_ban(message: types.Message):
    try:
        uidown = message.from_user.id

        if db_profile_access(uidown) >= 2:
            args = extract_arg(message.text)
            if len(args) == 2:
                uid = int(args[0])
                reason = args[1]
                if db_profile_exist(uid):
                    db_profile_updateone({"_id": uid}, {"$set": {'ban': 1}})
                    await message.reply(f'✅ Вы успешно забанили этого пользователя\nПричина: `{reason}`',parse_mode='Markdown')
                    await bot.send_message(uid, f"⚠ Администратор *заблокировал* Вас в боте\nПричина: `{reason}`", parse_mode='Markdown')
                    return
                else:
                    await message.reply("⚠ Этого пользователя *не* существует!", parse_mode='Markdown')
                    return
            else:
                await message.reply('⚠ Укажите аргументы команды\nПример: `/бан 51623722 Причина`',
                                    parse_mode='Markdown')
                return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')

async def admin_unban(message: types.Message):
    try:
        uidown = message.from_user.id

        if db_profile_access(uidown) >= 2:
            args = extract_arg(message.text)
            if len(args) == 1:
                uid = int(args[0])
                if db_profile_exist(uid):
                    db_profile_updateone({"_id": uid}, {"$set": {'ban': 0}})
                    await message.reply(f'✅ Вы успешно разблокировали этого пользователя',parse_mode='Markdown')
                    await bot.send_message(uid, f"⚠ Администратор *разблокировал* Вас в боте!", parse_mode='Markdown')
                    return
                else:
                    await message.reply("⚠ Этого пользователя *не* существует!", parse_mode='Markdown')
                    return
            else:
                await message.reply('⚠ Укажите аргументы команды\nПример: `/разбан 516272834`',
                                    parse_mode='Markdown')
                return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')

async def admin_id(message: types.Message):
    try:
        args = extract_arg(message.text)
        if len(args) == 1:
            username = args[0]
            if db_profile_exist_usr(username):
                uid = db_profile_get_usrname(username, '_id')
                await message.reply(f"🆔 {uid}")
            else:
                await message.reply("⚠ Этого пользователя *не* существует!", parse_mode='Markdown')
                return
        else:
            await message.reply('⚠ Укажите аргументы команды\nПример: `/айди nosemka`',
                                parse_mode='Markdown')
            return
    except Exception as e:
        cid = message.chat.id
        await message.answer(f"{errormessage}",
                             parse_mode='Markdown')
        await bot.send_message(devid, f"Случилась *ошибка* в чате *{cid}*\nСтатус ошибки: `{e}`",
                               parse_mode='Markdown')

def register_handler_admin():
    dp.register_message_handler(admin_ot, commands=['ответ', 'ot'])
    dp.register_message_handler(admin_giveaccess, commands=['доступ', 'access'])
    dp.register_message_handler(admin_ban, commands=['бан', 'ban'])
    dp.register_message_handler(admin_unban, commands=['разбан', 'unban'])
    dp.register_message_handler(admin_id, commands=['айди', 'id'])