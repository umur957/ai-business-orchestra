#!/usr/bin/env python3
"""
AI Business Orchestra - Intelligent HR and Admin Automation
A powerful CrewAI-based system for automating business operations

Author: Umur Kızıldaş (umur957)
License: MIT License
"""

import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

try:
    from crewai import Agent, Task, Crew, Process
    CREWAI_AVAILABLE = True
except ImportError:
    print("❌ CrewAI not available")
    CREWAI_AVAILABLE = False

class BusinessOrchestra:
    """Intelligent business automation system powered by CrewAI"""
    
    def __init__(self):
        self.company_name = os.getenv("COMPANY_NAME", "Your Company")
        self.company_values = os.getenv("COMPANY_CULTURE_VALUES", 
                                      "professional, innovative, customer-focused, quality-driven")
        self.tone_of_voice = os.getenv("COMPANY_TONE_OF_VOICE",
                                     "professional, friendly, solution-oriented")
        
        if CREWAI_AVAILABLE:
            self._setup_agents()
            self._setup_crew()
    
    def _setup_agents(self):
        """Setup Business Orchestra agents"""
        
        # Orchestra Conductor - Main coordinator
        self.conductor = Agent(
            role="Business Orchestra Conductor",
            goal=f"""Coordinate and orchestrate all HR and administrative tasks for {self.company_name}, 
            ensuring all operations align with company values: {self.company_values}""",
            backstory=f"""You are the central intelligence of the Business Orchestra, a sophisticated 
            AI system designed to automate HR recruitment and administrative operations. You understand 
            {self.company_name}'s business objectives and ensure all communications maintain a 
            {self.tone_of_voice} tone.""",
            verbose=True,
            allow_delegation=True
        )
        
        # HR Specialist
        self.hr_specialist = Agent(
            role="HR Recruitment Specialist",
            goal=f"""Handle all HR recruitment tasks including job posting creation, candidate analysis, 
            and interview coordination while maintaining {self.company_name}'s professional culture""",
            backstory=f"""You are an expert in HR recruitment with deep understanding of {self.company_name}'s 
            culture. You excel at creating job descriptions that reflect company values 
            and finding candidates who align with the company mission. 
            You always use professional, clear language and focus on finding the best talent.""",
            verbose=True,
            allow_delegation=False
        )
        
        # Admin Specialist
        self.admin_specialist = Agent(
            role="Administrative Operations Specialist", 
            goal=f"""Manage all administrative tasks including document processing, financial operations, 
            meeting preparation, and data analysis for {self.company_name}""",
            backstory=f"""You are an expert in administrative operations who ensures the smooth running 
            of {self.company_name}'s daily business. You excel at processing financial documents, organizing 
            files, preparing meeting materials, and analyzing business data. You maintain high standards 
            of accuracy and efficiency in all operations.""",
            verbose=True,
            allow_delegation=False
        )
    
    def _setup_crew(self):
        """Setup the main crew"""
        if not CREWAI_AVAILABLE:
            return
            
        self.crew = Crew(
            agents=[self.conductor, self.hr_specialist, self.admin_specialist],
            tasks=[],  # Tasks will be created dynamically
            process=Process.sequential,
            verbose=True
        )
    
    def process_request(self, request: str) -> str:
        """Process a request through the Orchestra"""
        
        if not CREWAI_AVAILABLE:
            return self._simulate_response(request)
        
        # Check if OpenAI API key is configured
        if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY").startswith("sk-your_"):
            return self._simulate_response(request)
        
        # Create task based on request
        task = self._create_task_for_request(request)
        
        # Create crew with the specific task
        crew = Crew(
            agents=[self.conductor, self.hr_specialist, self.admin_specialist],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        try:
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            return f"❌ Error processing request: {str(e)}\n\n{self._simulate_response(request)}"
    
    def _create_task_for_request(self, request: str) -> Task:
        """Create appropriate task based on request type"""
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['hire', 'recruit', 'candidate', 'job']):
            # HR recruitment task
            return Task(
                description=f"""Analyze this HR recruitment request: '{request}'
                
                Create a comprehensive response that includes:
                1. Job description that reflects company values
                2. Recruitment strategy for the target market
                3. Candidate evaluation criteria
                4. Interview process recommendations
                
                Maintain professional tone and focus on finding the best talent 
                that aligns with company culture and objectives.""",
                expected_output="""A detailed HR recruitment plan including job description, 
                recruitment strategy, and evaluation criteria that aligns with company values""",
                agent=self.hr_specialist
            )
        
        elif any(word in request_lower for word in ['invoice', 'financial', 'document', 'meeting', 'data']):
            # Admin task
            return Task(
                description=f"""Handle this administrative request: '{request}'
                
                Provide a comprehensive solution that includes:
                1. Analysis of the administrative need
                2. Step-by-step process to complete the task
                3. Timeline and resource requirements
                4. Quality control measures
                
                Ensure all recommendations align with professional business standards 
                and operational efficiency.""",
                expected_output="""A detailed administrative solution with clear steps, 
                timeline, and quality measures that meets business standards""",
                agent=self.admin_specialist
            )
        
        else:
            # General coordination task
            return Task(
                description=f"""Coordinate the response to this general request: '{request}'
                
                Analyze the request and provide:
                1. Classification of the request type
                2. Recommended approach and resources needed
                3. Timeline for completion
                4. Next steps for implementation
                
                Ensure the response reflects professional business approach.""",
                expected_output="""A coordinated response with clear classification, 
                approach, timeline, and next steps that reflects business values""",
                agent=self.conductor
            )
    
    def _simulate_response(self, request: str) -> str:
        """Simulate response when CrewAI is not available or configured"""
        
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['hire', 'recruit', 'candidate', 'job']):
            return f"""🎼 Business Orchestra - HR Recruitment Response

📝 Request: {request}

👥 HR SPECIALIST ANALYSIS:
Our HR team has analyzed your recruitment request. Here's our comprehensive plan:

📋 JOB DESCRIPTION FRAMEWORK:
We'll create a compelling job description that aligns with your company's mission and values. 
The posting will use professional language and attract qualified candidates.

🎯 RECRUITMENT STRATEGY:
• Target platforms: LinkedIn, Indeed, relevant job boards
• Emphasize company values and culture
• Highlight growth opportunities and impact

🔍 CANDIDATE EVALUATION:
• Technical competency assessment
• Cultural alignment with company values
• Relevant experience and skills
• Communication and teamwork abilities

📅 NEXT STEPS:
1. Create detailed job description (2-3 hours)
2. Publish on recommended platforms (1 hour)
3. Screen applications for best fit (ongoing)
4. Schedule interviews with top candidates (1 week)

Ready to help you find the perfect candidate! 🌟"""

        elif any(word in request_lower for word in ['invoice', 'financial', 'document', 'meeting', 'data']):
            return f"""🎼 Business Orchestra - Admin Operations Response

📝 Request: {request}

📊 ADMIN SPECIALIST ANALYSIS:
Our admin team is ready to handle your operational needs efficiently:

⚡ PROCESSING PLAN:
We'll streamline this administrative task using proven workflows, 
ensuring accuracy and compliance with business standards.

🔧 IMPLEMENTATION APPROACH:
• Automated document processing where possible
• Quality control checks at each stage
• Integration with existing systems
• Comprehensive reporting and tracking

📈 EXPECTED OUTCOMES:
• Improved efficiency and accuracy
• Standardized documentation
• Better data organization
• Time savings for strategic activities

📅 TIMELINE:
• Initial processing: 30-60 minutes
• Quality review: 15-30 minutes
• Final documentation: 15 minutes
• Total estimated time: 1-2 hours

Your administrative tasks are in capable hands! 🚀"""

        else:
            return f"""🎼 Business Orchestra - General Coordination Response

📝 Request: {request}

🎯 CONDUCTOR ANALYSIS:
As your Orchestra Conductor, I've analyzed your request and here's my coordination plan:

🔍 REQUEST CLASSIFICATION:
This appears to be a general business inquiry that may involve multiple departments. 
I'll coordinate the appropriate resources to provide you with a comprehensive solution.

📋 RECOMMENDED APPROACH:
• Detailed analysis of requirements
• Resource allocation from HR and/or Admin teams
• Phased implementation plan
• Regular progress updates

⏰ ESTIMATED TIMELINE:
Based on the scope of your request, we estimate 2-4 hours for complete resolution, 
depending on complexity and resource requirements.

🎯 COMPANY VALUES ALIGNMENT:
All solutions will maintain our commitment to professional service 
and support your business objectives.

Ready to orchestrate the perfect solution! 🎼"""

