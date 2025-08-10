# Python Generics - Complete Guide

## What are Generics?

**Generics** are a way to write flexible, reusable code that can work with different types while maintaining type safety. They allow you to create classes, functions, and data structures that can handle any type, but in a type-safe way that helps catch errors early.

### Simple Analogy
Think of generics like a universal container:
- **Regular container** = A box labeled "only books" - can only hold books
- **Generic container** = A box labeled "T" - can hold books, toys, clothes, etc., but once you decide it holds books, it only holds books
- **Type parameter T** = A placeholder that gets replaced with the actual type (Book, Toy, Clothing)

## Why Use Generics?

1. **Type Safety** - Catch type errors at development time, not runtime
2. **Code Reusability** - Write once, use with many types
3. **Better Documentation** - Code clearly shows what types it expects
4. **IDE Support** - Better autocomplete and error detection
5. **Avoid Code Duplication** - Don't repeat similar code for different types

## Basic Type Hints (Foundation for Generics)

Before diving into generics, let's review basic type hints:

```python
from typing import List, Dict, Tuple, Optional, Union

# Basic types
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Collections with specific types
def process_numbers(numbers: List[int]) -> int:
    return sum(numbers)

def get_user_data() -> Dict[str, str]:
    return {"name": "John", "email": "john@example.com"}

# Optional and Union types
def find_user(user_id: int) -> Optional[str]:
    users = {1: "John", 2: "Jane"}
    return users.get(user_id)

def process_id(user_id: Union[int, str]) -> str:
    return str(user_id)
```

## Introduction to TypeVar

`TypeVar` is the foundation of generics in Python. It's a placeholder for a type:

```python
from typing import TypeVar, List

# Create a type variable
T = TypeVar('T')

def first_item(items: List[T]) -> T:
    """Return the first item from a list of any type"""
    return items[0]

# Usage - type checker knows the return type matches input type
numbers = [1, 2, 3, 4, 5]
first_number = first_item(numbers)  # Type: int

names = ["Alice", "Bob", "Charlie"]
first_name = first_item(names)      # Type: str

booleans = [True, False, True]
first_boolean = first_item(booleans) # Type: bool
```

## Generic Functions

### Basic Generic Functions

```python
from typing import TypeVar, List, Optional

T = TypeVar('T')

def safe_get(items: List[T], index: int) -> Optional[T]:
    """Safely get an item from a list by index"""
    if 0 <= index < len(items):
        return items[index]
    return None

def swap_items(items: List[T], i: int, j: int) -> List[T]:
    """Swap two items in a list"""
    items[i], items[j] = items[j], items[i]
    return items

def filter_none(items: List[Optional[T]]) -> List[T]:
    """Remove None values from a list"""
    return [item for item in items if item is not None]

# Usage examples
numbers = [1, 2, 3, 4, 5]
print(safe_get(numbers, 2))     # 3 (type: Optional[int])
print(safe_get(numbers, 10))    # None

names = ["Alice", "Bob", "Charlie"]
swapped = swap_items(names.copy(), 0, 2)
print(swapped)  # ["Charlie", "Bob", "Alice"]

mixed_data: List[Optional[str]] = ["hello", None, "world", None]
clean_data = filter_none(mixed_data)
print(clean_data)  # ["hello", "world"] (type: List[str])
```

### Multiple Type Variables

```python
from typing import TypeVar, Tuple, Dict, List

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def zip_with_function(
    list1: List[T], 
    list2: List[U], 
    func: callable[[T, U], V]
) -> List[V]:
    """Apply a function to pairs of items from two lists"""
    return [func(a, b) for a, b in zip(list1, list2)]

def create_pair(first: T, second: U) -> Tuple[T, U]:
    """Create a tuple pair from two values"""
    return (first, second)

def map_values(dictionary: Dict[T, U], func: callable[[U], V]) -> Dict[T, V]:
    """Apply a function to all values in a dictionary"""
    return {key: func(value) for key, value in dictionary.items()}

# Usage examples
numbers = [1, 2, 3, 4]
strings = ["a", "b", "c", "d"]

# Combine numbers and strings
combined = zip_with_function(numbers, strings, lambda n, s: f"{s}{n}")
print(combined)  # ["a1", "b2", "c3", "d4"]

# Create pairs
pair = create_pair(42, "hello")
print(pair)  # (42, "hello") - type: Tuple[int, str]

# Transform dictionary values
scores = {"Alice": 85, "Bob": 92, "Charlie": 78}
grades = map_values(scores, lambda score: "A" if score >= 90 else "B" if score >= 80 else "C")
print(grades)  # {"Alice": "B", "Bob": "A", "Charlie": "C"}
```

## Generic Classes

### Basic Generic Class

