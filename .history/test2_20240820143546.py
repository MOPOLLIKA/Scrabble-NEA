from typing import Callable
import time

def timing(func: Callable[[], None]) -> Callable[[], None]:
        def wrapper(a, b):
                start = time.time()
                func(a, b)
                end = time.time()

                print(f"{func.__name__} execution time: {end - start}")

        return wrapper

@timing
def f(a, b) -> None:
        result = a ** (b)
        print(result)
        return result


f(2, 3)