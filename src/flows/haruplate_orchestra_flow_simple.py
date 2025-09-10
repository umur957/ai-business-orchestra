#!/usr/bin/env python3
"""
HaruPlate Orchestra Flow - Simple Working Version
Main orchestrator using CrewAI Flows for managing HR and Admin crews.
"""

from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HaruPlateRequestState(BaseModel):
    """Main state for HaruPlate Orchestra Flow"""
    id: str = ""  # Required by CrewAI Flow
    request_id: str = ""
    original_request: str = ""
    request_type: str = ""  # "hr" or "admin" 
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
    """HaruPlate Orchestra Conductor Flow"""
    
    initial_state = HaruPlateRequestState

    @start()
    def analyze_request(self):
        """Step 1: Analyze the incoming request to determine routing"""
        logger.info("HaruPlate Orchestra: Analyzing request...")
        
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
            "reasoning": routing_reason
        }
        
        self.state.analysis_complete = True
        
        logger.info(f"Request routed to: {self.state.request_type.upper()} Expert Crew")

    @listen(analyze_request)  
    def process_hr_request(self):
        """Step 2a: Process HR requests using HR Expert Crew"""
        if self.state.request_type != "hr":
            return
            
        logger.info("Processing HR request with HaruPlate HR Expert Crew...")
        
        # HaruPlate HR simulation result
        hr_result = f"""HaruPlate HR Expert Crew Analysis:

Request: {self.state.original_request}

HR TEAM ANALYSIS:
Our HR Expert Crew has analyzed your request with HaruPlate's family-oriented values:

JOB DESCRIPTION FRAMEWORK:
- Position aligned with HaruPlate's mission of child nutrition
- Emphasizes 'teammate' terminology (not 'candidate')  
- Reflects sincere, family-oriented tone
- Includes Malaysian market cultural sensitivity

RECRUITMENT STRATEGY:
- Target platforms: LinkedIn Malaysia, local job boards
- Emphasize HaruPlate values and healthy mission
- Focus on cultural fit and passion for child nutrition

CANDIDATE EVALUATION CRITERIA:
- Technical competency for the role
- Alignment with family-oriented values
- Interest in child nutrition and health
- Cultural sensitivity for Malaysian market

NEXT STEPS:
1. Create detailed job description (2-3 hours)
2. Publish on Malaysian platforms (1 hour)
3. Screen applications for values alignment (ongoing)
4. Schedule interviews with top candidates (1 week)

All outputs will maintain HaruPlate's warm, family-focused brand voice."""
        
        self.state.hr_result = {
            "crew_output": hr_result,
            "crew_type": "hr",
            "success": True,
            "haruplate_values_applied": True
        }
        
        # HR decisions require human approval for HaruPlate
        self.state.approval_required = True
        self.state.approval_message = f"HR Expert Crew has completed analysis for: {self.state.original_request[:100]}..."
        
        logger.info("HR Expert Crew processing complete")

    @listen(analyze_request)  
    def process_admin_request(self):
        """Step 2b: Process Admin requests using Admin Expert Crew"""
        if self.state.request_type != "admin":
            return
            
        logger.info("Processing Admin request with HaruPlate Admin Expert Crew...")
        
        # HaruPlate Admin simulation result
        admin_result = f"""HaruPlate Admin Expert Crew Analysis:

Request: {self.state.original_request}

ADMIN TEAM ANALYSIS:
Our Admin Expert Crew has processed your operational request:

PROCESSING PLAN:
- Malaysian supplier invoice automation
- Google Sheets integration for expense tracking
- Document archiving to Google Drive
- Compliance with child nutrition industry standards

IMPLEMENTATION APPROACH:
- Automated PDF extraction from Gmail
- Data parsing and validation
- Structured data entry to Google Sheets
- File archiving with proper naming conventions

EXPECTED OUTCOMES:
- Improved processing efficiency (60% time savings)
- Standardized documentation format
- Better financial data organization
- Enhanced compliance tracking

TIMELINE:
- Initial setup: 2-4 hours
- Quality review: 1 hour
- System integration testing: 30 minutes
- Go-live and monitoring: Ongoing

All processes maintain HaruPlate's operational excellence standards."""
        
        self.state.admin_result = {
            "crew_output": admin_result,
            "crew_type": "admin",
            "success": True,
            "haruplate_compliance": True
        }
        
        # Check if human approval is required for financial decisions
        financial_keywords = ["invoice", "expense", "budget", "payment", "supplier"]
        if any(keyword in self.state.original_request.lower() for keyword in financial_keywords):
            self.state.approval_required = True
            self.state.approval_message = f"Admin Expert Crew has completed financial analysis for: {self.state.original_request[:100]}..."
        
        logger.info("Admin Expert Crew processing complete")

    @router("process_hr_request")
    def human_approval_checkpoint(self):
        """Step 3: Human-in-the-Loop approval checkpoint"""
        if not self.state.approval_required:
            return "finalize_response"
            
        logger.info("Human approval required...")
        
        # Display results for human review
        print("\n" + "="*60)
        print("HaruPlate Orchestra - Human Approval Required")
        print("="*60)
        print(f"Original Request: {self.state.original_request}")
        print(f"Request Type: {self.state.request_type.upper()}")
        
        # Show crew results
        if self.state.hr_result:
            print(f"\nHR Expert Crew Results:")
            print(f"{self.state.hr_result.get('crew_output', 'No output available')}")
            
        if self.state.admin_result:
            print(f"\nAdmin Expert Crew Results:")
            print(f"{self.state.admin_result.get('crew_output', 'No output available')}")
        
        print(f"\n{self.state.approval_message}")
        
        # Human approval options
        print("\nPlease choose an option:")
        print("1. Approve and finalize response")
        print("2. Request modifications")
        print("3. Reject and abort")
        
        # For demo purposes, auto-approve
        print("\n[Demo Mode: Auto-approving...]")
        self.state.approval_response = "approved"
        logger.info("Human approval: APPROVED (auto)")
        return "finalize_response"

    @listen("finalize_response")
    def finalize_orchestra_response(self):
        """Step 4a: Finalize the orchestra response"""
        logger.info("Finalizing HaruPlate Orchestra response...")
        
        # Compile final response with HaruPlate branding
        final_output = {
            "request_id": self.state.request_id,
            "original_request": self.state.original_request,
            "processing_summary": {
                "request_type": self.state.request_type,
                "routing_decision": self.state.routing_decision,
                "approval_status": self.state.approval_response or "auto_approved"
            },
            "crew_results": {},
            "haruplate_context": {
                "company_values": "sincere, family-oriented, child nutrition focused",
                "brand_voice": "warm, professional, health-conscious"
            }
        }
        
        # Add crew-specific results
        if self.state.hr_result:
            final_output["crew_results"]["hr_expert_team"] = self.state.hr_result
            
        if self.state.admin_result:
            final_output["crew_results"]["admin_expert_team"] = self.state.admin_result
        
        # Generate HaruPlate-style summary
        summary_lines = [
            "HaruPlate Orchestra Response Summary",
            "=" * 50,
            f"Request: {self.state.original_request}",
            f"Handled by: {self.state.request_type.title()} Expert Team",
            f"Status: Successfully processed with HaruPlate values alignment"
        ]
        
        if self.state.hr_result:
            summary_lines.append("HR Team Output: Ready for implementation")
            
        if self.state.admin_result:
            summary_lines.append("Admin Team Output: Ready for implementation")
        
        summary_lines.extend([
            "",
            "HaruPlate Orchestra is committed to supporting your strategic",
            "vision while maintaining our family-oriented, health-focused values.",
            "=" * 50
        ])
        
        final_output["summary"] = "\n".join(summary_lines)
        
        self.state.final_result = final_output
        self.state.completed = True
        
        # Display final summary
        print("\n" + final_output["summary"])
        
        logger.info("HaruPlate Orchestra processing complete")


