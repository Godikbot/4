import asyncio
import typing as ty
import re

import aiohttp
import requests

from src.database.base import Location


def check_access_token(site: ty.Optional[str]) -> ty.Optional[dict]:
    if "access_token=" in site:
        site = re.findall(
            "access_token=[A-Za-z0-9]*",
            site
        )[0].replace("access_token=", "")

    regular_return = re.sub('[^A-Za-z0-9]', '', site) == site and len(
        site) == 85
    if not regular_return:
        return {"response": False, "desc": "Введите правильный формат токена."}

    json_response = requests.get("https://api.vk.com/method/users.get",
                                 params={
                                     "access_token": site,
                                     "v": 5.131
                                 }).json()

    try:
        _ = json_response['response']
        return {"response": True, "user": json_response, 'token': site}
    except:
        return {"response": False, "desc": "[5] Invalid token", "error": json_response}


class AutoCommands(Location):

    async def _request(self, method: ty.Optional[str], **kwargs) -> ty.Union[ty.List[ty.Any], None]:
        async with aiohttp.ClientSession() as reload:  # Запрос.
            async with reload.post(f'https://api.vk.com/method/{method}', data=kwargs) as resp:
                try:
                    return (await resp.json())['response']
                except:
                    return None

    async def auto_mine_for_user(self):
        iris_id: ty.Optional[int] = -174105461
        item_id: ty.Optional[int] = 6713149

        while True:
            async with aiohttp.ClientSession() as get_comment:  # Оставление коментария.
                async with get_comment.post('https://api.vk.com/method/wall.createComment', data={
                    "access_token": self.token,
                    "v": 5.131,
                    'owner_id': iris_id,
                    'post_id': item_id,
                    'message': "Ферма"
                }) as resp:
                    comment_id = (await resp.json())['response']['comment_id']

            message = None  # Получение комментария, после чего вместо None идёт ответ ириса.
            while not message:
                await asyncio.sleep(1)
                async with aiohttp.ClientSession() as get_response_iris:
                    async with get_response_iris.post('https://api.vk.com/method/wall.getComments', data={
                        "access_token": self.token,
                        "v": '5.131',
                        'owner_id': iris_id,
                        'post_id': item_id,
                        'comment_id': comment_id
                    }) as resp1:
                        comments = (await resp1.json())['response']['items']
                for comment in comments:
                    if comment['from_id'] == iris_id:
                        message = comment['text']
                    continue

            await self._request("messages.send",
                                user_id=(await self._request("users.get", access_token=self.token))[0]['id'],
                                message=f"Auto mine VQLP: \n{message}",
                                random_id=0)

            await asyncio.sleep(14500)
            location = Location()
            if not location.auto_mine:
                break
