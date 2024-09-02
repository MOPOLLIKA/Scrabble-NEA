from typing import Callable

def decorator(func: Callable[[], None]) -> Callable[[], None]:
        def wrapper():
                start = time.time

                func()

                print("Something after the function execution.")

        return wrapper

@decorator
def f() -> None:
        print("Inside the function.")

f()