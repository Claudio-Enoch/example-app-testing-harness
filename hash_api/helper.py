import time


def timer(time_list: list):
    def func_wrapper(func):
        def inner(*args, **kwargs):
            start = time.time()
            response = func(*args, **kwargs)
            finish = time.time() - start
            time_list.append(finish)
            return response

        return inner

    return func_wrapper
