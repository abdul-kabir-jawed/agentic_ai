Python Decorators - Complete Guide
==================================

What are Decorators?
--------------------

A **decorator** is a design pattern in Python that allows you to modify or enhance functions and classes without permanently modifying their code. Think of decorators as "wrappers" that add extra functionality to your existing functions.

### Simple Analogy

Imagine you have a gift (your function). A decorator is like gift wrapping - it adds something extra around your gift without changing the gift itself.

Basic Syntax
------------

```
@decorator_name
def my_function():
    pass

```

This is equivalent to:

```
def my_function():
    pass
my_function = decorator_name(my_function)

```

How Decorators Work
-------------------

### Step 1: Understanding Functions as First-Class Objects

In Python, functions are objects that can be:

-   Assigned to variables
-   Passed as arguments
-   Returned from other functions

```
def greet():
    return "Hello!"

# Assign function to variable
my_func = greet
print(my_func())  # Output: Hello!

```

### Step 2: Functions Inside Functions

```
def outer_function():
    def inner_function():
        return "I'm inside!"
    return inner_function()

print(outer_function())  # Output: I'm inside!

```

### Step 3: Returning Functions from Functions

```
def outer_function():
    def inner_function():
        return "I'm inside!"
    return inner_function  # Return the function itself

my_func = outer_function()
print(my_func())  # Output: I'm inside!

```

Creating Your First Decorator
-----------------------------

### Basic Decorator Structure

```
def my_decorator(func):
    def wrapper():
        print("Something before the function")
        result = func()
        print("Something after the function")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# Usage
say_hello()

```

**Output:**

```
Something before the function
Hello!
Something after the function

```

Common Decorator Patterns
-------------------------

### 1\. Timing Decorator

```
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done!"

slow_function()  # Output: slow_function took 1.0041 seconds

```

### 2\. Logging Decorator

```
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        print(f"Arguments: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned: {result}")
        return result
    return wrapper

@logger
def add_numbers(a, b):
    return a + b

add_numbers(5, 3)

```

**Output:**

```
Calling function: add_numbers
Arguments: (5, 3), {}
Function add_numbers returned: 8

```

### 3\. Retry Decorator

```
import random

def retry(max_attempts=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed: {e}")
            return None
        return wrapper
    return decorator

@retry(max_attempts=3)
def unreliable_function():
    if random.random() < 0.7:  # 70% chance of failure
        raise Exception("Random failure!")
    return "Success!"

```

Decorators with Arguments
-------------------------

### Basic Parameterized Decorator

```
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))  # Output: ['Hello, Alice!', 'Hello, Alice!', 'Hello, Alice!']

```

Built-in Decorators
-------------------

### 1\. @property

```
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

# Usage
circle = Circle(5)
print(circle.radius)  # Output: 5
print(circle.area)    # Output: 78.53975
circle.radius = 10    # Uses setter

```

### 2\. @staticmethod and @classmethod

```
class MathUtils:
    pi = 3.14159

    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def get_pi(cls):
        return cls.pi

# Usage
print(MathUtils.add(5, 3))    # Output: 8
print(MathUtils.get_pi())     # Output: 3.14159

```

Advanced Decorator Concepts
---------------------------

### 1\. Preserving Function Metadata with functools.wraps

```
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserves original function's metadata
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def example_function():
    """This is an example function."""
    pass

print(example_function.__name__)  # Output: example_function
print(example_function.__doc__)   # Output: This is an example function.

```

### 2\. Class-based Decorators

```
class CountCalls:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def say_hello():
    print("Hello!")

say_hello()  # Output: Call 1 of say_hello \n Hello!
say_hello()  # Output: Call 2 of say_hello \n Hello!

```

### 3\. Multiple Decorators

```
def bold(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<b>{result}</b>"
    return wrapper

def italic(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<i>{result}</i>"
    return wrapper

@bold
@italic
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))  # Output: <b><i>Hello, World!</i></b>

```

