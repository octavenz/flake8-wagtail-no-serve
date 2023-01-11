class Page:
    # not a wagtailcore.Page model
    pass


class MyPage(Page):
    def serve(self, *args, **kwargs):
        pass
