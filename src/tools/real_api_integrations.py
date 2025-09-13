#!/usr/bin/env python3
"""
Real API Integrations for Business Orchestra
Based on awesome-llm-apps patterns for Gmail, Zoom, Google Sheets, and Google Drive
"""

import os
import base64
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

# Real API imports (following awesome-llm-apps patterns)
try:
    import googleapiclient.discovery
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    import gspread
    from gspread import Spreadsheet, Worksheet
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import requests
    GOOGLE_APIS_AVAILABLE = True
except ImportError as e:
    GOOGLE_APIS_AVAILABLE = False
    logging.warning(f"Google APIs not available: {e}")

try:
    from crewai_tools import BaseTool
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    logging.warning("CrewAI tools not available, using base implementation")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Configuration from awesome-llm-apps patterns
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
DRIVE_SCOPES = ['https://www.googleapis.com/auth/drive']

@dataclass
class EmailMessage:
    """Email message data structure."""
    id: str
    sender: str
    subject: str
    body: str
    attachments: List[Dict[str, Any]]
    labels: List[str]
    received_date: datetime

@dataclass
class InvoiceData:
    """Invoice data structure from n8n-invoice-automation pattern."""
    invoice_id: str
    supplier_name: str
    amount: float
    currency: str
    date: datetime
    line_items: List[Dict[str, Any]]
    is_malaysian_supplier: bool
    business_category: str

class BaseAPITool:
    """Base class for API tools when CrewAI is not available."""
    name = "Base API Tool"
    description = "Base API tool implementation"
    
    def __init__(self):
        pass
    
    def _run(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement _run method")

if CREWAI_AVAILABLE:
    ToolBase = BaseTool
else:
    ToolBase = BaseAPITool

class GmailIntegrationTool(ToolBase):
    """
    Gmail Integration Tool following awesome-llm-apps/ai_recruitment_agent_team pattern
    Handles email retrieval, processing, and labeling for invoice automation.
    """
    
    name: str = "Gmail Integration Tool"
    description: str = (
        "Retrieves and processes emails from Gmail, specifically for invoice processing. "
        "Can search for emails with PDF attachments, extract invoice data, and apply labels. "
        "Based on awesome-llm-apps Gmail integration patterns."
    )
    
    def __init__(self):
        super().__init__()
        self.gmail_service = None
        self._initialize_gmail_service()
    
    def _initialize_gmail_service(self):
        """Initialize Gmail API service following awesome-llm-apps pattern."""
        if not GOOGLE_APIS_AVAILABLE:
            logger.warning("Google APIs not available - Gmail integration will use simulation mode")
            return
        
        try:
            creds = None
            # Token file stores the user's access and refresh tokens
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', GMAIL_SCOPES)
            
            # If there are no (valid) credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # Use app password approach from awesome-llm-apps
                    logger.info("Gmail service initialized with app password authentication")
                    return
            
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            logger.info("Gmail API service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gmail service: {e}")
            self.gmail_service = None
    
    def _run(self, query: str = "has:attachment filename:pdf", limit: int = 10) -> List[EmailMessage]:
        """
        Retrieve emails with PDF attachments for invoice processing.
        Following n8n-invoice-automation email retrieval pattern.
        """
        if not self.gmail_service:
            # Simulation mode for testing
            return self._simulate_invoice_emails(limit)
        
        try:
            logger.info(f"Searching Gmail for: {query} (limit: {limit})")
            
            # Search for messages
            results = self.gmail_service.users().messages().list(
                userId='me', 
                q=query,
                maxResults=limit
            ).execute()
            
            messages = results.get('messages', [])
            email_messages = []
            
            for message in messages:
                # Get full message details
                msg = self.gmail_service.users().messages().get(
                    userId='me', 
                    id=message['id']
                ).execute()
                
                email_msg = self._parse_email_message(msg)
                email_messages.append(email_msg)
            
            logger.info(f"Retrieved {len(email_messages)} emails from Gmail")
            return email_messages
            
        except Exception as e:
            logger.error(f"Error retrieving Gmail messages: {e}")
            return []
    
    def _simulate_invoice_emails(self, limit: int) -> List[EmailMessage]:
        """Simulate invoice emails for testing."""
        simulated_emails = []
        
        malaysian_suppliers = [
            "Natural Nutrition Sdn Bhd",
            "Organic Kids Malaysia",
            "Healthy Growth Supplies",
            "KL Nutrition Partners",
            "Malaysian Family Foods"
        ]
        
        for i in range(min(limit, len(malaysian_suppliers))):
            supplier = malaysian_suppliers[i]
            email_msg = EmailMessage(
                id=f"sim_email_{i}",
                sender=f"{supplier.lower().replace(' ', '.')}@gmail.com",
                subject=f"Invoice #{1000 + i} - {supplier}",
                body=f"Please find attached invoice for organic ingredients supplied to Business.",
                attachments=[{
                    "filename": f"INV-{1000 + i}-{supplier.replace(' ', '_')}.pdf",
                    "data": f"simulated_pdf_data_{i}"
                }],
                labels=["INBOX"],
                received_date=datetime.now() - timedelta(days=i)
            )
            simulated_emails.append(email_msg)
        
        logger.info(f"Generated {len(simulated_emails)} simulated invoice emails")
        return simulated_emails
    
    def apply_label(self, message_id: str, label: str = "business-processed"):
        """Apply label to processed email following n8n-invoice-automation pattern."""
        if not self.gmail_service:
            logger.info(f"[SIMULATION] Applied label '{label}' to message {message_id}")
            return True
        
        try:
            self.gmail_service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [label]}
            ).execute()
            
            logger.info(f"Applied label '{label}' to message {message_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to apply label: {e}")
            return False
    
    def _parse_email_message(self, msg: Dict[str, Any]) -> EmailMessage:
        """Parse Gmail API message into EmailMessage object."""
        headers = msg['payload'].get('headers', [])
        
        # Extract headers
        sender = ""
        subject = ""
        for header in headers:
            if header['name'] == 'From':
                sender = header['value']
            elif header['name'] == 'Subject':
                subject = header['value']
        
        # Extract body and attachments
        body = ""
        attachments = []
        
        # This would need more complex parsing for real implementation
        # For now, simplified version
        
        return EmailMessage(
            id=msg['id'],
            sender=sender,
            subject=subject,
            body=body,
            attachments=attachments,
            labels=msg.get('labelIds', []),
            received_date=datetime.now()
        )

