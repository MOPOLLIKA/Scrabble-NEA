from typing import Callable
import time

def decorator(func: Callable[[], None]) -> Callable[[], None]:
        def wrapper():
                start = time.time()

                func()

                end = time.time()
                print()

        return wrapper

@decorator
def f() -> None:
        print("Inside the function.")

f()