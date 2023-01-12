class MyBaseClass:
    pass


def class_factory():
    return MyBaseClass


class MyNonPage(class_factory()):
    def serve(*args, **kwargs):
        return super().serve(*args, **kwargs)
