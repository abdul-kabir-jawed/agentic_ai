# Python Class Methods - Complete Guide

## What are Class Methods?

A **class method** is a method that belongs to the class itself rather than to any specific instance. It receives the class (usually called `cls`) as its first argument instead of an instance (`self`). Class methods can access and modify class-level attributes and create new instances of the class.

### Simple Analogy
Think of a class as a blueprint for houses:
- **Instance methods** = actions you do with a specific house (paint this house, lock this door)
- **Class methods** = actions you do with the blueprint itself (create a new house from blueprint, modify the blueprint design)
- **Static methods** = general construction tools that work regardless of the blueprint

## Basic Syntax

```python
class MyClass:
    class_variable = "I belong to the class"
    
    @classmethod
    def my_class_method(cls):
        return f"This is a class method of {cls.__name__}"

# Called on the class (most common)
result = MyClass.my_class_method()

# Can also be called on an instance
obj = MyClass()
result = obj.my_class_method()  # Same result, but cls still refers to the class
```

## The Three Types of Methods - Side by Side

```python
class Example:
    class_count = 0  # Class variable
    
    def __init__(self, name):
        self.name = name  # Instance variable
        Example.class_count += 1
    
    # Instance Method - needs 'self', works with instance data
    def instance_method(self):
        return f"Instance method called by {self.name}"
    
    # Class Method - needs 'cls', works with class data
    @classmethod
    def class_method(cls):
        return f"Class method called. Total instances: {cls.class_count}"
    
    # Static Method - needs neither, independent function
    @staticmethod
    def static_method():
        return "Static method called. No access to instance or class data"

# Usage examples
obj1 = Example("Alice")
obj2 = Example("Bob")

print(obj1.instance_method())    # Instance method called by Alice
print(Example.class_method())    # Class method called. Total instances: 2
print(Example.static_method())   # Static method called. No access to instance or class data
```

## When to Use Class Methods

Use class methods when you need to:
1. **Create alternative constructors** (factory methods)
2. **Access or modify class-level data**
3. **Work with the class itself, not instances**
4. **Create instances in different ways**

## Alternative Constructors (Factory Methods)

This is the most common use case for class methods:

### Example 1: Person Class with Multiple Constructors

```python
from datetime import datetime

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"Person(name='{self.name}', age={self.age})"
    
    # Alternative constructor: create from birth year
    @classmethod
    def from_birth_year(cls, name, birth_year):
        current_year = datetime.now().year
        age = current_year - birth_year
        return cls(name, age)  # cls() calls the main constructor
    
    # Alternative constructor: create from string
    @classmethod
    def from_string(cls, person_string):
        # Parse "John-25" format
        name, age_str = person_string.split('-')
        age = int(age_str)
        return cls(name, age)
    
    # Alternative constructor: create adult (default age)
    @classmethod
    def create_adult(cls, name):
        return cls(name, 18)

# Usage - multiple ways to create Person objects
person1 = Person("Alice", 30)                           # Regular constructor
person2 = Person.from_birth_year("Bob", 1990)          # From birth year
person3 = Person.from_string("Charlie-25")             # From string
person4 = Person.create_adult("Diana")                 # Default adult

print(person1)  # Person(name='Alice', age=30)
print(person2)  # Person(name='Bob', age=34)
print(person3)  # Person(name='Charlie', age=25)
print(person4)  # Person(name='Diana', age=18)
```

### Example 2: Configuration Class

```python
import json
import os

class DatabaseConfig:
    def __init__(self, host, port, database, username, password):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
    
    def get_connection_string(self):
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    # Create from JSON file
    @classmethod
    def from_json_file(cls, filepath):
        with open(filepath, 'r') as file:
            config_data = json.load(file)
        return cls(**config_data)  # Unpack dictionary as arguments
    
    # Create from environment variables
    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', 'mydb'),
            username=os.getenv('DB_USER', 'admin'),
            password=os.getenv('DB_PASS', 'password')
        )
    
    # Create for local development
    @classmethod
    def for_development(cls):
        return cls('localhost', 5432, 'dev_db', 'dev_user', 'dev_pass')
    
    # Create for production
    @classmethod
    def for_production(cls, host, database):
        return cls(host, 5432, database, 'prod_user', 'secure_password')

# Usage - different ways to create config
dev_config = DatabaseConfig.for_development()
prod_config = DatabaseConfig.for_production('prod.server.com', 'prod_db')
env_config = DatabaseConfig.from_env()

print(dev_config.get_connection_string())
```

