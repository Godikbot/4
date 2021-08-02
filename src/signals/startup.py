import asyncio

from src.misc import app
from src.filters.other import check_access_token

from src.database.base import location
from src.filters.other import AutoCommands


@app.on_startup()
async def wrapper(_):
    if location.auto_mine:
        ac = AutoCommands()
        asyncio.create_task(ac.auto_mine_for_user())
