def decorator(func: function) -> function:
        def wrapper():
                print("Something before the function execution.")

                func()

                print("Something after the function execution.")

        return wrapper

@decorator
def f() -> None:
        print("Inside the function.")

f()