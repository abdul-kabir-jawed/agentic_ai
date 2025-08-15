# 🚀 OpenAI Agents SDK - Context Management Guide

> **Understanding and implementing context management for intelligent AI agents**

---

## 📖 What is Context?

Context in the OpenAI Agents SDK is data that your agent can access during execution. There are **two distinct types** of context that serve different purposes:

### 🏠 Local Context
- **Private backend data** that your tools and code can access
- **❌ Never sent to the LLM** - completely internal
- Contains dependencies, user info, database connections, configuration
- Available to all tools via `RunContextWrapper`

### 🤖 Agent/LLM Context  
- **Information the AI sees** when generating responses
- **✅ Directly visible to the LLM** - influences AI reasoning
- Part of conversation history, system prompts, and instructions
- Guides the agent's behavior and decision-making

---

## 🛠️ Creating Context Objects

### Using `@dataclass` (Simple & Fast)
```python
from dataclasses import dataclass
from typing import Dict, Any
import logging

@dataclass
class UserContext:
    user_id: str
    username: str
    email: str
    preferences: Dict[str, Any]
    logger: logging.Logger
    db_connection: Any  # Database connection
    
    def log_action(self, action: str):
        """Helper method available throughout agent execution"""
        self.logger.info(f"User {self.username} performed: {action}")
```

### Using Pydantic (Validation & Type Safety)
```python
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional

class UserContext(BaseModel):
    user_id: str = Field(..., description="Unique user identifier")
    username: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    preferences: Dict[str, Any] = Field(default_factory=dict)
    permissions: List[str] = Field(default_factory=list)
    session_id: Optional[str] = None
    
    @validator('user_id')
    def validate_user_id(cls, v):
        if len(v) < 3:
            raise ValueError('User ID must be at least 3 characters')
        return v
    
    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions
    
    class Config:
        # Prevent accidental modification
        frozen = True
```

---

## 🔄 How Context is Passed and Accessed

### 1. Context Flow Diagram
```
User Request → Runner.run(context=your_context) → Agent → Tools
                    ↓
            RunContextWrapper wraps your context
                    ↓
        Tools access via wrapper.context
```

### 2. Passing Context to Agent
```python
import asyncio
from agents import Agent, Runner

# Create your context object
user_context = UserContext(
    user_id="user_123",
    username="john_doe", 
    email="john@example.com",
    preferences={"theme": "dark", "language": "en"},
    permissions=["read", "write"]
)

# Run agent with context
result = await Runner.run(
    starting_agent=my_agent,
    input="What are my account settings?",
    context=user_context  # ← Your context is passed here
)
```

### 3. Accessing Context in Tools
```python
from agents import function_tool, RunContextWrapper

@function_tool
async def get_user_settings(wrapper: RunContextWrapper[UserContext]) -> str:
    # Access context through the wrapper
    ctx = wrapper.context
    
    # Use context data
    ctx.log_action("viewed_settings")
    
    settings = {
        "username": ctx.username,
        "email": ctx.email,
        "theme": ctx.preferences.get("theme", "light"),
        "language": ctx.preferences.get("language", "en")
    }
    
    return f"Settings for {ctx.username}: {settings}"

@function_tool  
async def update_preference(
    wrapper: RunContextWrapper[UserContext],
    setting: str,
    value: str
) -> str:
    ctx = wrapper.context
    
    # Check permissions
    if not ctx.has_permission("write"):
        return "❌ You don't have permission to update settings"
    
    # Update preference (this modifies the context)
    ctx.preferences[setting] = value
    ctx.log_action(f"updated_{setting}")
    
    return f"✅ Updated {setting} to '{value}'"
```

---

## 🎯 Complete Working Example

