from typing import Callable
import time

def timing(func: Callable[[], None]) -> Callable[[], None]:
        def wrapper():
                start = time.time()
                func()
                end = time.time()

                print(f"{func.__name__} execution time: {end - start}")

        return wrapper

@timing
def f(a, b) -> None:
        return a 


f()