import requests

from django.conf import settings
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _


def add_short_description(short_description: str):
    def decorator(admin_action):
        def wrapper(*args, **kwargs):
            return admin_action(*args, **kwargs)
        wrapper.__name__ = admin_action.__name__
        wrapper.short_description = _(short_description)
        return wrapper
    return decorator


def get_cdn_token(key="cdn-token"):
    token = cache.get(key)
    if not token:
        resp = requests.post(
            "https://api.cdnvideo.ru/app/oauth/v1/token/",
            data=dict(
                username=settings.CDN_USERNAME,
                password=settings.CDN_PASSWORD
            )
        )
        if resp.status_code == 200:
            data = resp.json()
            token = data["token"]
            lifetime = data["lifetime"]
            cache.set(key, token, lifetime)
    return token


def clean_url_cache(target_url):
    headers = {'CDN-AUTH-TOKEN': get_cdn_token()}
    url = (
        "https://api.cdnvideo.ru/"
        "app/cache/v2/objects?"
        "cdn_url={}"
    ).format(target_url)

    resp = requests.delete(
        url,
        headers=headers,
    )

    task_id = resp.json()["task_id"]
    print("""curl -X DELETE -H "CDN-AUTH-TOKEN: {}" '{}'""".format(
            headers["CDN-AUTH-TOKEN"],
            url
        )
    )
    print("""curl -X GET -H "CDN-AUTH-TOKEN: {}" '{}'""".format(
            headers["CDN-AUTH-TOKEN"],
            "https://api.cdnvideo.ru/app/cache/v2/tasks?id={}".format(task_id)
        )
    )
    print(resp.json())
    return task_id if resp.status_code == 200 else None