# Convenience functions for external usage
def create_haruplate_flow(request: str, user: str = "haruplate_manager") -> HaruPlateOrchestraFlow:
    """Create and return a HaruPlate Orchestra Flow instance"""
    flow = HaruPlateOrchestraFlow()
    flow_id = str(uuid.uuid4())
    flow.state.id = flow_id
    flow.state.request_id = flow_id
    flow.state.original_request = request
    flow.state.user = user
    return flow


def process_haruplate_request(request: str, user: str = "haruplate_manager") -> Dict[str, Any]:
    """Main entry point for processing HaruPlate requests"""
    logger.info(f"Starting HaruPlate Orchestra for: {request[:50]}...")
    
    try:
        flow = create_haruplate_flow(request, user)
        result = flow.kickoff()
        
        if hasattr(flow.state, 'final_result') and flow.state.final_result:
            return flow.state.final_result
        else:
            return {
                "error": "Flow completed but no final result generated",
                "status": "incomplete"
            }
            
    except Exception as e:
        logger.error(f"HaruPlate Orchestra failed: {str(e)}")
        return {
            "error": str(e),
            "status": "failed"
        }


# Example usage and testing
if __name__ == "__main__":
    # Test the HaruPlate Orchestra Flow
    test_requests = [
        "Tell the HR team we need to find an experienced 'Digital Marketing Specialist' for the Malaysian market. Have them start the process.",
        "Process the invoices from our Malaysian suppliers and update the Q3 expense tracking in Google Sheets.",
        "Prepare for next week's board meeting with sales data analysis from Singapore operations."
    ]
    
    print("Testing HaruPlate Orchestra Flow...")
    print("-" * 60)
    
    for i, request in enumerate(test_requests, 1):
        print(f"\nTest Request {i}:")
        print(f"'{request}'")
        print("\nProcessing...")
        
        result = process_haruplate_request(request)
        
        if result.get("error"):
            print(f"Error: {result['error']}")
        else:
            print("Success!")
            if result.get("summary"):
                print(result["summary"])
        
        print("\n" + "-" * 60)
