import vkquick as vq
import typing

from src.config import complete_sticker, error_sticker
from src.filters.error_handler import ErrorHandler
from src.filters.only_me import OnlyMe
from src.misc import app
from src.database.base import location


@app.command("+др", invalid_argument_config=ErrorHandler(), filter=OnlyMe())
async def friend_add(ctx: vq.NewMessage, user: vq.User):
    try:
        method = await ctx.api.friends.add(user_id=user.id)
        await ctx.edit(f"{complete_sticker} Выполнение...")
        if method == 1:
            await ctx.edit(f"{complete_sticker} Заявка в друзья отправлена пользователю {user:@[fullname]} отправлена.")
        elif method == 2:
            await ctx.edit(f"{complete_sticker} Заявка на добавление в друзья от {user:@[fullname} одобрена.")
        elif method == 4:
            await ctx.edit(f"{error_sticker} Повторная отправка заявки.")
    except vq.APIError[vq.CODE_174_FRIENDS_ADD_YOURSELF]:
        await ctx.edit(f"{error_sticker} Невозможно добавить в друзья самого себя.")


@app.command("-др", invalid_argument_config=ErrorHandler(), filter=OnlyMe())
async def friend_delete(ctx: vq.NewMessage, user: vq.User):
    method = await ctx.api.friends.delete(user_id=user.id)
    await ctx.edit(f"{complete_sticker} Выполнение...")
    if method['success']:
        await ctx.edit(f"{complete_sticker} {user:@[fullname]} удален из списка друзей.")
    elif method['out_request_deleted']:
        await ctx.edit(f"{complete_sticker} Отменена исходящая заявка в друзья от пользователя {user:@[fullname]}")
    elif method['in_request_deleted']:
        await ctx.edit(f"{complete_sticker} Отклонена входящая заявка в друзья от пользователя {user:@[fullname]}")


@app.command("ид", invalid_argument_config=ErrorHandler(), filter=OnlyMe())
async def revolve_user(ctx: vq.NewMessage, user: vq.User):
    await ctx.edit(f"{complete_sticker} Айди пользователя {user.fullname}: [id{user.id}|{user.id}]")


@app.command("влс", invalid_argument_config=ErrorHandler(), filter=OnlyMe())
async def send_message(ctx: vq.NewMessage, user: vq.User, *, text: str):
    await ctx.api.messages.send(
        user_id=user.id,
        random_id=0,
        message=text
    )
    await ctx.edit(f"{complete_sticker} Сообщение было отправлено пользователю : {user:@[fullname]}")


@app.command("+лайк", invalid_argument_config=ErrorHandler(), filter=OnlyMe())
async def likes_add(ctx: vq.NewMessage, user: vq.User[typing.Literal["photo_id"]]):
    photo_id = user.fields["photo_id"].split("_")[1]
    count_likes = await ctx.api.likes.add(type='photo', owner_id=user.id, item_id=photo_id)
    await ctx.edit(
        f"{complete_sticker} Лайк на аватарку пользователя {user:@[fullname]} оформлен!\n"
        f"⚠ Стало лайков: {count_likes['likes']}")


@app.command("-лайк", invalid_argument_config=ErrorHandler(), filter=OnlyMe())
async def likes_delete(ctx: vq.NewMessage, user: vq.User[typing.Literal["photo_id"]]):
    photo_id = user.fields["photo_id"].split("_")[1]
    count_likes = await ctx.api.likes.delete(type='photo', owner_id=user.id, item_id=photo_id)
    await ctx.edit(
        f"{complete_sticker} Лайк на аватарку пользователя {user:@[fullname]} убран!\n"
        f"⚠ Стало лайков: {count_likes['likes']}")


@app.command("диалоги", invalid_argument_config=ErrorHandler(), filter=OnlyMe())
async def dialog_get(ctx: vq.NewMessage):
    dialogs = await ctx.api.messages.getConversations()
    await ctx.edit(f"{complete_sticker} Количество ваших диалогов: {dialogs['count']}")


@app.command("чат", invalid_argument_config=ErrorHandler(), filter=OnlyMe())
async def get_chat(ctx: vq.NewMessage):
    chat = await ctx.api.messages.getChat(chat_id=ctx.msg.chat_id)
    await ctx.edit(f"⚙ Информация о чате\n"
                   f"💡 Название чата : {chat['title']}\n"
                   f"{complete_sticker} Количество участников : {chat['members_count']}\n"
                   f"⚠ Айди чата : {chat['id']}")


@app.command("кик", filter=OnlyMe())
async def chat(ctx: vq.NewMessage, user: vq.User):
    try:
        method = await ctx.api.messages.removeChatUser(chat_id=ctx.msg.chat_id, user_id=user.id)
        await ctx.edit(f"{complete_sticker} Исключение")
        if method == 1:
            await ctx.edit(f"{complete_sticker} Пользователь {user:@[fullname]} исключен из беседы.")
    except vq.APIError[vq.CODE_925_MESSAGES_CHAT_NOT_ADMIN]:
        await ctx.edit(f"{error_sticker} Нет доступа.")
    except vq.APIError[vq.CODE_935_MESSAGES_CHAT_USER_NOT_IN_CHAT]:
        await ctx.edit(f"{error_sticker} Пользователя нету в беседе.")
    except vq.APIError[vq.CODE_945_MESSAGES_CHAT_DISABLED]:
        await ctx.edit(f"{error_sticker} MESSAGES_CHAT_DISABLED")
    except vq.APIError[vq.CODE_946_MESSAGES_CHAT_UNSUPPORTED]:
        await ctx.edit(f"{error_sticker} MESSAGES_CHAT_UNSUPPORTED")
    except vq.APIError[vq.CODE_15_ACCESS]:
        await ctx.edit(f"{error_sticker} Нет доступа.")


@app.command("добавить", filter=OnlyMe())
async def chat(ctx: vq.NewMessage, user: vq.User):
    try:
        method = await ctx.api.messages.addChatUser(
            chat_id=ctx.msg.chat_id,
            user_id=user.id
        )
        await ctx.edit(f"{complete_sticker} Добавляю пользователя {user:@[fullname]}")
        if method == 1:
            await ctx.edit(f"{complete_sticker} ✅Пользователь {user:@[fullname]} добавлен.")
    except vq.APIError[vq.CODE_925_MESSAGES_CHAT_NOT_ADMIN]:
        await ctx.edit(f"{error_sticker} You are not admin of this chat")
    except vq.APIError[vq.CODE_932_MESSAGES_GROUP_PEER_ACCESS]:
        await ctx.edit(f"{error_sticker} Your community can't interact with this peer")
    except vq.APIError[vq.CODE_947_MESSAGES_MEMBER_ACCESS_TO_GROUP_DENIED]:
        await ctx.edit(f"{error_sticker} Can't add user to chat, because user has no access to group")
    except vq.APIError[vq.CODE_15_ACCESS]:
        await ctx.edit(f"{error_sticker} Access denied: can't add this user")


@app.command("репорт", filter=OnlyMe())
async def report(ctx: vq.NewMessage, user: vq.User):
    method = await ctx.api.users.report(
        user_id=user.id,
        type='spam'
    )
    await ctx.edit("✅Выполнение...")
    if method == 1:
        await ctx.edit(
            f"{complete_sticker} Жалоба на пользователя {user:@[fullname]} была успешно отправлена на модерацию.")