```python
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')

class Stack(Generic[T]):
    """A generic stack data structure"""
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        """Add an item to the top of the stack"""
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        """Remove and return the top item from the stack"""
        if self._items:
            return self._items.pop()
        return None
    
    def peek(self) -> Optional[T]:
        """Return the top item without removing it"""
        if self._items:
            return self._items[-1]
        return None
    
    def is_empty(self) -> bool:
        """Check if the stack is empty"""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Get the number of items in the stack"""
        return len(self._items)
    
    def __str__(self) -> str:
        return f"Stack({self._items})"

# Usage - type checker knows the stack type
int_stack = Stack[int]()
int_stack.push(1)
int_stack.push(2)
int_stack.push(3)
print(int_stack)  # Stack([1, 2, 3])
print(int_stack.pop())  # 3 (type: Optional[int])

string_stack = Stack[str]()
string_stack.push("hello")
string_stack.push("world")
print(string_stack.peek())  # "world" (type: Optional[str])
```

### Generic Class with Multiple Type Parameters

```python
from typing import TypeVar, Generic, Dict, List, Optional, Tuple

K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type

class Cache(Generic[K, V]):
    """A generic cache with key-value pairs"""
    
    def __init__(self, max_size: int = 100) -> None:
        self._data: Dict[K, V] = {}
        self._access_order: List[K] = []
        self._max_size = max_size
    
    def get(self, key: K) -> Optional[V]:
        """Get a value by key"""
        if key in self._data:
            # Move to end (most recently used)
            self._access_order.remove(key)
            self._access_order.append(key)
            return self._data[key]
        return None
    
    def put(self, key: K, value: V) -> None:
        """Store a key-value pair"""
        if key in self._data:
            # Update existing key
            self._access_order.remove(key)
        elif len(self._data) >= self._max_size:
            # Remove least recently used item
            oldest_key = self._access_order.pop(0)
            del self._data[oldest_key]
        
        self._data[key] = value
        self._access_order.append(key)
    
    def remove(self, key: K) -> bool:
        """Remove a key-value pair"""
        if key in self._data:
            del self._data[key]
            self._access_order.remove(key)
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cached items"""
        self._data.clear()
        self._access_order.clear()
    
    def items(self) -> List[Tuple[K, V]]:
        """Get all cached items as list of tuples"""
        return [(key, self._data[key]) for key in self._access_order]
    
    def size(self) -> int:
        """Get the number of cached items"""
        return len(self._data)

# Usage examples
# String to integer cache
user_scores = Cache[str, int](max_size=3)
user_scores.put("alice", 100)
user_scores.put("bob", 85)
user_scores.put("charlie", 92)
print(user_scores.get("alice"))  # 100

# Integer to string cache  
id_to_name = Cache[int, str]()
id_to_name.put(1, "John Doe")
id_to_name.put(2, "Jane Smith")
print(id_to_name.get(1))  # "John Doe"

# Complex type cache
user_data = Cache[str, Dict[str, any]]()
user_data.put("user123", {"name": "Alice", "age": 30, "active": True})
print(user_data.get("user123"))  # {"name": "Alice", "age": 30, "active": True}
```

## Bounded Type Variables

Sometimes you want to restrict what types can be used with your generic:

```python
from typing import TypeVar, Generic, Protocol, List
from abc import ABC, abstractmethod

# Bounded by a specific type
Number = TypeVar('Number', bound=float)

def average(numbers: List[Number]) -> Number:
    """Calculate average of numeric values"""
    return sum(numbers) / len(numbers)

# Usage - only works with numeric types
int_avg = average([1, 2, 3, 4, 5])        # Works: int is subclass of float
float_avg = average([1.5, 2.5, 3.5])      # Works: float
# str_avg = average(["a", "b", "c"])       # Error: str is not numeric

# Bounded by protocol/interface
class Comparable(Protocol):
    def __lt__(self, other) -> bool: ...
    def __eq__(self, other) -> bool: ...

T = TypeVar('T', bound=Comparable)

def sort_items(items: List[T]) -> List[T]:
    """Sort items that can be compared"""
    return sorted(items)

def find_min(items: List[T]) -> T:
    """Find minimum item that can be compared"""
    return min(items)

def find_max(items: List[T]) -> T:
    """Find maximum item that can be compared"""
    return max(items)

# Usage - works with any comparable type
numbers = [5, 2, 8, 1, 9]
print(sort_items(numbers))  # [1, 2, 5, 8, 9]

names = ["Charlie", "Alice", "Bob"]
print(find_min(names))      # "Alice"
print(find_max(names))      # "Charlie"

# Bounded by abstract base class
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

ShapeType = TypeVar('ShapeType', bound=Shape)

def total_area(shapes: List[ShapeType]) -> float:
    """Calculate total area of shapes"""
    return sum(shape.area() for shape in shapes)

def largest_shape(shapes: List[ShapeType]) -> ShapeType:
    """Find the shape with the largest area"""
    return max(shapes, key=lambda s: s.area())

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2

# Usage
rectangles = [Rectangle(3, 4), Rectangle(2, 6), Rectangle(5, 2)]
circles = [Circle(2), Circle(3), Circle(1)]

print(total_area(rectangles))  # 34.0
print(largest_shape(circles).radius)  # 3 (largest circle)
```

## Constrained Type Variables

You can constrain a type variable to a specific set of types:

