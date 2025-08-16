# 🔍 Python Logging Guide for OpenAI Agents SDK

> **Simple guide to understand `logging.Logger` and why we use it in agent contexts**

---

## 🤔 What is `logging.Logger`?

**`logging.Logger` is NOT part of OpenAI Agents SDK** - it's Python's built-in logging system. Think of it as your application's diary that records what happens, when it happens, and if something goes wrong.

### Why Use Logging in Agent Context?
- **🐛 Debug Issues**: See what your agent is doing step-by-step
- **📊 Track Usage**: Monitor which tools are being used
- **🚨 Catch Errors**: Get detailed error information
- **👤 Monitor Users**: Track user actions and patterns

---

## 📊 Log Levels (Most Important to Know)

```python
import logging

logger = logging.getLogger("my_agent")

logger.debug("Detailed info for developers")     # Level 10 - Development only
logger.info("General information")               # Level 20 - Normal events  
logger.warning("Something unexpected happened")  # Level 30 - Potential issues
logger.error("A serious problem occurred")       # Level 40 - Actual errors
logger.critical("System is broken!")             # Level 50 - Critical failures
```

**Rule**: If you set level to `INFO`, only `INFO`, `WARNING`, `ERROR`, and `CRITICAL` will show.

---

## 🚀 Basic Setup

### Simple Logging Setup
```python
import logging

# Basic configuration (do this once at the start)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Get a logger
logger = logging.getLogger("my_agent")

# Use it
logger.info("Agent started")
logger.error("Something went wrong")
```

### Better Setup for Agents
```python
import logging

def create_agent_logger(name: str) -> logging.Logger:
    """Create a logger for your agent"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console output
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - [%(name)s] %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

---

## 🤖 Using Logger in OpenAI Agents SDK

### Context with Logger
```python
from dataclasses import dataclass
import logging
from agents import function_tool, RunContextWrapper

@dataclass
class UserContext:
    user_id: str
    username: str
    logger: logging.Logger  # ← This is what we're learning about!
    
    def log_action(self, action: str):
        """Helper to log user actions"""
        self.logger.info(f"User {self.username} did: {action}")

# Create context with logger
def create_context(user_id: str, username: str) -> UserContext:
    logger = create_agent_logger(f"user_{user_id}")
    return UserContext(user_id, username, logger)
```

### Tools Using Logger
```python
@function_tool
async def get_profile(wrapper: RunContextWrapper[UserContext]) -> str:
    ctx = wrapper.context
    
    # Log what's happening
    ctx.logger.info(f"Getting profile for user: {ctx.username}")
    
    try:
        # Simulate getting profile
        profile_data = {"name": ctx.username, "status": "active"}
        
        # Log success
        ctx.logger.info("Profile retrieved successfully")
        return f"Profile: {profile_data}"
        
    except Exception as e:
        # Log error with details
        ctx.logger.error(f"Failed to get profile: {str(e)}")
        return "Sorry, couldn't get your profile"

@function_tool
async def update_settings(
    wrapper: RunContextWrapper[UserContext],
    setting: str,
    value: str
) -> str:
    ctx = wrapper.context
    
    # Log the attempt
    ctx.logger.info(f"Updating {setting} to {value} for {ctx.username}")
    
    # Use helper method
    ctx.log_action(f"updated_setting_{setting}")
    
    return f"✅ Updated {setting} to {value}"
```

---

## 🎯 Complete Working Example

```python
import asyncio
import logging
from dataclasses import dataclass
from agents import Agent, Runner, function_tool, RunContextWrapper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class ShopContext:
    customer_name: str
    cart_items: list
    logger: logging.Logger
    
    def add_item(self, item: str):
        self.cart_items.append(item)
        self.logger.info(f"Added {item} to {self.customer_name}'s cart")

