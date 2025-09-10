#!/usr/bin/env python3
"""
HaruPlate Orchestra Flow
Based on crewAI-examples/flows/meeting_assistant_flow and lead-score-flow patterns
The main orchestrator using CrewAI Flows for managing HR and Admin crews.
"""

from crewai.flow.flow import Flow, listen, start, router
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
    id: str  # Required by CrewAI Flow
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
    
    initial_state = HaruPlateRequestState

    @start()
    def analyze_request(self):
        """
        Step 1: Analyze the incoming request to determine routing
        Pattern from meeting_assistant_flow.load_meeting_notes()
        """
        logger.info(f"🎼 HaruPlate Orchestra: Analyzing request...")
        
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

    @listen(analyze_request)  
    def process_hr_request(self):
        """
        Step 2a: Process HR requests using HR Expert Crew
        Pattern from meeting_assistant_flow.generate_tasks_from_meeting_transcript()
        """
        if self.state.request_type != "hr":
            return
            
        logger.info(f"👥 Processing HR request with HaruPlate HR Expert Crew...")
        
        try:
            # Simulate HR crew processing (will be replaced with actual crew)
            hr_simulation_result = f"""
🎼 HaruPlate HR Expert Crew Analysis:

📝 Request: {self.state.original_request}

👥 HR TEAM ANALYSIS:
Our HR Expert Crew has analyzed your request with HaruPlate's family-oriented values:

📋 JOB DESCRIPTION FRAMEWORK:
- Position aligned with HaruPlate's mission of child nutrition
- Emphasizes "teammate" terminology (not "candidate")
- Reflects sincere, family-oriented tone
- Includes Malaysian market cultural sensitivity

🎯 RECRUITMENT STRATEGY:
- Target platforms: LinkedIn Malaysia, local job boards
- Emphasize HaruPlate values and healthy mission
- Focus on cultural fit and passion for child nutrition

🔍 CANDIDATE EVALUATION CRITERIA:
- Technical competency for the role
- Alignment with family-oriented values
- Interest in child nutrition and health
- Cultural sensitivity for Malaysian market
- Communication skills in multicultural environment

📅 NEXT STEPS:
1. Create detailed job description (2-3 hours)
2. Publish on Malaysian platforms (1 hour) 
3. Screen applications for values alignment (ongoing)
4. Schedule interviews with top candidates (1 week)

✨ All outputs will maintain HaruPlate's warm, family-focused brand voice.
"""
            
            self.state.hr_result = {
                "crew_output": hr_simulation_result,
                "processing_timestamp": datetime.now().isoformat(),
                "crew_type": "hr",
                "success": True,
                "haruplate_values_applied": True
            }
            
            # HR decisions always require human approval for HaruPlate
            self.state.approval_required = True
            self.state.approval_message = f"HR Expert Crew has completed analysis for: {self.state.original_request[:100]}..."
            
            logger.info(f"✅ HR Expert Crew processing complete")
            
        except Exception as e:
            logger.error(f"❌ HR Crew processing failed: {str(e)}")
            self.state.hr_result = {
                "error": str(e),
                "success": False,
                "crew_type": "hr"
            }

    @listen(analyze_request)  
    def process_admin_request(self):
        """
        Step 2b: Process Admin requests using Admin Expert Crew
        Pattern from meeting_assistant_flow.add_tasks_to_trello()
        """
        if self.state.request_type != "admin":
            return
            
        logger.info(f"📋 Processing Admin request with HaruPlate Admin Expert Crew...")
        
        try:
            # Simulate Admin crew processing (will be replaced with actual crew)
            from ..crews.haruplate_admin_crew import HaruPlateAdminCrew
            
            admin_crew = HaruPlateAdminCrew()
            
            # Process request with HaruPlate context
            crew_context = {
                "company_name": "HaruPlate",
                "operational_focus": "Malaysian suppliers, Singapore sales data",
                "file_systems": "Google Drive, Google Sheets integration",
                "compliance": "Child nutrition industry standards",
                "request_id": self.state.request_id
            }
            
            admin_result = admin_crew.kickoff({
                "request": self.state.original_request,
                "context": crew_context
            })
🎼 HaruPlate Admin Expert Crew Analysis:

📝 Request: {self.state.original_request}

📊 ADMIN TEAM ANALYSIS:
Our Admin Expert Crew has processed your operational request:

⚡ PROCESSING PLAN:
- Malaysian supplier invoice automation
- Google Sheets integration for expense tracking
- Document archiving to Google Drive
- Compliance with child nutrition industry standards

🔧 IMPLEMENTATION APPROACH:
- Automated PDF extraction from Gmail
- Data parsing and validation
- Structured data entry to Google Sheets
- File archiving with proper naming conventions

📈 EXPECTED OUTCOMES:
- Improved processing efficiency (60% time savings)
- Standardized documentation format
- Better financial data organization
- Enhanced compliance tracking

📅 TIMELINE:
- Initial setup: 2-4 hours
- Quality review: 1 hour
- System integration testing: 30 minutes
- Go-live and monitoring: Ongoing

🌟 All processes maintain HaruPlate's operational excellence standards.
"""
            
            self.state.admin_result = {
                "crew_output": admin_simulation_result,
                "processing_timestamp": datetime.now().isoformat(),
                "crew_type": "admin",
                "success": True,
                "haruplate_compliance": True
            }
            
            # Check if human approval is required for financial decisions
            financial_keywords = ["invoice", "expense", "budget", "payment", "supplier"]
            if any(keyword in self.state.original_request.lower() for keyword in financial_keywords):
                self.state.approval_required = True
                self.state.approval_message = f"Admin Expert Crew has completed financial analysis for: {self.state.original_request[:100]}..."
            
            logger.info(f"✅ Admin Expert Crew processing complete")
            
        except Exception as e:
            logger.error(f"❌ Admin Crew processing failed: {str(e)}")
            self.state.admin_result = {
                "error": str(e),
                "success": False,
                "crew_type": "admin"
            }

    @router("process_hr_request")
    def human_approval_checkpoint(self):
        """
        Step 3: Human-in-the-Loop approval checkpoint
        Pattern from lead-score-flow.human_in_the_loop()
        """
        if not self.state.approval_required:
            return "finalize_response"
            
        logger.info(f"🔐 Human approval required...")
        
        # Display results for human review
        print("\n" + "="*60)
        print("🎼 HaruPlate Orchestra - Human Approval Required")
        print("="*60)
        print(f"📋 Original Request: {self.state.original_request}")
        print(f"📊 Request Type: {self.state.request_type.upper()}")
        print(f"⏰ Processing Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show crew results
        if self.state.hr_result:
            print(f"\n👥 HR Expert Crew Results:")
            print(f"{self.state.hr_result.get('crew_output', 'No output available')}")
            
        if self.state.admin_result:
            print(f"\n📋 Admin Expert Crew Results:")
            print(f"{self.state.admin_result.get('crew_output', 'No output available')}")
        
        print(f"\n{self.state.approval_message}")
        
        # Human approval options (following lead-score-flow pattern)
        print("\n🔄 Please choose an option:")
        print("1. ✅ Approve and finalize response")
        print("2. 🔄 Request modifications")
        print("3. ❌ Reject and abort")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == "1":
                    self.state.approval_response = "approved"
                    logger.info("✅ Human approval: APPROVED")
                    return "finalize_response"
                    
                elif choice == "2":
                    feedback = input("Please provide modification feedback: ").strip()
                    self.state.approval_response = f"modification_requested: {feedback}"
                    logger.info(f"🔄 Human approval: MODIFICATION REQUESTED - {feedback}")
                    return "process_modifications"
                    
                elif choice == "3":
                    self.state.approval_response = "rejected"
                    logger.info("❌ Human approval: REJECTED")
                    return "abort_process"
                    
                else:
                    print("❌ Invalid choice. Please enter 1, 2, or 3.")
                    
            except KeyboardInterrupt:
                print("\n\n⚠️ Process interrupted by user")
                self.state.approval_response = "interrupted"
                return "abort_process"

    @listen("finalize_response")
    def finalize_orchestra_response(self):
        """
        Step 4a: Finalize the orchestra response
        Pattern from meeting_assistant_flow.send_slack_notification()
        """
        logger.info(f"🎯 Finalizing HaruPlate Orchestra response...")
        
        # Compile final response with HaruPlate branding
        final_output = {
            "request_id": self.state.request_id,
            "original_request": self.state.original_request,
            "processing_summary": {
                "request_type": self.state.request_type,
                "routing_decision": self.state.routing_decision,
                "approval_status": self.state.approval_response or "auto_approved",
                "processing_timestamp": datetime.now().isoformat()
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
            "🎼 HaruPlate Orchestra Response Summary",
            "=" * 50,
            f"📋 Request: {self.state.original_request}",
            f"🎯 Handled by: {self.state.request_type.title()} Expert Team",
            f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"✅ Status: Successfully processed with HaruPlate values alignment"
        ]
        
        if self.state.hr_result:
            summary_lines.append(f"👥 HR Team Output: Ready for implementation")
            
        if self.state.admin_result:
            summary_lines.append(f"📋 Admin Team Output: Ready for implementation")
        
        summary_lines.extend([
            "",
            "🌟 HaruPlate Orchestra is committed to supporting your strategic",
            "   vision while maintaining our family-oriented, health-focused values.",
            "=" * 50
        ])
        
        final_output["summary"] = "\n".join(summary_lines)
        
        self.state.final_result = final_output
        self.state.completed = True
        
        # Display final summary
        print("\n" + final_output["summary"])
        
        logger.info(f"🎉 HaruPlate Orchestra processing complete")

    @listen("process_modifications")
    def handle_modifications(self):
        """
        Step 4b: Handle modification requests
        Pattern from self_evaluation_loop_flow
        """
        logger.info(f"🔄 Processing modification request...")
        
        # Extract feedback from approval response
        feedback = self.state.approval_response.replace("modification_requested: ", "")
        logger.info(f"Modification feedback: {feedback}")
        
        # For now, just proceed to finalization
        # In real implementation, would re-route to appropriate crew
        return "finalize_response"

    @listen("abort_process")
    def abort_orchestra_process(self):
        """
        Step 4c: Handle process abortion
        """
        logger.info(f"🛑 Aborting HaruPlate Orchestra process...")
        
        self.state.final_result = {
            "request_id": self.state.request_id,
            "status": "aborted",
            "reason": self.state.approval_response,
            "message": "Process was terminated per user request.",
            "timestamp": datetime.now().isoformat()
        }
        
        self.state.completed = True
        
        print("\n🛑 HaruPlate Orchestra process has been aborted.")
        print("Thank you for using HaruPlate Orchestra.")


# Convenience functions for external usage
def create_haruplate_flow(request: str, user: str = "haruplate_manager") -> HaruPlateOrchestraFlow:
    """Create and return a HaruPlate Orchestra Flow instance"""
    flow = HaruPlateOrchestraFlow()
    flow.state.request_id = str(uuid.uuid4())
    flow.state.original_request = request
    flow.state.user = user
    flow.state.timestamp = datetime.now()
    return flow


def process_haruplate_request(request: str, user: str = "haruplate_manager") -> Dict[str, Any]:
    """
    Main entry point for processing HaruPlate requests
    Returns the final result dictionary
    """
    logger.info(f"🎼 Starting HaruPlate Orchestra for: {request[:50]}...")
    
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
        logger.error(f"❌ HaruPlate Orchestra failed: {str(e)}")
        return {
            "error": str(e),
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        }


# Example usage and testing
if __name__ == "__main__":
    # Test the HaruPlate Orchestra Flow
    test_requests = [
        "Tell the HR team we need to find an experienced 'Digital Marketing Specialist' for the Malaysian market. Have them start the process.",
        "Process the invoices from our Malaysian suppliers and update the Q3 expense tracking in Google Sheets.",
        "Prepare for next week's board meeting with sales data analysis from Singapore operations."
    ]
    
    print("🧪 Testing HaruPlate Orchestra Flow...")
    print("-" * 60)
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n🎼 Test Request {i}:")
        print(f"'{request}'")
        print("\n🔄 Processing...")
        
        result = process_haruplate_request(request)
        
        if result.get("error"):
            print(f"❌ Error: {result['error']}")
        else:
            print("✅ Success!")
            if result.get("summary"):
                print(result["summary"])
        
        print("\n" + "-" * 60)
