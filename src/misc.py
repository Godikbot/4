import vkquick as vq

from src.config import prefixes
from src.filters.only_me import OnlyMe

app = vq.App(
    description="vq LongPoll",
    name="vq lp",
    debug=False,
    prefixes=prefixes)