```python
from typing import TypeVar, Union

# Constrained to specific types
NumberType = TypeVar('NumberType', int, float)

def multiply_by_two(value: NumberType) -> NumberType:
    """Multiply a number by two, preserving the number type"""
    return value * 2

# Usage
int_result = multiply_by_two(5)      # Returns int: 10
float_result = multiply_by_two(3.5)  # Returns float: 7.0
# str_result = multiply_by_two("hi")  # Error: str not allowed

# More complex constraint example
from decimal import Decimal

PreciseNumber = TypeVar('PreciseNumber', int, float, Decimal)

def calculate_compound_interest(
    principal: PreciseNumber, 
    rate: float, 
    years: int
) -> PreciseNumber:
    """Calculate compound interest preserving number precision"""
    return principal * ((1 + rate) ** years)

# Usage with different numeric types
int_interest = calculate_compound_interest(1000, 0.05, 5)  # int
float_interest = calculate_compound_interest(1000.0, 0.05, 5)  # float
decimal_interest = calculate_compound_interest(Decimal('1000'), 0.05, 5)  # Decimal
```

## Real-World Example 1: Generic Repository Pattern

```python
from typing import TypeVar, Generic, List, Optional, Dict, Any, Protocol
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json

# Define what our entities need
class Identifiable(Protocol):
    id: Any

T = TypeVar('T', bound=Identifiable)

class Repository(Generic[T], ABC):
    """Abstract base repository for CRUD operations"""
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity"""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: Any) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an existing entity"""
        pass
    
    @abstractmethod
    def delete(self, entity_id: Any) -> bool:
        """Delete an entity by ID"""
        pass
    
    @abstractmethod
    def find_by(self, **criteria) -> List[T]:
        """Find entities by criteria"""
        pass

class InMemoryRepository(Repository[T]):
    """In-memory implementation of repository"""
    
    def __init__(self) -> None:
        self._storage: Dict[Any, T] = {}
        self._next_id = 1
    
    def create(self, entity: T) -> T:
        if not hasattr(entity, 'id') or entity.id is None:
            entity.id = self._next_id
            self._next_id += 1
        self._storage[entity.id] = entity
        return entity
    
    def get_by_id(self, entity_id: Any) -> Optional[T]:
        return self._storage.get(entity_id)
    
    def get_all(self) -> List[T]:
        return list(self._storage.values())
    
    def update(self, entity: T) -> T:
        if entity.id in self._storage:
            self._storage[entity.id] = entity
            return entity
        raise ValueError(f"Entity with id {entity.id} not found")
    
    def delete(self, entity_id: Any) -> bool:
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False
    
    def find_by(self, **criteria) -> List[T]:
        results = []
        for entity in self._storage.values():
            match = True
            for key, value in criteria.items():
                if not hasattr(entity, key) or getattr(entity, key) != value:
                    match = False
                    break
            if match:
                results.append(entity)
        return results

# Domain entities
@dataclass
class User:
    name: str
    email: str
    age: int
    id: Optional[int] = None

@dataclass
class Product:
    name: str
    price: float
    category: str
    id: Optional[int] = None

@dataclass
class Order:
    user_id: int
    product_id: int
    quantity: int
    total: float
    id: Optional[int] = None

# Usage - type-safe repositories for different entities
user_repo = InMemoryRepository[User]()
product_repo = InMemoryRepository[Product]()
order_repo = InMemoryRepository[Order]()

# Create users
user1 = user_repo.create(User("Alice", "alice@example.com", 30))
user2 = user_repo.create(User("Bob", "bob@example.com", 25))

# Create products
product1 = product_repo.create(Product("Laptop", 999.99, "Electronics"))
product2 = product_repo.create(Product("Book", 19.99, "Books"))

# Create orders
order1 = order_repo.create(Order(user1.id, product1.id, 1, 999.99))
order2 = order_repo.create(Order(user2.id, product2.id, 2, 39.98))

# Query operations
print("All users:", user_repo.get_all())
print("Electronics:", product_repo.find_by(category="Electronics"))
print("User 1 orders:", order_repo.find_by(user_id=1))

# Type safety - this would be caught by type checker
# user_repo.create(Product("Invalid", 0.0, "Wrong"))  # Type error!
```

## Real-World Example 2: Generic API Response Handler

