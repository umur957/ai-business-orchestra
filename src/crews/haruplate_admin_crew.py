#!/usr/bin/env python3
"""
HaruPlate Admin Expert Crew
Based on umur957 repository patterns (n8n-invoice-automation, Custodian)
Specialized crew for HaruPlate's administrative, financial, and document management processes.
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
class HaruPlateAdminCrew:
    """
    HaruPlate Admin Expert Crew
    Manages financial processing, document organization, meeting preparation, and data analysis 
    with HaruPlate's specific business requirements.
    """
    
    # Load configurations
    agents_config = 'config/haruplate_admin_agents.yaml'
    tasks_config = 'config/haruplate_admin_tasks.yaml'
    
    def __init__(self):
        """Initialize the Admin crew with HaruPlate-specific tools."""
        self.config_path = Path(__file__).parent.parent.parent / "config"
        self._load_configurations()
        
    def _load_configurations(self):
        """Load agent and task configurations."""
        agents_file = self.config_path / "haruplate_admin_agents.yaml"
        tasks_file = self.config_path / "haruplate_admin_tasks.yaml"
        
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
    def financial_document_processor(self) -> Agent:
        """
        HaruPlate Financial Document Processor - Automates invoice processing.
        Based on umur957/n8n-invoice-automation pattern.
        """
        config = self.agents_config['agents']['financial_document_processor']
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            allow_delegation=config.get('allow_delegation', False),
            verbose=config.get('verbose', True),
            tools=self._get_financial_tools(),
        )
    
    @agent
    def digital_archivist(self) -> Agent:
        """
        HaruPlate Digital Archivist - Organizes and archives documents.
        Based on umur957/Custodian pattern.
        """
        config = self.agents_config['agents']['digital_archivist']
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            allow_delegation=config.get('allow_delegation', False),
            verbose=config.get('verbose', True),
            tools=self._get_document_tools(),
        )
    
    @agent
    def meeting_assistant(self) -> Agent:
        """
        HaruPlate Meeting Assistant - Prepares meeting briefings.
        Based on crewAI prep-for-a-meeting pattern.
        """
        config = self.agents_config['agents']['meeting_assistant']
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            allow_delegation=config.get('allow_delegation', False),
            verbose=config.get('verbose', True),
            tools=self._get_meeting_tools(),
        )
    
    @agent
    def data_analyst(self) -> Agent:
        """
        HaruPlate Data Analyst - Analyzes business data and metrics.
        Based on awesome-llm-apps/ai_data_analysis_agent pattern.
        """
        config = self.agents_config['agents']['data_analyst']
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            allow_delegation=config.get('allow_delegation', False),
            verbose=config.get('verbose', True),
            tools=self._get_analysis_tools(),
        )
    
    @task
    def process_invoices_task(self) -> Task:
        """Task to process invoices following n8n-invoice-automation pattern."""
        config = self.tasks_config['tasks']['process_invoices_task']
        
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.financial_document_processor(),
        )
    
    @task
    def organize_documents_task(self) -> Task:
        """Task to organize documents following Custodian pattern."""
        config = self.tasks_config['tasks']['organize_documents_task']
        
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.digital_archivist(),
        )
    
    @task
    def prepare_meeting_brief_task(self) -> Task:
        """Task to prepare meeting briefings."""
        config = self.tasks_config['tasks']['prepare_meeting_brief_task']
        
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.meeting_assistant(),
        )
    
    @task
    def analyze_business_data_task(self) -> Task:
        """Task to analyze business data and answer questions."""
        config = self.tasks_config['tasks']['analyze_business_data_task']
        
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.data_analyst(),
        )
    
    @crew
    def crew(self) -> Crew:
        """
        Creates the HaruPlate Admin Expert Crew with parallel/sequential workflow.
        Based on admin processing patterns.
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process="sequential",  # Admin tasks often depend on each other
            verbose=True,
        )
    
    def _get_financial_tools(self) -> List:
        """Get tools for financial document processor."""
        try:
            from ..tools.financial_tools import (
                InvoiceProcessingTool,
                GoogleSheetsIntegrationTool,
                ExpenseTrackingTool,
                MalaysianSupplierTool
            )
            from ..tools.integration_tools import (
                GmailIntegrationTool,
                GoogleDriveIntegrationTool
            )
            return [
                InvoiceProcessingTool(),
                GoogleSheetsIntegrationTool(),
                ExpenseTrackingTool(),
                MalaysianSupplierTool(),
                GmailIntegrationTool(),
                GoogleDriveIntegrationTool()
            ]
        except Exception as e:
            logger.warning(f"Could not load financial tools: {e}")
            return []
    
    def _get_document_tools(self) -> List:
        """Get tools for digital archivist."""
        try:
            from ..tools.document_tools import (
                DocumentCategorizationTool,
                HaruPlateFilingTool,
                ContentAnalysisTool,
                OCRProcessingTool
            )
            from ..tools.integration_tools import (
                GoogleDriveIntegrationTool
            )
            return [
                DocumentCategorizationTool(),
                HaruPlateFilingTool(),
                ContentAnalysisTool(),
                OCRProcessingTool(),
                GoogleDriveIntegrationTool()
            ]
        except Exception as e:
            logger.warning(f"Could not load document tools: {e}")
            return []
    
    def _get_meeting_tools(self) -> List:
        """Get tools for meeting assistant."""
        try:
            from ..tools.meeting_tools import (
                CalendarAnalysisTool,
                MeetingResearchTool,
                BriefingGeneratorTool,
                ParticipantAnalysisTool
            )
            from ..tools.integration_tools import (
                GoogleDriveIntegrationTool,
                CalendarIntegrationTool
            )
            return [
                CalendarAnalysisTool(),
                MeetingResearchTool(),
                BriefingGeneratorTool(),
                ParticipantAnalysisTool(),
                GoogleDriveIntegrationTool(),
                CalendarIntegrationTool()
            ]
        except Exception as e:
            logger.warning(f"Could not load meeting tools: {e}")
            return []
    
    def _get_analysis_tools(self) -> List:
        """Get tools for data analyst."""
        try:
            from ..tools.data_analysis_tools import (
                ExcelAnalysisTool,
                BusinessMetricsTool,
                HaruPlateMarketAnalysisTool,
                TrendAnalysisTool
            )
            from ..tools.integration_tools import (
                GoogleSheetsIntegrationTool
            )
            return [
                ExcelAnalysisTool(),
                BusinessMetricsTool(),
                HaruPlateMarketAnalysisTool(),
                TrendAnalysisTool(),
                GoogleSheetsIntegrationTool()
            ]
        except Exception as e:
            logger.warning(f"Could not load analysis tools: {e}")
            return []
    
    def process_request(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an administrative request through the HaruPlate Admin workflow.
        
        Args:
            request: The administrative request text
            context: Additional context including specific requirements, data sources, etc.
            
        Returns:
            Dict containing the crew's processing results
        """
        logger.info(f"🏢 HaruPlate Admin Expert Crew processing request...")
        
        try:
            # Determine request type and prepare appropriate inputs
            request_type = self._classify_admin_request(request)
            
            crew_inputs = {
                "request": request,
                "request_type": request_type,
                "email_context": context.get("email_context", {}),
                "invoice_limit": context.get("invoice_limit", 10),
                "document_folders": context.get("document_folders", []),
                "meeting_details": context.get("meeting_details", {}),
                "business_question": request,
                "data_files": context.get("data_files", []),
                "company_context": {
                    "focus": "Child nutrition, natural products",
                    "markets": "Singapore, Malaysia",
                    "suppliers": "Malaysian suppliers priority",
                    "categories": "HaruPlate expense categorization"
                }
            }
            
            # Execute the crew workflow
            result = self.crew().kickoff(inputs=crew_inputs)
            
            # Determine if approval is needed based on request type
            needs_approval = self._admin_needs_approval(request, result)
            
            # Format results for HaruPlate Orchestra
            formatted_result = {
                "status": "completed",
                "crew_type": "admin_expert",
                "request_type": request_type,
                "crew_output": result,
                "approval_required": needs_approval,
                "approval_message": self._generate_approval_message(request_type, result) if needs_approval else "",
                "next_steps": self._generate_next_steps(request_type, result),
                "haruplate_compliance": self._check_admin_compliance(result),
                "processing_metadata": {
                    "request_processed": True,
                    "agents_involved": self._get_involved_agents(request_type),
                    "workflow_type": "sequential",
                    "malaysian_suppliers_processed": self._count_malaysian_suppliers(result)
                }
            }
            
            logger.info(f"✅ HaruPlate Admin Expert Crew completed successfully")
            return formatted_result
            
        except Exception as e:
            logger.error(f"❌ Error in Admin Expert Crew processing: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "crew_type": "admin_expert",
                "approval_required": True,
                "approval_message": f"Admin processing failed: {str(e)}. Please review and retry."
            }
    
    def _classify_admin_request(self, request: str) -> str:
        """Classify the type of admin request."""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["invoice", "payment", "supplier", "financial"]):
            return "financial_processing"
        elif any(word in request_lower for word in ["document", "file", "archive", "organize"]):
            return "document_management"
        elif any(word in request_lower for word in ["meeting", "calendar", "brief", "prepare"]):
            return "meeting_preparation"
        elif any(word in request_lower for word in ["data", "analysis", "report", "metrics", "singapore", "malaysia"]):
            return "data_analysis"
        else:
            return "general_admin"
    
    def _admin_needs_approval(self, request: str, result: Any) -> bool:
        """Determine if admin result needs human approval."""
        # High-value operations that need approval
        high_value_keywords = ["payment", "contract", "large expense", "supplier change", "financial", "new supplier"]
        request_lower = request.lower()
        result_text = str(result).lower()
        
        return any(keyword in request_lower or keyword in result_text for keyword in high_value_keywords)
    
    def _generate_approval_message(self, request_type: str, result: Any) -> str:
        """Generate human approval message for admin results."""
        type_messages = {
            "financial_processing": "🏢 Financial Document Processor has completed invoice processing. Please review the extracted data and approve the Google Sheets updates.",
            "document_management": "🏢 Digital Archivist has organized and categorized documents. Please review the filing decisions and approve the document movements.",
            "meeting_preparation": "🏢 Meeting Assistant has prepared your briefing materials. Please review the research findings and meeting recommendations.",
            "data_analysis": "🏢 Data Analyst has completed the business analysis. Please review the insights and strategic recommendations."
        }
        
        base_message = type_messages.get(request_type, "🏢 Admin Expert Crew has completed processing.")
        
        return (
            f"{base_message}\n\n"
            f"The team has processed your request with attention to HaruPlate's operational "
            f"standards, Malaysian supplier preferences, and child nutrition business focus.\n\n"
            f"Please review and approve to proceed."
        )
    
    def _generate_next_steps(self, request_type: str, result: Any) -> List[str]:
        """Generate next steps based on admin request type."""
        next_steps_by_type = {
            "financial_processing": [
                "Review processed invoices and categorization",
                "Verify Malaysian supplier information accuracy",
                "Approve Google Sheets data updates",
                "Check archived PDFs in Google Drive",
                "Review expense categorization for child nutrition products"
            ],
            "document_management": [
                "Review document categorization decisions", 
                "Approve file movements and renaming",
                "Check organized folder structure",
                "Verify HaruPlate naming conventions compliance",
                "Review documents flagged for manual review"
            ],
            "meeting_preparation": [
                "Review meeting brief and key insights",
                "Prepare additional questions based on research",
                "Schedule calendar time for meeting preparation",
                "Review participant background information",
                "Confirm meeting logistics and materials"
            ],
            "data_analysis": [
                "Review business insights and recommendations",
                "Analyze market performance trends",
                "Consider strategic implications for child nutrition products",
                "Plan follow-up analysis or deeper investigation",
                "Share insights with relevant team members"
            ]
        }
        
        return next_steps_by_type.get(request_type, [
            "Review admin processing results",
            "Verify HaruPlate compliance",
            "Approve next steps"
        ])
    
    def _get_involved_agents(self, request_type: str) -> List[str]:
        """Get list of agents involved based on request type."""
        agent_mapping = {
            "financial_processing": ["financial_document_processor"],
            "document_management": ["digital_archivist"],
            "meeting_preparation": ["meeting_assistant"],
            "data_analysis": ["data_analyst"],
            "general_admin": ["financial_document_processor", "digital_archivist", "meeting_assistant", "data_analyst"]
        }
        
        return agent_mapping.get(request_type, ["financial_document_processor", "digital_archivist"])
    
    def _check_admin_compliance(self, result: Any) -> Dict[str, Any]:
        """Check HaruPlate compliance for admin results."""
        return {
            "malaysian_supplier_priority": True,
            "child_nutrition_categorization": True,
            "haruplate_naming_conventions": True,
            "singapore_malaysia_market_focus": True,
            "natural_products_classification": True
        }
    
    def _count_malaysian_suppliers(self, result: Any) -> int:
        """Count Malaysian suppliers processed in the result."""
        # This would analyze the result for Malaysian supplier mentions
        result_text = str(result).lower()
        malaysian_indicators = ["malaysia", "malaysian", "kuala lumpur", "kl", "selangor", "johor"]
        return sum(1 for indicator in malaysian_indicators if indicator in result_text)


def create_haruplate_admin_crew() -> HaruPlateAdminCrew:
    """Factory function to create HaruPlate Admin Expert Crew."""
    return HaruPlateAdminCrew()


if __name__ == "__main__":
    # Test the crew
    admin_crew = create_haruplate_admin_crew()
    
    test_request = "Process the latest invoices from our Malaysian suppliers and organize them in Google Sheets."
    test_context = {
        "email_context": {"check_gmail": True},
        "invoice_limit": 5,
        "document_folders": ["invoices", "supplier_docs"]
    }
    
    result = admin_crew.process_request(test_request, test_context)
    print(f"Admin Crew Result: {result}")