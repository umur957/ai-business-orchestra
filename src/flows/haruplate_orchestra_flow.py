#!/usr/bin/env python3
"""
HaruPlate Orchestra Flow
Based on crewAI-examples/flows/meeting_assistant_flow pattern
The main orchestrator using CrewAI Flows for managing HR and Admin crews.
"""

from crewai.flow.flow import Flow, listen, start
from crewai import Agent, Task, Crew
from pydantic import BaseModel
from typing import Dict, Any, List, Optional, Union
import logging
import json
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# State Management Classes (Based on meeting_assistant_flow pattern)
class HaruPlateRequestState(BaseModel):
    """Main state for HaruPlate Orchestra Flow - similar to MeetingState pattern."""
    request_id: str
    original_request: str
    request_type: str = ""  # "hr" or "admin" 
    priority: str = "normal"
    timestamp: datetime = datetime.now()
    user: str = "haruplate_manager"
    
    # Analysis results
    analysis_complete: bool = False
    routing_decision: Dict[str, Any] = {}
    
    # Crew results  
    hr_result: Optional[Dict[str, Any]] = None
    admin_result: Optional[Dict[str, Any]] = None
    
    # Human approval workflow
    approval_required: bool = False
    approval_message: str = ""
    approval_response: Optional[str] = None
    
    # Final results
    final_result: Optional[Dict[str, Any]] = None
    completed: bool = False

