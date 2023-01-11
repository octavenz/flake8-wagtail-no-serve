from wagtail.models import Page


class MyPage(Page):
    def serve(*args, **kwargs):
        return super().serve(*args, **kwargs)