def main():
    """Main function to run Business Orchestra"""
    
    print("🎼 AI Business Orchestra - Intelligent Automation")
    print("=" * 55)
    
    # Initialize Orchestra
    orchestra = BusinessOrchestra()
    print(f"✅ Orchestra initialized for {orchestra.company_name}")
    
    if CREWAI_AVAILABLE and os.getenv("OPENAI_API_KEY") and not os.getenv("OPENAI_API_KEY").startswith("sk-your_"):
        print("🤖 CrewAI mode: Real AI agents active")
    else:
        print("🎭 Simulation mode: Mock responses (configure API keys for real AI)")
    
    print(f"📋 Company values: {orchestra.company_values}")
    print()
    
    # Example requests
    example_requests = [
        "We need to hire a Digital Marketing Specialist for our target market",
        "Please process the supplier invoices from this week",
        "Prepare meeting materials for tomorrow's board meeting about expansion strategy"
    ]
    
    print("🧪 Testing with example requests...")
    print("-" * 40)
    
    for i, request in enumerate(example_requests, 1):
        print(f"\n📧 Example Request {i}:")
        print(f"'{request}'")
        print("\n🔄 Processing...")
        
        response = orchestra.process_request(request)
        print(response)
        print("\n" + "="*80)
    
    print("\n🎉 Business Orchestra testing complete!")
    print("\n💡 To use with real AI:")
    print("1. Set your OpenAI API key in .env file")
    print("2. Run this script again")
    print("3. Try your own requests!")

if __name__ == "__main__":
    main()
