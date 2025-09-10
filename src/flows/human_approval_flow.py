"""
Human Approval Flow
Implements human-in-the-loop functionality for critical business decisions
"""

import os
from typing import Dict, Any, Optional
from enum import Enum

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"

class ApprovalRequest:
    """Represents a request requiring human approval"""
    
    def __init__(self, request_id: str, task_type: str, content: str, 
                 priority: str = "normal", requester: str = "system"):
        self.request_id = request_id
        self.task_type = task_type
        self.content = content
        self.priority = priority
        self.requester = requester
        self.status = ApprovalStatus.PENDING
        self.approval_notes = ""
        self.approved_by = ""
        self.timestamp = None

class HumanApprovalFlow:
    """Manages human approval workflow for critical business operations"""
    
    def __init__(self):
        self.pending_approvals = {}
        self.approval_history = []
        self.simulation_mode = os.getenv("USE_SIMULATION", "True").lower() == "true"
    
    def request_approval(self, task_type: str, content: str, 
                        priority: str = "normal") -> ApprovalRequest:
        """Submit a request for human approval"""
        request_id = f"approval_{len(self.pending_approvals) + 1:04d}"
        
        approval_request = ApprovalRequest(
            request_id=request_id,
            task_type=task_type,
            content=content,
            priority=priority
        )
        
        self.pending_approvals[request_id] = approval_request
        
        if self.simulation_mode:
            return self._simulate_approval(approval_request)
        
        return approval_request
    
    def _simulate_approval(self, request: ApprovalRequest) -> ApprovalRequest:
        """Simulate human approval in demo mode"""
        
        # Auto-approve low-risk tasks
        auto_approve_tasks = ["job_posting", "meeting_coordination", "document_creation"]
        
        if request.task_type in auto_approve_tasks and request.priority != "high":
            request.status = ApprovalStatus.APPROVED
            request.approved_by = "Simulation (Auto-approved)"
            request.approval_notes = "Low-risk task auto-approved in simulation mode"
        else:
            # Simulate human review for high-risk tasks
            request.status = ApprovalStatus.APPROVED
            request.approved_by = "Simulation (Human Manager)"
            request.approval_notes = "Reviewed and approved in simulation mode"
        
        # Move to history
        self.approval_history.append(request)
        if request.request_id in self.pending_approvals:
            del self.pending_approvals[request.request_id]
        
        return request
    
    def process_approval(self, request_id: str, decision: str, 
                        notes: str = "", approver: str = "Manager") -> bool:
        """Process a human approval decision"""
        
        if request_id not in self.pending_approvals:
            return False
        
        request = self.pending_approvals[request_id]
        
        if decision.lower() == "approve":
            request.status = ApprovalStatus.APPROVED
        elif decision.lower() == "reject":
            request.status = ApprovalStatus.REJECTED
        elif decision.lower() == "modify":
            request.status = ApprovalStatus.MODIFIED
        
        request.approval_notes = notes
        request.approved_by = approver
        
        # Move to history
        self.approval_history.append(request)
        del self.pending_approvals[request_id]
        
        return True
    
    def get_pending_approvals(self) -> Dict[str, ApprovalRequest]:
        """Get all pending approval requests"""
        return self.pending_approvals.copy()
    
    def get_approval_status(self, request_id: str) -> Optional[ApprovalStatus]:
        """Check the status of an approval request"""
        if request_id in self.pending_approvals:
            return self.pending_approvals[request_id].status
        
        # Check history
        for request in self.approval_history:
            if request.request_id == request_id:
                return request.status
        
        return None
    
    def get_high_priority_approvals(self) -> Dict[str, ApprovalRequest]:
        """Get high-priority pending approvals"""
        return {
            req_id: request 
            for req_id, request in self.pending_approvals.items() 
            if request.priority == "high"
        }

# Global approval flow instance
approval_flow = HumanApprovalFlow()

def require_approval(task_type: str, content: str, priority: str = "normal") -> ApprovalRequest:
    """Decorator/function to require human approval for tasks"""
    return approval_flow.request_approval(task_type, content, priority)

def check_approval_required(task_type: str) -> bool:
    """Check if a task type requires human approval"""
    approval_required_tasks = [
        "financial_transactions",
        "candidate_hiring", 
        "crisis_response",
        "budget_changes",
        "vendor_contracts",
        "data_access",
        "policy_changes"
    ]
    
    return task_type in approval_required_tasks
