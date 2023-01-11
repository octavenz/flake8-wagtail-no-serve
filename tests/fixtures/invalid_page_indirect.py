from wagtail.models import Page


class MyBasePage(Page):
    pass


class MyPage(MyBasePage):
    def serve(*args, **kwargs):
        return super().serve(*args, **kwargs)