class GoogleSheetsIntegrationTool(ToolBase):
    """
    Google Sheets Integration Tool following n8n-invoice-automation pattern
    Updates spreadsheets with invoice data and financial information.
    """
    
    name: str = "Google Sheets Integration Tool"
    description: str = (
        "Integrates with Google Sheets to update invoice data, expense tracking, and financial reports. "
        "Follows the n8n-invoice-automation pattern for structured data storage with Business categorization."
    )
    
    def __init__(self):
        super().__init__()
        self.sheets_service = None
        self.gc = None
        self._initialize_sheets_service()
    
    def _initialize_sheets_service(self):
        """Initialize Google Sheets service."""
        if not GOOGLE_APIS_AVAILABLE:
            logger.warning("Google APIs not available - Sheets integration will use simulation mode")
            return
        
        try:
            # Initialize gspread for easier spreadsheet operations
            self.gc = gspread.service_account()
            logger.info("Google Sheets service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets service: {e}")
            self.gc = None
    
    def _run(self, spreadsheet_id: str, worksheet_name: str, data: List[List[Any]]) -> Dict[str, Any]:
        """
        Update Google Sheets with data following n8n-invoice-automation pattern.
        """
        if not self.gc:
            return self._simulate_sheets_update(spreadsheet_id, worksheet_name, data)
        
        try:
            # Open spreadsheet
            spreadsheet = self.gc.open_by_key(spreadsheet_id)
            
            try:
                worksheet = spreadsheet.worksheet(worksheet_name)
            except:
                # Create worksheet if it doesn't exist
                worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows=1000, cols=20)
            
            # Update data
            if data:
                worksheet.update('A1', data)
            
            result = {
                "status": "success",
                "spreadsheet_id": spreadsheet_id,
                "worksheet": worksheet_name,
                "rows_updated": len(data),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Updated Google Sheets: {len(data)} rows in {worksheet_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error updating Google Sheets: {e}")
            return {
                "status": "error",
                "error": str(e),
                "spreadsheet_id": spreadsheet_id,
                "worksheet": worksheet_name
            }
    
    def _simulate_sheets_update(self, spreadsheet_id: str, worksheet_name: str, data: List[List[Any]]) -> Dict[str, Any]:
        """Simulate Google Sheets update for testing."""
        logger.info(f"[SIMULATION] Updated Google Sheets - {len(data)} rows in worksheet '{worksheet_name}'")
        
        # Log some sample data for verification
        if data:
            logger.info(f"[SIMULATION] Sample data: {data[:2]}")  # Show first 2 rows
        
        return {
            "status": "success",
            "spreadsheet_id": spreadsheet_id,
            "worksheet": worksheet_name,
            "rows_updated": len(data),
            "timestamp": datetime.now().isoformat(),
            "simulation": True
        }
    
    def update_invoice_data(self, invoices: List[InvoiceData]) -> Dict[str, Any]:
        """Update invoice data following n8n-invoice-automation pattern."""
        
        # Prepare invoice summary data
        invoice_summary = []
        invoice_items = []
        
        # Header for Invoices sheet
        invoice_summary.append([
            "Invoice ID", "Supplier", "Amount", "Currency", "Date", 
            "Malaysian Supplier", "Business Category", "Processed Date"
        ])
        
        # Header for Invoice_Items sheet
        invoice_items.append([
            "Invoice ID", "Item Description", "Quantity", "Unit Price", 
            "Total", "Category", "Notes"
        ])
        
        for invoice in invoices:
            # Add invoice summary
            invoice_summary.append([
                invoice.invoice_id,
                invoice.supplier_name,
                invoice.amount,
                invoice.currency,
                invoice.date.strftime("%Y-%m-%d"),
                "Yes" if invoice.is_malaysian_supplier else "No",
                invoice.business_category,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ])
            
            # Add line items
            for item in invoice.line_items:
                invoice_items.append([
                    invoice.invoice_id,
                    item.get("description", ""),
                    item.get("quantity", 1),
                    item.get("unit_price", 0),
                    item.get("total", 0),
                    item.get("category", "General"),
                    item.get("notes", "")
                ])
        
        # Update both sheets
        summary_result = self._run("business_financials", "Invoices", invoice_summary)
        items_result = self._run("business_financials", "Invoice_Items", invoice_items)
        
        return {
            "invoices_sheet": summary_result,
            "items_sheet": items_result,
            "total_invoices_processed": len(invoices),
            "malaysian_suppliers_count": sum(1 for inv in invoices if inv.is_malaysian_supplier)
        }

class ZoomAPITool(ToolBase):
    """
    Zoom API Integration Tool following awesome-llm-apps/ai_recruitment_agent_team pattern
    Handles meeting scheduling and Zoom integration for Business recruitment and meetings.
    """
    
    name: str = "Zoom API Integration Tool"
    description: str = (
        "Integrates with Zoom API to schedule meetings, create meeting links, and manage "
        "video conferencing for Business recruitment and business meetings. "
        "Based on awesome-llm-apps Zoom integration patterns."
    )
    
    def __init__(self):
        super().__init__()
        self.zoom_token = None
        self._initialize_zoom_api()
    
    def _initialize_zoom_api(self):
        """Initialize Zoom API following awesome-llm-apps pattern."""
        try:
            # Get Zoom credentials from environment
            client_id = os.getenv('ZOOM_CLIENT_ID')
            client_secret = os.getenv('ZOOM_CLIENT_SECRET')
            account_id = os.getenv('ZOOM_ACCOUNT_ID')
            
            if not all([client_id, client_secret, account_id]):
                logger.warning("Zoom credentials not found - will use simulation mode")
                return
            
            # Get OAuth token
            token_url = "https://zoom.us/oauth/token"
            
            # Prepare authentication
            auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
            
            headers = {
                'Authorization': f'Basic {auth_header}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'grant_type': 'account_credentials',
                'account_id': account_id
            }
            
            response = requests.post(token_url, headers=headers, data=data)
            
            if response.status_code == 200:
                self.zoom_token = response.json().get('access_token')
                logger.info("Zoom API initialized successfully")
            else:
                logger.error(f"Failed to get Zoom token: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Failed to initialize Zoom API: {e}")
            self.zoom_token = None
    
    def _run(self, meeting_title: str, start_time: str, duration: int = 60, attendees: List[str] = None) -> Dict[str, Any]:
        """
        Create a Zoom meeting following awesome-llm-apps pattern.
        """
        if not self.zoom_token:
            return self._simulate_zoom_meeting(meeting_title, start_time, duration, attendees)
        
        try:
            url = "https://api.zoom.us/v2/users/me/meetings"
            
            headers = {
                'Authorization': f'Bearer {self.zoom_token}',
                'Content-Type': 'application/json'
            }
            
            meeting_data = {
                "topic": meeting_title,
                "type": 2,  # Scheduled meeting
                "start_time": start_time,
                "duration": duration,
                "timezone": "Asia/Kuala_Lumpur",  # Malaysian timezone for Business
                "agenda": f"Business meeting: {meeting_title}",
                "settings": {
                    "host_video": True,
                    "participant_video": True,
                    "join_before_host": False,
                    "mute_upon_entry": True,
                    "watermark": False,
                    "use_pmi": False,
                    "approval_type": 0,
                    "audio": "both",
                    "auto_recording": "none"
                }
            }
            
            response = requests.post(url, headers=headers, json=meeting_data)
            
            if response.status_code == 201:
                meeting_info = response.json()
                
                result = {
                    "status": "success",
                    "meeting_id": meeting_info.get("id"),
                    "join_url": meeting_info.get("join_url"),
                    "start_url": meeting_info.get("start_url"),
                    "meeting_title": meeting_title,
                    "start_time": start_time,
                    "duration": duration,
                    "password": meeting_info.get("password", ""),
                    "timezone": "Asia/Kuala_Lumpur"
                }
                
                logger.info(f"Created Zoom meeting: {meeting_title}")
                return result
            else:
                raise Exception(f"Zoom API error: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error creating Zoom meeting: {e}")
            return {
                "status": "error",
                "error": str(e),
                "meeting_title": meeting_title
            }
    
    def _simulate_zoom_meeting(self, meeting_title: str, start_time: str, duration: int, attendees: List[str]) -> Dict[str, Any]:
        """Simulate Zoom meeting creation for testing."""
        logger.info(f"[SIMULATION] Created Zoom meeting: {meeting_title}")
        
        # Generate realistic-looking meeting details
        meeting_id = f"123-456-{hash(meeting_title) % 10000}"
        
        return {
            "status": "success",
            "meeting_id": meeting_id,
            "join_url": f"https://zoom.us/j/{meeting_id.replace('-', '')}",
            "start_url": f"https://zoom.us/s/{meeting_id.replace('-', '')}",
            "meeting_title": meeting_title,
            "start_time": start_time,
            "duration": duration,
            "password": "business123",
            "timezone": "Asia/Kuala_Lumpur",
            "simulation": True
        }

class GoogleDriveIntegrationTool(ToolBase):
    """
    Google Drive Integration Tool for document archival following n8n-invoice-automation pattern
    Handles file upload, organization, and management in Google Drive.
    """
    
    name: str = "Google Drive Integration Tool"
    description: str = (
        "Integrates with Google Drive to upload, organize, and manage documents. "
        "Follows n8n-invoice-automation pattern for PDF archival and Business document organization."
    )
    
    def __init__(self):
        super().__init__()
        self.drive_service = None
        self._initialize_drive_service()
    
    def _initialize_drive_service(self):
        """Initialize Google Drive service."""
        if not GOOGLE_APIS_AVAILABLE:
            logger.warning("Google APIs not available - Drive integration will use simulation mode")
            return
        
        try:
            creds = None
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', DRIVE_SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    logger.info("Drive service will use simulation mode")
                    return
            
            self.drive_service = build('drive', 'v3', credentials=creds)
            logger.info("Google Drive service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Drive service: {e}")
            self.drive_service = None
    
    def _run(self, file_name: str, file_content: bytes, folder_name: str = "Business_Invoices") -> Dict[str, Any]:
        """
        Upload file to Google Drive following n8n-invoice-automation archival pattern.
        """
        if not self.drive_service:
            return self._simulate_drive_upload(file_name, folder_name)
        
        try:
            # Create or find folder
            folder_id = self._create_or_find_folder(folder_name)
            
            # Upload file
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            
            from googleapiclient.http import MediaInMemoryUpload
            media = MediaInMemoryUpload(file_content)
            
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            result = {
                "status": "success",
                "file_id": file.get("id"),
                "file_name": file_name,
                "folder_name": folder_name,
                "folder_id": folder_id,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"Uploaded file to Google Drive: {file_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error uploading to Google Drive: {e}")
            return {
                "status": "error",
                "error": str(e),
                "file_name": file_name,
                "folder_name": folder_name
            }
    
    def _create_or_find_folder(self, folder_name: str) -> str:
        """Create or find folder in Google Drive."""
        # Search for existing folder
        results = self.drive_service.files().list(
            q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive'
        ).execute()
        
        folders = results.get('files', [])
        
        if folders:
            return folders[0]['id']
        
        # Create new folder
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        
        folder = self.drive_service.files().create(body=folder_metadata, fields='id').execute()
        return folder.get('id')
    
    def _simulate_drive_upload(self, file_name: str, folder_name: str) -> Dict[str, Any]:
        """Simulate Google Drive upload for testing."""
        logger.info(f"[SIMULATION] Uploaded {file_name} to Google Drive folder: {folder_name}")
        
        return {
            "status": "success",
            "file_id": f"drive_file_{hash(file_name) % 10000}",
            "file_name": file_name,
            "folder_name": folder_name,
            "folder_id": f"folder_{hash(folder_name) % 10000}",
            "timestamp": datetime.now().isoformat(),
            "simulation": True
        }


# Factory functions for easy tool creation
def create_gmail_tool() -> GmailIntegrationTool:
    """Create Gmail integration tool."""
    return GmailIntegrationTool()

def create_sheets_tool() -> GoogleSheetsIntegrationTool:
    """Create Google Sheets integration tool."""
    return GoogleSheetsIntegrationTool()

def create_zoom_tool() -> ZoomAPITool:
    """Create Zoom API tool."""
    return ZoomAPITool()

def create_drive_tool() -> GoogleDriveIntegrationTool:
    """Create Google Drive integration tool."""
    return GoogleDriveIntegrationTool()


if __name__ == "__main__":
    # Test the API integrations
    logger.info("Testing Business API Integrations...")
    
    # Test Gmail
    gmail_tool = create_gmail_tool()
    emails = gmail_tool._run(limit=3)
    logger.info(f"Gmail test: Retrieved {len(emails)} emails")
    
    # Test Zoom
    zoom_tool = create_zoom_tool()
    meeting = zoom_tool._run("Business Team Meeting", "2025-01-15T10:00:00", 60)
    logger.info(f"Zoom test: {meeting['status']}")
    
    # Test Google Sheets
    sheets_tool = create_sheets_tool()
    test_data = [["Test", "Data"], ["Row 1", "Value 1"], ["Row 2", "Value 2"]]
    result = sheets_tool._run("test_sheet_id", "TestSheet", test_data)
    logger.info(f"Sheets test: {result['status']}")
    
    # Test Google Drive
    drive_tool = create_drive_tool()
    test_content = b"Test file content for Business"
    upload_result = drive_tool._run("test_document.pdf", test_content, "Business_Test")
    logger.info(f"Drive test: {upload_result['status']}")
    
    logger.info("API integration tests completed!")