class HaruPlateOrchestraFlow(Flow[HaruPlateRequestState]):
    """
    HaruPlate Orchestra Conductor Flow
    Orchestrates HR and Admin crews using CrewAI Flows pattern
    """

    def __init__(self, request_text: str, user: str = "haruplate_manager"):
        """Initialize flow with request."""
        initial_state = HaruPlateRequestState(
            request_id=str(uuid.uuid4()),
            original_request=request_text,
            user=user,
            timestamp=datetime.now()
        )
        super().__init__(initial_state)

    @start()
    def analyze_request(self) -> HaruPlateRequestState:
        """
        Step 1: Analyze the incoming request to determine routing
        Pattern from meeting_assistant_flow.load_meeting_notes()
        """
        logger.info(f"🎼 HaruPlate Orchestra: Analyzing request {self.state.request_id[:8]}...")
        
        request_text = self.state.original_request.lower()
        
        # HaruPlate-specific keyword analysis
        hr_keywords = [
            "hire", "recruit", "teammate", "digital marketing specialist", "position", 
            "job description", "cv", "candidate", "interview", "malaysian market",
            "values alignment", "child nutrition", "sincere", "family-oriented"
        ]
        
        admin_keywords = [
            "invoice", "supplier", "malaysian supplier", "expense", "document", 
            "meeting", "calendar", "google sheets", "drive", "archive", "data analysis",
            "singapore", "sales data", "financial", "pdf"
        ]
        
        hr_score = sum(2 if keyword in request_text else 0 for keyword in hr_keywords)
        admin_score = sum(2 if keyword in request_text else 0 for keyword in admin_keywords)
        
        # Routing decision with HaruPlate context
        if hr_score > admin_score:
            self.state.request_type = "hr"
            routing_reason = f"HR-focused request detected (score: {hr_score})"
        elif admin_score > hr_score:
            self.state.request_type = "admin" 
            routing_reason = f"Admin-focused request detected (score: {admin_score})"
        else:
            # Default to HR for HaruPlate people-first philosophy
            self.state.request_type = "hr"
            routing_reason = "Ambiguous request - defaulting to HR (people-first philosophy)"
        
        self.state.routing_decision = {
            "route_to": self.state.request_type,
            "hr_score": hr_score,
            "admin_score": admin_score,
            "reasoning": routing_reason,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        self.state.analysis_complete = True
        
        logger.info(f"📋 Request routed to: {self.state.request_type.upper()} Expert Crew")
        logger.info(f"📊 Routing reason: {routing_reason}")
        
        return self.state

    @listen(analyze_request)  
    def process_hr_request(self) -> Optional[HaruPlateRequestState]:
        """
        Step 2a: Process HR requests using HR Expert Crew
        Pattern from meeting_assistant_flow.generate_tasks_from_meeting_transcript()
        """
        if self.state.request_type != "hr":
            return None
            
        logger.info(f"👥 Processing HR request with HaruPlate HR Expert Crew...")
        
        try:
            # Import and create HR crew (following repository pattern)
            from ..crews.hr_crew import HaruPlateHRCrew
            
            hr_crew = HaruPlateHRCrew()
            
            # Process request with HaruPlate context
            crew_context = {
                "company_values": "sincere, family-oriented, child nutrition focused",
                "market_focus": "Malaysian market cultural sensitivity required",
                "terminology": "Use 'teammates' not 'candidates'", 
                "brand_tone": "Warm, family-oriented, health-focused",
                "request_id": self.state.request_id
            }
            
            hr_result = hr_crew.kickoff({
                "request": self.state.original_request,
                "context": crew_context
            })
            
            self.state.hr_result = {
                "crew_output": hr_result,
                "processing_timestamp": datetime.now().isoformat(),
                "crew_type": "hr_expert",
                "haruplate_compliance": True,
                "approval_required": True,  # HR decisions always need approval
                "approval_message": self._generate_hr_approval_message(hr_result)
            }
            
            self.state.approval_required = True
            self.state.approval_message = self.state.hr_result["approval_message"]
            
            logger.info(f"✅ HR Expert Crew processing completed")
            
        except Exception as e:
            logger.error(f"❌ Error in HR processing: {str(e)}")
            self.state.hr_result = {
                "error": str(e),
                "status": "failed",
                "crew_type": "hr_expert",
                "processing_timestamp": datetime.now().isoformat()
            }
        
        return self.state

    @listen(analyze_request)
    def process_admin_request(self) -> Optional[HaruPlateRequestState]:
        """
        Step 2b: Process Admin requests using Admin Expert Crew  
        Pattern from meeting_assistant_flow workflow steps
        """
        if self.state.request_type != "admin":
            return None
            
        logger.info(f"🏢 Processing Admin request with HaruPlate Admin Expert Crew...")
        
        try:
            # Import and create Admin crew
            from ..crews.admin_crew import HaruPlateAdminCrew
            
            admin_crew = HaruPlateAdminCrew()
            
            # Process request with HaruPlate context
            crew_context = {
                "company_focus": "Child nutrition, natural products",
                "supplier_focus": "Malaysian suppliers priority", 
                "expense_categories": "HaruPlate-specific categorization",
                "file_organization": "Brand-compliant naming conventions",
                "request_id": self.state.request_id
            }
            
            admin_result = admin_crew.kickoff({
                "request": self.state.original_request,
                "context": crew_context
            })
            
            # Admin tasks usually don't need approval unless high-value
            needs_approval = self._admin_needs_approval(admin_result)
            
            self.state.admin_result = {
                "crew_output": admin_result,
                "processing_timestamp": datetime.now().isoformat(),
                "crew_type": "admin_expert",
                "approval_required": needs_approval,
                "approval_message": self._generate_admin_approval_message(admin_result) if needs_approval else ""
            }
            
            if needs_approval:
                self.state.approval_required = True
                self.state.approval_message = self.state.admin_result["approval_message"]
            
            logger.info(f"✅ Admin Expert Crew processing completed")
            
        except Exception as e:
            logger.error(f"❌ Error in Admin processing: {str(e)}")
            self.state.admin_result = {
                "error": str(e), 
                "status": "failed",
                "crew_type": "admin_expert",
                "processing_timestamp": datetime.now().isoformat()
            }
        
        return self.state

    @listen(process_hr_request)
    @listen(process_admin_request)  
    def finalize_results(self) -> HaruPlateRequestState:
        """
        Step 3: Finalize and format results for delivery
        Pattern from meeting_assistant_flow.save_new_tasks_to_csv()
        """
        logger.info(f"🎯 Finalizing HaruPlate Orchestra results...")
        
        # Determine which result to use
        active_result = self.state.hr_result if self.state.request_type == "hr" else self.state.admin_result
        
        if not active_result or active_result.get("status") == "failed":
            self.state.final_result = {
                "status": "error",
                "message": "Workflow processing failed",
                "error_details": active_result.get("error", "Unknown error") if active_result else "No result generated",
                "request_id": self.state.request_id
            }
        else:
            # Format successful results with HaruPlate branding
            self.state.final_result = {
                "status": "success",
                "request_id": self.state.request_id,
                "request_type": self.state.request_type,
                "crew_output": active_result["crew_output"],
                "processing_summary": {
                    "routing_decision": self.state.routing_decision,
                    "crew_type": active_result["crew_type"],
                    "processing_timestamp": active_result["processing_timestamp"],
                    "approval_required": active_result.get("approval_required", False)
                },
                "haruplate_context": {
                    "company_values": "Sincere, family-oriented approach to child nutrition",
                    "market_focus": "Malaysian market with cultural sensitivity",
                    "brand_compliance": "HaruPlate terminology and tone maintained",
                    "next_steps": self._generate_next_steps(active_result)
                }
            }
        
        self.state.completed = True
        
        logger.info(f"🎉 HaruPlate Orchestra workflow completed for request {self.state.request_id[:8]}")
        return self.state

    # Helper methods for approval and next steps
    def _generate_hr_approval_message(self, hr_result: Dict[str, Any]) -> str:
        """Generate human approval message for HR results."""
        return (
            f"🎼 HaruPlate HR Expert Crew has completed processing.\n\n"
            f"The team has analyzed your request and prepared recommendations "
            f"following HaruPlate's family-oriented values and Malaysian market focus.\n\n"
            f"Please review the results and provide approval to proceed with next steps."
        )
    
    def _generate_admin_approval_message(self, admin_result: Dict[str, Any]) -> str:
        """Generate human approval message for Admin results.""" 
        return (
            f"🎼 HaruPlate Admin Expert Crew has completed processing.\n\n"
            f"The team has processed your administrative request with attention "
            f"to HaruPlate's operational standards and supplier preferences.\n\n"
            f"Please review and approve to proceed."
        )
    
    def _admin_needs_approval(self, admin_result: Dict[str, Any]) -> bool:
        """Determine if admin result needs human approval."""
        # Check for high-value operations that need approval
        result_text = str(admin_result).lower()
        high_value_keywords = ["payment", "contract", "large expense", "supplier change", "financial"]
        return any(keyword in result_text for keyword in high_value_keywords)
    
    def _generate_next_steps(self, result: Dict[str, Any]) -> List[str]:
        """Generate next steps based on result type."""
        if self.state.request_type == "hr":
            return [
                "Review candidate recommendations",
                "Schedule interviews with top teammates", 
                "Prepare HaruPlate-specific interview questions",
                "Coordinate with Communications Coordinator for outreach"
            ]
        else:
            return [
                "Review processed documents and data",
                "Verify Malaysian supplier information",
                "Check Google Sheets updates",
                "Archive documents to appropriate folders"
            ]


def run_haruplate_orchestra(request: str, user: str = "haruplate_manager") -> Dict[str, Any]:
    """
    Main entry point to run HaruPlate Orchestra
    Similar to main() function in meeting_assistant_flow
    """
    logger.info(f"🚀 Starting HaruPlate Orchestra for request: {request[:50]}...")
    
    # Create and run the flow
    orchestra_flow = HaruPlateOrchestraFlow(request, user)
    
    # Execute the workflow
    result = orchestra_flow.kickoff()
    
    # Return the final result
    final_result = orchestra_flow.state.final_result
    
    if final_result:
        logger.info(f"🎉 Orchestra completed successfully!")
        return final_result
    else:
        logger.error(f"❌ Orchestra failed to complete")
        return {
            "status": "error", 
            "message": "Flow did not complete properly",
            "request_id": orchestra_flow.state.request_id
        }


if __name__ == "__main__":
    # Test the flow
    test_request = "We need to find an experienced Digital Marketing Specialist for the Malaysian market."
    result = run_haruplate_orchestra(test_request)
    print(f"Result: {json.dumps(result, indent=2)}")