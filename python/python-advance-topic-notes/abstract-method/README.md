# Python Abstract Methods - Complete Guide

## What are Abstract Methods?

An **abstract method** is a method that is declared but contains no implementation. It serves as a blueprint that forces subclasses to provide their own implementation. Abstract methods are defined in abstract base classes (ABCs) and cannot be called directly - they must be overridden in child classes.

### Simple Analogy
Think of abstract methods like a contract or template:
- **Abstract class** = A blueprint or contract (like a job description)
- **Abstract method** = Required skills listed in the job description
- **Concrete class** = An actual employee who must have all the required skills
- **Method implementation** = The actual way the employee performs those skills

## Why Use Abstract Methods?

1. **Enforce a contract** - Guarantee that subclasses implement required methods
2. **Define interfaces** - Specify what methods a class must have without caring how
3. **Prevent instantiation** - Can't create objects from incomplete classes
4. **Code documentation** - Clearly show what methods subclasses need to implement
5. **Polymorphism** - Use different implementations through the same interface

## Basic Setup - ABC Module

Python uses the `abc` (Abstract Base Class) module for abstract methods:

```python
from abc import ABC, abstractmethod

# Method 1: Inherit from ABC
class MyAbstractClass(ABC):
    @abstractmethod
    def my_abstract_method(self):
        pass

# Method 2: Use ABCMeta as metaclass
from abc import ABCMeta

class MyAbstractClass(metaclass=ABCMeta):
    @abstractmethod
    def my_abstract_method(self):
        pass
```

## Basic Example - Shape Classes

```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    """Abstract base class for all shapes"""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def area(self):
        """Calculate and return the area of the shape"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Calculate and return the perimeter of the shape"""
        pass
    
    # Concrete method - available to all subclasses
    def describe(self):
        return f"This is a {self.name} with area {self.area():.2f} and perimeter {self.perimeter():.2f}"

class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius

# Usage
rectangle = Rectangle(5, 3)
circle = Circle(4)

print(rectangle.describe())  # This is a Rectangle with area 15.00 and perimeter 16.00
print(circle.describe())     # This is a Circle with area 50.27 and perimeter 25.13

# This would raise TypeError: Can't instantiate abstract class Shape
# shape = Shape("Generic")  # Error!
```

## What Happens When You Don't Implement Abstract Methods?

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass
    
    @abstractmethod
    def move(self):
        pass

# This class doesn't implement all abstract methods
class BrokenDog(Animal):
    def make_sound(self):
        return "Woof!"
    # Missing move() implementation!

# This will raise a TypeError
try:
    dog = BrokenDog()
except TypeError as e:
    print(f"Error: {e}")
    # Error: Can't instantiate abstract class BrokenDog with abstract method move

# Correct implementation
class Dog(Animal):
    def make_sound(self):
        return "Woof!"
    
    def move(self):
        return "Running on four legs"

# This works fine
dog = Dog()
print(dog.make_sound())  # Woof!
print(dog.move())        # Running on four legs
```

## Abstract Methods vs Regular Methods

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
    
    # Abstract methods - MUST be implemented by subclasses
    @abstractmethod
    def start_engine(self):
        pass
    
    @abstractmethod
    def stop_engine(self):
        pass
    
    @abstractmethod
    def get_max_speed(self):
        pass
    
    # Concrete methods - can be used directly or overridden
    def get_info(self):
        return f"{self.brand} {self.model}"
    
    def honk(self):
        return "Beep beep!"
    
    # Concrete method that uses abstract methods
    def test_drive(self):
        result = []
        result.append(self.start_engine())
        result.append(f"Driving at max speed: {self.get_max_speed()} mph")
        result.append(self.honk())
        result.append(self.stop_engine())
        return "\n".join(result)

class Car(Vehicle):
    def __init__(self, brand, model, horsepower):
        super().__init__(brand, model)
        self.horsepower = horsepower
    
    def start_engine(self):
        return "Car engine started with a quiet hum"
    
    def stop_engine(self):
        return "Car engine stopped"
    
    def get_max_speed(self):
        return self.horsepower * 0.8  # Rough calculation

class Motorcycle(Vehicle):
    def __init__(self, brand, model, engine_cc):
        super().__init__(brand, model)
        self.engine_cc = engine_cc
    
    def start_engine(self):
        return "Motorcycle engine roars to life!"
    
    def stop_engine(self):
        return "Motorcycle engine stopped with a final rumble"
    
    def get_max_speed(self):
        return self.engine_cc * 0.1
    
    # Override concrete method
    def honk(self):
        return "BEEP BEEP! (loud motorcycle horn)"

# Usage
car = Car("Toyota", "Camry", 200)
motorcycle = Motorcycle("Harley", "Davidson", 1200)

print("=== Car Test Drive ===")
print(car.test_drive())
print(f"\nCar info: {car.get_info()}")

print("\n=== Motorcycle Test Drive ===")
print(motorcycle.test_drive())
print(f"\nMotorcycle info: {motorcycle.get_info()}")
```

