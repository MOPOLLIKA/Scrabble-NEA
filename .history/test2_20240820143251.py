from typing import Callable

def decorator(func: Callable[[], None]) -> Callable[[], None]:
        def wrapper():
                print("Something before the function execution.")

                func()

                print("Something after the function execution.")

        return wrapper
list[str]
@decorator
def f() -> None:
        print("Inside the function.")

f()