```python
from typing import TypeVar, Generic, Optional, List, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum
import json

T = TypeVar('T')

class ResponseStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"

@dataclass
class ApiResponse(Generic[T]):
    """Generic API response wrapper"""
    status: ResponseStatus
    data: Optional[T] = None
    message: Optional[str] = None
    errors: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @property
    def is_success(self) -> bool:
        return self.status == ResponseStatus.SUCCESS
    
    @property
    def is_error(self) -> bool:
        return self.status == ResponseStatus.ERROR
    
    def get_data_or_raise(self) -> T:
        """Get data or raise exception if response is error"""
        if self.is_error:
            raise ValueError(f"API Error: {self.message}")
        if self.data is None:
            raise ValueError("No data available")
        return self.data
    
    def get_data_or_default(self, default: T) -> T:
        """Get data or return default value"""
        return self.data if self.data is not None else default

class ApiClient(Generic[T]):
    """Generic API client for different data types"""
    
    def __init__(self, base_url: str, data_type: type):
        self.base_url = base_url
        self.data_type = data_type
    
    def get(self, endpoint: str) -> ApiResponse[T]:
        """Simulate GET request"""
        # In real implementation, this would make HTTP request
        return self._simulate_response()
    
    def post(self, endpoint: str, data: T) -> ApiResponse[T]:
        """Simulate POST request"""
        return self._simulate_response(data)
    
    def put(self, endpoint: str, data: T) -> ApiResponse[T]:
        """Simulate PUT request"""
        return self._simulate_response(data)
    
    def delete(self, endpoint: str) -> ApiResponse[bool]:
        """Simulate DELETE request"""
        return ApiResponse(
            status=ResponseStatus.SUCCESS,
            data=True,
            message="Resource deleted successfully"
        )
    
    def _simulate_response(self, data: Optional[T] = None) -> ApiResponse[T]:
        """Simulate API response (in real app, this would parse HTTP response)"""
        import random
        
        if random.random() > 0.8:  # 20% chance of error
            return ApiResponse(
                status=ResponseStatus.ERROR,
                message="Simulated API error",
                errors=["Connection timeout", "Invalid request"]
            )
        
        return ApiResponse(
            status=ResponseStatus.SUCCESS,
            data=data,
            message="Request successful",
            metadata={"timestamp": "2025-01-15T10:00:00Z", "request_id": "12345"}
        )

# Specific data models
@dataclass
class UserProfile:
    id: int
    name: str
    email: str
    avatar_url: str

@dataclass
class BlogPost:
    id: int
    title: str
    content: str
    author_id: int
    published_at: str

@dataclass
class ProductInfo:
    id: int
    name: str
    price: float
    description: str
    in_stock: bool

# Usage - type-safe API clients
user_client = ApiClient[UserProfile]("https://api.example.com", UserProfile)
blog_client = ApiClient[BlogPost]("https://blog.example.com", BlogPost)
product_client = ApiClient[ProductInfo]("https://shop.example.com", ProductInfo)

# Example usage with error handling
def get_user_safely(user_id: int) -> Optional[UserProfile]:
    """Safely get user with proper error handling"""
    try:
        response = user_client.get(f"/users/{user_id}")
        
        if response.is_success:
            return response.get_data_or_raise()
        else:
            print(f"Failed to get user: {response.message}")
            if response.errors:
                for error in response.errors:
                    print(f"  - {error}")
            return None
            
    except ValueError as e:
        print(f"Error getting user: {e}")
        return None

def create_blog_post(post_data: BlogPost) -> bool:
    """Create a blog post with error handling"""
    response = blog_client.post("/posts", post_data)
    
    if response.is_success:
        print(f"Blog post created successfully: {response.message}")
        return True
    else:
        print(f"Failed to create blog post: {response.message}")
        return False

# Batch operations with generics
def batch_process(items: List[T], processor: callable[[T], ApiResponse[T]]) -> List[T]:
    """Process a batch of items and return successful results"""
    successful_results = []
    
    for item in items:
        response = processor(item)
        if response.is_success and response.data:
            successful_results.append(response.data)
    
    return successful_results

# Usage examples
user = get_user_safely(123)
if user:
    print(f"Got user: {user.name} ({user.email})")

new_post = BlogPost(0, "My First Post", "Hello World!", 123, "2025-01-15")
success = create_blog_post(new_post)
```

## Advanced Generic Patterns

### Generic Decorators

```python
from typing import TypeVar, Callable, Any
from functools import wraps
import time

F = TypeVar('F', bound=Callable[..., Any])

def timer(func: F) -> F:
    """Generic decorator that preserves function signature"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def retry(max_attempts: int = 3):
    """Generic retry decorator"""
    def decorator(func: F) -> F:
        @wraps(func)
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

# Usage - decorators maintain type information
@timer
@retry(max_attempts=3)
def fetch_data(url: str) -> Dict[str, Any]:
    # Simulate API call that might fail
    import random
    if random.random() < 0.3:  # 30% chance of failure
        raise Exception("Network error")
    return {"data": "success", "url": url}

# Type checker knows this returns Dict[str, Any]
result = fetch_data("https://api.example.com/data")
```

### Generic Context Managers

```python
from typing import TypeVar, Generic, ContextManager, Optional
from contextlib import contextmanager

T = TypeVar('T')

class ResourceManager(Generic[T]):
    """Generic resource manager with automatic cleanup"""
    
    def __init__(self, resource: T, cleanup_func: Optional[Callable[[T], None]] = None):
        self.resource = resource
        self.cleanup_func = cleanup_func
        self.is_active = False
    
    def __enter__(self) -> T:
        self.is_active = True
        return self.resource
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.is_active = False
        if self.cleanup_func:
            self.cleanup_func(self.resource)

# Usage examples
class DatabaseConnection:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False
    
    def connect(self):
        self.connected = True
        print(f"Connected to {self.connection_string}")
    
    def disconnect(self):
        self.connected = False
        print("Disconnected from database")
    
    def execute(self, query: str):
        if not self.connected:
            raise Exception("Not connected to database")
        print(f"Executing: {query}")

def cleanup_db(db: DatabaseConnection):
    db.disconnect()

# Use generic resource manager
db = DatabaseConnection("postgresql://localhost:5432/mydb")
db.connect()

with ResourceManager(db, cleanup_db) as database:
    database.execute("SELECT * FROM users")
    # Database automatically disconnected when exiting context
```

