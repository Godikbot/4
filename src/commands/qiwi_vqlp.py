import vkquick as vq
import typing, pyqiwi

from src.config import complete_sticker, error_sticker
from src.filters.error_handler import ErrorHandler
from src.filters.only_me import OnlyMe
from src.misc import app
from src.database.base import location

try:
    wallet = pyqiwi.Wallet(token=location.qiwi_key)
except:
    pass


@app.command("перевод", filter=OnlyMe())
async def create_pay(number: str, sum: typing.Union[float, int], *, comment: str):
    wallet.qiwi_transfer(account=number, amount=sum, comment=comment)
    return f"vqlp | {complete_sticker} Перевод на QIWI Кошелёк с номером {number} выполнен.\n🦋 Сумма списания: {sum}₽\n✉ Комментарий к переводу: {comment}"


@app.command("оплата", filter=OnlyMe())
async def pay_mobile(ctx: vq.NewMessage, number: str, sum: typing.Union[float, int]):
    try:
        wallet.mobile(account=number, amount=sum)
        await ctx.edit(
            f"✨ vqlp | {complete_sticker} Платеж прошел успешно на номер {number} было пополнено {sum} рублей💰")
    except ValueError:
        await ctx.edit(f"✨ vqlp | {error_sticker} Указан не верный номер телефона : {number}")


@app.command("баланс", filter=OnlyMe())
async def qbalance_wrapper(ctx: vq.NewMessage):
    await ctx.edit(f"✨ vqlp | 💵 Баланс вашего Qiwi кошелька составляет: {wallet.balance()}₽.")