## Real-World Example 1: Database Interface

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DatabaseInterface(ABC):
    """Abstract base class for database operations"""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the database"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Close database connection"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results"""
        pass
    
    @abstractmethod
    def execute_command(self, command: str) -> bool:
        """Execute INSERT, UPDATE, DELETE commands"""
        pass
    
    @abstractmethod
    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        """Create a table with specified columns"""
        pass
    
    # Concrete method that uses abstract methods
    def setup_user_table(self):
        """Set up a standard user table"""
        columns = {
            "id": "INTEGER PRIMARY KEY",
            "username": "VARCHAR(50) UNIQUE",
            "email": "VARCHAR(100)",
            "created_at": "TIMESTAMP"
        }
        return self.create_table("users", columns)

class MySQLDatabase(DatabaseInterface):
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        # Simulate MySQL connection
        print(f"Connecting to MySQL at {self.host}...")
        self.connection = f"mysql://{self.host}/{self.database}"
        return True
    
    def disconnect(self) -> bool:
        print("Disconnecting from MySQL...")
        self.connection = None
        return True
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        print(f"Executing MySQL query: {query}")
        # Simulate query results
        return [{"id": 1, "name": "MySQL Result"}]
    
    def execute_command(self, command: str) -> bool:
        print(f"Executing MySQL command: {command}")
        return True
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        column_definitions = ", ".join([f"{name} {type_}" for name, type_ in columns.items()])
        command = f"CREATE TABLE {table_name} ({column_definitions})"
        return self.execute_command(command)

class PostgreSQLDatabase(DatabaseInterface):
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> bool:
        print(f"Connecting to PostgreSQL at {self.host}...")
        self.connection = f"postgresql://{self.host}/{self.database}"
        return True
    
    def disconnect(self) -> bool:
        print("Disconnecting from PostgreSQL...")
        self.connection = None
        return True
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        print(f"Executing PostgreSQL query: {query}")
        return [{"id": 1, "name": "PostgreSQL Result"}]
    
    def execute_command(self, command: str) -> bool:
        print(f"Executing PostgreSQL command: {command}")
        return True
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        column_definitions = ", ".join([f"{name} {type_}" for name, type_ in columns.items()])
        command = f"CREATE TABLE {table_name} ({column_definitions})"
        return self.execute_command(command)

class SQLiteDatabase(DatabaseInterface):
    def __init__(self, database_path):
        self.database_path = database_path
        self.connection = None
    
    def connect(self) -> bool:
        print(f"Connecting to SQLite database: {self.database_path}")
        self.connection = f"sqlite://{self.database_path}"
        return True
    
    def disconnect(self) -> bool:
        print("Disconnecting from SQLite...")
        self.connection = None
        return True
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        print(f"Executing SQLite query: {query}")
        return [{"id": 1, "name": "SQLite Result"}]
    
    def execute_command(self, command: str) -> bool:
        print(f"Executing SQLite command: {command}")
        return True
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> bool:
        column_definitions = ", ".join([f"{name} {type_}" for name, type_ in columns.items()])
        command = f"CREATE TABLE {table_name} ({column_definitions})"
        return self.execute_command(command)

# Usage - Polymorphism in action
def setup_database(db: DatabaseInterface):
    """Function that works with any database implementation"""
    db.connect()
    db.setup_user_table()
    results = db.execute_query("SELECT * FROM users")
    print(f"Query results: {results}")
    db.disconnect()

# Test with different database implementations
print("=== MySQL Setup ===")
mysql_db = MySQLDatabase("localhost", "user", "pass", "myapp")
setup_database(mysql_db)

print("\n=== PostgreSQL Setup ===")
postgres_db = PostgreSQLDatabase("localhost", "user", "pass", "myapp")
setup_database(postgres_db)

print("\n=== SQLite Setup ===")
sqlite_db = SQLiteDatabase("./myapp.db")
setup_database(sqlite_db)
```

## Real-World Example 2: Payment Processing System

```python
from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any

class PaymentStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"

@dataclass
class PaymentResult:
    status: PaymentStatus
    transaction_id: str
    message: str
    metadata: Dict[str, Any] = None

class PaymentProcessor(ABC):
    """Abstract base class for payment processing"""
    
    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id
        self.is_configured = False
    
    @abstractmethod
    def configure(self, **config) -> bool:
        """Configure the payment processor with credentials"""
        pass
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str, card_details: Dict[str, str]) -> PaymentResult:
        """Process a payment transaction"""
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> PaymentResult:
        """Refund a previous payment"""
        pass
    
    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> PaymentResult:
        """Get the status of a transaction"""
        pass
    
    # Concrete methods
    def validate_amount(self, amount: float) -> bool:
        """Validate payment amount"""
        return amount > 0 and amount <= 10000  # Max $10,000 per transaction
    
    def validate_currency(self, currency: str) -> bool:
        """Validate currency code"""
        supported_currencies = ["USD", "EUR", "GBP", "CAD", "AUD"]
        return currency.upper() in supported_currencies
    
    def process_payment_with_validation(self, amount: float, currency: str, card_details: Dict[str, str]) -> PaymentResult:
        """Process payment with built-in validation"""
        if not self.is_configured:
            return PaymentResult(
                status=PaymentStatus.FAILED,
                transaction_id="",
                message="Payment processor not configured"
            )
        
        if not self.validate_amount(amount):
            return PaymentResult(
                status=PaymentStatus.FAILED,
                transaction_id="",
                message="Invalid payment amount"
            )
        
        if not self.validate_currency(currency):
            return PaymentResult(
                status=PaymentStatus.FAILED,
                transaction_id="",
                message="Unsupported currency"
            )
        
        return self.process_payment(amount, currency, card_details)

class StripePaymentProcessor(PaymentProcessor):
    def __init__(self, merchant_id: str):
        super().__init__(merchant_id)
        self.secret_key = None
        self.publishable_key = None
    
    def configure(self, secret_key: str, publishable_key: str) -> bool:
        self.secret_key = secret_key
        self.publishable_key = publishable_key
        self.is_configured = True
        print(f"Stripe configured for merchant {self.merchant_id}")
        return True
    
    def process_payment(self, amount: float, currency: str, card_details: Dict[str, str]) -> PaymentResult:
        # Simulate Stripe API call
        import random
        
        transaction_id = f"stripe_{random.randint(100000, 999999)}"
        
        # Simulate payment processing
        if random.random() > 0.1:  # 90% success rate
            return PaymentResult(
                status=PaymentStatus.SUCCESS,
                transaction_id=transaction_id,
                message="Payment processed successfully via Stripe",
                metadata={"processor": "stripe", "fee": amount * 0.029}
            )
        else:
            return PaymentResult(
                status=PaymentStatus.FAILED,
                transaction_id=transaction_id,
                message="Payment failed - insufficient funds"
            )
    
    def refund_payment(self, transaction_id: str, amount: float) -> PaymentResult:
        return PaymentResult(
            status=PaymentStatus.REFUNDED,
            transaction_id=transaction_id,
            message=f"Refunded ${amount:.2f} via Stripe"
        )
    
    def get_transaction_status(self, transaction_id: str) -> PaymentResult:
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=transaction_id,
            message="Transaction found in Stripe records"
        )

class PayPalPaymentProcessor(PaymentProcessor):
    def __init__(self, merchant_id: str):
        super().__init__(merchant_id)
        self.client_id = None
        self.client_secret = None
    
    def configure(self, client_id: str, client_secret: str) -> bool:
        self.client_id = client_id
        self.client_secret = client_secret
        self.is_configured = True
        print(f"PayPal configured for merchant {self.merchant_id}")
        return True
    
    def process_payment(self, amount: float, currency: str, card_details: Dict[str, str]) -> PaymentResult:
        import random
        
        transaction_id = f"paypal_{random.randint(100000, 999999)}"
        
        if random.random() > 0.15:  # 85% success rate
            return PaymentResult(
                status=PaymentStatus.SUCCESS,
                transaction_id=transaction_id,
                message="Payment processed successfully via PayPal",
                metadata={"processor": "paypal", "fee": amount * 0.035}
            )
        else:
            return PaymentResult(
                status=PaymentStatus.FAILED,
                transaction_id=transaction_id,
                message="Payment declined by PayPal"
            )
    
    def refund_payment(self, transaction_id: str, amount: float) -> PaymentResult:
        return PaymentResult(
            status=PaymentStatus.REFUNDED,
            transaction_id=transaction_id,
            message=f"Refunded ${amount:.2f} via PayPal"
        )
    
    def get_transaction_status(self, transaction_id: str) -> PaymentResult:
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=transaction_id,
            message="Transaction found in PayPal records"
        )

class SquarePaymentProcessor(PaymentProcessor):
    def __init__(self, merchant_id: str):
        super().__init__(merchant_id)
        self.access_token = None
        self.application_id = None
    
    def configure(self, access_token: str, application_id: str) -> bool:
        self.access_token = access_token
        self.application_id = application_id
        self.is_configured = True
        print(f"Square configured for merchant {self.merchant_id}")
        return True
    
    def process_payment(self, amount: float, currency: str, card_details: Dict[str, str]) -> PaymentResult:
        import random
        
        transaction_id = f"square_{random.randint(100000, 999999)}"
        
        if random.random() > 0.12:  # 88% success rate
            return PaymentResult(
                status=PaymentStatus.SUCCESS,
                transaction_id=transaction_id,
                message="Payment processed successfully via Square",
                metadata={"processor": "square", "fee": amount * 0.026}
            )
        else:
            return PaymentResult(
                status=PaymentStatus.FAILED,
                transaction_id=transaction_id,
                message="Payment failed - card declined"
            )
    
    def refund_payment(self, transaction_id: str, amount: float) -> PaymentResult:
        return PaymentResult(
            status=PaymentStatus.REFUNDED,
            transaction_id=transaction_id,
            message=f"Refunded ${amount:.2f} via Square"
        )
    
    def get_transaction_status(self, transaction_id: str) -> PaymentResult:
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=transaction_id,
            message="Transaction found in Square records"
        )

# Usage - E-commerce checkout system
class CheckoutService:
    def __init__(self, payment_processor: PaymentProcessor):
        self.payment_processor = payment_processor
    
    def process_order(self, order_amount: float, currency: str, customer_card: Dict[str, str]) -> PaymentResult:
        print(f"Processing order for ${order_amount:.2f} {currency}")
        
        result = self.payment_processor.process_payment_with_validation(
            order_amount, currency, customer_card
        )
        
        if result.status == PaymentStatus.SUCCESS:
            print(f"✅ Payment successful! Transaction ID: {result.transaction_id}")
            if result.metadata:
                print(f"   Processing fee: ${result.metadata.get('fee', 0):.2f}")
        else:
            print(f"❌ Payment failed: {result.message}")
        
        return result

# Demo usage
def demo_payment_processing():
    # Configure different payment processors
    stripe = StripePaymentProcessor("MERCHANT_001")
    stripe.configure(secret_key="sk_test_123", publishable_key="pk_test_123")
    
    paypal = PayPalPaymentProcessor("MERCHANT_001")
    paypal.configure(client_id="paypal_client_123", client_secret="paypal_secret_123")
    
    square = SquarePaymentProcessor("MERCHANT_001")
    square.configure(access_token="sq_access_123", application_id="sq_app_123")
    
    # Sample card details
    card_details = {
        "number": "4111111111111111",
        "expiry": "12/25",
        "cvv": "123"
    }
    
    # Test each processor
    processors = [
        ("Stripe", stripe),
        ("PayPal", paypal),
        ("Square", square)
    ]
    
    for name, processor in processors:
        print(f"\n=== Testing {name} ===")
        checkout = CheckoutService(processor)
        result = checkout.process_order(99.99, "USD", card_details)
        
        if result.status == PaymentStatus.SUCCESS:
            # Test refund
            refund_result = processor.refund_payment(result.transaction_id, 50.0)
            print(f"Refund result: {refund_result.message}")

# Run the demo
demo_payment_processing()
```

## Abstract Properties

You can also create abstract properties using `@abstractproperty` or `@property` with `@abstractmethod`:

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def max_speed(self):
        """Maximum speed of the vehicle"""
        pass
    
    @property
    @abstractmethod
    def fuel_type(self):
        """Type of fuel used by the vehicle"""
        pass
    
    @max_speed.setter
    @abstractmethod
    def max_speed(self, value):
        pass

class Car(Vehicle):
    def __init__(self):
        self._max_speed = 120
        self._fuel_type = "Gasoline"
    
    @property
    def max_speed(self):
        return self._max_speed
    
    @max_speed.setter
    def max_speed(self, value):
        if value > 0:
            self._max_speed = value
    
    @property
    def fuel_type(self):
        return self._fuel_type

# Usage
car = Car()
print(car.max_speed)    # 120
print(car.fuel_type)    # Gasoline
car.max_speed = 150
print(car.max_speed)    # 150
```

## Multiple Abstract Base Classes (Mixins)

```python
from abc import ABC, abstractmethod

class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass
    
    @abstractmethod
    def land(self):
        pass

class Swimmable(ABC):
    @abstractmethod
    def swim(self):
        pass
    
    @abstractmethod
    def dive(self):
        pass

class Animal(ABC):
    @abstractmethod
    def eat(self):
        pass
    
    @abstractmethod
    def sleep(self):
        pass

# Duck can fly and swim
class Duck(Animal, Flyable, Swimmable):
    def eat(self):
        return "Duck eating seeds and insects"
    
    def sleep(self):
        return "Duck sleeping on water"
    
    def fly(self):
        return "Duck flying in formation"
    
    def land(self):
        return "Duck landing on water"
    
    def swim(self):
        return "Duck swimming gracefully"
    
    def dive(self):
        return "Duck diving for food"

# Penguin can only swim
class Penguin(Animal, Swimmable):
    def eat(self):
        return "Penguin eating fish"
    
    def sleep(self):
        return "Penguin sleeping in huddle"
    
    def swim(self):
        return "Penguin swimming underwater"
    
    def dive(self):
        return "Penguin diving deep for fish"

# Usage
duck = Duck()
penguin = Penguin()

print(duck.fly())     # Duck flying in formation
print(duck.swim())    # Duck swimming gracefully
print(penguin.swim()) # Penguin swimming underwater
print(penguin.dive()) # Penguin diving deep for fish
```

## Template Method Pattern

Abstract methods work great with the Template Method design pattern:

```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    """Template method pattern for data processing"""
    
    def process_data(self, data):
        """Template method that defines the algorithm"""
        print("Starting data processing...")
        
        # Step 1: Load data
        loaded_data = self.load_data(data)
        print(f"Loaded {len(loaded_data)} items")
        
        # Step 2: Validate data
        if not self.validate_data(loaded_data):
            raise ValueError("Data validation failed")
        print("Data validation passed")
        
        # Step 3: Transform data
        transformed_data = self.transform_data(loaded_data)
        print("Data transformation completed")
        
        # Step 4: Save results
        result = self.save_data(transformed_data)
        print("Data processing completed successfully")
        
        return result
    
    @abstractmethod
    def load_data(self, source):
        """Load data from source - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def validate_data(self, data):
        """Validate loaded data - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def transform_data(self, data):
        """Transform data - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def save_data(self, data):
        """Save processed data - must be implemented by subclasses"""
        pass

