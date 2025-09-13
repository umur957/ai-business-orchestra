#!/usr/bin/env python3
"""
Business Orchestra Flow
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
class BusinessRequestState(BaseModel):
    """Main state for Business Orchestra Flow - similar to MeetingState pattern."""
    id: str  # Required by CrewAI Flow
    request_id: str
    original_request: str
    request_type: str = ""  # "hr" or "admin" 
    priority: str = "normal"
    timestamp: datetime = datetime.now()
    user: str = "business_manager"
    
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

class BusinessOrchestraFlow(Flow[BusinessRequestState]):
    """
    Business Orchestra Conductor Flow
    Orchestrates HR and Admin crews using CrewAI Flows pattern
    """

    def __init__(self, request_text: str, user: str = "business_manager"):
        """Initialize flow with request."""
        initial_state = BusinessRequestState(
            request_id=str(uuid.uuid4()),
            original_request=request_text,
            user=user,
            timestamp=datetime.now()
        )
        super().__init__(initial_state)

    @start()
    def analyze_request(self) -> BusinessRequestState:
        """
        Step 1: Analyze the incoming request to determine routing
        Pattern from meeting_assistant_flow.load_meeting_notes()
        """
        logger.info(f"🎼 Business Orchestra: Analyzing request {self.state.request_id[:8]}...")
        
        request_text = self.state.original_request.lower()
        
        # Business-specific keyword analysis
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
        
        # Routing decision with Business context
        if hr_score > admin_score:
            self.state.request_type = "hr"
            routing_reason = f"HR-focused request detected (score: {hr_score})"
        elif admin_score > hr_score:
            self.state.request_type = "admin" 
            routing_reason = f"Admin-focused request detected (score: {admin_score})"
        else:
            # Default to HR for Business people-first philosophy
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
    def process_hr_request(self) -> Optional[BusinessRequestState]:
        """
        Step 2a: Process HR requests using HR Expert Crew
        Pattern from meeting_assistant_flow.generate_tasks_from_meeting_transcript()
        """
        if self.state.request_type != "hr":
            return None
            
        logger.info(f"👥 Processing HR request with Business HR Expert Crew...")
        
        try:
            # Import and create HR crew (following repository pattern)
            from ..crews.hr_crew import BusinessHRCrew
            
            hr_crew = BusinessHRCrew()
            
            # Process request with Business context
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
                "crew_type": "hr",
                "success": True
            }
            
            # Check if human approval is required for critical HR decisions
            critical_keywords = ["hire", "recruit", "interview", "position", "malaysian market"]
            if any(keyword in self.state.original_request.lower() for keyword in critical_keywords):
                self.state.approval_required = True
                self.state.approval_message = f"HR Expert Crew has completed analysis for: {self.state.original_request[:100]}..."
            
            logger.info(f"✅ HR Expert Crew processing complete")
            return self.state
            
        except Exception as e:
            logger.error(f"❌ HR Crew processing failed: {str(e)}")
            self.state.hr_result = {
                "error": str(e),
                "success": False,
                "crew_type": "hr"
            }
            return self.state

    @listen(analyze_request)  
    def process_admin_request(self) -> Optional[BusinessRequestState]:
        """
        Step 2b: Process Admin requests using Admin Expert Crew
        Pattern from meeting_assistant_flow.add_tasks_to_trello()
        """
        if self.state.request_type != "admin":
            return None
            
        logger.info(f"📋 Processing Admin request with Business Admin Expert Crew...")
        
        try:
            # Import and create Admin crew (following repository pattern)
            from ..crews.admin_crew import BusinessAdminCrew
            
            admin_crew = BusinessAdminCrew()
            
            # Process request with Business context
            crew_context = {
                "company_name": "Business",
                "operational_focus": "Malaysian suppliers, Singapore sales data",
                "file_systems": "Google Drive, Google Sheets integration",
                "compliance": "Child nutrition industry standards",
                "request_id": self.state.request_id
            }
            
            admin_result = admin_crew.kickoff({
                "request": self.state.original_request,
                "context": crew_context
            })
            
            self.state.admin_result = {
                "crew_output": admin_result,
                "processing_timestamp": datetime.now().isoformat(),
                "crew_type": "admin",
                "success": True
            }
            
            # Check if human approval is required for financial decisions
            financial_keywords = ["invoice", "expense", "budget", "payment", "supplier"]
            if any(keyword in self.state.original_request.lower() for keyword in financial_keywords):
                self.state.approval_required = True
                self.state.approval_message = f"Admin Expert Crew has completed analysis for: {self.state.original_request[:100]}..."
            
            logger.info(f"✅ Admin Expert Crew processing complete")
            return self.state
            
        except Exception as e:
            logger.error(f"❌ Admin Crew processing failed: {str(e)}")
            self.state.admin_result = {
                "error": str(e),
                "success": False,
                "crew_type": "admin"
            }
            return self.state

    @router("process_hr_request")
    def human_approval_checkpoint(self) -> str:
        """
        Step 3: Human-in-the-Loop approval checkpoint
        Pattern from lead-score-flow.human_in_the_loop()
        """
        if not self.state.approval_required:
            return "finalize_response"
            
        logger.info(f"🔐 Human approval required for request: {self.state.request_id[:8]}")
        
        # Display results for human review
        print("\n" + "="*60)
        print("🎼 Business Orchestra - Human Approval Required")
        print("="*60)
        print(f"📋 Original Request: {self.state.original_request}")
        print(f"📊 Request Type: {self.state.request_type.upper()}")
        print(f"⏰ Processing Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show crew results
        if self.state.hr_result:
            print(f"\n👥 HR Expert Crew Results:")
            print(f"   {self.state.hr_result.get('crew_output', 'No output available')}")
            
        if self.state.admin_result:
            print(f"\n📋 Admin Expert Crew Results:")
            print(f"   {self.state.admin_result.get('crew_output', 'No output available')}")
        
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
    def finalize_orchestra_response(self) -> BusinessRequestState:
        """
        Step 4a: Finalize the orchestra response
        Pattern from meeting_assistant_flow.send_slack_notification()
        """
        logger.info(f"🎯 Finalizing Business Orchestra response...")
        
        # Compile final response with Business branding
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
            "business_context": {
                "company_values": "sincere, family-oriented, child nutrition focused",
                "brand_voice": "warm, professional, health-conscious"
            }
        }
        
        # Add crew-specific results
        if self.state.hr_result:
            final_output["crew_results"]["hr_expert_team"] = self.state.hr_result
            
        if self.state.admin_result:
            final_output["crew_results"]["admin_expert_team"] = self.state.admin_result
        
        # Generate Business-style summary
        summary_lines = [
            "🎼 Business Orchestra Response Summary",
            "=" * 50,
            f"📋 Request: {self.state.original_request}",
            f"🎯 Handled by: {self.state.request_type.title()} Expert Team",
            f"⏰ Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"✅ Status: Successfully processed with Business values alignment"
        ]
        
        if self.state.hr_result:
            summary_lines.append(f"👥 HR Team Output: Ready for implementation")
            
        if self.state.admin_result:
            summary_lines.append(f"📋 Admin Team Output: Ready for implementation")
        
        summary_lines.extend([
            "",
            "🌟 Business Orchestra is committed to supporting your strategic",
            "   vision while maintaining our family-oriented, health-focused values.",
            "=" * 50
        ])
        
        final_output["summary"] = "\n".join(summary_lines)
        
        self.state.final_result = final_output
        self.state.completed = True
        
        # Display final summary
        print("\n" + final_output["summary"])
        
        logger.info(f"🎉 Business Orchestra processing complete for request {self.state.request_id[:8]}")
        return self.state

    @listen("process_modifications")
    def handle_modifications(self) -> str:
        """
        Step 4b: Handle modification requests
        Pattern from self_evaluation_loop_flow
        """
        logger.info(f"🔄 Processing modification request...")
        
        # Extract feedback from approval response
        feedback = self.state.approval_response.replace("modification_requested: ", "")
        
        # Re-route to appropriate crew with feedback
        if self.state.request_type == "hr":
            return "process_hr_request"
        else:
            return "process_admin_request"

    @listen("abort_process")
    def abort_orchestra_process(self) -> BusinessRequestState:
        """
        Step 4c: Handle process abortion
        """
        logger.info(f"🛑 Aborting Business Orchestra process...")
        
        self.state.final_result = {
            "request_id": self.state.request_id,
            "status": "aborted",
            "reason": self.state.approval_response,
            "message": "Process was terminated per user request.",
            "timestamp": datetime.now().isoformat()
        }
        
        self.state.completed = True
        
        print("\n🛑 Business Orchestra process has been aborted.")
        print("Thank you for using Business Orchestra.")
        
        return self.state


# Convenience functions for external usage
def create_business_flow(request: str, user: str = "business_manager") -> BusinessOrchestraFlow:
    """Create and return a Business Orchestra Flow instance"""
    return BusinessOrchestraFlow(request, user)


def process_business_request(request: str, user: str = "business_manager") -> Dict[str, Any]:
    """
    Main entry point for processing Business requests
    Returns the final result dictionary
    """
    logger.info(f"🎼 Starting Business Orchestra for: {request[:50]}...")
    
    try:
        flow = create_business_flow(request, user)
        result = flow.kickoff()
        
        if hasattr(result, 'final_result') and result.final_result:
            return result.final_result
        else:
            return {
                "error": "Flow completed but no final result generated",
                "status": "incomplete"
            }
            
    except Exception as e:
        logger.error(f"❌ Business Orchestra failed: {str(e)}")
        return {
            "error": str(e),
            "status": "failed",
            "timestamp": datetime.now().isoformat()
        }


# Example usage and testing
if __name__ == "__main__":
    # Test the Business Orchestra Flow
    test_requests = [
        "Tell the HR team we need to find an experienced 'Digital Marketing Specialist' for the Malaysian market. Have them start the process.",
        "Process the invoices from our Malaysian suppliers and update the Q3 expense tracking in Google Sheets.",
        "Prepare for next week's board meeting with sales data analysis from Singapore operations."
    ]
    
    print("🧪 Testing Business Orchestra Flow...")
    print("-" * 60)
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n🎼 Test Request {i}:")
        print(f"'{request}'")
        print("\n🔄 Processing...")
        
        result = process_business_request(request)
        
        if result.get("error"):
            print(f"❌ Error: {result['error']}")
        else:
            print("✅ Success!")
            if result.get("summary"):
                print(result["summary"])
                "crew_type": "hr_expert",
                "business_compliance": True,
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
    def process_admin_request(self) -> Optional[BusinessRequestState]:
        """
        Step 2b: Process Admin requests using Admin Expert Crew  
        Pattern from meeting_assistant_flow workflow steps
        """
        if self.state.request_type != "admin":
            return None
            
        logger.info(f"🏢 Processing Admin request with Business Admin Expert Crew...")
        
        try:
            # Import and create Admin crew
            from ..crews.admin_crew import BusinessAdminCrew
            
            admin_crew = BusinessAdminCrew()
            
            # Process request with Business context
            crew_context = {
                "company_focus": "Child nutrition, natural products",
                "supplier_focus": "Malaysian suppliers priority", 
                "expense_categories": "Business-specific categorization",
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
    def finalize_results(self) -> BusinessRequestState:
        """
        Step 3: Finalize and format results for delivery
        Pattern from meeting_assistant_flow.save_new_tasks_to_csv()
        """
        logger.info(f"🎯 Finalizing Business Orchestra results...")
        
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
            # Format successful results with Business branding
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
                "business_context": {
                    "company_values": "Sincere, family-oriented approach to child nutrition",
                    "market_focus": "Malaysian market with cultural sensitivity",
                    "brand_compliance": "Business terminology and tone maintained",
                    "next_steps": self._generate_next_steps(active_result)
                }
            }
        
        self.state.completed = True
        
        logger.info(f"🎉 Business Orchestra workflow completed for request {self.state.request_id[:8]}")
        return self.state

    # Helper methods for approval and next steps
    def _generate_hr_approval_message(self, hr_result: Dict[str, Any]) -> str:
        """Generate human approval message for HR results."""
        return (
            f"🎼 Business HR Expert Crew has completed processing.\n\n"
            f"The team has analyzed your request and prepared recommendations "
            f"following Business's family-oriented values and Malaysian market focus.\n\n"
            f"Please review the results and provide approval to proceed with next steps."
        )
    
    def _generate_admin_approval_message(self, admin_result: Dict[str, Any]) -> str:
        """Generate human approval message for Admin results.""" 
        return (
            f"🎼 Business Admin Expert Crew has completed processing.\n\n"
            f"The team has processed your administrative request with attention "
            f"to Business's operational standards and supplier preferences.\n\n"
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
                "Prepare Business-specific interview questions",
                "Coordinate with Communications Coordinator for outreach"
            ]
        else:
            return [
                "Review processed documents and data",
                "Verify Malaysian supplier information",
                "Check Google Sheets updates",
                "Archive documents to appropriate folders"
            ]


def run_business_orchestra(request: str, user: str = "business_manager") -> Dict[str, Any]:
    """
    Main entry point to run Business Orchestra
    Similar to main() function in meeting_assistant_flow
    """
    logger.info(f"🚀 Starting Business Orchestra for request: {request[:50]}...")
    
    # Create and run the flow
    orchestra_flow = BusinessOrchestraFlow(request, user)
    
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
    result = run_business_orchestra(test_request)
    print(f"Result: {json.dumps(result, indent=2)}")