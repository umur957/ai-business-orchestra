"""
HaruPlate HR & Admin Intelligence Orchestra - Main Conductor
The Orchestra Conductor manages all expert crews and workflows with human-in-the-loop approval.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from crewai import Flow, Agent, Task, Crew
from crewai.flow.flow import listen, start
import logging
from pathlib import Path

from ..crews.hr_crew import HRCrew
from ..crews.admin_crew import AdminCrew
from ..tools.haruplate_tools import HaruPlateTools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class HaruPlateRequest:
    """Represents a request from HaruPlate management."""
    request_id: str
    request_text: str
    request_type: str  # 'hr', 'admin', 'mixed'
    requester: str
    priority: str = "normal"  # low, normal, high, urgent
    context: Dict[str, Any] = None


@dataclass
class WorkflowResult:
    """Represents the result of a workflow execution."""
    request_id: str
    status: str  # 'completed', 'pending_approval', 'failed'
    results: Dict[str, Any]
    human_approval_required: bool = False
    approval_message: str = ""
    next_steps: List[str] = None


class OrchestraConductor(Flow):
    """
    The main orchestrator for HaruPlate's HR & Admin Intelligence system.
    
    This class manages the flow between different expert crews and handles
    human-in-the-loop approval processes following HaruPlate's philosophy:
    "Managers focus on strategy, not repetitive tasks."
    """
    
    def __init__(self):
        super().__init__()
        self.hr_crew = HRCrew()
        self.admin_crew = AdminCrew()
        self.haruplate_tools = HaruPlateTools()
        
        # HaruPlate brand identity context
        self.brand_context = {
            "tone": "sincere, healthy, family-oriented",
            "values": [
                "child nutrition excellence",
                "natural product focus",
                "family-first approach",
                "sincere communication",
                "healthy living promotion"
            ],
            "target_markets": ["Malaysia", "Southeast Asia"],
            "company_mission": "Providing the best nutrition for children through natural, healthy products"
        }
        
    @start("new_request")
    def analyze_request(self, request: HaruPlateRequest) -> str:
        """
        Analyzes incoming requests and determines the appropriate workflow path.
        
        This is the entry point where HaruPlate managers submit their requests
        in natural language.
        """
        logger.info(f"🎼 Orchestra Conductor received request: {request.request_id}")
        logger.info(f"Request: {request.request_text}")
        
        # Use AI to analyze and categorize the request
        analysis_agent = Agent(
            role="HaruPlate Request Analyzer",
            goal=f"""Analyze management requests and determine the best approach.
                     Always consider HaruPlate's {self.brand_context['tone']} brand identity.""",
            backstory="""You are an expert at understanding HaruPlate's business needs.
                        You know that HaruPlate focuses on child nutrition and natural products,
                        and you understand the company's sincere, family-oriented culture.""",
            verbose=True
        )
        
        analysis_task = Task(
            description=f"""
            Analyze this request from HaruPlate management: "{request.request_text}"
            
            Determine:
            1. Request type (hr, admin, or mixed)
            2. Priority level (low, normal, high, urgent)
            3. Required expert teams
            4. Expected deliverables
            5. Whether human approval will be needed
            
            Consider HaruPlate's focus on: {', '.join(self.brand_context['values'])}
            Target market: {', '.join(self.brand_context['target_markets'])}
            """,
            agent=analysis_agent,
            expected_output="Structured analysis with request categorization and workflow recommendations"
        )
        
        analysis_crew = Crew(
            agents=[analysis_agent],
            tasks=[analysis_task],
            verbose=True
        )
        
        result = analysis_crew.kickoff()
        logger.info(f"📋 Analysis complete: {result}")
        
        # Route to appropriate workflow
        if "hr" in result.lower():
            return "hr_workflow"
        elif "admin" in result.lower():
            return "admin_workflow"
        else:
            return "mixed_workflow"
    
    @listen("hr_workflow")
    def handle_hr_request(self, request: HaruPlateRequest) -> WorkflowResult:
        """
        Handles HR-related requests through the specialized HR crew.
        
        Example: "Find an experienced Digital Marketing Specialist for Malaysian market"
        """
        logger.info(f"👥 Processing HR request: {request.request_id}")
        
        # Execute HR crew workflow
        hr_result = self.hr_crew.execute_workflow(
            request=request.request_text,
            brand_context=self.brand_context
        )
        
        # Determine if human approval is needed
        approval_required = self._requires_approval(hr_result, "hr")
        
        if approval_required:
            approval_message = self._create_approval_message(hr_result, "hr")
            return WorkflowResult(
                request_id=request.request_id,
                status="pending_approval",
                results=hr_result,
                human_approval_required=True,
                approval_message=approval_message,
                next_steps=["await_human_approval", "continue_hr_workflow"]
            )
        
        return WorkflowResult(
            request_id=request.request_id,
            status="completed",
            results=hr_result,
            human_approval_required=False
        )
    
    @listen("admin_workflow")
    def handle_admin_request(self, request: HaruPlateRequest) -> WorkflowResult:
        """
        Handles administrative requests through the specialized Admin crew.
        
        Example: "Process this month's invoices and update financial records"
        """
        logger.info(f"📊 Processing Admin request: {request.request_id}")
        
        # Execute Admin crew workflow
        admin_result = self.admin_crew.execute_workflow(
            request=request.request_text,
            brand_context=self.brand_context
        )
        
        # Determine if human approval is needed
        approval_required = self._requires_approval(admin_result, "admin")
        
        if approval_required:
            approval_message = self._create_approval_message(admin_result, "admin")
            return WorkflowResult(
                request_id=request.request_id,
                status="pending_approval",
                results=admin_result,
                human_approval_required=True,
                approval_message=approval_message,
                next_steps=["await_human_approval", "continue_admin_workflow"]
            )
        
        return WorkflowResult(
            request_id=request.request_id,
            status="completed",
            results=admin_result,
            human_approval_required=False
        )
    
    @listen("mixed_workflow")
    def handle_mixed_request(self, request: HaruPlateRequest) -> WorkflowResult:
        """
        Handles complex requests requiring both HR and Admin crews.
        
        Example: "Prepare for next quarter: hire 2 marketing specialists and 
                 analyze this quarter's sales data"
        """
        logger.info(f"🎭 Processing Mixed request: {request.request_id}")
        
        # Execute both crews in coordination
        hr_result = self.hr_crew.execute_workflow(
            request=request.request_text,
            brand_context=self.brand_context
        )
        
        admin_result = self.admin_crew.execute_workflow(
            request=request.request_text,
            brand_context=self.brand_context
        )
        
        # Combine results
        combined_results = {
            "hr_results": hr_result,
            "admin_results": admin_result,
            "coordination_summary": self._create_coordination_summary(hr_result, admin_result)
        }
        
        return WorkflowResult(
            request_id=request.request_id,
            status="completed",
            results=combined_results,
            human_approval_required=True,
            approval_message=self._create_approval_message(combined_results, "mixed"),
            next_steps=["review_combined_results", "approve_next_actions"]
        )
    
    def _requires_approval(self, results: Dict[str, Any], workflow_type: str) -> bool:
        """
        Determines if human approval is required based on the results and workflow type.
        
        HaruPlate philosophy: Important decisions always require human insight.
        """
        # Always require approval for:
        # - Job postings before publishing
        # - Candidate shortlists before contacting
        # - Financial transactions above threshold
        # - External communications
        
        approval_triggers = {
            "hr": ["job_posting", "candidate_shortlist", "interview_scheduling"],
            "admin": ["financial_transaction", "document_archival", "meeting_preparation"],
            "mixed": True  # Always require approval for complex workflows
        }
        
        if workflow_type == "mixed":
            return True
        
        for trigger in approval_triggers.get(workflow_type, []):
            if trigger in str(results).lower():
                return True
        
        return False
    
    def _create_approval_message(self, results: Dict[str, Any], workflow_type: str) -> str:
        """
        Creates a human-readable approval message for HaruPlate managers.
        
        The message is crafted in HaruPlate's sincere, family-oriented tone.
        """
        if workflow_type == "hr":
            return f"""
            🌱 HaruPlate HR Team Update
            
            Dear Team,
            
            Our HR specialists have prepared the following for your review:
            
            {self._format_results_for_approval(results)}
            
            Please review and approve so we can proceed with connecting with potential 
            teammates who share our passion for child nutrition and healthy living.
            
            With sincere regards,
            HaruPlate HR & Admin Intelligence Orchestra
            """
        elif workflow_type == "admin":
            return f"""
            📈 HaruPlate Administrative Update
            
            Dear Team,
            
            Our administrative specialists have completed the following tasks:
            
            {self._format_results_for_approval(results)}
            
            Please review to ensure everything aligns with our family-first business values.
            
            With sincere regards,
            HaruPlate HR & Admin Intelligence Orchestra
            """
        else:
            return f"""
            🎼 HaruPlate Comprehensive Update
            
            Dear Team,
            
            Our entire orchestra has worked together on your request:
            
            {self._format_results_for_approval(results)}
            
            This coordinated effort reflects our commitment to excellence in everything we do.
            Please review and guide us on the next steps.
            
            With sincere regards,
            HaruPlate HR & Admin Intelligence Orchestra
            """
    
    def _format_results_for_approval(self, results: Dict[str, Any]) -> str:
        """Formats results in a human-readable format for approval."""
        formatted = []
        
        for key, value in results.items():
            if isinstance(value, dict):
                formatted.append(f"• {key.replace('_', ' ').title()}:")
                for sub_key, sub_value in value.items():
                    formatted.append(f"  - {sub_key.replace('_', ' ').title()}: {sub_value}")
            else:
                formatted.append(f"• {key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(formatted)
    
    def _create_coordination_summary(self, hr_results: Dict, admin_results: Dict) -> str:
        """Creates a summary of how HR and Admin results coordinate together."""
        return f"""
        🤝 Coordination Summary:
        
        Our HR and Administrative teams have worked in harmony to address your request:
        
        HR Team delivered: {len(hr_results)} key deliverables
        Admin Team delivered: {len(admin_results)} key deliverables
        
        All outputs maintain HaruPlate's {self.brand_context['tone']} approach and 
        support our mission: {self.brand_context['company_mission']}
        """
    
    def get_workflow_status(self, request_id: str) -> Dict[str, Any]:
        """Returns the current status of a workflow."""
        # Implementation would track workflow states
        pass
    
    def handle_human_approval(self, request_id: str, approved: bool, feedback: str = "") -> WorkflowResult:
        """
        Handles human approval responses and continues workflows accordingly.
        """
        logger.info(f"👤 Human approval for {request_id}: {'✅ Approved' if approved else '❌ Rejected'}")
        
        if approved:
            # Continue the workflow
            return self._continue_approved_workflow(request_id)
        else:
            # Handle rejection with feedback
            return self._handle_workflow_rejection(request_id, feedback)
    
    def _continue_approved_workflow(self, request_id: str) -> WorkflowResult:
        """Continues workflow after human approval."""
        # Implementation would continue the specific workflow
        pass
    
    def _handle_workflow_rejection(self, request_id: str, feedback: str) -> WorkflowResult:
        """Handles workflow rejection and incorporates feedback."""
        # Implementation would restart workflow with feedback
        pass


# Usage Example for HaruPlate
if __name__ == "__main__":
    # Example: Digital Marketing Specialist hiring request
    conductor = OrchestraConductor()
    
    sample_request = HaruPlateRequest(
        request_id="HR-001-2025",
        request_text="Tell the HR team we need to find an experienced 'Digital Marketing Specialist' for the Malaysian market. Have them start the process.",
        request_type="hr",
        requester="Founder",
        priority="high",
        context={"department": "marketing", "location": "Malaysia", "urgency": "Q1 hiring"}
    )
    
    # This would start the orchestral workflow
    result = conductor.kickoff({"new_request": sample_request})
    print(f"🎼 Orchestra Result: {result}")