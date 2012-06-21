class NotImplementedClass:
    pass


def giveMeSomething():
    return ""


def methodWithNotImplementedClass(value):
    NotImplementedClass.notImplementedMethod(value)
    return False