## Working with Built-in Generic Types

### List, Dict, Set, Tuple

```python
from typing import List, Dict, Set, Tuple, Optional

# Generic functions with built-in types
def merge_dictionaries(dict1: Dict[str, int], dict2: Dict[str, int]) -> Dict[str, int]:
    """Merge two dictionaries, summing values for duplicate keys"""
    result = dict1.copy()
    for key, value in dict2.items():
        result[key] = result.get(key, 0) + value
    return result

def unique_items(items: List[T]) -> Set[T]:
    """Get unique items from a list"""
    return set(items)

def group_by_length(strings: List[str]) -> Dict[int, List[str]]:
    """Group strings by their length"""
    groups: Dict[int, List[str]] = {}
    for string in strings:
        length = len(string)
        if length not in groups:
            groups[length] = []
        groups[length].append(string)
    return groups

def tuple_operations(data: List[Tuple[str, int]]) -> Tuple[List[str], List[int]]:
    """Separate tuple data into two lists"""
    names = [item[0] for item in data]
    numbers = [item[1] for item in data]
    return (names, numbers)

# Usage
scores1 = {"Alice": 85, "Bob": 90}
scores2 = {"Alice": 15, "Charlie": 95}
merged = merge_dictionaries(scores1, scores2)  # {"Alice": 100, "Bob": 90, "Charlie": 95}

numbers = [1, 2, 2, 3, 3, 3, 4]
unique_numbers = unique_items(numbers)  # {1, 2, 3, 4}

words = ["hi", "hello", "world", "python", "code"]
by_length = group_by_length(words)  # {2: ["hi"], 5: ["hello", "world"], 6: ["python"], 4: ["code"]}
```

### Advanced Generic Collections

```python
from typing import TypeVar, Generic, List, Dict, Optional, Callable, Iterator
from collections import defaultdict

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class MultiDict(Generic[K, V]):
    """Dictionary that can store multiple values per key"""
    
    def __init__(self):
        self._data: Dict[K, List[V]] = defaultdict(list)
    
    def add(self, key: K, value: V) -> None:
        """Add a value to the key (multiple values allowed)"""
        self._data[key].append(value)
    
    def get(self, key: K) -> List[V]:
        """Get all values for a key"""
        return self._data.get(key, [])
    
    def get_first(self, key: K) -> Optional[V]:
        """Get the first value for a key"""
        values = self._data.get(key, [])
        return values[0] if values else None
    
    def remove(self, key: K, value: V) -> bool:
        """Remove a specific value from a key"""
        if key in self._data and value in self._data[key]:
            self._data[key].remove(value)
            if not self._data[key]:  # Remove empty list
                del self._data[key]
            return True
        return False
    
    def keys(self) -> Iterator[K]:
        """Get all keys"""
        return iter(self._data.keys())
    
    def items(self) -> Iterator[tuple[K, List[V]]]:
        """Get all key-value pairs"""
        return iter(self._data.items())
    
    def __len__(self) -> int:
        return len(self._data)

# Usage
contacts = MultiDict[str, str]()
contacts.add("phone", "555-1234")
contacts.add("phone", "555-5678")
contacts.add("email", "user@example.com")

print(contacts.get("phone"))      # ["555-1234", "555-5678"]
print(contacts.get_first("email")) # "user@example.com"

class EventBus(Generic[T]):
    """Generic event bus for publishing and subscribing to events"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[T], None]]] = defaultdict(list)
    
    def subscribe(self, event_type: str, callback: Callable[[T], None]) -> None:
        """Subscribe to an event type"""
        self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable[[T], None]) -> bool:
        """Unsubscribe from an event type"""
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
            return True
        return False
    
    def publish(self, event_type: str, event_data: T) -> None:
        """Publish an event to all subscribers"""
        for callback in self._subscribers.get(event_type, []):
            try:
                callback(event_data)
            except Exception as e:
                print(f"Error in event handler: {e}")
    
    def get_subscriber_count(self, event_type: str) -> int:
        """Get number of subscribers for an event type"""
        return len(self._subscribers.get(event_type, []))

# Usage with different event types
@dataclass
class UserEvent:
    user_id: int
    action: str
    timestamp: str

@dataclass
class OrderEvent:
    order_id: int
    customer_id: int
    total: float
    status: str

# Create event buses for different event types
user_bus = EventBus[UserEvent]()
order_bus = EventBus[OrderEvent]()

def handle_user_login(event: UserEvent):
    print(f"User {event.user_id} logged in at {event.timestamp}")

def handle_order_placed(event: OrderEvent):
    print(f"Order {event.order_id} placed by customer {event.customer_id} for ${event.total}")

# Subscribe to events
user_bus.subscribe("login", handle_user_login)
order_bus.subscribe("placed", handle_order_placed)

# Publish events
user_bus.publish("login", UserEvent(123, "login", "2025-01-15T10:00:00Z"))
order_bus.publish("placed", OrderEvent(456, 123, 99.99, "pending"))
```

## Generic Protocols and Interfaces

