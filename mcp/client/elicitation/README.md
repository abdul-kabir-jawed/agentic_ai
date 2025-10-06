# 🎯 MCP Elicitation Mastery Guide

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;">

## What is Elicitation?

**Elicitation** enables servers to pause execution and request specific information from users dynamically, creating intelligent, conversational workflows instead of rigid, upfront data collection.

> **Think of it like this:** A smart assistant that asks clarifying questions exactly when needed, rather than demanding everything upfront.

</div>

---

## 🔄 The Elicitation Flow

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 5px solid #667eea;">

```
🖥️  Server needs data
    ↓
📤  Creates elicitation request
    ↓
🎨  Client displays beautiful UI
    ↓
👤  User provides information
    ↓
✅  Server receives validated data
    ↓
⚡  Continues processing with new context
```

</div>

---

## 📋 Elicitation Parameters

<div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin: 20px 0;">

### Core Parameters Explained

**`session`** - The active server session that manages communication between server and client

**`message`** - Human-readable text explaining what you need and why (e.g., "Please confirm your booking details")

**`schema`** - Pydantic model defining the structure of data you're collecting (field types, constraints, validation rules)

**`related_request_id`** *(optional)* - Links this elicitation to a parent operation, providing context about which tool/request triggered it

</div>

---

## 🏗️ Anatomy of an Elicitation Request

<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin: 30px 0;">

<div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">

### 1️⃣ Message
The clear, contextual question

*"Please confirm your Barcelona vacation booking details:"*

**Purpose:** Tells users what you need and why

</div>

<div style="background: #f3e5f5; padding: 20px; border-radius: 10px;">

### 2️⃣ Schema
The data structure definition

Field types, constraints, validation, required fields

**Purpose:** Ensures you get properly formatted data

</div>

<div style="background: #e8f5e9; padding: 20px; border-radius: 10px;">

### 3️⃣ Response
User's answer

Accept, Decline, or Cancel with validated data

**Purpose:** Contains the user's input or decision

</div>

</div>

---

## 🎨 Beautiful Example: Travel Booking

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">

```python
{
  method: "elicitation/requestInput",
  params: {
    message: "Please confirm your Barcelona vacation booking details:",
    schema: {
      type: "object",
      properties: {
        confirmBooking: {
          type: "boolean",
          description: "Confirm the booking (Flights + Hotel = $3,000)"
        },
        seatPreference: {
          type: "string",
          enum: ["window", "aisle", "no preference"],
          description: "Preferred seat type for flights"
        },
        roomType: {
          type: "string",
          enum: ["sea view", "city view", "garden view"],
          description: "Preferred room type at hotel"
        },
        travelInsurance: {
          type: "boolean",
          default: false,
          description: "Add travel insurance ($150)"
        }
      },
      required: ["confirmBooking"]
    }
  }
}
```

**What Happens:**
1. 🛑 Server pauses booking process
2. 📋 Shows user a beautiful form with options
3. ✍️ User selects preferences
4. ✅ Server receives validated data
5. 🚀 Completes booking with user's choices

</div>

---

## 📐 Schema Rules: The Golden Law

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d4edda; padding: 25px; border-radius: 10px; border: 2px solid #28a745;">

### ✅ Allowed Types

**Primitives Only:**
- `string` - Text input
- `int` / `float` - Numbers  
- `boolean` - True/False choices
- `Optional[primitive]` - Any above, but optional

**Why?** Simple questions get simple answers

</div>

<div style="background: #f8d7da; padding: 25px; border-radius: 10px; border: 2px solid #dc3545;">

### ❌ NOT Allowed

**Complex Types:**
- Lists/Arrays
- Nested objects
- Dictionaries
- Custom models

**Why?** Elicitation is for focused questions, not complex data structures

</div>

</div>

---

## 🎭 Three Possible Outcomes

<div style="margin: 30px 0;">

<div style="background: #d1f2eb; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #28a745;">

### ✅ Accepted
User provides the requested information

```python
AcceptedElicitation(
    action="accept",
    data={validated_user_input}  # Fully validated against schema
)
```

*Server continues with the user's data*

</div>

<div style="background: #fff3cd; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #ffc107;">

### ⊘ Declined
User chooses not to provide information

```python
DeclinedElicitation(action="decline")
```

