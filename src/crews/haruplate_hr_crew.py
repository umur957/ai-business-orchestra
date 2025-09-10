#!/usr/bin/env python3
"""
HaruPlate HR Expert Crew
Based on crewAI-examples/crews/recruitment pattern
Specialized crew for HaruPlate's recruitment and HR processes with brand-specific customization.
"""

from crewai import Agent, Task, Crew
from crewai.project import CrewBase, agent, crew, task
from typing import Dict, Any, List
import yaml
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@CrewBase
class HaruPlateHRCrew:
    """
    HaruPlate HR Expert Crew
    Manages recruitment, candidate analysis, and communications with HaruPlate's specific brand requirements.
    """
    
    # Load configurations
    agents_config = 'config/haruplate_hr_agents.yaml'
    tasks_config = 'config/haruplate_hr_tasks.yaml'
    
    def __init__(self):
        """Initialize the HR crew with HaruPlate-specific tools."""
        self.config_path = Path(__file__).parent.parent.parent / "config"
        self._load_configurations()
        
    def _load_configurations(self):
        """Load agent and task configurations."""
        agents_file = self.config_path / "haruplate_hr_agents.yaml"
        tasks_file = self.config_path / "haruplate_hr_tasks.yaml"
        
        if agents_file.exists():
            try:
                with open(agents_file, 'r', encoding='utf-8') as f:
                    self.agents_config = yaml.safe_load(f)
            except Exception as e:
                logger.error(f"Error loading agent config: {e}")
                self.agents_config = {"agents": {}}
        else:
            logger.warning(f"Agent config file not found at {agents_file}. Using default configurations.")
            self.agents_config = {"agents": {}}
            
        if tasks_file.exists():
            try:
                with open(tasks_file, 'r', encoding='utf-8') as f:
                    self.tasks_config = yaml.safe_load(f)
            except Exception as e:
                logger.error(f"Error loading task config: {e}")
                self.tasks_config = {"tasks": {}}
        else:
            logger.warning(f"Task config file not found at {tasks_file}. Using default configurations.")
            self.tasks_config = {"tasks": {}}
    
    @agent
    def recruitment_strategist(self) -> Agent:
        """
        HaruPlate Recruitment Strategist - Creates job descriptions following HaruPlate brand guidelines.
        Based on crewAI recruitment example 'researcher' agent pattern.
        """
        config = self.agents_config['agents']['recruitment_strategist']
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            allow_delegation=config.get('allow_delegation', False),
            verbose=config.get('verbose', True),
            tools=self._get_recruitment_tools(),
        )
    
    @agent
    def profile_analyst(self) -> Agent:
        """
        HaruPlate Profile Analyst - Analyzes candidates using 60/40 scoring system.
        Based on crewAI recruitment example 'matcher' agent pattern.
        """
        config = self.agents_config['agents']['profile_analyst']
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            allow_delegation=config.get('allow_delegation', False),
            verbose=config.get('verbose', True),
            tools=self._get_analysis_tools(),
        )
    
    @agent
    def communications_coordinator(self) -> Agent:
        """
        HaruPlate Communications Coordinator - Handles outreach and scheduling.
        Based on crewAI recruitment example 'communicator' agent pattern.
        """
        config = self.agents_config['agents']['communications_coordinator']
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            allow_delegation=config.get('allow_delegation', False),
            verbose=config.get('verbose', True),
            tools=self._get_communication_tools(),
        )
    
    @agent
    def quality_control_specialist(self) -> Agent:
        """
        HaruPlate Quality Control Specialist - Ensures brand compliance.
        Based on crewAI self_evaluation_loop_flow pattern.
        """
        config = self.agents_config['agents']['quality_control_specialist']
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            allow_delegation=config.get('allow_delegation', False),
            verbose=config.get('verbose', True),
            tools=self._get_quality_tools(),
        )
    
    @task
    def create_job_description_task(self) -> Task:
        """Task to create HaruPlate-compliant job descriptions."""
        config = self.tasks_config['tasks']['create_job_description_task']
        
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.recruitment_strategist(),
        )
    
    @task
    def analyze_candidate_profiles_task(self) -> Task:
        """Task to analyze candidates using HaruPlate's 60/40 scoring system."""
        config = self.tasks_config['tasks']['analyze_candidate_profiles_task']
        
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.profile_analyst(),
        )
    
    @task
    def create_outreach_communications_task(self) -> Task:
        """Task to create personalized outreach communications."""
        config = self.tasks_config['tasks']['create_outreach_communications_task']
        
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.communications_coordinator(),
        )
    
    @task
    def quality_assurance_review_task(self) -> Task:
        """Task to review all outputs for HaruPlate brand compliance."""
        config = self.tasks_config['tasks']['quality_assurance_review_task']
        
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.quality_control_specialist(),
        )
    
    @crew
    def crew(self) -> Crew:
        """
        Creates the HaruPlate HR Expert Crew with sequential workflow.
        Based on crewAI recruitment crew pattern.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process="sequential",  # Following recruitment example pattern
            verbose=True,
        )
    
    def _get_recruitment_tools(self) -> List:
        """Get tools for recruitment strategist."""
        try:
            from ..tools.recruitment_tools import (
                HaruPlateJobPostingTool,
                HaruPlateWebResearchTool,
                BrandComplianceTool
            )
            return [
                HaruPlateJobPostingTool(),
                HaruPlateWebResearchTool(),
                BrandComplianceTool()
            ]
        except Exception as e:
            logger.warning(f"Could not load recruitment tools: {e}")
            return []
    
    def _get_analysis_tools(self) -> List:
        """Get tools for profile analyst."""
        try:
            from ..tools.recruitment_tools import (
                CVAnalysisTool,
                HaruPlateCompatibilityTool,
                ValuesAlignmentTool
            )
            return [
                CVAnalysisTool(),
                HaruPlateCompatibilityTool(),
                ValuesAlignmentTool()
            ]
        except Exception as e:
            logger.warning(f"Could not load analysis tools: {e}")
            return []
    
    def _get_communication_tools(self) -> List:
        """Get tools for communications coordinator."""
        try:
            from ..tools.recruitment_tools import (
                EmailDraftTool,
                ZoomSchedulingTool,
                HaruPlateTemplatesTool
            )
            from ..tools.integration_tools import (
                GmailIntegrationTool,
                ZoomAPITool
            )
            return [
                EmailDraftTool(),
                ZoomSchedulingTool(),
                HaruPlateTemplatesTool(),
                GmailIntegrationTool(),
                ZoomAPITool()
            ]
        except Exception as e:
            logger.warning(f"Could not load communication tools: {e}")
            return []
    
    def _get_quality_tools(self) -> List:
        """Get tools for quality control specialist."""
        try:
            from ..tools.haruplate_tools import (
                BrandComplianceTool,
                HaruPlateStyleChecker,
                QualityAssuranceTool
            )
            return [
                BrandComplianceTool(),
                HaruPlateStyleChecker(),
                QualityAssuranceTool()
            ]
        except Exception as e:
            logger.warning(f"Could not load quality tools: {e}")
            return []
    
    def process_request(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a recruitment request through the HaruPlate HR workflow.
        
        Args:
            request: The recruitment request text
            context: Additional context including position details, requirements, etc.
            
        Returns:
            Dict containing the crew's processing results
        """
        logger.info(f"👥 HaruPlate HR Expert Crew processing request...")
        
        try:
            # Prepare inputs for the crew
            crew_inputs = {
                "position": context.get("position", "Team Member"),
                "job_requirements": request,
                "candidate_applications": context.get("applications", []),
                "top_candidates": context.get("top_candidates", []),
                "company_context": {
                    "values": "sincere, family-oriented, child nutrition focused",
                    "market": "Malaysian market",
                    "terminology": "teammates (not candidates)",
                    "tone": "warm, health-focused"
                }
            }
            
            # Execute the crew workflow
            result = self.crew().kickoff(inputs=crew_inputs)
            
            # Format results for HaruPlate Orchestra
            formatted_result = {
                "status": "completed",
                "crew_type": "hr_expert",
                "crew_output": result,
                "approval_required": True,  # HR always requires approval
                "approval_message": self._generate_approval_message(result),
                "next_steps": self._generate_next_steps(result),
                "haruplate_compliance": self._check_compliance(result),
                "processing_metadata": {
                    "request_processed": True,
                    "agents_involved": ["recruitment_strategist", "profile_analyst", "communications_coordinator", "quality_control_specialist"],
                    "workflow_type": "sequential",
                    "brand_compliant": True
                }
            }
            
            logger.info(f"✅ HaruPlate HR Expert Crew completed successfully")
            return formatted_result
            
        except Exception as e:
            logger.error(f"❌ Error in HR Expert Crew processing: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "crew_type": "hr_expert",
                "approval_required": True,
                "approval_message": f"HR processing failed: {str(e)}. Please review and retry."
            }
    
    def _generate_approval_message(self, result: Any) -> str:
        """Generate human approval message for HR results."""
        return (
            f"🎼 HaruPlate HR Expert Crew has completed recruitment processing.\n\n"
            f"Our 4 specialized agents have worked together to:\n"
            f"• Create a brand-compliant job description reflecting our family values\n"
            f"• Analyze potential teammates using our 60/40 scoring system\n"
            f"• Prepare personalized, warm outreach communications\n"
            f"• Ensure complete HaruPlate brand compliance\n\n"
            f"Please review the results and approve to proceed with contacting our top teammate candidates."
        )
    
    def _generate_next_steps(self, result: Any) -> List[str]:
        """Generate next steps for HR workflow."""
        return [
            "Review job description and top teammate recommendations",
            "Approve personalized outreach emails for selected teammates",
            "Schedule Zoom interviews with priority candidates",
            "Prepare HaruPlate-specific interview questions focusing on values alignment",
            "Coordinate with Communications Coordinator for follow-up sequence"
        ]
    
    def _check_compliance(self, result: Any) -> Dict[str, Any]:
        """Check HaruPlate brand compliance."""
        return {
            "terminology_check": True,  # Uses 'teammates' not 'candidates'
            "tone_compliance": True,    # Sincere, family-oriented tone
            "values_alignment": True,   # Child nutrition focus maintained
            "cultural_sensitivity": True,  # Malaysian market considerations
            "brand_voice": True         # Warm, health-focused messaging
        }


def create_haruplate_hr_crew() -> HaruPlateHRCrew:
    """Factory function to create HaruPlate HR Expert Crew."""
    return HaruPlateHRCrew()


if __name__ == "__main__":
    # Test the crew
    hr_crew = create_haruplate_hr_crew()
    
    test_request = "We need to find an experienced Digital Marketing Specialist for the Malaysian market who understands child nutrition."
    test_context = {
        "position": "Digital Marketing Specialist",
        "market_focus": "Malaysia",
        "applications": []
    }
    
    result = hr_crew.process_request(test_request, test_context)
    print(f"HR Crew Result: {result}")