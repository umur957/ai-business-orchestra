#!/usr/bin/env python3
"""
Business Orchestra Main Execution
Updated main file that uses the improved Business Orchestra Flow
"""

import os
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variablesaaa
load_dotenv()

try:
    from src.flows.business_orchestra_flow_simple import (
        BusinessOrchestraFlow, 
        process_business_request,
        create_business_flow
    )
    FLOW_AVAILABLE = True
except ImportError as e:
    print(f"WARNING: Flow import failed: {e}")
    FLOW_AVAILABLE = False


class BusinessOrchestra:
    """
    Main Business Orchestra class
    Enhanced version with proper flow integration
    """
    
    def __init__(self):
        self.company_name = os.getenv("COMPANY_NAME", "Business")
        self.company_values = "sincere, family-oriented, child nutrition focused"
        self.tone_of_voice = "warm, professional, health-conscious"
        
        print(f"{self.company_name} Orchestra initialized")
        print(f"Company values: {self.company_values}")
        print(f"Brand voice: {self.tone_of_voice}")

    def process_request(self, request: str, user: str = "business_manager") -> Dict[str, Any]:
        """
        Process a business request through the Business Orchestra
        """
        print(f"\nBusiness Orchestra - Processing Request")
        print(f" User: {user}")
        print(f" Request: {request}")
        print("-" * 60)
        
        if FLOW_AVAILABLE:
            return process_business_request(request, user)
        else:
            return self._simulate_response(request)

    def _simulate_response(self, request: str) -> Dict[str, Any]:
        """Fallback simulation when flow is not available"""
        
        request_lower = request.lower()
        
        # Determine request type
        hr_keywords = ["hire", "recruit", "teammate", "position", "job", "malaysian market"]
        admin_keywords = ["invoice", "supplier", "expense", "meeting", "data", "singapore"]
        
        if any(keyword in request_lower for keyword in hr_keywords):
            request_type = "hr"
            simulation_result = f"""
Business Orchestra - HR Expert Team Response

 Request: {request}

 HR EXPERT TEAM ANALYSIS:
Our HR team has analyzed your request with Business's family-oriented values:

 RECRUITMENT STRATEGY:
 Position aligned with child nutrition mission
 Malaysian market cultural sensitivity applied
 "Teammate" terminology (not "candidate") used
 Family-oriented, sincere tone maintained

NEXT STEPS:
1. Create Business-aligned job description (2-3 hours)
2. Publish on Malaysian platforms (1 hour)
3. Screen for values alignment (ongoing)
4. Schedule interviews with compatible individuals (1 week)

All processes maintain Business's warm, health-focused brand voice.
"""
        else:
            request_type = "admin"
            simulation_result = f"""
Business Orchestra - Admin Expert Team Response

 Request: {request}

 ADMIN EXPERT TEAM ANALYSIS:
Our admin team has processed your operational request:

 PROCESSING PLAN:
 Malaysian supplier integration optimized
 Google Sheets automation configured  
 Document archiving to Google Drive
 Child nutrition industry compliance maintained

 EXPECTED OUTCOMES:
• 60% improvement in processing efficiency
• Standardized Business documentation
• Enhanced financial data organization
• Better compliance tracking

All operations align with Business's operational excellence.
"""

        return {
            "request_id": "sim_" + str(hash(request))[-8:],
            "original_request": request,
            "request_type": request_type,
            "status": "completed_simulation",
            "summary": simulation_result,
            "business_values_applied": True,
            "simulation_mode": True
        }

    def run_scenario(self, scenario_type: str, context: str) -> Dict[str, Any]:
        """Run a specific Business business scenario"""
        
        scenarios = {
            "hr_recruitment": "Tell the HR team we need to find an experienced 'Digital Marketing Specialist' for the Malaysian market. Have them start the process and ensure cultural fit with our family-oriented values.",
            
            "admin_invoice": "Process the invoices from our Malaysian suppliers and update the Q3 expense tracking in Google Sheets. Ensure compliance with child nutrition industry standards.",
            
            "meeting_prep": "Prepare for next week's board meeting with sales data analysis from Singapore operations. Include trends in child nutrition products.",
            
            "crisis_management": "Critical: Our main Malaysian supplier has delivery delays affecting our Q4 child nutrition product launch. Need immediate alternative sourcing.",
            
            "daily_operations": "Coordinate team meeting for 15 Business staff with catering that aligns with our healthy nutrition values and presentation setup for product roadmap."
        }
        
        if scenario_type in scenarios:
            scenario_request = scenarios[scenario_type]
            if context:
                scenario_request += f" Additional context: {context}"
                
            print(f"\nRunning Business Scenario: {scenario_type.replace('_', ' ').title()}")
            return self.process_request(scenario_request)
        else:
            return {
                "error": f"Unknown scenario type: {scenario_type}",
                "available_scenarios": list(scenarios.keys())
            }

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "company": self.company_name,
            "values": self.company_values,
            "tone": self.tone_of_voice,
            "flow_available": FLOW_AVAILABLE,
            "components": {
                "orchestra_conductor": True,
                "hr_expert_crew": True,
                "admin_expert_crew": True,
                "human_approval_flow": FLOW_AVAILABLE,
                "business_integration": True
            },
            "status": "operational"
        }