*Server adapts or uses defaults*

</div>

<div style="background: #f8d7da; padding: 20px; border-radius: 10px; border-left: 5px solid #dc3545;">

### ✕ Cancelled
User cancels the entire operation

```python
CancelledElicitation(action="cancel")
```

*Server stops the current workflow*

</div>

</div>

---

## 💻 Implementation Pattern

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

```python
# Step 1: Define your schema model
class BookingConfirmation(BaseModel):
    confirmBooking: bool
    seatPreference: str | None = None
    roomType: str | None = None
    travelInsurance: bool = False

# Step 2: Request user input
result = await elicit_with_validation(
    session=session,
    message="Please confirm your Barcelona vacation booking:",
    schema=BookingConfirmation,
    related_request_id=request_id
)

# Step 3: Handle the response elegantly
match result.action:
    case "accept":
        booking_data = result.data  # Type-safe, validated data
        await complete_booking(booking_data)
    case "decline":
        await use_default_booking()
    case "cancel":
        return "Booking cancelled"
```

</div>

---

## 🎯 Key Benefits

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🌟 Better UX
No overwhelming forms  
Ask what's needed, when needed  
Natural conversation flow

</div>

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🔄 Flexible Workflows
Adapt to scenarios  
Handle missing data gracefully  
Progressive complexity

</div>

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px; text-align: center;">

### 🛡️ Type Safety
Automatic validation  
Catch errors early  
Clear data contracts

</div>

</div>

---

## 🔒 Privacy & Security

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### 🚫 NEVER Request

- **Passwords** - Absolutely never!
- **API keys** - Security risk!
- **Sensitive credentials** - Privacy violation!

### 🛡️ Client Must

- ✅ Warn about suspicious requests
- ✅ Show which server is asking
- ✅ Let users review before sending
- ✅ Provide clear context and purpose

</div>

---

## 💡 Common Use Cases

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;">

**Confirmation Dialogs**  
*"Proceed with deletion?" · "Confirm payment of $100?"*

**Missing Information**  
*"What's your preferred date format?" · "Which account should we use?"*

**User Preferences**  
*"How would you like results sorted?" · "Enable notifications?"*

**Progressive Details**  
*Basic info first, then specifics · "Need more details about X?"*

</div>

---

## 🎓 Best Practices

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #d1f2eb; padding: 25px; border-radius: 10px;">

### ✓ DO

- Keep messages clear and concise
- Use descriptive field names
- Provide helpful descriptions
- Set sensible defaults
- Mark truly required fields only
- Handle all response types

</div>

<div style="background: #f8d7da; padding: 25px; border-radius: 10px;">

### ✗ DON'T

- Ask for complex nested data
- Request sensitive credentials
- Make everything required
- Use vague field descriptions
- Ignore decline/cancel responses
- Chain multiple elicitations needlessly

</div>

</div>

---

## 🧠 Mental Model

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin: 30px 0; text-align: center;">

### Think of Elicitation as a Polite Interruption

**Traditional Approach:** "Give me ALL information NOW or I fail!"

**Elicitation Approach:** "I'm working on this... oh, I need one more thing. May I ask?"

It's an **interactive conversation** during execution, not a database query or rigid form.

</div>

---

## 🔧 The Validation Function

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

```python
async def elicit_with_validation(
    session: ServerSession,           # Active communication session
    message: str,                      # What you're asking for
    schema: type[ElicitSchemaModelT],  # Data structure (primitives only)
    related_request_id: RequestId | None = None  # Link to parent request
) -> ElicitationResult[ElicitSchemaModelT]
```

**Does Everything:**
- ✅ Validates schema before sending
- ✅ Sends request to client
- ✅ Receives response from user
- ✅ Parses and validates data
- ✅ Returns typed result

</div>

---

## 🎯 Master It in One Sentence

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 40px; border-radius: 15px; margin: 30px 0; text-align: center; font-size: 1.2em; font-weight: bold;">

*"Elicitation lets servers pause and ask users for specific information during execution, creating adaptive workflows instead of rigid forms."*

</div>

---

<div style="text-align: center; margin-top: 50px; color: #6c757d; font-style: italic;">

**You now have everything needed to master MCP Elicitation.**  
Build conversational, intelligent servers that adapt to user needs dynamically! 🚀

</div>