class CSVProcessor(DataProcessor):
    def load_data(self, csv_file):
        # Simulate CSV loading
        return [
            {"name": "John", "age": "30", "salary": "50000"},
            {"name": "Jane", "age": "25", "salary": "60000"},
            {"name": "Bob", "age": "35", "salary": "55000"}
        ]
    
    def validate_data(self, data):
        # Check if all required fields are present
        required_fields = ["name", "age", "salary"]
        for record in data:
            if not all(field in record for field in required_fields):
                return False
        return True
    
    def transform_data(self, data):
        # Convert strings to appropriate types
        transformed = []
        for record in data:
            transformed.append({
                "name": record["name"].strip(),
                "age": int(record["age"]),
                "salary": float(record["salary"])
            })
        return transformed
    
    def save_data(self, data):
        # Simulate saving to database
        print("Saving to database...")
        for record in data:
            print(f"  Saved: {record}")
        return len(data)

class JSONProcessor(DataProcessor):
    def load_data(self, json_data):
        # Simulate JSON loading
        return json_data.get("employees", [])
    
    def validate_data(self, data):
        # Validate JSON structure
        return isinstance(data, list) and len(data) > 0
    
    def transform_data(self, data):
        # Add computed fields
        for record in data:
            record["annual_salary"] = record.get("salary", 0) * 12
            record["category"] = "senior" if record.get("age", 0) > 30 else "junior"
        return data
    
    def save_data(self, data):
        # Simulate saving to file
        print("Saving to JSON file...")
        for record in data:
            print(f"  Saved: {record}")
        return len(data)