Real-World Examples
-------------------

### 1\. Authentication Decorator

```
def require_auth(func):
    def wrapper(*args, **kwargs):
        # In a real app, you'd check actual authentication
        user_authenticated = True  # Simulate auth check

        if not user_authenticated:
            return "Access denied: Please log in"

        return func(*args, **kwargs)
    return wrapper

@require_auth
def sensitive_operation():
    return "Accessing sensitive data..."

```

### 2\. Cache Decorator

```
def cache(func):
    cached_results = {}

    def wrapper(*args, **kwargs):
        # Create a key from arguments
        key = str(args) + str(kwargs)

        if key in cached_results:
            print(f"Cache hit for {func.__name__}")
            return cached_results[key]

        print(f"Cache miss for {func.__name__}")
        result = func(*args, **kwargs)
        cached_results[key] = result
        return result

    return wrapper

@cache
def expensive_calculation(n):
    time.sleep(1)  # Simulate expensive operation
    return n * n

print(expensive_calculation(5))  # Cache miss, takes 1 second
print(expensive_calculation(5))  # Cache hit, instant

```

### 3\. Rate Limiting Decorator

```
import time
from collections import defaultdict

def rate_limit(max_calls_per_second=1):
    call_times = defaultdict(list)

    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.time()
            func_name = func.__name__

            # Remove old calls (older than 1 second)
            call_times[func_name] = [
                call_time for call_time in call_times[func_name]
                if now - call_time < 1
            ]

            if len(call_times[func_name]) >= max_calls_per_second:
                return "Rate limit exceeded. Try again later."

            call_times[func_name].append(now)
            return func(*args, **kwargs)

        return wrapper
    return decorator

@rate_limit(max_calls_per_second=2)
def api_call():
    return "API response"

```

Best Practices
--------------

### 1\. Use functools.wraps

Always use `@functools.wraps(func)` to preserve the original function's metadata.

### 2\. Handle Arguments Properly

Use `*args` and `**kwargs` to handle functions with different signatures.

### 3\. Keep It Simple

Don't make decorators too complex. If logic is getting complicated, consider using classes or separate functions.

### 4\. Make Decorators Reusable

Design decorators to work with different types of functions.

### 5\. Document Your Decorators

```
def my_decorator(func):
    """
    A decorator that does something useful.

    Args:
        func: The function to be decorated

    Returns:
        The wrapped function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # decorator logic here
        return func(*args, **kwargs)
    return wrapper

```

Common Pitfalls and Solutions
-----------------------------

### 1\. Forgetting to Return the Result

```
# Wrong
def bad_decorator(func):
    def wrapper():
        func()  # Missing return!
    return wrapper

# Correct
def good_decorator(func):
    def wrapper():
        return func()  # Return the result
    return wrapper

```

### 2\. Not Handling Arguments

```
# Wrong - only works with functions that take no arguments
def bad_decorator(func):
    def wrapper():
        return func()
    return wrapper

# Correct - works with any function
def good_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

```

### 3\. Losing Function Metadata

```
# Without @wraps, you lose the original function's name and docstring
from functools import wraps

def proper_decorator(func):
    @wraps(func)  # This preserves func's metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

```

Summary
-------

Decorators are a powerful Python feature that allow you to:

-   Add functionality to existing functions without modifying them
-   Keep your code DRY (Don't Repeat Yourself)
-   Implement cross-cutting concerns like logging, timing, authentication
-   Create reusable components

Remember: A decorator is just a function that takes another function as input and returns a modified version of that function. Once you understand this concept, decorators become much easier to create and use!

Quick Reference
---------------

```
# Basic decorator
def decorator(func):
    def wrapper(*args, **kwargs):
        # Do something before
        result = func(*args, **kwargs)
        # Do something after
        return result
    return wrapper

# Parameterized decorator
def decorator_with_params(param):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Use param here
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@decorator
def function1(): pass

@decorator_with_params("value")
def function2(): pass

```