def main():
    """Main function demonstrating Business Orchestra capabilities"""
    
    print("Business Orchestra - Intelligent HR & Admin Automation")
    print("=" * 65)
    print("Like Business's founders, focus on strategy & product vision")
    print("AI Let the Orchestra handle repetitive HR & admin tasks")
    print("=" * 65)
    
    # Initialize Business Orchestra
    orchestra = BusinessOrchestra()
    
    # System status
    print(f"\n System Status:")
    status = orchestra.get_system_status()
    for key, value in status.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for sub_key, sub_value in value.items():
                print(f"      {sub_key}: {sub_value}")
        else:
            print(f"    {key}: {value}")
    
    # Demo requests with Business context
    demo_requests = [
        ("HR Recruitment", "Tell the HR team we need to find an experienced 'Digital Marketing Specialist' for the Malaysian market. Ensure they understand our family-oriented values and passion for child nutrition."),
        
        ("Admin Processing", "Process the invoices from our Malaysian suppliers and update the Q3 expense tracking in Google Sheets. Focus on our health food suppliers."),
        
        ("Strategic Planning", "Prepare for next week's board meeting with sales data analysis from Singapore operations. Include performance of our child nutrition products.")
    ]
    
    print(f"\n Testing Business Orchestra with Demo Requests...")
    print("-" * 65)
    
    for i, (request_type, request) in enumerate(demo_requests, 1):
        print(f"\nDemo Request {i}: {request_type}")
        print(f"'{request[:80]}{'...' if len(request) > 80 else ''}'")
        print(f"\n Processing through Business Orchestra...")
        
        try:
            result = orchestra.process_request(request)
            
            if result.get("error"):
                print(f" Error: {result['error']}")
            else:
                print(" Success!")
                if result.get("summary"):
                    # Show first part of summary
                    summary_lines = result["summary"].split('\n')
                    for line in summary_lines[:10]:  # Show first 10 lines
                        print(line)
                    if len(summary_lines) > 10:
                        print("   ... (truncated for demo)")
                        
                print(f"\n Request Type: {result.get('request_type', 'unknown').upper()}")
                print(f"Business Values Applied: {'YES' if result.get('business_values_applied') else 'NO'}")
                
        except Exception as e:
            print(f" Unexpected error: {str(e)}")
        
        print("\n" + "-" * 65)
    
    # Interactive mode
    print(f"\nInteractive Mode:")
    print("Enter your Business business requests, or 'quit' to exit")
    print("Example: 'Find a nutritionist for our Malaysian team'")
    
    while True:
        try:
            user_request = input("\nYour request: ").strip()
            
            if user_request.lower() in ['quit', 'exit', 'q']:
                break
                
            if user_request:
                result = orchestra.process_request(user_request)
                
                if result.get("summary"):
                    print(f"\n{result['summary']}")
                else:
                    print(f" Request processed: {result.get('status', 'unknown')}")
            else:
                print("Please enter a request or 'quit' to exit.")
                
        except KeyboardInterrupt:
            break
    
    print(f"\nThank you for using Business Orchestra!")
    print("Supporting your strategic vision with intelligent automation")


if __name__ == "__main__":
    main()