```python
from typing import TypeVar, Generic, Protocol, runtime_checkable

T = TypeVar('T')

@runtime_checkable
class Serializable(Protocol[T]):
    """Protocol for objects that can be serialized"""
    
    def serialize(self) -> str:
        """Convert object to string representation"""
        ...
    
    @classmethod
    def deserialize(cls, data: str) -> T:
        """Create object from string representation"""
        ...

@runtime_checkable
class Comparable(Protocol):
    """Protocol for objects that can be compared"""
    
    def __lt__(self, other) -> bool: ...
    def __eq__(self, other) -> bool: ...

# Generic functions that work with protocols
def save_to_file(obj: Serializable[T], filename: str) -> None:
    """Save any serializable object to file"""
    with open(filename, 'w') as f:
        f.write(obj.serialize())

def load_from_file(cls: type[Serializable[T]], filename: str) -> T:
    """Load any serializable object from file"""
    with open(filename, 'r') as f:
        data = f.read()
        return cls.deserialize(data)

def sort_generic(items: List[Comparable]) -> List[Comparable]:
    """Sort any comparable items"""
    return sorted(items)

# Implementations
@dataclass
class Person:
    name: str
    age: int
    email: str
    
    def serialize(self) -> str:
        import json
        return json.dumps({
            "name": self.name,
            "age": self.age,
            "email": self.email
        })
    
    @classmethod
    def deserialize(cls, data: str) -> 'Person':
        import json
        obj_data = json.loads(data)
        return cls(**obj_data)
    
    def __lt__(self, other: 'Person') -> bool:
        return self.age < other.age
    
    def __eq__(self, other: 'Person') -> bool:
        return self.age == other.age

# Usage
person = Person("Alice", 30, "alice@example.com")
save_to_file(person, "person.json")
loaded_person = load_from_file(Person, "person.json")

people = [Person("Alice", 30, ""), Person("Bob", 25, ""), Person("Charlie", 35, "")]
sorted_people = sort_generic(people)  # Sorted by age
```

## Error Handling with Generics

```python
from typing import TypeVar, Generic, Union, Optional, Callable
from enum import Enum
from dataclasses import dataclass

T = TypeVar('T')
E = TypeVar('E')

class ResultType(Enum):
    SUCCESS = "success"
    ERROR = "error"

@dataclass
class Result(Generic[T, E]):
    """Generic Result type for error handling without exceptions"""
    
    type: ResultType
    value: Optional[T] = None
    error: Optional[E] = None
    
    @classmethod
    def success(cls, value: T) -> 'Result[T, E]':
        """Create a successful result"""
        return cls(ResultType.SUCCESS, value=value)
    
    @classmethod
    def error(cls, error: E) -> 'Result[T, E]':
        """Create an error result"""
        return cls(ResultType.ERROR, error=error)
    
    @property
    def is_success(self) -> bool:
        return self.type == ResultType.SUCCESS
    
    @property
    def is_error(self) -> bool:
        return self.type == ResultType.ERROR
    
    def unwrap(self) -> T:
        """Get the value or raise exception if error"""
        if self.is_error:
            raise ValueError(f"Result is error: {self.error}")
        return self.value
    
    def unwrap_or(self, default: T) -> T:
        """Get the value or return default if error"""
        return self.value if self.is_success else default
    
    def map(self, func: Callable[[T], U]) -> 'Result[U, E]':
        """Transform the value if success, otherwise return error"""
        if self.is_success:
            try:
                new_value = func(self.value)
                return Result.success(new_value)
            except Exception as e:
                return Result.error(e)
        return Result.error(self.error)
    
    def and_then(self, func: Callable[[T], 'Result[U, E]']) -> 'Result[U, E]':
        """Chain operations that return Results"""
        if self.is_success:
            return func(self.value)
        return Result.error(self.error)

U = TypeVar('U')

# Usage examples
def divide(a: float, b: float) -> Result[float, str]:
    """Safe division that returns Result instead of raising exception"""
    if b == 0:
        return Result.error("Division by zero")
    return Result.success(a / b)

def parse_int(s: str) -> Result[int, str]:
    """Safe integer parsing"""
    try:
        return Result.success(int(s))
    except ValueError:
        return Result.error(f"Cannot parse '{s}' as integer")

def sqrt(x: float) -> Result[float, str]:
    """Safe square root"""
    if x < 0:
        return Result.error("Cannot take square root of negative number")
    return Result.success(x ** 0.5)

# Chain operations safely
def calculate_result(a_str: str, b_str: str) -> Result[float, str]:
    """Parse two strings, divide them, and take square root"""
    return (parse_int(a_str)
            .and_then(lambda a: parse_int(b_str)
                     .and_then(lambda b: divide(float(a), float(b))))
            .and_then(lambda result: sqrt(result)))

# Usage
result1 = calculate_result("16", "4")  # Success: 2.0
result2 = calculate_result("16", "0")  # Error: Division by zero
result3 = calculate_result("abc", "4") # Error: Cannot parse 'abc' as integer

print("Result 1:", result1.unwrap_or(-1))  # 2.0
print("Result 2:", result2.unwrap_or(-1))  # -1 (default)
print("Result 3:", result3.unwrap_or(-1))  # -1 (default)

if result1.is_success:
    print("Calculation succeeded:", result1.value)
if result2.is_error:
    print("Calculation failed:", result2.error)
```