## Working with Class Variables

```python
class Counter:
    total_count = 0  # Class variable shared by all instances
    
    def __init__(self, name):
        self.name = name
        Counter.increment_count()  # Update class variable
    
    @classmethod
    def increment_count(cls):
        cls.total_count += 1
    
    @classmethod
    def reset_count(cls):
        cls.total_count = 0
    
    @classmethod
    def get_count(cls):
        return cls.total_count
    
    def __str__(self):
        return f"Counter '{self.name}' (Total: {self.total_count})"

# Usage
print(Counter.get_count())  # 0

counter1 = Counter("First")
counter2 = Counter("Second")
counter3 = Counter("Third")

print(Counter.get_count())  # 3
print(counter1)             # Counter 'First' (Total: 3)

Counter.reset_count()
print(Counter.get_count())  # 0
```

## Class Methods in Inheritance

Class methods work beautifully with inheritance because `cls` refers to the actual class being called:

```python
class Animal:
    species_count = 0
    
    def __init__(self, name):
        self.name = name
        self.__class__.species_count += 1  # Increment for the specific class
    
    @classmethod
    def get_species_count(cls):
        return f"{cls.__name__}: {cls.species_count} animals"
    
    @classmethod
    def create_random_animal(cls):
        import random
        names = ["Buddy", "Max", "Luna", "Charlie", "Bella"]
        return cls(random.choice(names))

class Dog(Animal):
    species_count = 0  # Separate counter for dogs
    
    def bark(self):
        return f"{self.name} says Woof!"
    
    @classmethod
    def create_guard_dog(cls):
        return cls("Rex")

class Cat(Animal):
    species_count = 0  # Separate counter for cats
    
    def meow(self):
        return f"{self.name} says Meow!"
    
    @classmethod
    def create_house_cat(cls):
        return cls("Whiskers")

# Usage - each class maintains its own count
dog1 = Dog("Buddy")
dog2 = Dog.create_guard_dog()
cat1 = Cat("Luna")
cat2 = Cat.create_house_cat()

print(Dog.get_species_count())    # Dog: 2 animals
print(Cat.get_species_count())    # Cat: 2 animals
print(Animal.get_species_count()) # Animal: 0 animals (base class not used directly)

# Class methods return the correct type
random_dog = Dog.create_random_animal()  # Returns a Dog instance
print(type(random_dog))  # <class '__main__.Dog'>
print(random_dog.bark()) # Works because it's a Dog
```

## Real-World Examples

### Example 1: User Management System

```python
from datetime import datetime, timedelta
import hashlib
import uuid

class User:
    active_users = []  # Class variable to track active users
    
    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.now()
        self.last_login = None
        self.is_active = True
        User.active_users.append(self)
    
    @classmethod
    def create_user(cls, username, email, password):
        """Create a new user with hashed password"""
        password_hash = cls._hash_password(password)
        return cls(username, email, password_hash)
    
    @classmethod
    def create_admin_user(cls, username, email):
        """Create an admin user with default credentials"""
        default_password = str(uuid.uuid4())[:8]  # Random 8-char password
        user = cls.create_user(username, email, default_password)
        user.is_admin = True
        print(f"Admin user created. Temporary password: {default_password}")
        return user
    
    @classmethod
    def from_csv_row(cls, csv_row):
        """Create user from CSV data"""
        username, email, password = csv_row.strip().split(',')
        return cls.create_user(username, email, password)
    
    @classmethod
    def get_active_users_count(cls):
        """Get count of currently active users"""
        return len([user for user in cls.active_users if user.is_active])
    
    @classmethod
    def get_users_created_today(cls):
        """Get users created today"""
        today = datetime.now().date()
        return [user for user in cls.active_users 
                if user.created_at.date() == today]
    
    @classmethod
    def cleanup_inactive_users(cls):
        """Remove users inactive for more than 30 days"""
        cutoff_date = datetime.now() - timedelta(days=30)
        inactive_users = [user for user in cls.active_users 
                         if user.last_login and user.last_login < cutoff_date]
        
        for user in inactive_users:
            user.is_active = False
        
        return len(inactive_users)
    
    @staticmethod
    def _hash_password(password):
        """Hash a password (simple example - use proper hashing in production)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        self.last_login = datetime.now()
        return f"User {self.username} logged in successfully"
    
    def __str__(self):
        return f"User(username='{self.username}', email='{self.email}')"

# Usage examples
# Different ways to create users
user1 = User.create_user("john_doe", "john@example.com", "mypassword")
user2 = User.create_admin_user("admin", "admin@example.com")
user3 = User.from_csv_row("jane_doe,jane@example.com,password123")

# Class-level operations
print(f"Active users: {User.get_active_users_count()}")
print(f"Users created today: {len(User.get_users_created_today())}")

user1.login()
user2.login()

inactive_count = User.cleanup_inactive_users()
print(f"Cleaned up {inactive_count} inactive users")
```

