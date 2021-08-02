import vkquick as vq

from vkquick.chatbot.dependency import Depends
from vkquick.chatbot.storages import NewMessage

from src.database.base import Location


class FromFriend(vq.BaseFilter):

    async def make_decision(self, ctx: NewMessage, **kwargs: Depends):
        location = Location()
        print(ctx.msg.fields)
        print(location.friend_ids)
        if ctx.msg.from_id not in location.friend_ids:
            raise vq.StopCurrentHandling()
