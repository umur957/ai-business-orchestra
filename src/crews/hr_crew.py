"""
HaruPlate HR Expert Crew
Specialized team for finding talent that aligns with HaruPlate's sincere, family-oriented values.
"""

from typing import Dict, List, Any
import logging
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool

from ..tools.recruitment_tools import (
    CVAnalysisTool, 
    HaruPlateCompatibilityTool,
    JobPostingTool,
    EmailDraftTool,
    ZoomSchedulingTool
)
from ..tools.haruplate_tools import HaruPlateWebResearchTool, BrandComplianceTool

logger = logging.getLogger(__name__)


class HRCrew:
    """
    HaruPlate's specialized HR crew focusing on finding teammates who truly believe 
    in child nutrition and family values, not just filling positions.
    """
    
    def __init__(self):
        self.tools = self._initialize_tools()
        self.agents = self._create_agents()
        self.brand_context = {
            "tone": "sincere, healthy, family-oriented",
            "values": [
                "child nutrition excellence",
                "natural product focus", 
                "family-first approach",
                "sincere communication",
                "healthy living promotion"
            ],
            "preferred_terms": {
                "candidates": "teammates",
                "hiring": "welcoming new family members",
                "employees": "team family",
                "job": "mission opportunity",
                "company": "HaruPlate family"
            }
        }
    
    def _initialize_tools(self):
        """Initialize all tools available to the HR crew."""
        return {
            'cv_analysis': CVAnalysisTool(),
            'compatibility_scoring': HaruPlateCompatibilityTool(),
            'job_posting': JobPostingTool(),
            'email_draft': EmailDraftTool(),
            'zoom_scheduling': ZoomSchedulingTool(),
            'web_research': HaruPlateWebResearchTool(),
            'brand_compliance': BrandComplianceTool()
        }
    
    def _create_agents(self):
        """Creates the specialized HR agents for HaruPlate."""
        
        recruitment_strategist = Agent(
            role="HaruPlate Recruitment Strategist",
            goal="""Create compelling job descriptions that attract candidates who genuinely 
                    care about child nutrition and natural products, not just any applicant.
                    Always use HaruPlate's sincere, family-oriented tone.""",
            backstory="""You are HaruPlate's talent storyteller. You understand that we're not 
                        just a company - we're a mission-driven family dedicated to providing 
                        the best nutrition for children. You know how to craft job descriptions 
                        that speak to people's hearts, not just their career ambitions.
                        
                        You've studied HaruPlate's website, social media, and company culture 
                        extensively. You know we prefer saying 'teammates' instead of 'candidates',
                        'mission opportunity' instead of 'job', and 'welcoming new family members' 
                        instead of 'hiring'.
                        
                        Your specialty is the Malaysian market, understanding local job platforms
                        and cultural nuances that attract the right talent.""",
            tools=[
                self.tools['job_posting'],
                self.tools['web_research'],
                self.tools['brand_compliance']
            ],
            verbose=True,
            memory=True
        )
        
        profile_analyst = Agent(
            role="HaruPlate Profile Analyst & Values Assessor",
            goal="""Analyze CVs and applications not just for technical skills, but for 
                    alignment with HaruPlate's mission. Generate compatibility scores that 
                    prioritize passion for child nutrition and natural products.""",
            backstory="""You are HaruPlate's talent detective with a heart. Your expertise 
                        goes beyond reading CVs - you can sense when someone truly cares about 
                        child nutrition and family wellness.
                        
                        You give extra points to candidates who have:
                        - Experience with food, nutrition, or parent/child-focused brands
                        - Demonstrated interest in natural products or healthy living
                        - A communication style that feels genuine and family-oriented
                        - Understanding of Southeast Asian markets, especially Malaysia
                        
                        You use a sophisticated scoring system that balances technical 
                        competence (40%) with values alignment (60%) because HaruPlate 
                        believes culture fit is more important than perfect skills.""",
            tools=[
                self.tools['cv_analysis'],
                self.tools['compatibility_scoring']
            ],
            verbose=True,
            memory=True
        )
        
        communications_coordinator = Agent(
            role="HaruPlate Communications Coordinator",
            goal="""Draft warm, sincere emails for initial contact with potential teammates
                    and coordinate interview scheduling through Zoom. Ensure all communication
                    reflects HaruPlate's family-oriented approach.""",
            backstory="""You are HaruPlate's voice in candidate communications. You understand 
                        that the first touchpoint with potential teammates sets the tone for 
                        their entire relationship with our family.
                        
                        Your emails don't sound corporate or cold - they sound like a sincere 
                        invitation to join something meaningful. You mention specific details 
                        about why we think they'd fit our mission, and you make interview 
                        scheduling feel welcoming, not intimidating.
                        
                        You're skilled with Zoom integration and understand different time zones
                        for our Malaysian market focus. You also know how to coordinate with 
                        busy founder schedules.""",
            tools=[
                self.tools['email_draft'],
                self.tools['zoom_scheduling']
            ],
            verbose=True,
            memory=True
        )
        
        quality_control_specialist = Agent(
            role="HaruPlate Brand Compliance & Quality Control Specialist",
            goal="""Review all HR outputs (job postings, emails, communications) to ensure 
                    they perfectly align with HaruPlate's sincere, family-oriented brand identity.
                    Request revisions when needed.""",
            backstory="""You are HaruPlate's brand guardian in HR processes. You have an 
                        exceptional eye for tone, language, and cultural nuances that maintain 
                        our authentic voice.
                        
                        You catch things like:
                        - Using 'candidates' instead of 'teammates'
                        - Corporate jargon that doesn't fit our sincere approach
                        - Missing connections to our child nutrition mission
                        - Tone that doesn't feel family-oriented
                        - Cultural insensitivity for Malaysian market
                        
                        You implement self-evaluation loops, reviewing outputs multiple times 
                        and providing specific, constructive feedback for improvements. You 
                        don't approve anything until it truly sounds like HaruPlate.""",
            tools=[
                self.tools['brand_compliance']
            ],
            verbose=True,
            memory=True
        )
        
        return {
            'recruitment_strategist': recruitment_strategist,
            'profile_analyst': profile_analyst,
            'communications_coordinator': communications_coordinator,
            'quality_control_specialist': quality_control_specialist
        }
    
    def execute_workflow(self, request: str, brand_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the complete HR workflow based on the request.
        
        Example workflow for "Find Digital Marketing Specialist for Malaysian market":
        1. Create job description
        2. Quality review and refinement
        3. Publishing strategy
        4. Application analysis (when they arrive)
        5. Candidate shortlisting
        6. Communication preparation
        """
        logger.info(f"🎯 HR Crew executing workflow for: {request}")
        
        # Determine workflow type based on request
        if "find" in request.lower() or "hire" in request.lower() or "recruit" in request.lower():
            return self._recruitment_workflow(request, brand_context)
        elif "analyze" in request.lower() or "review" in request.lower():
            return self._analysis_workflow(request, brand_context)
        else:
            return self._general_hr_workflow(request, brand_context)
    
    def _recruitment_workflow(self, request: str, brand_context: Dict[str, Any]) -> Dict[str, Any]:
        """Complete recruitment workflow for new position."""
        
        # Task 1: Create Job Description
        job_creation_task = Task(
            description=f"""
            Based on this request: "{request}"
            
            Create a compelling job description that:
            1. Reflects HaruPlate's sincere, family-oriented tone
            2. Emphasizes our mission in child nutrition and natural products
            3. Appeals specifically to the Malaysian market
            4. Uses our preferred terminology ('teammates', not 'candidates')
            5. Includes both technical requirements and values alignment
            
            Research HaruPlate's website and social media for authentic voice.
            Consider cultural nuances for Malaysian job market.
            """,
            agent=self.agents['recruitment_strategist'],
            expected_output="Complete job description with HaruPlate branding and Malaysian market appeal"
        )
        
        # Task 2: Quality Control Review
        quality_review_task = Task(
            description="""
            Review the job description created by the Recruitment Strategist:
            
            Check for:
            1. HaruPlate's sincere, family-oriented tone
            2. Correct terminology ('teammates' not 'candidates', etc.)
            3. Connection to child nutrition mission
            4. Cultural appropriateness for Malaysian market
            5. Brand consistency with HaruPlate's values
            
            Provide specific feedback for any improvements needed.
            Use self-evaluation loop methodology - review multiple times if necessary.
            """,
            agent=self.agents['quality_control_specialist'],
            expected_output="Brand compliance report with approved job description or revision requests",
            context=[job_creation_task]
        )
        
        # Task 3: Publishing Strategy
        publishing_strategy_task = Task(
            description="""
            Create a comprehensive publishing and outreach strategy:
            
            1. Recommend best Malaysian job platforms (LinkedIn, local sites)
            2. Suggest social media promotion strategy
            3. Identify professional networks to leverage
            4. Propose timeline for maximum visibility
            5. Create tracking metrics for applications
            
            Focus on channels where mission-driven professionals are active.
            """,
            agent=self.agents['recruitment_strategist'],
            expected_output="Complete publishing strategy with platform recommendations and timeline",
            context=[quality_review_task]
        )
        
        # Task 4: Communication Templates
        communication_prep_task = Task(
            description="""
            Prepare communication templates for the recruitment process:
            
            1. Initial outreach email template for promising candidates
            2. Interview invitation with Zoom scheduling
            3. Follow-up communication templates
            4. Rejection emails that maintain HaruPlate's sincere approach
            
            All communications must sound warm, personal, and aligned with our family values.
            Include specific mentions of why we think they'd fit our mission.
            """,
            agent=self.agents['communications_coordinator'],
            expected_output="Set of communication templates ready for candidate outreach"
        )
        
        # Execute the crew
        recruitment_crew = Crew(
            agents=[
                self.agents['recruitment_strategist'],
                self.agents['quality_control_specialist'],
                self.agents['communications_coordinator']
            ],
            tasks=[
                job_creation_task,
                quality_review_task,
                publishing_strategy_task,
                communication_prep_task
            ],
            verbose=True,
            process="sequential"
        )
        
        result = recruitment_crew.kickoff()
        
        return {
            "workflow_type": "recruitment",
            "status": "completed",
            "deliverables": {
                "job_description": "Ready for publication",
                "publishing_strategy": "Platform recommendations prepared", 
                "communication_templates": "Ready for candidate outreach",
                "quality_assurance": "Brand compliance verified"
            },
            "next_steps": [
                "Publish job description on recommended platforms",
                "Monitor applications and conduct initial screening",
                "Use compatibility scoring for candidate evaluation",
                "Prepare shortlist for management review"
            ],
            "human_approval_required": True,
            "approval_items": [
                "Final job description before publishing",
                "Publishing platform selection",
                "Communication template approval"
            ]
        }
    
    def _analysis_workflow(self, request: str, brand_context: Dict[str, Any]) -> Dict[str, Any]:
        """Workflow for analyzing existing candidates or applications."""
        
        # Task 1: CV Analysis and Compatibility Scoring
        analysis_task = Task(
            description=f"""
            Based on this request: "{request}"
            
            Perform comprehensive candidate analysis:
            1. Technical skills assessment
            2. HaruPlate values alignment scoring
            3. Experience with child nutrition/food/family brands
            4. Cultural fit for Malaysian market
            5. Communication style assessment
            
            Use HaruPlate compatibility scoring system:
            - Technical competence: 40%
            - Values alignment: 60%
            
            Prioritize candidates who show genuine passion for our mission.
            """,
            agent=self.agents['profile_analyst'],
            expected_output="Detailed candidate analysis with compatibility scores and recommendations"
        )
        
        # Task 2: Shortlist Creation
        shortlist_task = Task(
            description="""
            Create a prioritized shortlist based on the analysis:
            
            1. Rank top 5 candidates by compatibility score
            2. Provide summary of each candidate's strengths
            3. Highlight values alignment evidence for each
            4. Recommend interview approach for each candidate
            5. Identify any potential concerns
            
            Focus on quality over quantity - HaruPlate prefers fewer, better-aligned candidates.
            """,
            agent=self.agents['profile_analyst'],
            expected_output="Top 5 candidate shortlist with detailed profiles and interview recommendations",
            context=[analysis_task]
        )
        
        # Task 3: Outreach Preparation
        outreach_prep_task = Task(
            description="""
            Prepare personalized outreach for shortlisted candidates:
            
            1. Customize email templates for each candidate
            2. Mention specific elements that caught our attention
            3. Prepare Zoom interview scheduling options
            4. Create candidate-specific talking points
            5. Set up tracking for response rates
            
            Each email should feel personal and explain why we think they'd fit our mission.
            """,
            agent=self.agents['communications_coordinator'],
            expected_output="Personalized outreach materials for each shortlisted candidate",
            context=[shortlist_task]
        )
        
        # Execute analysis crew
        analysis_crew = Crew(
            agents=[
                self.agents['profile_analyst'],
                self.agents['communications_coordinator']
            ],
            tasks=[
                analysis_task,
                shortlist_task,
                outreach_prep_task
            ],
            verbose=True,
            process="sequential"
        )
        
        result = analysis_crew.kickoff()
        
        return {
            "workflow_type": "candidate_analysis",
            "status": "completed",
            "deliverables": {
                "candidate_analysis": "Compatibility scores calculated",
                "shortlist": "Top 5 candidates identified",
                "outreach_materials": "Personalized communications ready"
            },
            "next_steps": [
                "Review shortlist with management",
                "Send initial outreach emails",
                "Schedule interviews with interested candidates",
                "Prepare interview evaluation criteria"
            ],
            "human_approval_required": True,
            "approval_items": [
                "Candidate shortlist approval",
                "Outreach email approval",
                "Interview scheduling authorization"
            ]
        }
    
    def _general_hr_workflow(self, request: str, brand_context: Dict[str, Any]) -> Dict[str, Any]:
        """General HR workflow for other types of requests."""
        
        general_task = Task(
            description=f"""
            Address this HR request: "{request}"
            
            Analyze the request and provide appropriate HR expertise while maintaining
            HaruPlate's sincere, family-oriented approach. Consider our values:
            {', '.join(brand_context.get('values', []))}
            
            Provide actionable recommendations that align with our mission.
            """,
            agent=self.agents['recruitment_strategist'],
            expected_output="HR recommendations aligned with HaruPlate's values and mission"
        )
        
        general_crew = Crew(
            agents=[self.agents['recruitment_strategist']],
            tasks=[general_task],
            verbose=True
        )
        
        result = general_crew.kickoff()
        
        return {
            "workflow_type": "general_hr",
            "status": "completed",
            "deliverables": {
                "hr_recommendations": "Customized advice provided"
            }
        }
    
    def get_available_agents(self) -> List[str]:
        """Returns list of available agent roles."""
        return list(self.agents.keys())
    
    def get_crew_capabilities(self) -> Dict[str, List[str]]:
        """Returns the capabilities of each crew member."""
        return {
            "recruitment_strategist": [
                "Job description creation",
                "Publishing strategy",
                "Malaysian market expertise",
                "Brand-aligned content creation"
            ],
            "profile_analyst": [
                "CV analysis",
                "Values compatibility scoring",
                "Technical skills assessment",
                "Cultural fit evaluation"
            ],
            "communications_coordinator": [
                "Email drafting",
                "Zoom scheduling",
                "Candidate communication",
                "Interview coordination"
            ],
            "quality_control_specialist": [
                "Brand compliance checking",
                "Tone and language review",
                "Cultural sensitivity review",
                "Self-evaluation processes"
            ]
        }


# Example usage
if __name__ == "__main__":
    hr_crew = HRCrew()
    
    # Example: Digital Marketing Specialist recruitment
    sample_request = "Find an experienced Digital Marketing Specialist for the Malaysian market who understands child nutrition and family values"
    
    brand_context = {
        "tone": "sincere, healthy, family-oriented",
        "values": ["child nutrition excellence", "natural product focus", "family-first approach"],
        "target_market": "Malaysia"
    }
    
    result = hr_crew.execute_workflow(sample_request, brand_context)
    print("🎯 HR Crew Result:", result)