### Example 2: Product Catalog System

```python
class Product:
    all_products = []  # Class variable to store all products
    next_id = 1       # Class variable for auto-incrementing IDs
    
    def __init__(self, name, price, category):
        self.id = Product.next_id
        Product.next_id += 1
        self.name = name
        self.price = price
        self.category = category
        Product.all_products.append(self)
    
    @classmethod
    def create_book(cls, title, price, author):
        """Factory method for creating books"""
        name = f"{title} by {author}"
        return cls(name, price, "Books")
    
    @classmethod
    def create_electronics(cls, name, price, brand):
        """Factory method for electronics"""
        name = f"{brand} {name}"
        return cls(name, price, "Electronics")
    
    @classmethod
    def bulk_create_from_data(cls, products_data):
        """Create multiple products from a list of dictionaries"""
        created_products = []
        for data in products_data:
            product = cls(**data)  # Unpack dictionary
            created_products.append(product)
        return created_products
    
    @classmethod
    def find_by_category(cls, category):
        """Find all products in a category"""
        return [product for product in cls.all_products 
                if product.category.lower() == category.lower()]
    
    @classmethod
    def find_in_price_range(cls, min_price, max_price):
        """Find products within a price range"""
        return [product for product in cls.all_products 
                if min_price <= product.price <= max_price]
    
    @classmethod
    def get_categories(cls):
        """Get all unique categories"""
        return list(set(product.category for product in cls.all_products))
    
    @classmethod
    def get_total_value(cls):
        """Get total value of all products"""
        return sum(product.price for product in cls.all_products)
    
    @classmethod
    def clear_catalog(cls):
        """Clear all products and reset ID counter"""
        cls.all_products.clear()
        cls.next_id = 1
    
    def __str__(self):
        return f"Product({self.id}: {self.name} - ${self.price:.2f})"

# Usage examples
# Create products using factory methods
book1 = Product.create_book("Python Programming", 29.99, "John Smith")
book2 = Product.create_book("Web Development", 34.99, "Jane Doe")
laptop = Product.create_electronics("MacBook Pro", 1299.99, "Apple")
phone = Product.create_electronics("iPhone 15", 999.99, "Apple")

# Bulk create from data
products_data = [
    {"name": "Wireless Mouse", "price": 25.99, "category": "Electronics"},
    {"name": "Mechanical Keyboard", "price": 89.99, "category": "Electronics"},
    {"name": "Desk Lamp", "price": 45.99, "category": "Furniture"}
]
bulk_products = Product.bulk_create_from_data(products_data)

# Query products using class methods
print("All categories:", Product.get_categories())
print("Electronics:", [str(p) for p in Product.find_by_category("Electronics")])
print("Products under $50:", [str(p) for p in Product.find_in_price_range(0, 50)])
print(f"Total catalog value: ${Product.get_total_value():.2f}")
```

## Singleton Pattern with Class Methods

```python
class DatabaseConnection:
    _instance = None
    _initialized = False
    
    def __init__(self, host, port):
        if not DatabaseConnection._initialized:
            self.host = host
            self.port = port
            self.connected = False
            DatabaseConnection._initialized = True
    
    @classmethod
    def get_instance(cls, host="localhost", port=5432):
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = cls(host, port)
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """Reset the singleton (useful for testing)"""
        cls._instance = None
        cls._initialized = False
    
    def connect(self):
        self.connected = True
        return f"Connected to {self.host}:{self.port}"
    
    def disconnect(self):
        self.connected = False
        return f"Disconnected from {self.host}:{self.port}"

# Usage - always returns the same instance
db1 = DatabaseConnection.get_instance()
db2 = DatabaseConnection.get_instance()
print(db1 is db2)  # True - same object

print(db1.connect())
print(f"DB2 connected: {db2.connected}")  # True - same object
```

