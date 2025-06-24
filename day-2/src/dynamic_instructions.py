# src/day2/dynamic_instructions.py
import asyncio
from agents import Agent, Runner
from setup import create_gemini_config

class DynamicAgent:
    """
    A wrapper class that allows changing agent behavior dynamically
    
    Why we create this:
    - Sometimes we need to change agent behavior during runtime
    - More flexible than creating new agents each time
    - Useful for conversational flows where context changes
    """
    
    def __init__(self, base_name="Dynamic Agent"):
        self.base_name = base_name
        self.config, _, _ = create_gemini_config()
    
    def create_agent_for_task(self, task_type, additional_context=""):
        """
        Creates an agent with instructions tailored for specific tasks
        
        Parameters:
        - task_type: The type of task (email, code, creative, etc.)
        - additional_context: Extra context for this specific interaction
        """
        
        # Define different instruction templates
        instruction_templates = {
            'email': f"""You are a professional email assistant.
            Write clear, polite, and business-appropriate emails.
            Keep responses concise and actionable.
            {additional_context}""",
            
            'code': f"""You are a senior software engineer.
            Provide clean, well-commented code with explanations.
            Focus on best practices and readability.
            {additional_context}""",
            
            'creative': f"""You are a creative writing assistant.
            Be imaginative, engaging, and descriptive.
            Use vivid language and compelling narratives.
            {additional_context}""",
            
            'tutor': f"""You are a patient and encouraging tutor.
            Explain concepts step-by-step with examples.
            Ask clarifying questions to ensure understanding.
            {additional_context}""",
            
            'analyst': f"""You are a data analyst.
            Provide structured, logical analysis.
            Use facts and evidence to support conclusions.
            {additional_context}"""
        }
        
        if task_type not in instruction_templates:
            raise ValueError(f"Unknown task type: {task_type}")
        
        return Agent(
            name=f"{self.base_name} - {task_type.title()}",
            instructions=instruction_templates[task_type],
            model="gemini-2.0-flash"
        )
    
    async def handle_request(self, task_type, user_input, context=""):
        """
        Handle a user request with appropriate agent configuration
        """
        try:
            agent = self.create_agent_for_task(task_type, context)
            result = await Runner.run(agent, user_input, run_config=self.config)
            return result.final_output
        except Exception as e:
            print(f"you type wrong task_type {e}")


async def demo_dynamic_agents():
    """
    Demonstrate how one agent system can handle different types of tasks
    """
    print("🔄 Dynamic Agent Demo\n")
    
    # Create our dynamic agent system
    dynamic_system = DynamicAgent("Versatile Assistant")
    
    # Test different task types with the same system
    test_cases = [
        {
            'task': 'email',
            'input': 'Write a follow-up email to a client about a delayed project',
            'context': 'The delay is due to unexpected technical challenges.'
        },
        {
            'task': 'code', 
            'input': 'Write a Python function to calculate fibonacci numbers',
            'context': 'Make it efficient and handle edge cases.'
        },
        {
            'task': 'creative',
            'input': 'Describe a futuristic city',
            'context': 'Focus on environmental sustainability.'
        },
        {
            'task': 'tutor',
            'input': 'Explain what loops are in programming',
            'context': 'Explain to a beginner with no programming experience.'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"🎯 Test {i}: {test_case['task'].title()} Task")
        print(f"Input: {test_case['input']}")
        print(f"Context: {test_case['context']}")
        print("-" * 50)
        
        response = await dynamic_system.handle_request(
            test_case['task'],
            test_case['input'], 
            test_case['context']
        )
        
        print(f"Response: {response}")
        print("\n" + "="*60 + "\n")
        

async def demo_context_evolution():
    """
    Show how agent behavior can evolve with additional context
    """
    print("🌱 Context Evolution Demo\n")
    
    dynamic_system = DynamicAgent("Learning Assistant")
    
    # Start with basic tutoring
    print("1️⃣ Basic explanation:")
    response1 = await dynamic_system.handle_request(
        'tutor',
        'What is machine learning?',
        ''
    )
    print(f"Response: {response1}\n")
    
    # Add context about student level
    print("2️⃣ With student level context:")
    response2 = await dynamic_system.handle_request(
        'tutor',
        'What is machine learning?',
        'The student is a college computer science major with programming experience.'
    )
    print(f"Response: {response2}\n")
    
    # Add specific learning goals
    print("3️⃣ With specific learning goals:")
    response3 = await dynamic_system.handle_request(
        'tutor',
        'What is machine learning?',
        '''The student is a college CS major preparing for a job interview at a tech company. 
        Focus on practical applications and common interview topics.'''
    )
    print(f"Response: {response3}\n")

if __name__ == "__main__":
    asyncio.run(demo_dynamic_agents())
    asyncio.run(demo_context_evolution())
