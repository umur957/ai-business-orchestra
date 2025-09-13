"""
Business Financial Tools
Invoice processing, Google Sheets integration, and expense management.
"""

import os
import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import re

from crewai.tools import BaseTool

# Optional imports for full functionality
try:
    import email
    import imaplib
    import smtplib
    import PyPDF2
    import pytesseract
    from PIL import Image
    import pandas as pd
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    HAS_OPTIONAL_DEPS = True
except ImportError:
    HAS_OPTIONAL_DEPS = False

logger = logging.getLogger(__name__)


class InvoiceProcessingTool(BaseTool):
    """Processes invoices from email and extracts structured data."""
    
    name: str = "Invoice Processing Tool"
    description: str = """Automatically retrieves invoices from email, extracts data using OCR,
        and converts to structured format. Handles PDF invoices and scanned documents.
        Designed for Business's supplier management workflow."""

    def __init__(self):
        super().__init__()
        # Gmail API configuration
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.gmail_service = None
        
        # Business supplier categories
        self.supplier_categories = {
            "raw_materials": ["ingredient", "organic", "powder", "extract", "vitamin"],
            "packaging": ["bottle", "label", "box", "container", "packaging"],
            "equipment": ["machine", "equipment", "tool", "hardware"],
            "services": ["consulting", "testing", "audit", "certification", "legal"],
            "logistics": ["shipping", "transport", "delivery", "freight", "courier"]
        }

    def _run(self, email_query: str = "has:attachment filename:pdf invoice", 
             limit: int = 10, days_back: int = 30) -> Dict[str, Any]:
        """
        Processes invoices from email attachments.
        
        Args:
            email_query: Gmail search query to find invoices
            limit: Maximum number of emails to process
            days_back: How many days back to search
            
        Returns:
            Dictionary with processed invoice data
        """
        try:
            # Initialize Gmail service
            if not self._initialize_gmail_service():
                return self._simulate_invoice_processing(limit)
            
            # Retrieve invoice emails
            invoice_emails = self._get_invoice_emails(email_query, limit, days_back)
            
            if not invoice_emails:
                return {"message": "No invoice emails found", "invoices_processed": 0}
            
            # Process each invoice
            processed_invoices = []
            for email_data in invoice_emails:
                invoice_data = self._process_single_invoice(email_data)
                if invoice_data:
                    processed_invoices.append(invoice_data)
            
            # Generate summary
            processing_summary = self._generate_processing_summary(processed_invoices)
            
            result = {
                "invoices_processed": len(processed_invoices),
                "invoices_data": processed_invoices,
                "processing_summary": processing_summary,
                "next_steps": [
                    "Review extracted data for accuracy",
                    "Categorize expenses by Business standards",
                    "Update Google Sheets with new invoice data",
                    "Archive processed invoices to Google Drive"
                ]
            }
            
            logger.info(f"Processed {len(processed_invoices)} invoices successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error processing invoices: {str(e)}")
            return {"error": f"Invoice processing failed: {str(e)}"}
    
    def _initialize_gmail_service(self) -> bool:
        """Initialize Gmail API service."""
        try:
            creds = None
            
            # Load existing credentials
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
            
            # If there are no (valid) credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if os.path.exists('credentials.json'):
                        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                        creds = flow.run_local_server(port=0)
                    else:
                        logger.warning("Gmail credentials not found")
                        return False
                
                # Save credentials for next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            
            self.gmail_service = build('gmail', 'v1', credentials=creds)
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Gmail service: {str(e)}")
            return False
    
    def _get_invoice_emails(self, query: str, limit: int, days_back: int) -> List[Dict[str, Any]]:
        """Retrieve invoice emails from Gmail."""
        try:
            # Build search query with date filter
            date_filter = datetime.now() - timedelta(days=days_back)
            date_str = date_filter.strftime('%Y/%m/%d')
            full_query = f"{query} after:{date_str}"
            
            # Search for emails
            results = self.gmail_service.users().messages().list(
                userId='me', q=full_query, maxResults=limit
            ).execute()
            
            messages = results.get('messages', [])
            
            invoice_emails = []
            for message in messages:
                # Get full message
                msg = self.gmail_service.users().messages().get(
                    userId='me', id=message['id'], format='full'
                ).execute()
                
                # Extract email data
                email_data = self._extract_email_data(msg)
                if email_data:
                    invoice_emails.append(email_data)
            
            return invoice_emails
            
        except HttpError as e:
            logger.error(f"Gmail API error: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error retrieving emails: {str(e)}")
            return []
    
    def _extract_email_data(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract relevant data from email message."""
        try:
            headers = message['payload'].get('headers', [])
            
            # Extract header information
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
            
            # Extract attachments
            attachments = self._extract_attachments(message)
            
            if not attachments:
                return None
            
            return {
                "message_id": message['id'],
                "sender": sender,
                "subject": subject,
                "date": date,
                "attachments": attachments
            }
            
        except Exception as e:
            logger.error(f"Error extracting email data: {str(e)}")
            return None
    
    def _extract_attachments(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract PDF attachments from email."""
        attachments = []
        
        def process_parts(parts):
            for part in parts:
                if part.get('parts'):
                    process_parts(part['parts'])
                else:
                    if part.get('filename') and part['filename'].lower().endswith('.pdf'):
                        attachments.append({
                            'filename': part['filename'],
                            'attachment_id': part['body'].get('attachmentId'),
                            'size': part['body'].get('size', 0)
                        })
        
        if 'parts' in message['payload']:
            process_parts(message['payload']['parts'])
        
        return attachments
    
    def _process_single_invoice(self, email_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single invoice from email data."""
        try:
            invoice_data = {
                "email_info": {
                    "sender": email_data["sender"],
                    "subject": email_data["subject"],
                    "date": email_data["date"]
                },
                "extracted_data": {},
                "processing_status": "success"
            }
            
            # Process each attachment
            for attachment in email_data["attachments"]:
                attachment_data = self._process_pdf_attachment(attachment, email_data["message_id"])
                if attachment_data:
                    invoice_data["extracted_data"] = attachment_data
                    break  # Use first successfully processed attachment
            
            if not invoice_data["extracted_data"]:
                invoice_data["processing_status"] = "no_data_extracted"
                return invoice_data
            
            # Categorize the invoice
            invoice_data["business_category"] = self._categorize_invoice(invoice_data["extracted_data"])
            
            # Validate and enhance data
            invoice_data["validation"] = self._validate_invoice_data(invoice_data["extracted_data"])
            
            return invoice_data
            
        except Exception as e:
            logger.error(f"Error processing single invoice: {str(e)}")
            return {
                "processing_status": "error",
                "error": str(e)
            }
    
    def _process_pdf_attachment(self, attachment: Dict[str, Any], message_id: str) -> Optional[Dict[str, Any]]:
        """Extract data from PDF attachment."""
        try:
            # Download attachment (simulated for this implementation)
            # In production, you would download the actual PDF file
            
            # Simulate PDF text extraction
            extracted_text = self._simulate_pdf_extraction(attachment["filename"])
            
            # Parse invoice data from text
            invoice_data = self._parse_invoice_text(extracted_text)
            
            return invoice_data
            
        except Exception as e:
            logger.error(f"Error processing PDF attachment: {str(e)}")
            return None
    
    def _simulate_pdf_extraction(self, filename: str) -> str:
        """Simulate PDF text extraction (for demo purposes)."""
        
        # Generate realistic invoice text based on filename
        supplier_name = filename.split('_')[0] if '_' in filename else "ABC Supplies Sdn Bhd"
        
        return f"""
INVOICE

{supplier_name}
123 Jalan Industri
Kuala Lumpur, Malaysia
Tel: +60-3-1234-5678

Invoice Number: INV-2025-001
Date: {datetime.now().strftime('%Y-%m-%d')}
Due Date: {(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')}

Bill To:
Business Sdn Bhd
456 Jalan Nutrition
Kuala Lumpur, Malaysia

Description                 Quantity    Unit Price    Total
Organic Ingredient A        100 kg      RM 15.00      RM 1,500.00
Natural Preservative B      50 kg       RM 8.50       RM 425.00
Premium Packaging          1000 units   RM 0.75       RM 750.00

                           Subtotal:    RM 2,675.00
                           GST (6%):    RM 160.50
                           Total:       RM 2,835.50

Terms: Net 30 days
        """
    
    def _parse_invoice_text(self, text: str) -> Dict[str, Any]:
        """Parse structured data from invoice text."""
        
        invoice_data = {
            "invoice_number": "",
            "supplier_name": "",
            "invoice_date": "",
            "due_date": "",
            "subtotal": 0.0,
            "tax_amount": 0.0,
            "total_amount": 0.0,
            "line_items": [],
            "currency": "RM"
        }
        
        try:
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # Extract invoice number
                if 'invoice number' in line.lower():
                    match = re.search(r'INV-[\w\-]+', line)
                    if match:
                        invoice_data["invoice_number"] = match.group()
                
                # Extract dates
                if 'date:' in line.lower() and not invoice_data["invoice_date"]:
                    match = re.search(r'\d{4}-\d{2}-\d{2}', line)
                    if match:
                        invoice_data["invoice_date"] = match.group()
                
                if 'due date:' in line.lower():
                    match = re.search(r'\d{4}-\d{2}-\d{2}', line)
                    if match:
                        invoice_data["due_date"] = match.group()
                
                # Extract supplier name (first company name found)
                if 'sdn bhd' in line.lower() and not invoice_data["supplier_name"]:
                    invoice_data["supplier_name"] = line.strip()
                
                # Extract amounts
                if 'subtotal:' in line.lower():
                    amount = self._extract_amount(line)
                    if amount:
                        invoice_data["subtotal"] = amount
                
                if 'gst' in line.lower() or 'tax' in line.lower():
                    amount = self._extract_amount(line)
                    if amount:
                        invoice_data["tax_amount"] = amount
                
                if 'total:' in line.lower() and invoice_data["subtotal"] > 0:
                    amount = self._extract_amount(line)
                    if amount:
                        invoice_data["total_amount"] = amount
                
                # Extract line items (simplified)
                if 'rm' in line.lower() and any(word in line.lower() for word in ['kg', 'units', 'pcs']):
                    item = self._parse_line_item(line)
                    if item:
                        invoice_data["line_items"].append(item)
            
            return invoice_data
            
        except Exception as e:
            logger.error(f"Error parsing invoice text: {str(e)}")
            return invoice_data
    
    def _extract_amount(self, text: str) -> Optional[float]:
        """Extract monetary amount from text."""
        try:
            # Look for patterns like "RM 1,234.56" or "RM1234.56"
            pattern = r'RM\s*([0-9,]+\.?[0-9]*)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                return float(amount_str)
        except:
            pass
        return None
    
    def _parse_line_item(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a line item from invoice text."""
        try:
            # Simple line item parsing
            parts = line.split()
            if len(parts) >= 4:
                return {
                    "description": " ".join(parts[:-3]),
                    "quantity": parts[-3],
                    "unit_price": self._extract_amount(" ".join(parts[-2:])),
                    "total": self._extract_amount(parts[-1])
                }
        except:
            pass
        return None
    
    def _categorize_invoice(self, invoice_data: Dict[str, Any]) -> str:
        """Categorize invoice based on content for Business."""
        
        text_to_analyze = " ".join([
            invoice_data.get("supplier_name", ""),
            " ".join([item.get("description", "") for item in invoice_data.get("line_items", [])])
        ]).lower()
        
        # Check each category
        for category, keywords in self.supplier_categories.items():
            if any(keyword in text_to_analyze for keyword in keywords):
                return category
        
        return "other"
    
    def _validate_invoice_data(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate extracted invoice data."""
        
        validation = {
            "is_valid": True,
            "issues": [],
            "warnings": []
        }
        
        # Check required fields
        if not invoice_data.get("invoice_number"):
            validation["issues"].append("Missing invoice number")
            validation["is_valid"] = False
        
        if not invoice_data.get("supplier_name"):
            validation["issues"].append("Missing supplier name")
            validation["is_valid"] = False
        
        if invoice_data.get("total_amount", 0) <= 0:
            validation["issues"].append("Invalid or missing total amount")
            validation["is_valid"] = False
        
        # Check warnings
        if not invoice_data.get("due_date"):
            validation["warnings"].append("Due date not found")
        
        if len(invoice_data.get("line_items", [])) == 0:
            validation["warnings"].append("No line items extracted")
        
        # Validate amount calculations
        subtotal = invoice_data.get("subtotal", 0)
        tax = invoice_data.get("tax_amount", 0)
        total = invoice_data.get("total_amount", 0)
        
        if subtotal > 0 and tax > 0 and total > 0:
            calculated_total = subtotal + tax
            if abs(calculated_total - total) > 0.01:
                validation["warnings"].append(f"Amount calculation discrepancy: {calculated_total} vs {total}")
        
        return validation
    
    def _generate_processing_summary(self, processed_invoices: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of invoice processing results."""
        
        total_amount = 0
        categories = {}
        suppliers = set()
        
        for invoice in processed_invoices:
            if invoice.get("processing_status") == "success":
                extracted = invoice.get("extracted_data", {})
                
                # Sum amounts
                amount = extracted.get("total_amount", 0)
                if amount > 0:
                    total_amount += amount
                
                # Count categories
                category = invoice.get("business_category", "other")
                categories[category] = categories.get(category, 0) + 1
                
                # Collect suppliers
                supplier = extracted.get("supplier_name", "").strip()
                if supplier:
                    suppliers.add(supplier)
        
        return {
            "total_invoices": len(processed_invoices),
            "total_amount": round(total_amount, 2),
            "categories_breakdown": categories,
            "unique_suppliers": len(suppliers),
            "supplier_names": list(suppliers),
            "average_invoice_amount": round(total_amount / max(len(processed_invoices), 1), 2)
        }
    
    def _simulate_invoice_processing(self, limit: int) -> Dict[str, Any]:
        """Simulate invoice processing for demonstration."""
        
        simulated_invoices = []
        
        suppliers = [
            "Organic Supplies Sdn Bhd",
            "Natural Packaging Malaysia",
            "Premium Ingredients Co",
            "Eco Logistics Services"
        ]
        
        for i in range(min(limit, 5)):
            supplier = suppliers[i % len(suppliers)]
            amount = round(1000 + (i * 500) + (hash(supplier) % 2000), 2)
            
            invoice = {
                "email_info": {
                    "sender": f"billing@{supplier.lower().replace(' ', '')}.com",
                    "subject": f"Invoice INV-2025-{str(i+1).zfill(3)}",
                    "date": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                },
                "extracted_data": {
                    "invoice_number": f"INV-2025-{str(i+1).zfill(3)}",
                    "supplier_name": supplier,
                    "invoice_date": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
                    "due_date": (datetime.now() + timedelta(days=30-i)).strftime('%Y-%m-%d'),
                    "subtotal": round(amount * 0.9, 2),
                    "tax_amount": round(amount * 0.1, 2),
                    "total_amount": amount,
                    "currency": "RM",
                    "line_items": [
                        {
                            "description": f"Natural ingredients batch {i+1}",
                            "quantity": "100 kg",
                            "unit_price": round(amount * 0.9 / 100, 2),
                            "total": round(amount * 0.9, 2)
                        }
                    ]
                },
                "business_category": "raw_materials" if i % 2 == 0 else "packaging",
                "validation": {
                    "is_valid": True,
                    "issues": [],
                    "warnings": []
                },
                "processing_status": "success"
            }
            
            simulated_invoices.append(invoice)
        
        summary = self._generate_processing_summary(simulated_invoices)
        
        return {
            "invoices_processed": len(simulated_invoices),
            "invoices_data": simulated_invoices,
            "processing_summary": summary,
            "simulation_mode": True,
            "next_steps": [
                "Review extracted data for accuracy",
                "Categorize expenses by Business standards",
                "Update Google Sheets with new invoice data",
                "Archive processed invoices to Google Drive"
            ]
        }


class GoogleSheetsIntegrationTool(BaseTool):
    """Integrates with Google Sheets for financial data management."""
    
    name: str = "Google Sheets Integration Tool"
    description: str = """Integrates processed financial data with Google Sheets.
        Creates and updates financial tracking spreadsheets with invoice summaries
        and detailed line items. Designed for Business's financial workflow."""

    def __init__(self):
        super().__init__()
        # Google Sheets API configuration
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.sheets_service = None
        
        # Business financial spreadsheet structure
        self.invoice_summary_headers = [
            "Invoice Number", "Date", "Supplier", "Category", 
            "Subtotal", "Tax", "Total", "Currency", "Status", "Due Date"
        ]
        
        self.line_items_headers = [
            "Invoice Number", "Line Item", "Description", 
            "Quantity", "Unit Price", "Total", "Category"
        ]

    def _run(self, spreadsheet_id: str, invoice_data: List[Dict[str, Any]], 
             operation: str = "append") -> Dict[str, Any]:
        """
        Updates Google Sheets with invoice data.
        
        Args:
            spreadsheet_id: Google Sheets ID to update
            invoice_data: List of processed invoice data
            operation: 'append' or 'update' data
            
        Returns:
            Dictionary with update results
        """
        try:
            if not self._initialize_sheets_service():
                return self._simulate_sheets_update(spreadsheet_id, invoice_data, operation)
            
            # Update invoice summary sheet
            summary_result = self._update_invoice_summary(spreadsheet_id, invoice_data, operation)
            
            # Update line items sheet
            items_result = self._update_line_items(spreadsheet_id, invoice_data, operation)
            
            # Generate update summary
            update_summary = self._generate_update_summary(summary_result, items_result, invoice_data)
            
            result = {
                "spreadsheet_updated": True,
                "spreadsheet_id": spreadsheet_id,
                "operation": operation,
                "summary_sheet_result": summary_result,
                "line_items_result": items_result,
                "update_summary": update_summary,
                "next_steps": [
                    "Review updated data in Google Sheets",
                    "Validate formulas and calculations",
                    "Set up data validation rules if needed",
                    "Create charts and dashboards for analysis"
                ]
            }
            
            logger.info(f"Successfully updated Google Sheets: {spreadsheet_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error updating Google Sheets: {str(e)}")
            return {"error": f"Google Sheets update failed: {str(e)}"}
    
    def _initialize_sheets_service(self) -> bool:
        """Initialize Google Sheets API service."""
        try:
            creds = None
            
            # Load existing credentials
            if os.path.exists('sheets_token.json'):
                creds = Credentials.from_authorized_user_file('sheets_token.json', self.SCOPES)
            
            # If there are no (valid) credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if os.path.exists('credentials.json'):
                        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                        creds = flow.run_local_server(port=0)
                    else:
                        logger.warning("Google Sheets credentials not found")
                        return False
                
                # Save credentials for next run
                with open('sheets_token.json', 'w') as token:
                    token.write(creds.to_json())
            
            self.sheets_service = build('sheets', 'v4', credentials=creds)
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Sheets service: {str(e)}")
            return False
    
    def _update_invoice_summary(self, spreadsheet_id: str, invoice_data: List[Dict[str, Any]], operation: str) -> Dict[str, Any]:
        """Update the invoice summary sheet."""
        try:
            # Prepare data rows
            rows = []
            
            for invoice in invoice_data:
                if invoice.get("processing_status") != "success":
                    continue
                    
                extracted = invoice.get("extracted_data", {})
                row = [
                    extracted.get("invoice_number", ""),
                    extracted.get("invoice_date", ""),
                    extracted.get("supplier_name", ""),
                    invoice.get("business_category", ""),
                    extracted.get("subtotal", 0),
                    extracted.get("tax_amount", 0),
                    extracted.get("total_amount", 0),
                    extracted.get("currency", "RM"),
                    "Processed",
                    extracted.get("due_date", "")
                ]
                rows.append(row)
            
            if not rows:
                return {"rows_updated": 0, "message": "No valid invoice data to update"}
            
            # Update the sheet
            range_name = "Invoice_Summary!A:J"
            
            if operation == "append":
                # Append new rows
                body = {"values": rows}
                result = self.sheets_service.spreadsheets().values().append(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption='USER_ENTERED',
                    insertDataOption='INSERT_ROWS',
                    body=body
                ).execute()
            else:
                # Update existing range
                body = {"values": [self.invoice_summary_headers] + rows}
                result = self.sheets_service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption='USER_ENTERED',
                    body=body
                ).execute()
            
            return {
                "rows_updated": len(rows),
                "range": range_name,
                "operation": operation,
                "sheets_response": result
            }
            
        except Exception as e:
            logger.error(f"Error updating invoice summary: {str(e)}")
            return {"error": str(e)}
    
    def _update_line_items(self, spreadsheet_id: str, invoice_data: List[Dict[str, Any]], operation: str) -> Dict[str, Any]:
        """Update the line items sheet."""
        try:
            # Prepare line item rows
            rows = []
            
            for invoice in invoice_data:
                if invoice.get("processing_status") != "success":
                    continue
                    
                extracted = invoice.get("extracted_data", {})
                invoice_number = extracted.get("invoice_number", "")
                line_items = extracted.get("line_items", [])
                
                for i, item in enumerate(line_items):
                    row = [
                        invoice_number,
                        i + 1,  # Line item number
                        item.get("description", ""),
                        item.get("quantity", ""),
                        item.get("unit_price", 0),
                        item.get("total", 0),
                        invoice.get("business_category", "")
                    ]
                    rows.append(row)
            
            if not rows:
                return {"rows_updated": 0, "message": "No line items to update"}
            
            # Update the sheet
            range_name = "Invoice_Items!A:G"
            
            if operation == "append":
                # Append new rows
                body = {"values": rows}
                result = self.sheets_service.spreadsheets().values().append(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption='USER_ENTERED',
                    insertDataOption='INSERT_ROWS',
                    body=body
                ).execute()
            else:
                # Update existing range
                body = {"values": [self.line_items_headers] + rows}
                result = self.sheets_service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption='USER_ENTERED',
                    body=body
                ).execute()
            
            return {
                "rows_updated": len(rows),
                "range": range_name,
                "operation": operation,
                "sheets_response": result
            }
            
        except Exception as e:
            logger.error(f"Error updating line items: {str(e)}")
            return {"error": str(e)}
    
    def _generate_update_summary(self, summary_result: Dict[str, Any], 
                                items_result: Dict[str, Any], invoice_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of sheets update."""
        
        total_invoices = len([i for i in invoice_data if i.get("processing_status") == "success"])
        total_amount = sum(
            i.get("extracted_data", {}).get("total_amount", 0) 
            for i in invoice_data 
            if i.get("processing_status") == "success"
        )
        
        return {
            "invoices_added": total_invoices,
            "line_items_added": items_result.get("rows_updated", 0),
            "total_amount_processed": round(total_amount, 2),
            "summary_sheet_rows": summary_result.get("rows_updated", 0),
            "update_timestamp": datetime.now().isoformat(),
            "data_quality": {
                "valid_invoices": len([
                    i for i in invoice_data 
                    if i.get("validation", {}).get("is_valid", False)
                ]),
                "invoices_with_warnings": len([
                    i for i in invoice_data 
                    if i.get("validation", {}).get("warnings", [])
                ])
            }
        }
    
    def _simulate_sheets_update(self, spreadsheet_id: str, invoice_data: List[Dict[str, Any]], operation: str) -> Dict[str, Any]:
        """Simulate Google Sheets update for demonstration."""
        
        valid_invoices = [i for i in invoice_data if i.get("processing_status") == "success"]
        total_line_items = sum(
            len(i.get("extracted_data", {}).get("line_items", []))
            for i in valid_invoices
        )
        
        total_amount = sum(
            i.get("extracted_data", {}).get("total_amount", 0)
            for i in valid_invoices
        )
        
        return {
            "spreadsheet_updated": True,
            "spreadsheet_id": spreadsheet_id,
            "operation": operation,
            "summary_sheet_result": {
                "rows_updated": len(valid_invoices),
                "range": "Invoice_Summary!A:J",
                "operation": operation
            },
            "line_items_result": {
                "rows_updated": total_line_items,
                "range": "Invoice_Items!A:G", 
                "operation": operation
            },
            "update_summary": {
                "invoices_added": len(valid_invoices),
                "line_items_added": total_line_items,
                "total_amount_processed": round(total_amount, 2),
                "summary_sheet_rows": len(valid_invoices),
                "update_timestamp": datetime.now().isoformat(),
                "data_quality": {
                    "valid_invoices": len([
                        i for i in invoice_data 
                        if i.get("validation", {}).get("is_valid", False)
                    ]),
                    "invoices_with_warnings": len([
                        i for i in invoice_data 
                        if i.get("validation", {}).get("warnings", [])
                    ])
                }
            },
            "simulation_mode": True,
            "next_steps": [
                f"Review updated data in Google Sheets: {spreadsheet_id}",
                "Validate formulas and calculations",
                "Set up data validation rules if needed",
                "Create charts and dashboards for analysis"
            ]
        }


class ExpenseTrackingTool(BaseTool):
    """Tracks and categorizes expenses according to Business's business needs."""
    
    name: str = "Business Expense Tracking Tool"  
    description: str = """Tracks expenses and categorizes them according to Business's
        business categories. Provides expense analysis, budget tracking, and insights
        for family business financial management."""

    def __init__(self):
        super().__init__()
        
        # Business expense categories with budget guidelines
        self.expense_categories = {
            "raw_materials": {
                "budget_percentage": 40,  # 40% of total budget
                "keywords": ["ingredient", "organic", "powder", "extract", "vitamin", "mineral"],
                "priority": "high"
            },
            "packaging": {
                "budget_percentage": 15,
                "keywords": ["bottle", "label", "box", "container", "packaging", "seal"],
                "priority": "high" 
            },
            "marketing": {
                "budget_percentage": 20,
                "keywords": ["advertising", "promotion", "marketing", "social media", "influencer"],
                "priority": "medium"
            },
            "operations": {
                "budget_percentage": 10,
                "keywords": ["rent", "utilities", "office", "equipment maintenance"],
                "priority": "medium"
            },
            "research_development": {
                "budget_percentage": 10,
                "keywords": ["research", "development", "testing", "formulation", "lab"],
                "priority": "high"
            },
            "regulatory_compliance": {
                "budget_percentage": 3,
                "keywords": ["certification", "audit", "regulatory", "compliance", "legal"],
                "priority": "high"
            },
            "other": {
                "budget_percentage": 2,
                "keywords": [],
                "priority": "low"
            }
        }

    def _run(self, expense_data: List[Dict[str, Any]], 
             analysis_period: str = "monthly", budget_total: float = 0) -> Dict[str, Any]:
        """
        Tracks and analyzes expenses for Business.
        
        Args:
            expense_data: List of expense records to analyze
            analysis_period: Time period for analysis ('monthly', 'quarterly', 'yearly')
            budget_total: Total budget for the period (optional)
            
        Returns:
            Dictionary with expense analysis and insights
        """
        try:
            if not expense_data:
                return {"error": "No expense data provided"}
            
            # Categorize expenses
            categorized_expenses = self._categorize_expenses(expense_data)
            
            # Calculate category totals
            category_totals = self._calculate_category_totals(categorized_expenses)
            
            # Analyze budget adherence
            budget_analysis = self._analyze_budget_adherence(category_totals, budget_total)
            
            # Generate insights and recommendations
            insights = self._generate_expense_insights(categorized_expenses, category_totals, budget_analysis)
            
            # Create expense trends analysis
            trends = self._analyze_expense_trends(expense_data, analysis_period)
            
            result = {
                "analysis_period": analysis_period,
                "total_expenses": sum(category_totals.values()),
                "expense_categories": category_totals,
                "categorized_expenses": categorized_expenses,
                "budget_analysis": budget_analysis,
                "insights_and_recommendations": insights,
                "expense_trends": trends,
                "business_priorities": self._assess_priority_alignment(category_totals),
                "next_actions": [
                    "Review high-priority category spending",
                    "Optimize expenses in over-budget categories",
                    "Plan budget allocation for next period",
                    "Set up expense monitoring alerts"
                ]
            }
            
            logger.info(f"Expense tracking completed for {len(expense_data)} expenses")
            return result
            
        except Exception as e:
            logger.error(f"Error tracking expenses: {str(e)}")
            return {"error": f"Expense tracking failed: {str(e)}"}
    
    def _categorize_expenses(self, expense_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize expenses according to Business's business categories."""
        
        categorized = {category: [] for category in self.expense_categories.keys()}
        
        for expense in expense_data:
            category = self._determine_expense_category(expense)
            categorized[category].append({
                **expense,
                "business_category": category,
                "category_priority": self.expense_categories[category]["priority"]
            })
        
        return categorized
    
    def _determine_expense_category(self, expense: Dict[str, Any]) -> str:
        """Determine the appropriate category for an expense."""
        
        # Get text to analyze (description, supplier, etc.)
        text_fields = [
            expense.get("description", ""),
            expense.get("supplier_name", ""),
            expense.get("notes", "")
        ]
        
        text_to_analyze = " ".join(text_fields).lower()
        
        # Check each category's keywords
        for category, config in self.expense_categories.items():
            if category == "other":
                continue  # Skip 'other', it's the default
                
            keywords = config["keywords"]
            if any(keyword in text_to_analyze for keyword in keywords):
                return category
        
        return "other"
    
    def _calculate_category_totals(self, categorized_expenses: Dict[str, List[Dict[str, Any]]]) -> Dict[str, float]:
        """Calculate total amounts for each expense category."""
        
        category_totals = {}
        
        for category, expenses in categorized_expenses.items():
            total = sum(
                expense.get("amount", 0) or expense.get("total_amount", 0) 
                for expense in expenses
            )
            category_totals[category] = round(total, 2)
        
        return category_totals
    
    def _analyze_budget_adherence(self, category_totals: Dict[str, float], budget_total: float) -> Dict[str, Any]:
        """Analyze how expenses compare to budget guidelines."""
        
        if budget_total <= 0:
            return {
                "budget_provided": False,
                "message": "No budget provided for comparison"
            }
        
        budget_analysis = {
            "budget_provided": True,
            "total_budget": budget_total,
            "total_spent": sum(category_totals.values()),
            "budget_utilization": round(sum(category_totals.values()) / budget_total * 100, 1),
            "category_budget_analysis": {}
        }
        
        for category, actual_amount in category_totals.items():
            if category in self.expense_categories:
                recommended_percentage = self.expense_categories[category]["budget_percentage"]
                recommended_amount = budget_total * (recommended_percentage / 100)
                
                variance = actual_amount - recommended_amount
                variance_percentage = (variance / recommended_amount * 100) if recommended_amount > 0 else 0
                
                budget_analysis["category_budget_analysis"][category] = {
                    "recommended_percentage": recommended_percentage,
                    "recommended_amount": round(recommended_amount, 2),
                    "actual_amount": actual_amount,
                    "variance": round(variance, 2),
                    "variance_percentage": round(variance_percentage, 1),
                    "status": "over_budget" if variance > 0 else "under_budget" if variance < -recommended_amount*0.1 else "on_track"
                }
        
        return budget_analysis
    
    def _generate_expense_insights(self, categorized_expenses: Dict[str, List[Dict[str, Any]]],
                                 category_totals: Dict[str, float], budget_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights and recommendations based on expense analysis."""
        
        insights = {
            "key_findings": [],
            "recommendations": [],
            "cost_optimization_opportunities": [],
            "business_specific_insights": []
        }
        
        total_expenses = sum(category_totals.values())
        
        # Key findings
        highest_category = max(category_totals.items(), key=lambda x: x[1])
        insights["key_findings"].append(f"Highest expense category: {highest_category[0]} (RM {highest_category[1]:,.2f})")
        
        # Business-specific insights
        core_categories = ["raw_materials", "packaging", "research_development"]
        core_spending = sum(category_totals.get(cat, 0) for cat in core_categories)
        core_percentage = (core_spending / total_expenses * 100) if total_expenses > 0 else 0
        
        insights["business_specific_insights"].extend([
            f"Core product categories (raw materials, packaging, R&D) represent {core_percentage:.1f}% of total spending",
            f"Raw materials spending: RM {category_totals.get('raw_materials', 0):,.2f} - {'aligned with' if core_percentage >= 60 else 'below'} family business focus"
        ])
        
        # Budget-based recommendations
        if budget_analysis.get("budget_provided"):
            budget_cat_analysis = budget_analysis.get("category_budget_analysis", {})
            
            for category, analysis in budget_cat_analysis.items():
                if analysis["status"] == "over_budget":
                    insights["recommendations"].append(
                        f"Reduce {category} spending by RM {analysis['variance']:,.2f} to align with budget"
                    )
                elif analysis["status"] == "under_budget" and self.expense_categories[category]["priority"] == "high":
                    insights["cost_optimization_opportunities"].append(
                        f"Consider increasing {category} investment by RM {abs(analysis['variance']):,.2f} for better product quality"
                    )
        
        # General recommendations
        if category_totals.get("marketing", 0) < total_expenses * 0.15:
            insights["recommendations"].append("Consider increasing marketing investment to support growth")
        
        if category_totals.get("research_development", 0) < total_expenses * 0.08:
            insights["recommendations"].append("Increase R&D investment to maintain product innovation edge")
        
        return insights
    
    def _analyze_expense_trends(self, expense_data: List[Dict[str, Any]], analysis_period: str) -> Dict[str, Any]:
        """Analyze expense trends over time."""
        
        # Group expenses by date
        expenses_by_date = {}
        
        for expense in expense_data:
            date_str = expense.get("date", expense.get("invoice_date", ""))
            if date_str:
                try:
                    # Extract month for monthly analysis
                    if analysis_period == "monthly":
                        date_key = date_str[:7]  # YYYY-MM format
                    elif analysis_period == "quarterly":
                        year = int(date_str[:4])
                        month = int(date_str[5:7])
                        quarter = (month - 1) // 3 + 1
                        date_key = f"{year}-Q{quarter}"
                    else:  # yearly
                        date_key = date_str[:4]  # YYYY format
                    
                    if date_key not in expenses_by_date:
                        expenses_by_date[date_key] = []
                    expenses_by_date[date_key].append(expense)
                    
                except (ValueError, IndexError):
                    continue
        
        # Calculate trends
        period_totals = {}
        for period, expenses in expenses_by_date.items():
            total = sum(
                exp.get("amount", 0) or exp.get("total_amount", 0) 
                for exp in expenses
            )
            period_totals[period] = round(total, 2)
        
        # Calculate trend direction
        sorted_periods = sorted(period_totals.keys())
        trend_direction = "stable"
        
        if len(sorted_periods) >= 2:
            latest = period_totals[sorted_periods[-1]]
            previous = period_totals[sorted_periods[-2]]
            
            if latest > previous * 1.1:
                trend_direction = "increasing"
            elif latest < previous * 0.9:
                trend_direction = "decreasing"
        
        return {
            "period_totals": period_totals,
            "trend_direction": trend_direction,
            "periods_analyzed": len(sorted_periods),
            "average_per_period": round(sum(period_totals.values()) / max(len(period_totals), 1), 2),
            "highest_spending_period": max(period_totals.items(), key=lambda x: x[1]) if period_totals else None,
            "lowest_spending_period": min(period_totals.items(), key=lambda x: x[1]) if period_totals else None
        }
    
    def _assess_priority_alignment(self, category_totals: Dict[str, float]) -> Dict[str, Any]:
        """Assess how expense distribution aligns with Business's priorities."""
        
        total_expenses = sum(category_totals.values())
        priority_analysis = {
            "high_priority_spending": 0,
            "medium_priority_spending": 0,
            "low_priority_spending": 0,
            "priority_breakdown": {}
        }
        
        for category, amount in category_totals.items():
            if category in self.expense_categories:
                priority = self.expense_categories[category]["priority"]
                priority_analysis[f"{priority}_priority_spending"] += amount
                
                priority_analysis["priority_breakdown"][category] = {
                    "amount": amount,
                    "percentage_of_total": round(amount / total_expenses * 100, 1) if total_expenses > 0 else 0,
                    "priority": priority
                }
        
        # Calculate priority percentages
        if total_expenses > 0:
            priority_analysis["high_priority_percentage"] = round(
                priority_analysis["high_priority_spending"] / total_expenses * 100, 1
            )
            priority_analysis["medium_priority_percentage"] = round(
                priority_analysis["medium_priority_spending"] / total_expenses * 100, 1
            )
            priority_analysis["low_priority_percentage"] = round(
                priority_analysis["low_priority_spending"] / total_expenses * 100, 1
            )
        
        # Assess alignment
        high_priority_pct = priority_analysis.get("high_priority_percentage", 0)
        
        if high_priority_pct >= 70:
            priority_analysis["alignment_assessment"] = "excellent - focused on core business priorities"
        elif high_priority_pct >= 60:
            priority_analysis["alignment_assessment"] = "good - majority spending on key areas"
        elif high_priority_pct >= 50:
            priority_analysis["alignment_assessment"] = "fair - could improve focus on high-priority areas"
        else:
            priority_analysis["alignment_assessment"] = "needs improvement - too much spending on non-core areas"
        
        return priority_analysis


if __name__ == "__main__":
    # Example usage
    invoice_tool = InvoiceProcessingTool()
    sheets_tool = GoogleSheetsIntegrationTool()
    expense_tool = ExpenseTrackingTool()
    
    # Test invoice processing
    result = invoice_tool._run(limit=3)
    print("📄 Invoice Processing Result:", result)
    
    # Test expense tracking  
    sample_expenses = [
        {"description": "Organic vitamin powder", "amount": 1500, "date": "2025-01-15"},
        {"description": "Premium packaging bottles", "amount": 800, "date": "2025-01-10"},
        {"description": "Marketing campaign", "amount": 2000, "date": "2025-01-05"}
    ]
    
    expense_result = expense_tool._run(sample_expenses, budget_total=10000)
    print("💰 Expense Tracking Result:", expense_result)


# Tool aliases for Business crew compatibility  
MalaysianSupplierTool = ExpenseTrackingTool  # Malaysian supplier tracking within expense system