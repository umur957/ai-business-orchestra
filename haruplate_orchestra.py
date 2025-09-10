#!/usr/bin/env python3
"""
HaruPlate HR & Admin Intelligence Orchestra - Main Entry Point
The complete AI-powered business automation system for HaruPlate, built using real CrewAI patterns.

Based on GitHub repository patterns:
- crewAI-examples/flows for orchestration
- crewAI-examples/crews/recruitment for HR processes
- umur957/n8n-invoice-automation for financial automation
- umur957/Custodian for document management
- awesome-llm-apps for real API integrations

Project Philosophy: "Like the founders of HaruPlate, managers should dedicate their time to 
strategic thinking, product development, and the brand vision—not to repetitive, time-consuming 
HR and administrative tasks."
"""

import sys
import os
from pathlib import Path
import logging
import json
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# HaruPlate Orchestra imports
try:
    from flows.haruplate_orchestra_flow import HaruPlateOrchestraFlow, run_haruplate_orchestra
    from crews.haruplate_hr_crew import create_haruplate_hr_crew
    from crews.haruplate_admin_crew import create_haruplate_admin_crew
    from tools.real_api_integrations import (
        create_gmail_tool, create_sheets_tool, create_zoom_tool, create_drive_tool
    )
    HARUPLATE_IMPORTS_AVAILABLE = True