## Generic Builders and Factories

```python
from typing import TypeVar, Generic, Dict, Any, Callable, Optional
from abc import ABC, abstractmethod

T = TypeVar('T')

class Builder(Generic[T], ABC):
    """Abstract generic builder"""
    
    @abstractmethod
    def build(self) -> T:
        """Build and return the final object"""
        pass
    
    @abstractmethod
    def reset(self) -> 'Builder[T]':
        """Reset builder to initial state"""
        pass

class FluentBuilder(Builder[T]):
    """Fluent interface builder for any object"""
    
    def __init__(self, target_class: type, **initial_values):
        self.target_class = target_class
        self.values: Dict[str, Any] = initial_values.copy()
    
    def set(self, key: str, value: Any) -> 'FluentBuilder[T]':
        """Set a property value"""
        self.values[key] = value
        return self
    
    def when(self, condition: bool, action: Callable[['FluentBuilder[T]'], 'FluentBuilder[T]']) -> 'FluentBuilder[T]':
        """Conditionally apply an action"""
        if condition:
            return action(self)
        return self
    
    def build(self) -> T:
        """Build the final object"""
        return self.target_class(**self.values)
    
    def reset(self) -> 'FluentBuilder[T]':
        """Reset to initial values"""
        self.values.clear()
        return self

# Example domain objects
@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "mydb"
    username: str = "user"
    password: str = "password"
    ssl_enabled: bool = False
    timeout: int = 30
    pool_size: int = 10

@dataclass
class EmailTemplate:
    subject: str
    body: str
    sender: str = "noreply@example.com"
    template_type: str = "html"
    attachments: List[str] = None

# Usage - fluent builders
db_config = (FluentBuilder(DatabaseConfig)
    .set("host", "production.db.com")
    .set("port", 5432)
    .set("database", "prod_db")
    .when(True, lambda b: b.set("ssl_enabled", True))  # Conditional setting
    .when(False, lambda b: b.set("timeout", 60))       # Won't execute
    .set("pool_size", 20)
    .build())

email_template = (FluentBuilder(EmailTemplate)
    .set("subject", "Welcome to our service!")
    .set("body", "<h1>Welcome!</h1><p>Thanks for joining us.</p>")
    .set("template_type", "html")
    .build())

print("DB Config:", db_config)
print("Email Template:", email_template)

# Generic Factory
class Factory(Generic[T]):
    """Generic factory for creating objects"""
    
    def __init__(self):
        self._creators: Dict[str, Callable[..., T]] = {}
        self._default_creator: Optional[Callable[..., T]] = None
    
    def register(self, name: str, creator: Callable[..., T]) -> None:
        """Register a creator function"""
        self._creators[name] = creator
    
    def set_default(self, creator: Callable[..., T]) -> None:
        """Set default creator"""
        self._default_creator = creator
    
    def create(self, name: str, *args, **kwargs) -> T:
        """Create object by name"""
        if name in self._creators:
            return self._creators[name](*args, **kwargs)
        elif self._default_creator:
            return self._default_creator(*args, **kwargs)
        else:
            raise ValueError(f"No creator registered for '{name}'")
    
    def available_types(self) -> List[str]:
        """Get list of available creator names"""
        return list(self._creators.keys())

# Usage - database connection factory
class DatabaseConnection:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False

def create_postgres_connection(host: str, database: str) -> DatabaseConnection:
    conn_str = f"postgresql://{host}:5432/{database}"
    return DatabaseConnection(conn_str)

def create_mysql_connection(host: str, database: str) -> DatabaseConnection:
    conn_str = f"mysql://{host}:3306/{database}"
    return DatabaseConnection(conn_str)

def create_sqlite_connection(database_file: str) -> DatabaseConnection:
    conn_str = f"sqlite:///{database_file}"
    return DatabaseConnection(conn_str)

# Create factory and register creators
db_factory = Factory[DatabaseConnection]()
db_factory.register("postgres", create_postgres_connection)
db_factory.register("mysql", create_mysql_connection)
db_factory.register("sqlite", create_sqlite_connection)

# Create different types of connections
postgres_db = db_factory.create("postgres", "localhost", "myapp")
mysql_db = db_factory.create("mysql", "db.server.com", "production")
sqlite_db = db_factory.create("sqlite", "local.db")

print("Available database types:", db_factory.available_types())
```

## Best Practices for Generics

### 1. Use Meaningful Type Variable Names

```python
# Good: Descriptive type variable names
K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type
T = TypeVar('T')  # Generic type
E = TypeVar('E')  # Error type

class Cache(Generic[K, V]):
    def get(self, key: K) -> Optional[V]: ...
    def put(self, key: K, value: V) -> None: ...

# Bad: Non-descriptive names
A = TypeVar('A')
B = TypeVar('B')

class Cache(Generic[A, B]):  # What are A and B?
    def get(self, key: A) -> Optional[B]: ...
```

### 2. Document Generic Types

