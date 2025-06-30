class Calculator():
    def __init__(self,name: str):
        self.name=name

    def addition(self, a:int, b:int )->int:
        """Add two numbers."""
        return a+b

    def subtract(self, a:int, b:int )->int:
        """Subtract two numbers."""
        return a-b

    def divide(self, a:int, b:int )->float:
        """Divivde two numbers."""
        return a/b

    def multiply(self, a:int, b:int )->int:
        """Multiply two numbers."""
        return a*b
    
    def reverse_string(self, text:str )->str:
        """Reverse a string."""
        return text[::-1]

# Test the class

calc=Calculator("calc")
print(calc.multiply(4, 2))  # Output: 8
print(calc.reverse_string("hello"))  # Output: olleh
