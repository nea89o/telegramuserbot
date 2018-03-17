
def property_decorator(key):
    def decorator(value):
        def wrapper(func):
            setattr(func, key, value)
            return func

        return wrapper

    return decorator

