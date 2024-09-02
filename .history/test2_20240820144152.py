from typing import Callable
import time

def timing(func: Callable[[], None]) -> Callable[[], None]:
        def wrapper(a, b, **kwargs):
                start: float = time.time()
                result = func(a, b, zero=kwargs["isZero"])
                end: float = time.time()

                timing: float = end - start
                print(f"{func.__name__} execution time: {timing}")
                return timing - result

        return wrapper

@timing
def f(a, b, isZero=False) -> None:
        result = a ** (2 * b) * isZero
        print(result)
        return result


timing = f(2, 3)
print(timing)