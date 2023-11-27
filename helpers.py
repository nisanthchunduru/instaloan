def memoize(func):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            result = func(*args)
            cache[args] = result
            return result
        else:
            return cache[args]

    return wrapper
