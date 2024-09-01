from typing import Callable
import time

def timing(func: Callable[[], None]) -> Callable[[], None]:
        def wrapper(a, b):
                start = time.time()
                func(a, b)
                end = time.time()

                timing = end - start
                print(f"{func.__name__} execution time: {timing}")
                return timing

        return wrapper

@timing
def f(a, b, zero=False) -> None:
        result = a ** (2 * b)
        print(result)
        return result


timing = f(2, 3)
print(timing)