## Validation and Data Processing

```python
from datetime import datetime
import re

class Employee:
    company_name = "TechCorp Inc."
    employees = []
    
    def __init__(self, name, email, salary, department):
        self.name = name
        self.email = email
        self.salary = salary
        self.department = department
        self.hire_date = datetime.now()
        Employee.employees.append(self)
    
    @classmethod
    def create_validated_employee(cls, name, email, salary, department):
        """Create employee with validation"""
        # Validate inputs
        if not cls._is_valid_email(email):
            raise ValueError(f"Invalid email format: {email}")
        
        if not cls._is_valid_salary(salary):
            raise ValueError(f"Invalid salary: {salary}")
        
        if not cls._is_valid_department(department):
            raise ValueError(f"Invalid department: {department}")
        
        return cls(name, email, salary, department)
    
    @classmethod
    def from_csv_string(cls, csv_string):
        """Create employee from CSV format: name,email,salary,department"""
        parts = csv_string.strip().split(',')
        if len(parts) != 4:
            raise ValueError("CSV must have exactly 4 fields")
        
        name, email, salary_str, department = parts
        salary = float(salary_str)
        
        return cls.create_validated_employee(name, email, salary, department)
    
    @classmethod
    def get_employees_by_department(cls, department):
        """Get all employees in a department"""
        return [emp for emp in cls.employees if emp.department == department]
    
    @classmethod
    def get_average_salary_by_department(cls, department):
        """Calculate average salary for a department"""
        dept_employees = cls.get_employees_by_department(department)
        if not dept_employees:
            return 0
        return sum(emp.salary for emp in dept_employees) / len(dept_employees)
    
    @classmethod
    def get_company_statistics(cls):
        """Get company-wide statistics"""
        if not cls.employees:
            return {"total_employees": 0}
        
        salaries = [emp.salary for emp in cls.employees]
        departments = set(emp.department for emp in cls.employees)
        
        return {
            "company_name": cls.company_name,
            "total_employees": len(cls.employees),
            "departments": list(departments),
            "average_salary": sum(salaries) / len(salaries),
            "min_salary": min(salaries),
            "max_salary": max(salaries)
        }
    
    @staticmethod
    def _is_valid_email(email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def _is_valid_salary(salary):
        return isinstance(salary, (int, float)) and salary > 0
    
    @staticmethod
    def _is_valid_department(department):
        valid_departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
        return department in valid_departments
    
    def __str__(self):
        return f"{self.name} ({self.department}) - ${self.salary:,.2f}"

# Usage
try:
    # Create employees using different methods
    emp1 = Employee.create_validated_employee("John Doe", "john@techcorp.com", 75000, "Engineering")
    emp2 = Employee.from_csv_string("Jane Smith,jane@techcorp.com,65000,Marketing")
    emp3 = Employee.from_csv_string("Bob Johnson,bob@techcorp.com,80000,Engineering")
    
    # Get department-specific information
    eng_employees = Employee.get_employees_by_department("Engineering")
    print("Engineering employees:", [str(emp) for emp in eng_employees])
    
    avg_eng_salary = Employee.get_average_salary_by_department("Engineering")
    print(f"Average Engineering salary: ${avg_eng_salary:,.2f}")
    
    # Get company statistics
    stats = Employee.get_company_statistics()
    print("\nCompany Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
except ValueError as e:
    print(f"Validation error: {e}")
```

## Class Method Best Practices

### 1. Use Descriptive Names for Factory Methods
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    # Good: Descriptive factory method names
    @classmethod
    def create_square(cls, side_length):
        return cls(side_length, side_length)
    
    @classmethod
    def from_area_and_ratio(cls, area, width_height_ratio):
        height = (area / width_height_ratio) ** 0.5
        width = area / height
        return cls(width, height)
```

### 2. Always Return cls() for Proper Inheritance
```python
class Shape:
    @classmethod
    def create_default(cls):
        return cls()  # Use cls(), not Shape()

class Circle(Shape):
    def __init__(self, radius=1):
        self.radius = radius