@function_tool
async def add_to_cart(
    wrapper: RunContextWrapper[ShopContext],
    item: str
) -> str:
    ctx = wrapper.context
    
    # Log the action
    ctx.logger.info(f"Customer wants to add: {item}")
    
    # Add item using context method
    ctx.add_item(item)
    
    return f"Added {item} to your cart!"

@function_tool
async def view_cart(wrapper: RunContextWrapper[ShopContext]) -> str:
    ctx = wrapper.context
    
    # Log cart access
    ctx.logger.info(f"Showing cart to {ctx.customer_name}")
    
    if not ctx.cart_items:
        ctx.logger.info("Cart is empty")
        return "Your cart is empty"
    
    # Log cart contents (but not in production with real data!)
    ctx.logger.debug(f"Cart contents: {ctx.cart_items}")
    
    return f"Your cart: {', '.join(ctx.cart_items)}"

# Create agent
shop_agent = Agent[ShopContext](
    name="ShopBot",
    instructions="You help customers shop. Be friendly!",
    tools=[add_to_cart, view_cart]
)

async def main():
    # Create context with logger
    logger = logging.getLogger("shop_customer")
    context = ShopContext(
        customer_name="Alice",
        cart_items=[],
        logger=logger
    )
    
    print("🛍️ Shopping Bot Demo\n")
    
    # Example interactions
    requests = [
        "Add a laptop to my cart",
        "Also add a mouse",
        "Show me my cart"
    ]
    
    for request in requests:
        print(f"Customer: {request}")
        
        result = await Runner.run(
            starting_agent=shop_agent,
            input=request,
            context=context  # Logger is inside this context
        )
        
        print(f"Bot: {result.final_output}")
        print()  # Empty line for readability

if __name__ == "__main__":
    asyncio.run(main())
```

**Output will look like:**
```
2024-01-15 10:30:01,123 - INFO - Customer wants to add: laptop
2024-01-15 10:30:01,124 - INFO - Added laptop to Alice's cart
Customer: Add a laptop to my cart
Bot: Added laptop to your cart!

2024-01-15 10:30:02,125 - INFO - Customer wants to add: mouse  
2024-01-15 10:30:02,126 - INFO - Added mouse to Alice's cart
Customer: Also add a mouse
Bot: Added mouse to your cart!

2024-01-15 10:30:03,127 - INFO - Showing cart to Alice
2024-01-15 10:30:03,128 - DEBUG - Cart contents: ['laptop', 'mouse']
Customer: Show me my cart
Bot: Your cart: laptop, mouse
```

---

## ✅ Simple Best Practices

### Do This ✅
```python
# Good logging
logger.info("User logged in successfully")
logger.error("Database connection failed", exc_info=True)  # Shows full error
logger.debug("Processing data: %s", data)  # Efficient string formatting
```

### Don't Do This ❌
```python
# Bad logging  
print("User logged in")  # Use logger, not print
logger.info(f"Password: {password}")  # Never log sensitive data
logger.info("Debug info") # Wrong level - use logger.debug()
```

### Error Handling with Logging
```python
@function_tool
async def risky_operation(wrapper: RunContextWrapper[UserContext]) -> str:
    ctx = wrapper.context
    
    try:
        # Risky code here
        result = dangerous_function()
        ctx.logger.info("Operation succeeded")
        return result
        
    except Exception as e:
        # Log the error with full details
        ctx.logger.error(
            f"Operation failed for user {ctx.username}: {str(e)}",
            exc_info=True  # This includes the full error traceback
        )
        return "Sorry, something went wrong"
```

---

## 🎓 Key Takeaways

1. **`logging.Logger`** = Python's built-in system for recording what happens in your code
2. **We put it in context** so all tools can log consistently with user info
3. **Use appropriate levels**: `info()` for normal events, `error()` for problems
4. **Always log errors** with `exc_info=True` to get full details
5. **Never log sensitive data** like passwords or personal info
6. **Logging helps debug and monitor** your agents in production

That's it! Now you understand why we use `logger: logging.Logger` in our contexts and how to use it effectively. 🚀
