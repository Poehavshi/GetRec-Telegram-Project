import pydantic


class TelegramPost(pydantic.BaseModel):
    # todo split image urls and image paths to different pydantic models
    content: str
    author: str
    posted_at: str
    image_urls: list[str] = []
    image_paths: list[str] = []
    video_urls: list[str] = []
