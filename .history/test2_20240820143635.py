from typing import Callable
import time

def timing(func: Callable[[], None]) -> Callable[[], None]:
        def wrapper(a, b):
                start = time.time()
                func(a, b)
                end = time.time()

                time = end - start
                print(f"{func.__name__} execution time: {time}")
                return time

        return wrapper

@timing
def f(a, b) -> None:
        result = a ** (2 * b)
        print(result)
        return result


f(2, 3)