# Usage
csv_processor = CSVProcessor()
result = csv_processor.process_data("employees.csv")
print(f"Processed {result} CSV records\n")

json_data = {
    "employees": [
        {"name": "Alice", "age": 28, "salary": 5500},
        {"name": "Charlie", "age": 32, "salary": 6200}
    ]
}

json_processor = JSONProcessor()
result = json_processor.process_data(json_data)
print(f"Processed {result} JSON records")
```

## Testing Abstract Classes

```python
import unittest
from abc import ABC, abstractmethod

class Calculator(ABC):
    @abstractmethod
    def add(self, a, b):
        pass
    
    @abstractmethod
    def subtract(self, a, b):
        pass
    
    def multiply(self, a, b):
        """Concrete method using abstract methods"""
        result = 0
        for _ in range(b):
            result = self.add(result, a)
        return result

class BasicCalculator(Calculator):
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = BasicCalculator()
    
    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
    
    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
    
    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)
    
    def test_cannot_instantiate_abstract_class(self):
        with self.assertRaises(TypeError):
            Calculator()

# Run tests
if __name__ == '__main__':
    unittest.main()
```

## Best Practices for Abstract Methods

### 1. Use Clear and Descriptive Method Names

```python
from abc import ABC, abstractmethod

# Good: Clear, descriptive abstract methods
class FileHandler(ABC):
    @abstractmethod
    def read_file(self, filepath: str) -> str:
        """Read and return file contents"""
        pass
    
    @abstractmethod
    def write_file(self, filepath: str, content: str) -> bool:
        """Write content to file, return success status"""
        pass
    
    @abstractmethod
    def validate_file_format(self, filepath: str) -> bool:
        """Validate if file format is supported"""
        pass