```python
from typing import TypeVar, Generic, List

T = TypeVar('T', bound='Comparable')

class SortedList(Generic[T]):
    """
    A list that maintains items in sorted order.
    
    Type Parameters:
        T: The type of items stored in the list. Must be comparable
           (support < and == operators).
    
    Example:
        >>> numbers = SortedList[int]()
        >>> numbers.add(5)
        >>> numbers.add(2)
        >>> numbers.get_all()  # Returns [2, 5]
    """
    
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        """Add an item maintaining sorted order"""
        # Binary search insertion logic here
        self._items.append(item)
        self._items.sort()
    
    def get_all(self) -> List[T]:
        """Get all items in sorted order"""
        return self._items.copy()
```

### 3. Use Bounds and Constraints Appropriately

```python
from typing import TypeVar, Protocol

# Good: Use bounds when you need specific capabilities
class Addable(Protocol):
    def __add__(self, other): ...

Summable = TypeVar('Summable', bound=Addable)

def sum_items(items: List[Summable]) -> Summable:
    """Sum items that support addition"""
    result = items[0]
    for item in items[1:]:
        result = result + item
    return result

# Good: Use constraints for specific types
NumberType = TypeVar('NumberType', int, float, complex)

def multiply(a: NumberType, b: NumberType) -> NumberType:
    """Multiply two numbers of the same type"""
    return a * b
```

### 4. Avoid Over-Generification

```python
# Bad: Over-generified for simple use case
T = TypeVar('T')
def simple_greeting(name: T) -> str:
    return f"Hello, {name}!"

# Good: Just use the specific type
def simple_greeting(name: str) -> str:
    return f"Hello, {name}!"

# Good: Use generics when there's real benefit
T = TypeVar('T')
def safe_head(items: List[T]) -> Optional[T]:
    """Get first item from list of any type"""
    return items[0] if items else None
```

### 5. Provide Clear Error Messages

```python
from typing import TypeVar, List, Union

T = TypeVar('T')

def validate_non_empty_list(items: List[T], name: str = "items") -> List[T]:
    """Validate that a list is not empty"""
    if not items:
        raise ValueError(f"{name} cannot be empty")
    return items

def process_batch(items: List[T]) -> List[T]:
    """Process a batch of items"""
    validated_items = validate_non_empty_list(items, "batch items")
    # Processing logic here
    return validated_items
```

## Common Pitfalls and Solutions

### 1. Runtime Type Checking

```python
# Wrong: Generics don't provide runtime type checking
def add_to_list(items: List[int], item: str) -> None:
    items.append(item)  # This will run but is type-unsafe

# Solution: Use isinstance for runtime validation
def safe_add_to_list(items: List[T], item: T, expected_type: type) -> None:
    if not isinstance(item, expected_type):
        raise TypeError(f"Expected {expected_type}, got {type(item)}")
    items.append(item)
```

### 2. Mutable Default Arguments

```python
from typing import TypeVar, List, Optional

T = TypeVar('T')

# Wrong: Mutable default argument
def process_items(items: Optional[List[T]] = []) -> List[T]:
    if items is None:
        items = []
    return items

# Correct: Use None as default
def process_items(items: Optional[List[T]] = None) -> List[T]:
    if items is None:
        items = []
    return items
```

### 3. Variance Issues

```python
from typing import TypeVar, List, Generic

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, item: T):
        self.item = item

# This might seem like it should work, but doesn't
def process_containers(containers: List[Container[object]]) -> None:
    pass

# This won't work due to invariance
string_containers: List[Container[str]] = [Container("hello")]
# process_containers(string_containers)  # Type error!

# Solution: Use covariant type variables when appropriate
T_co = TypeVar('T_co', covariant=True)

class ReadOnlyContainer(Generic[T_co]):
    def __init__(self, item: T_co):
        self._item = item
    
    def get(self) -> T_co:
        return self._item
```

## Summary

**Python Generics are powerful for:**
- **Type Safety** - Catch errors early with static type checking
- **Code Reusability** - Write functions and classes that work with multiple types
- **Better Documentation** - Make code intentions clear
- **IDE Support** - Get better autocomplete and error detection
- **Maintainability** - Easier to refactor and understand code

**Key Components:**
1. **TypeVar** - Create type variables for generic functions and classes
2. **Generic[T]** - Make classes generic by inheriting from Generic
3. **Bounds and Constraints** - Limit which types can be used
4. **Protocols** - Define interfaces for structural typing
5. **Built-in Generic Types** - List[T], Dict[K, V], Optional[T], etc.

**Best Practices:**
- Use meaningful type variable names (K, V, T, E)
- Document your generic types clearly
- Use bounds when you need specific capabilities
- Don't over-generify simple cases
- Provide clear error messages
- Be aware of variance (covariant/contravariant)

**Quick Reference:**
```python
from typing import TypeVar, Generic, List, Optional

# Basic type variable
T = TypeVar('T')

# Generic function
def first_item(items: List[T]) -> Optional[T]:
    return items[0] if items else None

# Generic class
class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> Optional[T]:
        return self._items.pop() if self._items else None

# Usage
numbers = first_item([1, 2, 3])  # Type: Optional[int]
int_stack = Stack[int]()         # Type: Stack[int]
```

Generics make Python code more robust, reusable, and maintainable while providing excellent tooling support!
