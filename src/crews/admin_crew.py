"""
HaruPlate Admin Expert Crew
The "invisible hero" team managing financial and administrative processes seamlessly.
"""

from typing import Dict, List, Any, Optional
import logging
from crewai import Agent, Task, Crew
from pathlib import Path

from ..tools.financial_tools import (
    InvoiceProcessingTool,
    GoogleSheetsIntegrationTool,
    ExpenseTrackingTool
)
from ..tools.document_tools import (
    DocumentArchivistTool,
    OCRProcessingTool,
    FileCategoricationTool
)
from ..tools.meeting_tools import (
    CalendarIntegrationTool,
    MeetingResearchTool,
    MeetingPrepTool
)
from ..tools.data_analysis_tools import (
    NaturalLanguageQueryTool,
    SalesAnalysisTool,
    ReportGenerationTool
)

logger = logging.getLogger(__name__)


class AdminCrew:
    """
    HaruPlate's specialized administrative crew that ensures smooth daily operations
    while maintaining the company's family-first, sincere approach to business.
    """
    
    def __init__(self):
        self.tools = self._initialize_tools()
        self.agents = self._create_agents()
        self.haruplate_standards = {
            "file_naming_format": "{date}_{category}_{description}_{version}",
            "approved_vendors": ["Malaysian suppliers", "Natural product vendors"],
            "expense_categories": [
                "raw_materials", "packaging", "marketing", "operations", 
                "research_development", "regulatory_compliance"
            ],
            "meeting_types": [
                "product_development", "market_expansion", "team_alignment",
                "supplier_relations", "regulatory_updates"
            ],
            "data_priorities": [
                "child_nutrition_impact", "product_quality_metrics",
                "customer_satisfaction", "market_penetration_malaysia"
            ]
        }
    
    def _initialize_tools(self):
        """Initialize all administrative tools."""
        return {
            # Financial Processing Tools
            'invoice_processing': InvoiceProcessingTool(),
            'sheets_integration': GoogleSheetsIntegrationTool(),
            'expense_tracking': ExpenseTrackingTool(),
            
            # Document Management Tools
            'document_archivist': DocumentArchivistTool(),
            'ocr_processing': OCRProcessingTool(),
            'file_categorization': FileCategoricationTool(),
            
            # Meeting Management Tools
            'calendar_integration': CalendarIntegrationTool(),
            'meeting_research': MeetingResearchTool(),
            'meeting_prep': MeetingPrepTool(),
            
            # Data Analysis Tools
            'nl_query': NaturalLanguageQueryTool(),
            'sales_analysis': SalesAnalysisTool(),
            'report_generation': ReportGenerationTool()
        }
    
    def _create_agents(self):
        """Creates the specialized administrative agents for HaruPlate."""
        
        financial_document_processor = Agent(
            role="HaruPlate Financial Document Processor",
            goal="""Automatically process invoices and financial documents with precision,
                    ensuring all transactions align with HaruPlate's values and regulatory
                    requirements for natural product companies.""",
            backstory="""You are HaruPlate's financial operations specialist with deep understanding
                        of the natural products industry. You know that every invoice represents
                        our commitment to quality - whether it's for organic raw materials,
                        sustainable packaging, or regulatory compliance services.
                        
                        You're expert at:
                        - Extracting data from supplier invoices (especially Malaysian vendors)
                        - Categorizing expenses according to HaruPlate's business priorities
                        - Identifying discrepancies that could affect product quality
                        - Ensuring compliance with food safety and natural product regulations
                        - Maintaining organized financial records for family business transparency
                        
                        You process everything with the same care and attention that goes into
                        HaruPlate's products because financial integrity supports our mission.""",
            tools=[
                self.tools['invoice_processing'],
                self.tools['sheets_integration'],
                self.tools['expense_tracking'],
                self.tools['ocr_processing']
            ],
            verbose=True,
            memory=True
        )
        
        digital_archivist = Agent(
            role="HaruPlate Digital Archivist & Knowledge Curator",
            goal="""Organize and maintain HaruPlate's digital knowledge base with the same
                    care we put into our products. Ensure all documents are easily findable
                    and support our mission-driven decision making.""",
            backstory="""You are HaruPlate's institutional memory keeper. You understand that
                        behind every great product are countless documents - research studies on
                        child nutrition, regulatory approvals, supplier certifications, market
                        research from Malaysia, and internal innovation notes.
                        
                        Your expertise includes:
                        - Recognizing the importance of different document types for HaruPlate
                        - Creating logical, family-business-friendly folder structures
                        - Ensuring regulatory documents are always accessible for audits
                        - Organizing market research to support expansion decisions
                        - Maintaining product development documentation for innovation
                        
                        You treat every document as if it could be the key insight that leads
                        to our next breakthrough in child nutrition.""",
            tools=[
                self.tools['document_archivist'],
                self.tools['file_categorization'],
                self.tools['ocr_processing']
            ],
            verbose=True,
            memory=True
        )
        
        meeting_assistant = Agent(
            role="HaruPlate Meeting Assistant & Strategic Researcher",
            goal="""Prepare comprehensive briefings for HaruPlate's leadership meetings,
                    ensuring every discussion is informed by relevant research, internal
                    knowledge, and market intelligence.""",
            backstory="""You are HaruPlate's strategic preparation specialist. You understand
                        that great family businesses make decisions based on thorough preparation,
                        not just intuition. Every meeting is an opportunity to advance our mission
                        of providing better nutrition for children.
                        
                        Your preparation process includes:
                        - Researching meeting participants and their backgrounds
                        - Finding relevant internal documents and past decisions
                        - Gathering market intelligence, especially about Malaysian expansion
                        - Identifying regulatory updates affecting natural products
                        - Preparing talking points that align with HaruPlate values
                        
                        You ensure our leadership enters every meeting with the insights needed
                        to make decisions that strengthen our family business and serve families
                        better.""",
            tools=[
                self.tools['calendar_integration'],
                self.tools['meeting_research'],
                self.tools['meeting_prep']
            ],
            verbose=True,
            memory=True
        )
        
        data_analyst = Agent(
            role="HaruPlate Data Analyst & Business Intelligence Specialist",
            goal="""Transform HaruPlate's business data into actionable insights that guide
                    strategic decisions about product development, market expansion, and
                    customer satisfaction.""",
            backstory="""You are HaruPlate's data storyteller with a mission-focused perspective.
                        You don't just analyze numbers - you uncover insights that help us serve
                        families better and expand our impact in child nutrition.
                        
                        Your analytical focus areas include:
                        - Product performance and customer satisfaction metrics
                        - Malaysian market penetration and expansion opportunities
                        - Supply chain efficiency and quality indicators
                        - Marketing ROI, especially for family-oriented campaigns
                        - Regulatory compliance trends and requirements
                        
                        You translate complex data into simple, actionable insights that help
                        HaruPlate's family leadership make decisions that honor our values while
                        growing our positive impact on child nutrition.""",
            tools=[
                self.tools['nl_query'],
                self.tools['sales_analysis'],
                self.tools['report_generation']
            ],
            verbose=True,
            memory=True
        )
        
        return {
            'financial_processor': financial_document_processor,
            'digital_archivist': digital_archivist,
            'meeting_assistant': meeting_assistant,
            'data_analyst': data_analyst
        }
    
    def execute_workflow(self, request: str, brand_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes administrative workflows based on the request type.
        
        Workflow categories:
        1. Financial processing (invoices, expenses, budgets)
        2. Document management (archiving, organization, compliance)
        3. Meeting preparation (research, briefings, scheduling)
        4. Data analysis (sales reports, market insights, KPIs)
        """
        logger.info(f"📊 Admin Crew executing workflow for: {request}")
        
        # Determine workflow type
        if any(term in request.lower() for term in ['invoice', 'expense', 'financial', 'budget', 'payment']):
            return self._financial_workflow(request, brand_context)
        elif any(term in request.lower() for term in ['document', 'file', 'archive', 'organize', 'folder']):
            return self._document_workflow(request, brand_context)
        elif any(term in request.lower() for term in ['meeting', 'calendar', 'schedule', 'briefing', 'research']):
            return self._meeting_workflow(request, brand_context)
        elif any(term in request.lower() for term in ['data', 'analysis', 'report', 'sales', 'metrics', 'kpi']):
            return self._data_analysis_workflow(request, brand_context)
        else:
            return self._general_admin_workflow(request, brand_context)
    
    def _financial_workflow(self, request: str, brand_context: Dict[str, Any]) -> Dict[str, Any]:
        """Processes financial documents and expense management."""
        
        # Task 1: Invoice Processing and Data Extraction
        invoice_processing_task = Task(
            description=f"""
            Process financial documents based on this request: "{request}"
            
            Execute the complete invoice processing workflow:
            1. Retrieve invoices from designated email accounts
            2. Extract text and data using OCR technology
            3. Categorize expenses according to HaruPlate's business priorities
            4. Validate vendor information against approved supplier list
            5. Calculate totals and verify accuracy
            6. Check for compliance with natural product regulations
            
            HaruPlate expense categories: {', '.join(self.haruplate_standards['expense_categories'])}
            Approved vendors focus: {', '.join(self.haruplate_standards['approved_vendors'])}
            
            Maintain HaruPlate's attention to detail and quality standards.
            """,
            agent=self.agents['financial_processor'],
            expected_output="Processed invoice data with categorization and compliance validation"
        )
        
        # Task 2: Google Sheets Integration and Archive
        sheets_integration_task = Task(
            description="""
            Integrate processed financial data into HaruPlate's financial tracking system:
            
            1. Update the main financial tracking spreadsheet
            2. Create separate entries for invoice summaries and line items
            3. Update vendor payment tracking
            4. Generate expense category summaries
            5. Archive original PDF invoices to Google Drive with proper naming
            6. Create audit trail for compliance purposes
            
            Ensure all data supports HaruPlate's financial transparency and family business values.
            Use proper file naming: {date}_{vendor}_{invoice_number}_{amount}
            """,
            agent=self.agents['financial_processor'],
            expected_output="Financial data integrated into tracking systems with proper archival",
            context=[invoice_processing_task]
        )
        
        # Task 3: Financial Insights and Reporting
        financial_analysis_task = Task(
            description="""
            Generate insights from the processed financial data:
            
            1. Identify spending patterns and trends
            2. Flag any unusual expenses or vendor changes
            3. Calculate monthly/quarterly expense summaries
            4. Highlight opportunities for cost optimization
            5. Check budget adherence for key categories
            6. Prepare summary for management review
            
            Focus on insights that support HaruPlate's mission and sustainable growth.
            """,
            agent=self.agents['data_analyst'],
            expected_output="Financial insights report with actionable recommendations",
            context=[sheets_integration_task]
        )
        
        # Execute financial processing crew
        financial_crew = Crew(
            agents=[
                self.agents['financial_processor'],
                self.agents['data_analyst']
            ],
            tasks=[
                invoice_processing_task,
                sheets_integration_task,
                financial_analysis_task
            ],
            verbose=True,
            process="sequential"
        )
        
        result = financial_crew.kickoff()
        
        return {
            "workflow_type": "financial_processing",
            "status": "completed",
            "deliverables": {
                "invoices_processed": "Data extracted and categorized",
                "sheets_updated": "Financial tracking systems current",
                "documents_archived": "Organized in Google Drive",
                "insights_generated": "Financial analysis complete"
            },
            "next_steps": [
                "Review financial insights with leadership",
                "Process approved payments",
                "Update budget forecasts",
                "Schedule vendor reviews if needed"
            ],
            "human_approval_required": True,
            "approval_items": [
                "Large expense approvals (>$1000)",
                "New vendor additions",
                "Budget variance explanations"
            ]
        }
    
    def _document_workflow(self, request: str, brand_context: Dict[str, Any]) -> Dict[str, Any]:
        """Organizes and manages HaruPlate's document archives."""
        
        # Task 1: Document Scanning and Classification
        document_scanning_task = Task(
            description=f"""
            Scan and organize HaruPlate's digital documents based on: "{request}"
            
            Process all document types:
            1. Regulatory compliance documents (certifications, approvals)
            2. Product development files (research, formulations, testing)
            3. Marketing materials and brand guidelines
            4. Supplier contracts and certifications
            5. Financial records and audit materials
            6. Meeting minutes and strategic planning documents
            
            Apply HaruPlate's document classification system focusing on:
            - Child nutrition and safety priorities
            - Malaysian market expansion materials
            - Natural product compliance requirements
            - Family business governance documents
            """,
            agent=self.agents['digital_archivist'],
            expected_output="Complete document inventory with classification and priority ranking"
        )
        
        # Task 2: File Organization and Renaming
        organization_task = Task(
            description="""
            Organize classified documents using HaruPlate's standards:
            
            1. Apply consistent naming convention: {date}_{category}_{description}_{version}
            2. Create logical folder structure by business function
            3. Ensure regulatory documents are easily accessible
            4. Organize product development files by product line
            5. Archive outdated versions while maintaining version history
            6. Create quick-access folders for frequently used documents
            
            Maintain organization that supports HaruPlate's family business efficiency.
            """,
            agent=self.agents['digital_archivist'],
            expected_output="Organized document structure with proper naming and accessibility",
            context=[document_scanning_task]
        )
        
        # Task 3: Knowledge Base Enhancement
        knowledge_base_task = Task(
            description="""
            Enhance HaruPlate's institutional knowledge system:
            
            1. Create searchable document summaries
            2. Tag documents with relevant keywords for easy discovery
            3. Identify knowledge gaps and missing documentation
            4. Create document relationship mappings
            5. Establish review schedules for time-sensitive documents
            6. Generate knowledge base usage reports
            
            Ensure our document system supports quick, informed decision-making.
            """,
            agent=self.agents['digital_archivist'],
            expected_output="Enhanced knowledge base with search capabilities and gap analysis",
            context=[organization_task]
        )
        
        # Execute document management crew
        document_crew = Crew(
            agents=[self.agents['digital_archivist']],
            tasks=[
                document_scanning_task,
                organization_task,
                knowledge_base_task
            ],
            verbose=True,
            process="sequential"
        )
        
        result = document_crew.kickoff()
        
        return {
            "workflow_type": "document_management",
            "status": "completed",
            "deliverables": {
                "documents_classified": "Complete inventory with categories",
                "files_organized": "Proper structure and naming applied",
                "knowledge_base": "Enhanced searchability and access",
                "compliance_ready": "Regulatory documents easily accessible"
            },
            "next_steps": [
                "Train team on new document organization",
                "Implement regular document review cycles",
                "Address identified knowledge gaps",
                "Set up automated backup systems"
            ]
        }
    
    def _meeting_workflow(self, request: str, brand_context: Dict[str, Any]) -> Dict[str, Any]:
        """Prepares comprehensive meeting briefings and research."""
        
        # Task 1: Meeting Context Research
        research_task = Task(
            description=f"""
            Research and prepare for upcoming meetings based on: "{request}"
            
            Comprehensive meeting preparation:
            1. Research all meeting participants and their backgrounds
            2. Review agenda items and gather relevant context
            3. Identify recent industry developments affecting HaruPlate
            4. Search internal documents for related discussions and decisions
            5. Gather Malaysian market intelligence if relevant
            6. Review regulatory updates affecting natural products
            
            Focus on information that supports HaruPlate's mission and strategic goals.
            """,
            agent=self.agents['meeting_assistant'],
            expected_output="Complete meeting context research with participant backgrounds and relevant intelligence"
        )
        
        # Task 2: Internal Knowledge Synthesis  
        knowledge_synthesis_task = Task(
            description="""
            Synthesize HaruPlate's internal knowledge relevant to the meeting:
            
            1. Review previous meeting minutes on related topics
            2. Gather relevant product development updates
            3. Collect financial performance data if applicable
            4. Identify past decisions that inform current discussions
            5. Highlight successful strategies and lessons learned
            6. Prepare talking points aligned with HaruPlate values
            
            Create a coherent knowledge foundation for strategic discussions.
            """,
            agent=self.agents['meeting_assistant'],
            expected_output="Synthesized internal knowledge with strategic talking points",
            context=[research_task]
        )
        
        # Task 3: Strategic Briefing Preparation
        briefing_task = Task(
            description="""
            Create comprehensive strategic briefing for HaruPlate leadership:
            
            1. Executive summary of key points and recommendations
            2. Background context and relevant history
            3. Strategic options and their implications
            4. Risk assessment and mitigation strategies
            5. Success metrics and follow-up actions
            6. Questions to drive productive discussion
            
            Ensure briefing supports HaruPlate's family-oriented decision-making style.
            Present complex information in clear, actionable format.
            """,
            agent=self.agents['meeting_assistant'],
            expected_output="Executive briefing document with strategic recommendations and discussion framework",
            context=[knowledge_synthesis_task]
        )
        
        # Execute meeting preparation crew
        meeting_crew = Crew(
            agents=[self.agents['meeting_assistant']],
            tasks=[
                research_task,
                knowledge_synthesis_task,
                briefing_task
            ],
            verbose=True,
            process="sequential"
        )
        
        result = meeting_crew.kickoff()
        
        return {
            "workflow_type": "meeting_preparation",
            "status": "completed",
            "deliverables": {
                "external_research": "Market and participant intelligence gathered",
                "internal_knowledge": "Relevant company information synthesized",
                "strategic_briefing": "Executive summary with recommendations",
                "discussion_framework": "Questions and talking points prepared"
            },
            "next_steps": [
                "Distribute briefing to meeting participants",
                "Schedule pre-meeting alignment if needed",
                "Prepare meeting materials and logistics",
                "Set up follow-up tracking system"
            ]
        }
    
    def _data_analysis_workflow(self, request: str, brand_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes business data and generates insights."""
        
        # Task 1: Data Query and Extraction
        data_extraction_task = Task(
            description=f"""
            Process this data analysis request: "{request}"
            
            Execute natural language data queries:
            1. Interpret the business question in context of HaruPlate's priorities
            2. Identify relevant data sources (sales, customer, operational)
            3. Extract and validate data accuracy
            4. Apply appropriate analytical methods
            5. Consider Malaysian market specifics if relevant
            6. Ensure data privacy and confidentiality
            
            Focus on insights that support HaruPlate's mission and family values.
            """,
            agent=self.agents['data_analyst'],
            expected_output="Extracted and validated data ready for analysis"
        )
        
        # Task 2: Analysis and Insight Generation
        analysis_task = Task(
            description="""
            Generate actionable insights from the extracted data:
            
            1. Apply statistical analysis appropriate to the question
            2. Identify trends, patterns, and anomalies
            3. Compare against industry benchmarks where relevant
            4. Consider seasonal and market factors
            5. Assess implications for HaruPlate's strategic goals
            6. Generate visualizations to support understanding
            
            Translate complex analysis into clear, business-relevant insights.
            """,
            agent=self.agents['data_analyst'],
            expected_output="Comprehensive analysis with insights and visualizations",
            context=[data_extraction_task]
        )
        
        # Task 3: Strategic Recommendations
        recommendations_task = Task(
            description="""
            Develop strategic recommendations based on the analysis:
            
            1. Identify specific actions HaruPlate should consider
            2. Prioritize recommendations by impact and feasibility
            3. Consider resource requirements and timeline
            4. Address potential risks and mitigation strategies
            5. Align recommendations with company values and mission
            6. Prepare implementation roadmap
            
            Ensure recommendations are practical for a family business environment.
            """,
            agent=self.agents['data_analyst'],
            expected_output="Strategic recommendations with implementation roadmap",
            context=[analysis_task]
        )
        
        # Execute data analysis crew
        analysis_crew = Crew(
            agents=[self.agents['data_analyst']],
            tasks=[
                data_extraction_task,
                analysis_task,
                recommendations_task
            ],
            verbose=True,
            process="sequential"
        )
        
        result = analysis_crew.kickoff()
        
        return {
            "workflow_type": "data_analysis",
            "status": "completed",
            "deliverables": {
                "data_analysis": "Comprehensive analytical insights",
                "visualizations": "Charts and graphs for understanding",
                "strategic_recommendations": "Prioritized action items",
                "implementation_plan": "Roadmap with timelines"
            },
            "next_steps": [
                "Present findings to leadership team",
                "Validate recommendations with stakeholders",
                "Begin implementation of approved actions",
                "Set up monitoring for recommended metrics"
            ]
        }
    
    def _general_admin_workflow(self, request: str, brand_context: Dict[str, Any]) -> Dict[str, Any]:
        """Handles general administrative requests."""
        
        general_task = Task(
            description=f"""
            Address this administrative request: "{request}"
            
            Provide comprehensive administrative support while maintaining
            HaruPlate's efficient, family-oriented approach to business operations.
            
            Consider how this request supports our core values:
            {', '.join(brand_context.get('values', []))}
            
            Deliver solutions that strengthen our operational excellence.
            """,
            agent=self.agents['digital_archivist'],  # Most versatile for general admin
            expected_output="Administrative solution aligned with HaruPlate's operational standards"
        )
        
        general_crew = Crew(
            agents=[self.agents['digital_archivist']],
            tasks=[general_task],
            verbose=True
        )
        
        result = general_crew.kickoff()
        
        return {
            "workflow_type": "general_administration",
            "status": "completed",
            "deliverables": {
                "administrative_solution": "Customized support provided"
            }
        }
    
    def get_available_agents(self) -> List[str]:
        """Returns list of available administrative agents."""
        return list(self.agents.keys())
    
    def get_crew_capabilities(self) -> Dict[str, List[str]]:
        """Returns the capabilities of each admin crew member."""
        return {
            "financial_processor": [
                "Invoice processing and data extraction",
                "Expense categorization and tracking",
                "Google Sheets integration",
                "Compliance validation",
                "Vendor management"
            ],
            "digital_archivist": [
                "Document organization and archiving",
                "File naming and categorization",
                "Knowledge base management",
                "OCR processing",
                "Compliance document management"
            ],
            "meeting_assistant": [
                "Meeting research and preparation",
                "Strategic briefing creation",
                "Calendar integration",
                "Participant background research",
                "Internal knowledge synthesis"
            ],
            "data_analyst": [
                "Natural language data queries",
                "Sales and business analysis",
                "Report generation",
                "Strategic recommendations",
                "Data visualization"
            ]
        }


# Example usage
if __name__ == "__main__":
    admin_crew = AdminCrew()
    
    # Example: Invoice processing request
    sample_request = "Process this month's invoices from Malaysian suppliers and update our financial tracking"
    
    brand_context = {
        "values": ["family-first approach", "financial transparency", "operational excellence"]
    }
    
    result = admin_crew.execute_workflow(sample_request, brand_context)
    print("📊 Admin Crew Result:", result)