# Bad: Vague method names
class BadFileHandler(ABC):
    @abstractmethod
    def process(self, data):  # What kind of processing?
        pass
    
    @abstractmethod
    def handle(self, item):  # Handle what? How?
        pass
```

### 2. Provide Documentation for Abstract Methods

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DataAnalyzer(ABC):
    @abstractmethod
    def load_data(self, source: str) -> List[Dict[str, Any]]:
        """
        Load data from the specified source.
        
        Args:
            source (str): Path to data source (file, URL, etc.)
            
        Returns:
            List[Dict[str, Any]]: List of data records
            
        Raises:
            FileNotFoundError: If source doesn't exist
            ValueError: If source format is invalid
        """
        pass
    
    @abstractmethod
    def analyze_data(self, data: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Perform analysis on the loaded data.
        
        Args:
            data: List of data records to analyze
            
        Returns:
            Dict containing analysis results with metric names as keys
            and calculated values as values
        """
        pass
```

### 3. Combine Abstract and Concrete Methods Effectively

```python
from abc import ABC, abstractmethod

class AuthenticationService(ABC):
    def __init__(self):
        self.max_attempts = 3
        self.lockout_duration = 300  # 5 minutes
    
    # Abstract methods - must be implemented
    @abstractmethod
    def validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials against the authentication source"""
        pass
    
    @abstractmethod
    def get_user_info(self, username: str) -> Dict[str, Any]:
        """Retrieve user information from the authentication source"""
        pass
    
    # Concrete method using abstract methods
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """
        Complete authentication process with error handling and security features
        """
        if self._is_account_locked(username):
            return {
                "success": False,
                "message": "Account temporarily locked due to too many failed attempts"
            }
        
        if self.validate_credentials(username, password):
            self._reset_failed_attempts(username)
            user_info = self.get_user_info(username)
            return {
                "success": True,
                "message": "Authentication successful",
                "user": user_info
            }
        else:
            self._increment_failed_attempts(username)
            return {
                "success": False,
                "message": "Invalid credentials"
            }
    
    # Helper concrete methods
    def _is_account_locked(self, username: str) -> bool:
        # Implementation for checking account lock status
        return False  # Simplified for example
    
    def _reset_failed_attempts(self, username: str):
        # Implementation for resetting failed attempts counter
        pass
    
    def _increment_failed_attempts(self, username: str):
        # Implementation for incrementing failed attempts
        pass

class DatabaseAuthService(AuthenticationService):
    def __init__(self, db_connection):
        super().__init__()
        self.db = db_connection
    
    def validate_credentials(self, username: str, password: str) -> bool:
        # Database-specific credential validation
        query = "SELECT password_hash FROM users WHERE username = ?"
        result = self.db.execute(query, (username,))
        if result:
            stored_hash = result[0]['password_hash']
            return self._verify_password(password, stored_hash)
        return False
    
    def get_user_info(self, username: str) -> Dict[str, Any]:
        query = "SELECT id, username, email, role FROM users WHERE username = ?"
        result = self.db.execute(query, (username,))
        return result[0] if result else {}
    
    def _verify_password(self, password: str, hash: str) -> bool:
        # Password verification logic
        return True  # Simplified for example

class LDAPAuthService(AuthenticationService):
    def __init__(self, ldap_server, base_dn):
        super().__init__()
        self.server = ldap_server
        self.base_dn = base_dn
    
    def validate_credentials(self, username: str, password: str) -> bool:
        # LDAP-specific credential validation
        try:
            # Simulate LDAP bind operation
            return self._ldap_bind(username, password)
        except Exception:
            return False
    
    def get_user_info(self, username: str) -> Dict[str, Any]:
        # LDAP-specific user info retrieval
        return {
            "username": username,
            "email": f"{username}@company.com",
            "role": "user"
        }
    
    def _ldap_bind(self, username: str, password: str) -> bool:
        # LDAP binding logic
        return True  # Simplified for example
```