# This works correctly because we used cls()
circle = Circle.create_default()  # Returns Circle instance, not Shape
print(type(circle))  # <class '__main__.Circle'>
```

### 3. Use Class Methods for Data Validation
```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    
    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        if fahrenheit < -459.67:  # Absolute zero in Fahrenheit
            raise ValueError("Temperature cannot be below absolute zero")
        celsius = (fahrenheit - 32) * 5/9
        return cls(celsius)
    
    @classmethod
    def from_kelvin(cls, kelvin):
        if kelvin < 0:
            raise ValueError("Kelvin cannot be negative")
        celsius = kelvin - 273.15
        return cls(celsius)
```

### 4. Document Your Class Methods
```python
class User:
    @classmethod
    def from_json(cls, json_data):
        """
        Create a User instance from JSON data.
        
        Args:
            json_data (dict): Dictionary containing user data with keys:
                            'username', 'email', 'age'
        
        Returns:
            User: A new User instance
            
        Raises:
            KeyError: If required keys are missing from json_data
            ValueError: If data validation fails
        """
        required_keys = ['username', 'email', 'age']
        for key in required_keys:
            if key not in json_data:
                raise KeyError(f"Missing required key: {key}")
        
        return cls(json_data['username'], json_data['email'], json_data['age'])
```

## Common Patterns and Use Cases

### 1. Registry Pattern
```python
class TaskRegistry:
    _tasks = {}
    
    @classmethod
    def register_task(cls, name, task_func):
        """Register a task function"""
        cls._tasks[name] = task_func
    
    @classmethod
    def get_task(cls, name):
        """Get a registered task"""
        return cls._tasks.get(name)
    
    @classmethod
    def list_tasks(cls):
        """List all registered task names"""
        return list(cls._tasks.keys())
    
    @classmethod
    def execute_task(cls, name, *args, **kwargs):
        """Execute a registered task"""
        task = cls.get_task(name)
        if task:
            return task(*args, **kwargs)
        raise ValueError(f"Task '{name}' not found")

# Usage
def send_email(recipient, message):
    return f"Email sent to {recipient}: {message}"

def backup_database():
    return "Database backup completed"

TaskRegistry.register_task("email", send_email)
TaskRegistry.register_task("backup", backup_database)

print(TaskRegistry.list_tasks())  # ['email', 'backup']
print(TaskRegistry.execute_task("email", "user@example.com", "Hello!"))
```

### 2. Configuration Management
```python
class AppConfig:
    _config = {}
    _loaded = False
    
    @classmethod
    def load_from_dict(cls, config_dict):
        """Load configuration from dictionary"""
        cls._config.update(config_dict)
        cls._loaded = True
    
    @classmethod
    def get(cls, key, default=None):
        """Get configuration value"""
        return cls._config.get(key, default)
    
    @classmethod
    def set(cls, key, value):
        """Set configuration value"""
        cls._config[key] = value
    
    @classmethod
    def is_loaded(cls):
        """Check if configuration has been loaded"""
        return cls._loaded
    
    @classmethod
    def get_all(cls):
        """Get all configuration as dictionary"""
        return cls._config.copy()

# Usage
AppConfig.load_from_dict({
    "database_url": "postgresql://localhost:5432/mydb",
    "debug": True,
    "max_connections": 100
})

print(AppConfig.get("database_url"))
print(AppConfig.get("timeout", 30))  # Returns default value
```

## Summary

**Class Methods are perfect when you want to:**
- Create alternative constructors (factory methods)
- Work with class-level data and variables
- Create instances in different ways
- Perform operations that relate to the class as a whole
- Maintain class-level state or statistics

**Key Points:**
1. **Always receive `cls` as first parameter** - refers to the class itself
2. **Use `cls()` to create instances** - ensures proper inheritance behavior
3. **Can access class variables** but not instance variables
4. **Great for factory methods** - alternative ways to create objects
5. **Work perfectly with inheritance** - `cls` refers to the actual subclass

**Quick Reference:**
```python
class MyClass:
    class_variable = "shared data"
    
    @classmethod
    def factory_method(cls, param):
        # Process param
        return cls(processed_param)  # Create and return new instance
    
    @classmethod
    def class_operation(cls):
        # Work with class-level data
        return cls.class_variable

# Usage
obj = MyClass.factory_method("some_data")  # Alternative constructor
result = MyClass.class_operation()         # Class-level operation
```

Class methods are essential for creating flexible, maintainable object-oriented code that supports multiple ways of creating and working with your classes!
