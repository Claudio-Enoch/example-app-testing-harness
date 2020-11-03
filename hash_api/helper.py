import time


# This wrapper was originally created to wrap the HashApi.post_hash method and keep track of requests and average time
# The class would hold a request_list property.
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
