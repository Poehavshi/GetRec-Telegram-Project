import pydantic


class TelegramPost(pydantic.BaseModel):
    content: str
    author: str
    posted_at: str
    image_urls: list[str] = []