### 4. Use Type Hints for Better Interface Definition

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Union, Any
from datetime import datetime

class ReportGenerator(ABC):
    @abstractmethod
    def generate_report(
        self, 
        data: List[Dict[str, Any]], 
        report_type: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> Union[str, bytes]:
        """
        Generate a report from the provided data.
        
        Args:
            data: List of data records
            report_type: Type of report to generate ('summary', 'detailed', 'chart')
            filters: Optional filters to apply to data
            
        Returns:
            Generated report as string (for text reports) or bytes (for binary reports)
        """
        pass
    
    @abstractmethod
    def save_report(
        self, 
        report_content: Union[str, bytes], 
        filename: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Save the generated report to storage"""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Return list of supported report formats"""
        pass
```

## Common Pitfalls and How to Avoid Them

### 1. Forgetting to Use ABC or abstractmethod

```python
# Wrong: Missing ABC inheritance and @abstractmethod decorator
class BadShape:
    def area(self):
        pass  # This is just a regular method, not abstract

# Right: Proper abstract class
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
```

### 2. Implementing Abstract Methods Incorrectly

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        """Make animal sound"""
        pass

# Wrong: Not actually implementing the method
class Dog(Animal):
    def make_sound(self):
        pass  # Empty implementation defeats the purpose

# Right: Proper implementation
class Dog(Animal):
    def make_sound(self):
        return "Woof!"
```

### 3. Making Abstract Classes Too Complex

```python
# Wrong: Too many responsibilities in one abstract class
class BadUserManager(ABC):
    @abstractmethod
    def authenticate_user(self, username, password): pass
    
    @abstractmethod
    def send_email(self, user, message): pass
    
    @abstractmethod
    def generate_report(self, report_type): pass
    
    @abstractmethod
    def backup_database(self): pass
    
    @abstractmethod
    def process_payments(self, amount): pass

# Right: Single responsibility principle
class AuthenticationService(ABC):
    @abstractmethod
    def authenticate_user(self, username, password): pass

class EmailService(ABC):
    @abstractmethod
    def send_email(self, recipient, message): pass

class ReportService(ABC):
    @abstractmethod
    def generate_report(self, report_type): pass
```

## When NOT to Use Abstract Methods

### 1. When You Have a Simple Base Class

```python
# Don't need abstract methods for simple inheritance
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):
    def speak(self):
        return f"{self.name} barks"
```

### 2. When Using Composition Instead of Inheritance

```python
# Sometimes composition is better than abstract inheritance
class EmailSender:
    def send(self, message):
        print(f"Sending email: {message}")

class SMSSender:
    def send(self, message):
        print(f"Sending SMS: {message}")

class NotificationService:
    def __init__(self, sender):
        self.sender = sender  # Composition instead of inheritance
    
    def notify(self, message):
        self.sender.send(message)

# Usage
email_service = NotificationService(EmailSender())
sms_service = NotificationService(SMSSender())
```

## Summary

**Abstract Methods are perfect when you want to:**
- **Enforce a contract** - guarantee that subclasses implement specific methods
- **Define interfaces** - specify what methods a class must have
- **Prevent instantiation** - stop incomplete classes from being instantiated
- **Enable polymorphism** - use different implementations through the same interface
- **Document requirements** - clearly show what subclasses need to implement

**Key Points:**
1. **Must inherit from ABC** - use `from abc import ABC, abstractmethod`
2. **Use @abstractmethod decorator** - marks methods as abstract
3. **Cannot instantiate abstract classes** - Python prevents this automatically
4. **Must implement all abstract methods** - subclasses can't skip any
5. **Great for interfaces** - define what methods a class should have
6. **Support inheritance** - can combine with regular methods
7. **Enable polymorphism** - different classes, same interface

**Quick Reference:**
```python
from abc import ABC, abstractmethod

class AbstractClass(ABC):
    @abstractmethod
    def required_method(self):
        """This method must be implemented by subclasses"""
        pass
    
    def optional_method(self):
        """This method can be used as-is or overridden"""
        return "Default implementation"

class ConcreteClass(AbstractClass):
    def required_method(self):
        return "Implemented in concrete class"

# Usage
# abstract = AbstractClass()  # Error! Can't instantiate
concrete = ConcreteClass()     # Works fine
result = concrete.required_method()  # "Implemented in concrete class"
```

Abstract methods are essential for creating robust, maintainable object-oriented designs that enforce contracts and enable clean polymorphism!
