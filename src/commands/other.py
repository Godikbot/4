import asyncio
import typing as ty

import vkquick as vq

from src.misc import app

from src.database.base import location
from src.config import error_sticker, complete_sticker
from src.filters.error_handler import ErrorHandler


async def messages_send(context: vq.NewMessage,
                        cul: int,
                        time_sleep: float,
                        text: str,
                        attachments: ty.Union[None, list, str]):
    for i in range(cul):
        await asyncio.sleep(time_sleep)
        await context.answer(text, attachment=attachments)


@app.command("спам")
async def spam(ctx: vq.NewMessage, cul: int, time_sleep: float, *, text: str):
    attachments_all = []
    await ctx.msg.extend(ctx.api)
    fields = ctx.msg.fields
    for i in fields['attachments']:
        try:
            if i is None:
                ...
            else:
                attachments_all.append(f"{i['type']}{i[i['type']]['owner_id']}_{i[i['type']]['id']}")
        except:
            ...

    asyncio.create_task(messages_send(
        context=ctx,
        text=text,
        cul=cul,
        attachments=attachments_all if len(attachments_all) > 0 else None,
        time_sleep=time_sleep
    ))
    await ctx.edit(text)


@app.command("шаб", invalid_argument_config=ErrorHandler())
async def get_note(ctx: vq.NewMessage, name: str):
    if name not in [_['name_note'] for _ in location.notes]:
        return f"{error_sticker} У вас нет шаблона <<{name}>>"

    for i in location.notes:
        if i['name_note'] == name:
            await ctx.edit(i['message'], attachment=i['attachment'])


@app.command("рп", invalid_argument_config=ErrorHandler())
async def role_play_command(ctx: vq.NewMessage,
                            name_role: str,
                            user: vq.User) -> str:
    role_list = [role['name'] for role in location.role_plays_commands]
    if name_role.strip() not in role_list:
        return f"{error_sticker} У Вас нету данной команды."

    sticker = ''
    value_ = ''
    for v in location.role_plays_commands:
        if v['name'] == name_role.strip():
            sticker += v['sticker']
            value_ += v['value']
    _, i = await ctx.api.define_token_owner()
    await ctx.edit(
        f"{sticker} | {i:@[fullname]} {value_} {user:@[fullname]}")


@app.command(".doc location", prefixes=[''])
async def _():
    return location.__doc__


@app.command(".doc startup", prefixes=[''])
async def _():
    return """
    Custom startup the Virtual Quarter

    Documentation: path <<autodocs>>. Html file.

    author: ymoth | VKQuick author: deknowny
    At the start, it is checked for the presence of a token.
    A separate function for testing is found in src.filters.other.

    The token can be transferred as a link or in other ways.
    Multiple tokens can be transferred.

    await app.coroutine_run ('token1', 'token2', 'token3')
    With the condition that you need to close the previous coroutine"""


@app.command("инфа")
async def get_information() -> str:
    text = f'''
🌀 Успешный стикер: {complete_sticker}
⚒ Еррор стикер: {error_sticker}

🔗 Префиксы: {' | '.join([prefix for prefix in location.custom_prefixes])}
🎗 Триггер: {' | '.join([prefix for prefix in location.trigger_prefixes])}
✨ Удалялки: {' | '.join([prefix for prefix in location.deleter_prefixes['prefixes']])}
Текст удалялки: {location.deleter_prefixes['text_prefixes']}

🌌 Шаблонов: {len(location.notes)}
🧸 РП-Команд: {len(location.role_plays_commands)}
🤬 Людей в игноре: {len(location.ignore_list)}
🤬 Людей в автокике: {len(location.auto_kicked_user)}
Доверенных: {len(location.friend_ids)}

🔵 IDM: {'Покдлючен' if len(location.idm_secret_code) < 0 else "Не подключен."}
💠 IDM-Префиксы сигнала: {' | '.join([prefix for prefix in location.idm_signal_prefixes])}

🔰 | Авто-команды:
🍬 Автоферма: {'Включена' if location.auto_mine else "Выключенна."}
🍃 Авто выход: {'Покдлючен' if location.auto_leave_chat else "Не подключен."}
'''
    return text
