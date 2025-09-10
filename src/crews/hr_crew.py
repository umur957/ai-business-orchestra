"""
HR Crew Module
Specialized crew for human resources and recruitment operations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crewai import Crew, Process
from src.agents.hr_agent import HRAgent
from src.agents.conductor_agent import ConductorAgent
from src.tasks.hr_tasks import HRTasks
from src.tools.integration_tools import get_tool

class HRCrew:
    """Specialized crew for HR operations"""
    
    def __init__(self):
        self.hr_agent = HRAgent().get_agent()
        self.conductor_agent = ConductorAgent().get_agent()
        self.hr_tasks = HRTasks()
        
        # Add tools to agents
        self._setup_tools()
        
        self.crew = Crew(
            agents=[self.conductor_agent, self.hr_agent],
            tasks=[],  # Tasks will be added dynamically
            process=Process.sequential,
            verbose=True,
            memory=True
        )
    
    def _setup_tools(self):
        """Setup tools for HR agents"""
        email_tool = get_tool('email')
        calendar_tool = get_tool('calendar')
        hr_system_tool = get_tool('hr_system')
        
        if email_tool:
            self.hr_agent.tools.append(email_tool)
        if calendar_tool:
            self.hr_agent.tools.append(calendar_tool)
        if hr_system_tool:
            self.hr_agent.tools.append(hr_system_tool)
    
    def recruitment_process(self, job_details: dict) -> str:
        """Run complete recruitment process"""
        tasks = [
            self.hr_tasks.create_recruitment_analysis_task(job_details),
            self.hr_tasks.create_job_posting_task(job_details),
        ]
        
        self.crew.tasks = tasks
        result = self.crew.kickoff()
        return str(result)
    
    def candidate_evaluation(self, candidates: list) -> str:
        """Evaluate candidates for a position"""
        task = self.hr_tasks.create_candidate_evaluation_task(candidates)
        self.crew.tasks = [task]
        result = self.crew.kickoff()
        return str(result)
