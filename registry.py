func_registry:dict = dict()


def task(func):
    func_registry[func.__name__] = func
    async def wrapper(*args,**kwargs):
        return await func(*args,**kwargs)
    return wrapper