except ImportError as e:
    HARUPLATE_IMPORTS_AVAILABLE = False
    logging.error(f"HaruPlate Orchestra imports failed: {e}")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('haruplate_orchestra.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HaruPlateOrchestra:
    """
    Main HaruPlate Orchestra class - the single point of contact for all automation.
    
    This class embodies HaruPlate's philosophy: managers focus on strategy while AI handles
    repetitive HR and administrative tasks with human-in-the-loop approval for key decisions.
    """
    
    def __init__(self):
        """Initialize the HaruPlate Orchestra system."""
        self.session_id = str(uuid.uuid4())
        self.active_requests = {}
        self.api_tools = {}
        
        logger.info("🎼 Initializing HaruPlate HR & Admin Intelligence Orchestra...")
        logger.info(f"Session ID: {self.session_id}")
        
        if not HARUPLATE_IMPORTS_AVAILABLE:
            logger.error("❌ HaruPlate Orchestra dependencies not available")
            return
        
        self._initialize_api_integrations()
        self._validate_system()
        
        logger.info("✅ HaruPlate Orchestra initialized successfully!")
        self._print_welcome_message()
    
    def _initialize_api_integrations(self):
        """Initialize real API integrations following awesome-llm-apps patterns."""
        logger.info("🔧 Initializing API integrations...")
        
        try:
            self.api_tools = {
                'gmail': create_gmail_tool(),
                'sheets': create_sheets_tool(), 
                'zoom': create_zoom_tool(),
                'drive': create_drive_tool()
            }
            logger.info("✅ API integrations initialized (Gmail, Sheets, Zoom, Drive)")
        except Exception as e:
            logger.warning(f"⚠️ API integrations using simulation mode: {e}")
            self.api_tools = {}
    
    def _validate_system(self):
        """Validate that all system components are ready."""
        validation_results = {
            "hr_crew": self._test_hr_crew(),
            "admin_crew": self._test_admin_crew(),
            "flow_orchestration": self._test_flow_system(),
            "api_integrations": len(self.api_tools) > 0
        }
        
        success_count = sum(1 for v in validation_results.values() if v)
        total_count = len(validation_results)
        
        logger.info(f"🎯 System validation: {success_count}/{total_count} components ready")
        
        for component, status in validation_results.items():
            status_emoji = "✅" if status else "❌"
            logger.info(f"  {status_emoji} {component}")
    
    def _test_hr_crew(self) -> bool:
        """Test HR Expert Crew initialization."""
        try:
            hr_crew = create_haruplate_hr_crew()
            return hr_crew is not None
        except Exception as e:
            logger.error(f"HR Crew test failed: {e}")
            return False
    
    def _test_admin_crew(self) -> bool:
        """Test Admin Expert Crew initialization."""
        try:
            admin_crew = create_haruplate_admin_crew()
            return admin_crew is not None
        except Exception as e:
            logger.error(f"Admin Crew test failed: {e}")
            return False
    
    def _test_flow_system(self) -> bool:
        """Test Flow orchestration system."""
        try:
            # Test flow creation without execution
            test_flow = HaruPlateOrchestraFlow("test request", "system_test")
            return test_flow is not None
        except Exception as e:
            logger.error(f"Flow system test failed: {e}")
            return False
    
    def _print_welcome_message(self):
        """Print welcome message with HaruPlate branding."""
        welcome_message = """
        
===============================================================================

    HARUPLATE HR & ADMIN INTELLIGENCE ORCHESTRA
    
    "Sincere, Family-Oriented AI for Child Nutrition Business Excellence"
    
    MISSION: Enable HaruPlate management to focus on strategic thinking,
        product development, and brand vision while AI handles repetitive tasks.
    
    HR EXPERT CREW (4 Specialists):
       - Recruitment Strategist: Creates job descriptions with HaruPlate values
       - Profile Analyst: 60/40 scoring (values/skills) for teammate selection
       - Communications Coordinator: Warm, family-oriented outreach via Gmail/Zoom
       - Quality Control Specialist: Ensures brand compliance ("teammates" not "candidates")
    
    ADMIN EXPERT CREW (4 Specialists):
       - Financial Document Processor: Automates Malaysian supplier invoices -> Google Sheets
       - Digital Archivist: AI-powered document organization with HaruPlate categories
       - Meeting Assistant: Strategic briefings for child nutrition industry meetings
       - Data Analyst: Singapore/Malaysia market insights from business data
    
    REAL API INTEGRATIONS:
       - Gmail: Invoice processing and recruitment communications
       - Google Sheets: Financial data and expense categorization
       - Zoom: Interview scheduling and meeting coordination
       - Google Drive: Document archival and organization
    
    USAGE: Simply describe your HR or administrative need in natural language.
        The Orchestra Conductor will analyze, route, execute, and present results
        with human-in-the-loop approval for strategic decisions.

===============================================================================
        """
        print(welcome_message)
    
    def process_request(self, request: str, user: str = "haruplate_manager") -> Dict[str, Any]:
        """
        Main method to process any HaruPlate request through the Orchestra.
        
        Args:
            request: Natural language description of what needs to be done
            user: The requesting user (defaults to haruplate_manager)
            
        Returns:
            Complete results from the Orchestra workflow
        """
        if not HARUPLATE_IMPORTS_AVAILABLE:
            return {
                "status": "error",
                "message": "HaruPlate Orchestra system not properly initialized",
                "error": "Missing dependencies"
            }
        
        request_id = str(uuid.uuid4())
        logger.info(f"🎼 Processing new HaruPlate request: {request_id[:8]}")
        logger.info(f"📝 Request: {request[:100]}{'...' if len(request) > 100 else ''}")
        logger.info(f"👤 User: {user}")
        
        # Store request for tracking
        self.active_requests[request_id] = {
            "request": request,
            "user": user,
            "start_time": datetime.now(),
            "status": "processing"
        }
        
        try:
            # Run the HaruPlate Orchestra Flow
            result = run_haruplate_orchestra(request, user)
            
            # Update request tracking
            self.active_requests[request_id].update({
                "status": "completed",
                "end_time": datetime.now(),
                "result": result
            })
            
            # Add request tracking to result
            result["request_id"] = request_id
            result["session_id"] = self.session_id
            result["processing_time"] = (
                self.active_requests[request_id]["end_time"] - 
                self.active_requests[request_id]["start_time"]
            ).total_seconds()
            
            logger.info(f"✅ Request {request_id[:8]} completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Request {request_id[:8]} failed: {str(e)}")
            
            # Update request tracking
            self.active_requests[request_id].update({
                "status": "failed",
                "end_time": datetime.now(),
                "error": str(e)
            })
            
            return {
                "status": "error",
                "request_id": request_id,
                "session_id": self.session_id,
                "message": f"HaruPlate Orchestra processing failed: {str(e)}",
                "error": str(e)
            }
    
    def handle_approval_response(self, request_id: str, approval_response: str) -> Dict[str, Any]:
        """
        Handle human approval responses for requests requiring approval.
        
        Args:
            request_id: The ID of the request awaiting approval
            approval_response: "approve", "reject", or "modify"
            
        Returns:
            Results of the approval handling
        """
        logger.info(f"🔍 Handling approval response for request {request_id[:8]}: {approval_response}")
        
        if request_id not in self.active_requests:
            return {
                "status": "error",
                "message": f"Request {request_id} not found",
                "request_id": request_id
            }
        
        request_info = self.active_requests[request_id]
        
        if approval_response.lower() == "approve":
            logger.info(f"✅ Request {request_id[:8]} approved - proceeding with next steps")
            return {
                "status": "approved",
                "message": "Request approved and next steps initiated",
                "request_id": request_id,
                "next_steps": request_info.get("result", {}).get("haruplate_context", {}).get("next_steps", [])
            }
        
        elif approval_response.lower() == "reject":
            logger.info(f"❌ Request {request_id[:8]} rejected")
            return {
                "status": "rejected",
                "message": "Request rejected - workflow terminated",
                "request_id": request_id
            }
        
        else:
            logger.info(f"🔄 Request {request_id[:8]} requires modification")
            return {
                "status": "modification_requested",
                "message": "Please provide specific modification requirements",
                "request_id": request_id
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get overall system status and statistics."""
        total_requests = len(self.active_requests)
        completed_requests = sum(1 for req in self.active_requests.values() if req["status"] == "completed")
        failed_requests = sum(1 for req in self.active_requests.values() if req["status"] == "failed")
        
        return {
            "session_id": self.session_id,
            "system_status": "operational" if HARUPLATE_IMPORTS_AVAILABLE else "degraded",
            "api_integrations": list(self.api_tools.keys()),
            "request_statistics": {
                "total_requests": total_requests,
                "completed_requests": completed_requests,
                "failed_requests": failed_requests,
                "success_rate": (completed_requests / total_requests * 100) if total_requests > 0 else 0
            },
            "haruplate_context": {
                "company_values": "Sincere, family-oriented, child nutrition focused",
                "market_focus": "Malaysian and Singapore markets",
                "terminology": "Teammates (not candidates or employees)",
                "brand_tone": "Warm, health-focused, family-oriented"
            }
        }


def main():
    """Main entry point for HaruPlate Orchestra."""
    print("Starting HaruPlate HR & Admin Intelligence Orchestra...")
    
    # Initialize the Orchestra
    orchestra = HaruPlateOrchestra()
    
    if not HARUPLATE_IMPORTS_AVAILABLE:
        print("Failed to initialize HaruPlate Orchestra. Please check dependencies.")
        return
    
    # Example usage scenarios for testing
    example_scenarios = [
        {
            "name": "HR: Digital Marketing Specialist Recruitment",
            "request": "We need to find an experienced Digital Marketing Specialist for the Malaysian market who understands child nutrition and family values."
        },
        {
            "name": "Admin: Invoice Processing",
            "request": "Process the latest invoices from our Malaysian suppliers and organize them in Google Sheets with proper categorization."
        },
        {
            "name": "Admin: Meeting Preparation",
            "request": "Prepare a briefing for tomorrow's strategy meeting about expanding our child nutrition products in Singapore."
        },
        {
            "name": "Admin: Data Analysis", 
            "request": "Which was our most popular child nutrition product in Singapore this quarter, and how does it compare to Malaysian market performance?"
        }
    ]
    
    print("\n📋 Example scenarios available for testing:")
    for i, scenario in enumerate(example_scenarios, 1):
        print(f"  {i}. {scenario['name']}")
    
    # Interactive mode
    try:
        while True:
            print("\n" + "="*80)
            choice = input(
                "Enter scenario number (1-4), 'custom' for custom request, 'status' for system status, or 'quit' to exit: "
            ).strip().lower()
            
            if choice == 'quit':
                break
            elif choice == 'status':
                status = orchestra.get_status()
                print(f"\n📊 System Status:")
                print(json.dumps(status, indent=2, default=str))
            elif choice in ['1', '2', '3', '4']:
                scenario_idx = int(choice) - 1
                if 0 <= scenario_idx < len(example_scenarios):
                    scenario = example_scenarios[scenario_idx]
                    print(f"\n🎼 Executing: {scenario['name']}")
                    print(f"📝 Request: {scenario['request']}")
                    
                    result = orchestra.process_request(scenario['request'])
                    
                    print(f"\n📈 Results:")
                    print(json.dumps(result, indent=2, default=str))
                    
                    # Handle approval if required
                    if result.get("status") == "success" and result.get("processing_summary", {}).get("approval_required"):
                        approval = input("\n🤔 This request requires human approval. Approve? (yes/no): ").strip().lower()
                        if approval == 'yes':
                            approval_result = orchestra.handle_approval_response(result["request_id"], "approve")
                            print(f"✅ Approval result: {approval_result}")
                        else:
                            approval_result = orchestra.handle_approval_response(result["request_id"], "reject")
                            print(f"❌ Rejection result: {approval_result}")
                    
            elif choice == 'custom':
                custom_request = input("Enter your custom request: ").strip()
                if custom_request:
                    print(f"\n🎼 Processing custom request...")
                    result = orchestra.process_request(custom_request)
                    print(f"\n📈 Results:")
                    print(json.dumps(result, indent=2, default=str))
            else:
                print("❌ Invalid choice. Please try again.")
    
    except KeyboardInterrupt:
        print("\n\n👋 HaruPlate Orchestra session ended. Thank you!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
    # Final status
    final_status = orchestra.get_status()
    print(f"\n📊 Final Session Statistics:")
    print(f"  Total Requests: {final_status['request_statistics']['total_requests']}")
    print(f"  Success Rate: {final_status['request_statistics']['success_rate']:.1f}%")
    print(f"\n🌱 HaruPlate Orchestra session completed. Session ID: {orchestra.session_id[:8]}")


if __name__ == "__main__":
    main()