import time, psutil
import typing as ty

import vkquick as vq

from src.filters.error_handler import ErrorHandler
from src.filters.only_me import OnlyMe
from src.misc import app


@app.command("пинг подробно", invalid_argument_config=ErrorHandler(), filter=OnlyMe())
async def pinged(ctx: vq.NewMessage) -> ty.Optional[str]:
    delta = round(time.time() - ctx.msg.date.timestamp(), 4)
    return (f"✨ vqlp | Ответ за ➙ {delta} сек.\n"
            f"⚙ Занятость ОЗУ : {round(psutil.virtual_memory()[3] / 2. ** 30, 2)}GB из {round(psutil.virtual_memory()[0] / 2. ** 30, 2)}GB\n"
            f" 📈 Занятость ЦПУ {round(psutil.cpu_percent())} %\n "
            f"📀 Диск загружен на {(psutil.disk_usage('/')[3])}%")


@app.command("пинг", invalid_argument_config=ErrorHandler(), filter=OnlyMe())
async def pinged(ctx: vq.NewMessage) -> ty.Optional[str]:
    delta = round(time.time() - ctx.msg.date.timestamp(), 4)
    return (f"✨ vqlp | Ответ за ➙ {delta if delta > 0 else 0.1} сек.")