```python
import asyncio
import logging
from dataclasses import dataclass, field
from typing import Dict, Any
from agents import Agent, Runner, function_tool, RunContextWrapper

# 1. Define Context Structure
@dataclass
class ECommerceContext:
    customer_id: str
    customer_name: str
    email: str
    cart_items: Dict[str, int] = field(default_factory=dict)  # product_id -> quantity
    loyalty_points: int = 0
    order_history: list = field(default_factory=list)
    logger: logging.Logger = field(default_factory=lambda: logging.getLogger(__name__))
    
    def add_to_cart(self, product_id: str, quantity: int = 1):
        """Helper method to manage cart"""
        current_qty = self.cart_items.get(product_id, 0)
        self.cart_items[product_id] = current_qty + quantity
        self.logger.info(f"Added {quantity} of {product_id} to cart for {self.customer_name}")

# 2. Create Tools that Use Context
@function_tool
async def view_cart(wrapper: RunContextWrapper[ECommerceContext]) -> str:
    """Show current cart contents"""
    ctx = wrapper.context
    
    if not ctx.cart_items:
        return f"🛒 Your cart is empty, {ctx.customer_name}!"
    
    cart_summary = f"🛒 Cart for {ctx.customer_name}:\n"
    total_items = 0
    
    for product_id, quantity in ctx.cart_items.items():
        cart_summary += f"  • Product {product_id}: {quantity} items\n"
        total_items += quantity
    
    cart_summary += f"Total items: {total_items}"
    return cart_summary

@function_tool
async def add_product_to_cart(
    wrapper: RunContextWrapper[ECommerceContext],
    product_id: str,
    quantity: int = 1
) -> str:
    """Add product to customer's cart"""
    ctx = wrapper.context
    
    # Use context helper method
    ctx.add_to_cart(product_id, quantity)
    
    return f"✅ Added {quantity} of Product {product_id} to your cart!"

@function_tool
async def check_loyalty_points(wrapper: RunContextWrapper[ECommerceContext]) -> str:
    """Check customer's loyalty points"""
    ctx = wrapper.context
    
    return f"💎 {ctx.customer_name}, you have {ctx.loyalty_points} loyalty points!"

@function_tool
async def place_order(wrapper: RunContextWrapper[ECommerceContext]) -> str:
    """Place order with current cart items"""
    ctx = wrapper.context
    
    if not ctx.cart_items:
        return "❌ Cannot place order - your cart is empty!"
    
    # Create order from cart
    order = {
        "order_id": f"ORD_{len(ctx.order_history) + 1:03d}",
        "items": ctx.cart_items.copy(),
        "customer_id": ctx.customer_id,
        "status": "confirmed"
    }
    
    # Add to order history and clear cart
    ctx.order_history.append(order)
    total_items = sum(ctx.cart_items.values())
    ctx.cart_items.clear()
    
    # Award loyalty points (1 point per item)
    ctx.loyalty_points += total_items
    
    ctx.logger.info(f"Order placed: {order}")
    
    return f"🎉 Order {order['order_id']} placed successfully! You earned {total_items} loyalty points."

# 3. Create Agent with Context-Aware Tools
shopping_agent = Agent[ECommerceContext](
    name="ShoppingAssistant",
    instructions="""
    You are a helpful e-commerce shopping assistant.
    
    You can help customers:
    - View their cart contents
    - Add products to cart
    - Check loyalty points
    - Place orders
    
    Always be friendly and use the customer's name when possible.
    Suggest relevant actions based on their cart status.
    """,
    tools=[view_cart, add_product_to_cart, check_loyalty_points, place_order]
)

# 4. Usage Example
async def main():
    # Create customer context
    customer_context = ECommerceContext(
        customer_id="CUST_001",
        customer_name="Alice Johnson",
        email="alice@example.com",
        loyalty_points=150,
        logger=logging.getLogger("ecommerce")
    )
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    print("🛍️ E-Commerce Shopping Assistant Demo\n")
    
    # Example interactions
    interactions = [
        "Hi! Can you show me my current cart?",
        "I'd like to add product ABC123 to my cart",
        "Add 2 more of product XYZ789 please", 
        "How many loyalty points do I have?",
        "I want to place my order now"
    ]
    
    for user_input in interactions:
        print(f"👤 Customer: {user_input}")
        
        result = await Runner.run(
            starting_agent=shopping_agent,
            input=user_input,
            context=customer_context  # ← Context passed here
        )
        
        print(f"🤖 Assistant: {result.final_output}\n")
        
        # Show context state changes
        print(f"   📊 Cart: {customer_context.cart_items}")
        print(f"   💎 Points: {customer_context.loyalty_points}")
        print(f"   📦 Orders: {len(customer_context.order_history)}\n")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔍 Testing Your Context

```python
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def test_context():
    """Create test context for testing"""
    return ECommerceContext(
        customer_id="TEST_001",
        customer_name="Test User",
        email="test@example.com",
        logger=MagicMock()
    )

@pytest.mark.asyncio
async def test_add_to_cart_tool(test_context):
    """Test the add to cart functionality"""
    # Create wrapper (simulate what SDK does)
    wrapper = MagicMock()
    wrapper.context = test_context
    
    # Test the tool
    result = await add_product_to_cart(wrapper, "PROD_123", 2)
    
    # Verify results
    assert "Added 2 of Product PROD_123" in result
    assert test_context.cart_items["PROD_123"] == 2
    test_context.logger.info.assert_called()
```

---

## ✅ Best Practices

### Do's ✅
- **Use type hints**: `RunContextWrapper[YourContextType]` for better IDE support
- **Keep context focused**: Don't put everything in one context object
- **Validate context**: Use Pydantic for automatic validation
- **Use helper methods**: Add utility methods to your context classes

### Don'ts ❌  
- **Don't put secrets in Agent/LLM context** - use local context only
- **Don't make context too complex** - keep it simple and focused
- **Don't forget error handling** - check if context attributes exist
- **Don't modify immutable contexts** - use `frozen=True` in Pydantic when appropriate

---

## 🎯 Key Takeaways

1. **Local Context** = Private backend data (databases, user info, config)
2. **Agent/LLM Context** = Information that guides AI reasoning  
3. **RunContextWrapper** = How tools access the context you provide
4. **Type Safety** = Use generics like `Agent[YourContext]` for better development experience
5. **Testing** = Mock the wrapper and test your tools independently

Context makes your agents stateful, personalized, and powerful! 🚀
