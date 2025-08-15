# 🚀 Mastering AI Agent Model Settings

> **Transform your AI agents from generic chatbots to precision-tuned assistants**

## 📖 Table of Contents
- [What Are Model Settings?](#-what-are-model-settings)
- [Core Configuration Options](#-core-configuration-options)
- [Practical Implementation Examples](#-practical-implementation-examples)
- [Advanced Configuration Techniques](#-advanced-configuration-techniques)
- [Best Practices & Use Cases](#-best-practices--use-cases)
- [Troubleshooting Common Issues](#-troubleshooting-common-issues)

---

## 🎯 What Are Model Settings?

Model Settings are the **control panel** for your AI agent's behavior. Think of them as the difference between a Swiss Army knife and a precision surgical instrument - both are tools, but one is specifically configured for the task at hand.

### 🎨 Real-World Analogy

Just like adjusting your camera settings for different photography scenarios:

| Scenario | Camera Setting | AI Equivalent |
|----------|---------------|---------------|
| 📸 Portrait Photo | Low Aperture (Sharp Focus) | Low Temperature (Precise Responses) |
| 🌅 Landscape | Wide Angle | High Max Tokens (Detailed Responses) |
| 🎪 Action Shot | Fast Shutter | Quick Tool Selection |

---

## ⚙️ Core Configuration Options

### 🌡️ Temperature: The Creativity Dial

**Temperature** controls the randomness and creativity of your AI's responses.

```python
# 🎯 Precision Mode (Temperature: 0.1-0.3)
precise_agent = Agent(
    name="DataAnalyst",
    instructions="Provide accurate, factual analysis of data patterns.",
    model_settings=ModelSettings(temperature=0.1)
)

# 🎨 Creative Mode (Temperature: 0.7-0.9)
creative_agent = Agent(
    name="ContentCreator", 
    instructions="Generate engaging, imaginative content.",
    model_settings=ModelSettings(temperature=0.8)
)

# ⚖️ Balanced Mode (Temperature: 0.4-0.6)
balanced_agent = Agent(
    name="GeneralAssistant",
    instructions="Provide helpful, well-rounded responses.",
    model_settings=ModelSettings(temperature=0.5)
)
```

#### 🎚️ Temperature Scale Guide

```
0.0 ████████████████████████ Deterministic (Same output every time)
0.2 ████████████████████░░░░ Highly Consistent  
0.5 ████████████░░░░░░░░░░░░ Balanced Creativity
0.8 ████░░░░░░░░░░░░░░░░░░░░ Highly Creative
1.0 ░░░░░░░░░░░░░░░░░░░░░░░░ Maximum Randomness
```

### 🛠️ Tool Choice: Functionality Control

Control when and how your agent uses available tools.

```python
from agents import Agent, ModelSettings, function_tool

@function_tool
def advanced_calculator(expression: str) -> str:
    """Evaluate complex mathematical expressions safely."""
    try:
        result = eval(expression)  # In production, use a safer evaluator
        return f"Result: {expression} = {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

# 🤖 Autonomous Tool Usage
auto_agent = Agent(
    name="SmartCalculator",
    tools=[advanced_calculator],
    model_settings=ModelSettings(tool_choice="auto")
)

# 🎯 Mandatory Tool Usage
required_agent = Agent(
    name="MustUseTool",
    tools=[advanced_calculator], 
    model_settings=ModelSettings(tool_choice="required")
)

# 💬 Chat-Only Mode
chat_agent = Agent(
    name="ConversationOnly",
    tools=[advanced_calculator],
    model_settings=ModelSettings(tool_choice="none")
)
```

### 📏 Max Tokens: Response Length Control

**Max Tokens** sets the absolute limit for response length. Think of it as the "word count limit" for your AI agent.

#### 🔢 Understanding Token Calculation
- **1 token ≈ 0.75 words** (English)
- **1 token ≈ 4 characters** (including spaces)
- **100 tokens ≈ 75 words ≈ 1-2 sentences**
- **500 tokens ≈ 375 words ≈ 1 paragraph**
- **1000 tokens ≈ 750 words ≈ 1-2 pages**

```python
# 📝 Concise Responses (50-300 tokens)
brief_agent = Agent(
    name="QuickAnswers",
    instructions="Provide concise, to-the-point responses. Be brief but complete.",
    model_settings=ModelSettings(
        max_tokens=200,            # ~150 words, perfect for quick answers
        temperature=0.4            # Focused and direct
    )
)

# 📚 Detailed Explanations (500-1500 tokens)  
detailed_agent = Agent(
    name="DetailedExplainer",
    instructions="Provide comprehensive, educational responses with examples.",
    model_settings=ModelSettings(
        max_tokens=1200,           # ~900 words, room for detailed explanations
        temperature=0.5            # Balanced detail and creativity
    )
)

# 📖 In-Depth Analysis (2000+ tokens)
comprehensive_agent = Agent(
    name="ResearchAssistant", 
    instructions="Provide thorough analysis with examples, context, and multiple perspectives.",
    model_settings=ModelSettings(
        max_tokens=3000,           # ~2250 words, extensive analysis
        temperature=0.4            # Structured and comprehensive
    )
)

# 🎯 Context-Aware Token Limits
smart_agent = Agent(
    name="AdaptiveResponder",
    instructions="""
    Adapt your response length to the complexity of the question:
    - Simple questions: 1-2 sentences  
    - Complex topics: Detailed explanations
    - Always use your full token allowance when needed
    """,
    model_settings=ModelSettings(max_tokens=1500)  # Flexible upper limit
)
```

#### 📊 Token Length Guide

| Token Count | Word Count | Use Case | Example Response Type |
|-------------|------------|----------|----------------------|
| **50-150** | 40-115 words | Quick answers, confirmations | "Yes, Python is object-oriented..." |
| **200-400** | 150-300 words | Short explanations, summaries | Brief how-to guides, definitions |
| **500-800** | 375-600 words | Detailed responses, tutorials | Step-by-step instructions |
| **1000-1500** | 750-1125 words | Comprehensive explanations | Educational content, analysis |
| **2000-3000** | 1500-2250 words | In-depth articles, reports | Research papers, detailed guides |
| **3000+** | 2250+ words | Extensive documentation | Technical manuals, comprehensive studies |

---

## 💻 Practical Implementation Examples

### Example 1: 🧮 Mathematical Problem Solver

```python
from agents import Agent, ModelSettings, Runner, function_tool
import math

@function_tool
def scientific_calculator(operation: str, x: float, y: float = None) -> str:
    """Perform scientific calculations."""
    operations = {
        'sqrt': lambda a, b: math.sqrt(a),
        'pow': lambda a, b: math.pow(a, b),
        'log': lambda a, b: math.log(a),
        'sin': lambda a, b: math.sin(math.radians(a))
    }
    
    if operation in operations:
        result = operations[operation](x, y)
        return f"{operation}({x}{f', {y}' if y else ''}) = {result}"
    return "Operation not supported"

math_expert = Agent(
    name="MathematicsExpert",
    instructions="""
    You are a precise mathematics expert. Always:
    1. Show step-by-step solutions
    2. Use tools for calculations
    3. Explain the mathematical concepts involved
    4. Verify your answers
    """,
    tools=[scientific_calculator],
    model_settings=ModelSettings(
        temperature=0.1,        # Maximum precision
        max_tokens=800,         # Detailed explanations
        tool_choice="auto"      # Use tools when needed
    )
)

# Test the math expert
result = Runner.run_sync(
    math_expert, 
    "Solve the quadratic equation: x² - 5x + 6 = 0. Show all steps."
)
print(result.final_output)
```

### Example 2: ✍️ Creative Writing Assistant

```python
@function_tool
def story_structure_analyzer(plot_type: str) -> str:
    """Analyze different story structures."""
    structures = {
        'hero_journey': "Hero's Journey: Call to Adventure → Trials → Transformation → Return",
        'three_act': "Three-Act Structure: Setup (25%) → Confrontation (50%) → Resolution (25%)",
        'mystery': "Mystery Structure: Hook → Investigation → Clues → Red Herrings → Revelation → Resolution"
    }
    return structures.get(plot_type, "Structure type not recognized")

creative_writer = Agent(
    name="CreativeWritingMentor",
    instructions="""
    You are an inspiring creative writing mentor. Help users:
    1. Develop compelling characters and plots
    2. Understand story structures
    3. Improve their writing style
    4. Overcome writer's block with creative exercises
    """,
    tools=[story_structure_analyzer],
    model_settings=ModelSettings(
        temperature=0.75,       # High creativity
        max_tokens=1500,        # Room for detailed feedback
        tool_choice="auto",     # Use structure analysis when helpful
        top_p=0.9              # Diverse vocabulary choices
    )
)

# Test the creative writer
result = Runner.run_sync(
    creative_writer,
    "I want to write a mystery novel about a detective who can see ghosts. Help me develop this concept."
)
print(result.final_output)
```

### Example 3: 🔍 Research Assistant

```python
@function_tool
def citation_formatter(source_type: str, **details) -> str:
    """Format academic citations in different styles."""
    if source_type == "book":
        return f"{details.get('author', 'Unknown')} ({details.get('year', 'n.d.')}). {details.get('title', 'Untitled')}. {details.get('publisher', 'Unknown Publisher')}."
    elif source_type == "article":
        return f"{details.get('author', 'Unknown')} ({details.get('year', 'n.d.')}). {details.get('title', 'Untitled')}. *{details.get('journal', 'Unknown Journal')}*, {details.get('volume', 'n.v.')}({details.get('issue', 'n.i.')}), {details.get('pages', 'n.p.')}."
    return "Citation format not supported"

research_assistant = Agent(
    name="AcademicResearcher",
    instructions="""
    You are a meticulous academic research assistant. Always:
    1. Provide well-structured, evidence-based responses
    2. Include proper citations and references
    3. Suggest multiple perspectives on complex topics
    4. Maintain academic integrity and objectivity
    """,
    tools=[citation_formatter],
    model_settings=ModelSettings(
        temperature=0.3,           # Balanced accuracy and insight
        max_tokens=2000,           # Comprehensive responses
        tool_choice="auto",        # Use citation tools
        frequency_penalty=0.3,     # Avoid repetitive language
        presence_penalty=0.2       # Encourage topic diversity
    )
)
```

---

## 🔬 Advanced Configuration Techniques

### 🔄 Parallel Tool Processing

```python
from agents import function_tool

@function_tool 
def weather_check(city: str) -> str:
    """Get weather information for a city."""
    # Simulated weather data
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Rainy, 58°F", 
        "Tokyo": "Cloudy, 68°F"
    }
    return weather_data.get(city, "Weather data not available")

@function_tool
def time_converter(time_str: str, from_zone: str, to_zone: str) -> str:
    """Convert time between timezones."""
    return f"Converting {time_str} from {from_zone} to {to_zone}: [Converted Time]"

# Multi-tasking agent with parallel processing
multitask_agent = Agent(
    name="MultiTaskAssistant",
    instructions="You can handle multiple requests simultaneously and efficiently.",
    tools=[weather_check, time_converter, scientific_calculator],
    model_settings=ModelSettings(
        temperature=0.4,
        max_tokens=1000,
        tool_choice="auto",
        parallel_tool_calls=True    # Enable parallel processing
    )
)

# Test parallel processing
result = Runner.run_sync(
    multitask_agent,
    "What's the weather in Tokyo and what time is 3 PM EST in Tokyo time?"
)
print(result.final_output)
```

### 🎛️ Advanced Response Control Parameters

#### 🎯 Top-P (Nucleus Sampling) 
**Top-P** controls vocabulary diversity by limiting the AI to consider only the most likely words that make up a certain probability mass.

```python
# 🎯 Focused Vocabulary (Top-P: 0.1-0.3)
focused_vocab_agent = Agent(
    name="PreciseWriter",
    instructions="Write technical documentation with precise terminology.",
    model_settings=ModelSettings(
        temperature=0.5,
        top_p=0.2,                # Only use top 20% most likely words
        max_tokens=800
    )
)

# 🌈 Diverse Vocabulary (Top-P: 0.8-0.95)
diverse_vocab_agent = Agent(
    name="CreativeWriter", 
    instructions="Write engaging creative content with varied language.",
    model_settings=ModelSettings(
        temperature=0.7,
        top_p=0.9,                # Use top 90% of vocabulary options
        max_tokens=1000
    )
)
```

#### 📊 Top-P Visualization
```
Top-P = 0.1:  ████░░░░░░ (10% of vocabulary - very focused)
Top-P = 0.5:  █████░░░░░ (50% of vocabulary - balanced)  
Top-P = 0.9:  █████████░ (90% of vocabulary - very diverse)
```

#### 🔄 Frequency Penalty
**Frequency Penalty** reduces the likelihood of repeating words that have already appeared, making responses less repetitive.Only work with OpenAI and Azure API.

```python
# 📝 High Repetition Tolerance (Frequency Penalty: 0.0)
repetitive_agent = Agent(
    name="TechnicalWriter",
    instructions="Write technical specifications that may need repeated terminology.",
    model_settings=ModelSettings(
        temperature=0.4,
        frequency_penalty=0.0,     # Allow repetition of technical terms
        max_tokens=800
    )
)

# 🔄 Anti-Repetition Mode (Frequency Penalty: 0.5-1.0)
varied_agent = Agent(
    name="EssayWriter",
    instructions="Write engaging essays with varied language.",
    model_settings=ModelSettings(
        temperature=0.6,
        frequency_penalty=0.7,     # Strong penalty against word repetition
        max_tokens=1200
    )
)
```

#### 🚀 Presence Penalty  
**Presence Penalty** encourages the AI to introduce new topics and concepts rather than staying on the same subject.

```python
# 🎯 Topic Focus (Presence Penalty: 0.0)
focused_topic_agent = Agent(
    name="SubjectExpert",
    instructions="Provide deep, focused analysis on specific topics.",
    model_settings=ModelSettings(
        temperature=0.4,
        presence_penalty=0.0,      # Stay focused on current topics
        max_tokens=1000
    )
)

# 🌟 Topic Exploration (Presence Penalty: 0.5-1.0)
exploratory_agent = Agent(
    name="BrainstormingPartner", 
    instructions="Help explore ideas from multiple angles and perspectives.",
    model_settings=ModelSettings(
        temperature=0.6,
        presence_penalty=0.6,      # Encourage exploring new topics
        max_tokens=1500
    )
)
```

#### 📈 Penalty Scale Reference
```
Frequency Penalty:
0.0 ████████████████████████ No penalty (allows repetition)
0.3 ████████████████░░░░░░░░ Light penalty  
0.6 ████████████░░░░░░░░░░░░ Moderate penalty
1.0 ░░░░░░░░░░░░░░░░░░░░░░░░ Maximum penalty (strong anti-repetition)

Presence Penalty:
0.0 ████████████████████████ Stay on topic
0.3 ████████████████░░░░░░░░ Slight topic variation
0.6 ████████████░░░░░░░░░░░░ Encourage new topics  
1.0 ░░░░░░░░░░░░░░░░░░░░░░░░ Maximum topic diversity
```

#### 🔬 Comprehensive Example: Blog Post Writer

```python
@function_tool
def research_topic(topic: str) -> str:
    """Research information about a given topic."""
    research_data = {
        "AI ethics": "Key considerations: bias, transparency, accountability, privacy",
        "climate change": "Current focus: renewable energy, carbon capture, policy changes",
        "space exploration": "Recent developments: Mars missions, private space companies, satellite technology"
    }
    return research_data.get(topic.lower(), "Research data not available for this topic")

blog_writer = Agent(
    name="ProfessionalBlogWriter",
    instructions="""
    You are a professional blog writer who creates engaging, well-researched content.
    Your writing should be:
    1. Informative and accurate
    2. Engaging with varied vocabulary  
    3. Well-structured with smooth transitions
    4. Free from unnecessary repetition
    """,
    tools=[research_topic],
    model_settings=ModelSettings(
        temperature=0.65,          # Balanced creativity and consistency
        max_tokens=1500,           # Room for comprehensive posts
        top_p=0.85,               # Rich vocabulary but not too scattered
        frequency_penalty=0.4,     # Reduce word repetition
        presence_penalty=0.3,      # Encourage topic development
        tool_choice="auto"
    )
)

# Test the blog writer
result = Runner.run_sync(
    blog_writer,
    "Write a blog post about the future of AI in education, covering both opportunities and challenges."
)
print(result.final_output)
```

#### 🎯 Parameter Interaction Effects

Understanding how these parameters work together:

```python
# 🏛️ Academic Writing Configuration
academic_agent = Agent(
    name="AcademicWriter",
    model_settings=ModelSettings(
        temperature=0.3,           # Consistent, formal tone
        top_p=0.7,                # Professional vocabulary
        frequency_penalty=0.2,     # Allow some technical repetition
        presence_penalty=0.1,      # Stay focused on academic topics
        max_tokens=2000
    )
)

# 🎨 Creative Writing Configuration  
creative_agent = Agent(
    name="CreativeWriter",
    model_settings=ModelSettings(
        temperature=0.8,           # High creativity
        top_p=0.9,                # Diverse vocabulary
        frequency_penalty=0.6,     # Avoid repetitive language
        presence_penalty=0.5,      # Explore various themes
        max_tokens=1800
    )
)

# 💼 Business Communication Configuration
business_agent = Agent(
    name="BusinessWriter", 
    model_settings=ModelSettings(
        temperature=0.4,           # Professional consistency
        top_p=0.75,               # Clear, professional language
        frequency_penalty=0.3,     # Some repetition OK for clarity
        presence_penalty=0.2,      # Stay on business topics
        max_tokens=1000
    )
)
```

---

## 📊 Best Practices & Use Cases

### 🎯 Complete Configuration Matrix

| Task Type | Temp | Tokens | Top-P | Freq Penalty | Presence Penalty | Tool Choice | Purpose |
|-----------|------|--------|-------|--------------|------------------|-------------|---------|
| **Data Analysis** | 0.1-0.2 | 800-1500 | 0.6-0.7 | 0.2 | 0.1 | Auto/Required | Precision & Accuracy |
| **Creative Writing** | 0.7-0.9 | 1000-2500 | 0.85-0.95 | 0.5-0.7 | 0.4-0.6 | Auto | Creativity & Variety |
| **Technical Documentation** | 0.2-0.3 | 1000-2000 | 0.6-0.7 | 0.1-0.2 | 0.1 | Auto | Clarity & Consistency |
| **Educational Tutoring** | 0.3-0.5 | 600-1200 | 0.7-0.8 | 0.3 | 0.2 | Auto | Engagement & Clarity |
| **Customer Support** | 0.3-0.4 | 300-800 | 0.7 | 0.2 | 0.1 | Auto | Consistency & Helpfulness |
| **Research Writing** | 0.4-0.6 | 1500-3000 | 0.75-0.85 | 0.3-0.4 | 0.2-0.3 | Auto | Thoroughness & Variety |
| **Code Review** | 0.1-0.2 | 800-1500 | 0.6 | 0.1 | 0.0 | Required | Technical Accuracy |
| **Brainstorming** | 0.8-0.9 | 800-1500 | 0.9-0.95 | 0.6-0.8 | 0.5-0.7 | Auto | Idea Generation |
| **Legal Writing** | 0.1-0.2 | 1500-2500 | 0.6-0.7 | 0.1 | 0.0 | Auto | Precision & Formality |
| **Marketing Copy** | 0.6-0.8 | 500-1200 | 0.8-0.9 | 0.4-0.6 | 0.3-0.4 | Auto | Persuasion & Variety |

### ⚠️ Common Pitfalls and Solutions

#### ❌ Problem: Generic, Boring Responses
**Symptoms:** Responses feel robotic and predictable
```python
# DON'T: Too restrictive settings
boring_agent = Agent(
    model_settings=ModelSettings(
        temperature=0.1,           # Too deterministic
        top_p=0.3,                # Too limited vocabulary
        frequency_penalty=0.0,     # Allows repetition
        presence_penalty=0.0       # No topic variation
    )
)

# ✅ DO: Balanced engagement settings  
engaging_agent = Agent(
    model_settings=ModelSettings(
        temperature=0.5,           # Balanced creativity
        top_p=0.8,                # Rich vocabulary
        frequency_penalty=0.3,     # Some variety in word choice
        presence_penalty=0.2       # Slight topic exploration
    )
)
```

#### ❌ Problem: Incoherent, Rambling Responses
**Symptoms:** Responses jump topics randomly or don't make sense
```python
# DON'T: Too chaotic settings
chaotic_agent = Agent(
    model_settings=ModelSettings(
        temperature=0.95,          # Too random
        top_p=0.95,               # Too diverse
        frequency_penalty=0.9,     # Excessive word avoidance  
        presence_penalty=0.9       # Constant topic jumping
    )
)

# ✅ DO: Controlled creativity settings
coherent_agent = Agent(
    model_settings=ModelSettings(
        temperature=0.7,           # Creative but controlled
        top_p=0.85,               # Diverse but focused
        frequency_penalty=0.4,     # Moderate word variety
        presence_penalty=0.3       # Some topic exploration
    )
)
```

#### ❌ Problem: Overly Repetitive Responses  
**Symptoms:** Same words/phrases repeated throughout response
```python
# DON'T: No repetition controls
repetitive_agent = Agent(
    model_settings=ModelSettings(
        temperature=0.3,
        frequency_penalty=0.0,     # No penalty for repetition
        presence_penalty=0.0       # No topic diversity
    )
)

# ✅ DO: Anti-repetition settings
varied_agent = Agent(
    model_settings=ModelSettings(
        temperature=0.4,
        frequency_penalty=0.5,     # Penalize word repetition
        presence_penalty=0.3,      # Encourage topic variety
        top_p=0.8                 # Access diverse vocabulary
    )
)
```

#### 🔧 Parameter Debugging Guide

```python
def debug_agent_settings():
    """Test different parameter combinations to find optimal settings."""
    
    test_prompt = "Explain the benefits of renewable energy"
    
    test_configs = [
        {
            "name": "Conservative", 
            "settings": ModelSettings(temperature=0.2, top_p=0.6, frequency_penalty=0.1, presence_penalty=0.1)
        },
        {
            "name": "Balanced",
            "settings": ModelSettings(temperature=0.5, top_p=0.8, frequency_penalty=0.3, presence_penalty=0.2) 
        },
        {
            "name": "Creative",
            "settings": ModelSettings(temperature=0.8, top_p=0.9, frequency_penalty=0.5, presence_penalty=0.4)
        }
    ]
    
    for config in test_configs:
        agent = Agent(
            name=f"Test_{config['name']}",
            instructions="Provide a helpful explanation.",
            model_settings=config["settings"]
        )
        
        result = Runner.run_sync(agent, test_prompt)
        
        print(f"\n🧪 {config['name']} Configuration:")
        print(f"Settings: {config['settings']}")
        print(f"Response: {result.final_output[:200]}...")
        print("-" * 60)

# Run parameter debugging
debug_agent_settings()
```

### 🧪 A/B Testing Your Settings

```python
def test_agent_configurations():
    """Compare different model settings for the same task."""
    
    test_prompt = "Explain quantum computing in simple terms"
    
    configs = [
        {"name": "Precise", "temp": 0.1, "tokens": 500},
        {"name": "Balanced", "temp": 0.5, "tokens": 500}, 
        {"name": "Creative", "temp": 0.8, "tokens": 500}
    ]
    
    for config in configs:
        agent = Agent(
            name=f"Test_{config['name']}",
            model_settings=ModelSettings(
                temperature=config['temp'],
                max_tokens=config['tokens']
            )
        )
        
        result = Runner.run_sync(agent, test_prompt)
        print(f"\n--- {config['name']} Response ---")
        print(result.final_output)
        print("-" * 40)

# Run A/B test
test_agent_configurations()
```

---

## 🔧 Troubleshooting Common Issues

### 🐛 Issue: Inconsistent Responses
**Solution:** Lower the temperature and increase frequency_penalty
```python
consistent_agent = Agent(
    model_settings=ModelSettings(
        temperature=0.2,           # More deterministic
        frequency_penalty=0.4      # Reduce repetition
    )
)
```

### 🐛 Issue: Responses Too Short
**Solution:** Increase max_tokens and adjust instructions
```python
verbose_agent = Agent(
    instructions="Provide detailed, comprehensive responses with examples.",
    model_settings=ModelSettings(max_tokens=1500)
)
```

### 🐛 Issue: Agent Not Using Tools
**Solution:** Set tool_choice to "required" or improve instructions
```python
tool_focused_agent = Agent(
    instructions="Always use available tools to provide accurate information.",
    model_settings=ModelSettings(tool_choice="required")
)
```

---

## 🚀 Next Steps

1. **Experiment** with the provided examples in your own environment
2. **Create** your own specialized agents for specific use cases
3. **Monitor** and **iterate** on your model settings based on performance
4. **Document** your successful configurations for future reference

---

## 📚 Additional Resources

- 📖 [Advanced Prompting Techniques](./advanced-prompting.md)
- 🛠️ [Custom Tool Development Guide](./custom-tools.md)
- 📊 [Performance Monitoring Best Practices](./monitoring.md)
- 🤝 [Multi-Agent Coordination](./multi-agent-systems.md)


*Happy Agent Building!* 🤖✨

</div>
