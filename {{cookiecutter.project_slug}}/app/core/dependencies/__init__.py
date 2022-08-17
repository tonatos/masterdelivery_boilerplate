import inspect
from functools import wraps
from fastapi.params import Depends


def inject(func):
    """
    Wrapper for connect dependency out of fastapi routes

    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        parameters = inspect.signature(func).parameters
        for k, d in parameters.items():
            if type(d.default) is Depends:
                kwargs[k] = d.default.dependency
        func(*args, **kwargs)
    return wrapper
