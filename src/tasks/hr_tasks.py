"""
HR Tasks Module
Task definitions for human resources and recruitment operations
"""

from crewai import Task
from typing import Dict, Any, List

class HRTasks:
    """Task factory for HR operations"""
    
    def create_recruitment_analysis_task(self, job_details: Dict[str, Any]) -> Task:
        """Create recruitment analysis task"""
        return Task(
            description=f"""
            Analyze the recruitment request for: {job_details.get('position', 'Position TBD')}
            
            Requirements:
            - Position: {job_details.get('position', 'Not specified')}
            - Experience Level: {job_details.get('experience', 'Not specified')}
            - Key Skills: {job_details.get('skills', 'Not specified')}
            - Department: {job_details.get('department', 'Not specified')}
            - Work Type: {job_details.get('work_type', 'Not specified')}
            
            Create a comprehensive hiring strategy including:
            1. Detailed job description reflecting company values
            2. Required qualifications and preferred skills
            3. Recruitment strategy for target market
            4. Candidate evaluation criteria
            5. Interview process recommendations
            6. Timeline for hiring process
            """,
            expected_output="""
            A comprehensive recruitment analysis document containing:
            - Professional job description
            - Clear qualification requirements  
            - Targeted recruitment strategy
            - Evaluation criteria matrix
            - Structured interview process
            - Realistic timeline with milestones
            """,
            agent=None  # Will be set when task is used
        )
    
    def create_job_posting_task(self, job_details: Dict[str, Any]) -> Task:
        """Create job posting creation task"""
        return Task(
            description=f"""
            Create a compelling job posting for: {job_details.get('position', 'Position TBD')}
            
            The job posting should:
            1. Use engaging, professional language
            2. Highlight company culture and values
            3. Clearly state requirements and qualifications
            4. Include competitive benefits and growth opportunities
            5. Be optimized for job board algorithms
            6. Reflect diversity and inclusion commitments
            
            Format the posting for multiple platforms:
            - LinkedIn Jobs
            - Indeed
            - Company website
            - Industry-specific job boards
            """,
            expected_output="""
            A professionally formatted job posting ready for publication including:
            - Compelling job title and summary
            - Detailed role description
            - Clear requirements and qualifications
            - Company culture highlights
            - Benefits and compensation overview
            - Application instructions
            - Multiple format versions for different platforms
            """,
            agent=None  # Will be set when task is used
        )
    
    def create_candidate_evaluation_task(self, candidates: List[Dict[str, Any]]) -> Task:
        """Create candidate evaluation task"""
        return Task(
            description=f"""
            Evaluate {len(candidates)} candidates for the position.
            
            Candidate Information:
            {self._format_candidates(candidates)}
            
            Evaluation Criteria:
            1. Technical skills alignment with job requirements
            2. Experience level and relevance
            3. Cultural fit with company values
            4. Communication and interpersonal skills
            5. Growth potential and career trajectory
            6. Availability and timeline fit
            
            Provide:
            - Individual candidate assessments
            - Ranking with scoring rationale
            - Interview recommendations
            - Next steps for top candidates
            """,
            expected_output="""
            Comprehensive candidate evaluation report including:
            - Individual candidate profiles with scores
            - Ranked candidate list with detailed reasoning
            - Strengths and concerns for each candidate
            - Interview question recommendations
            - Hiring recommendations with risk assessment
            """,
            agent=None  # Will be set when task is used
        )
    
    def _format_candidates(self, candidates: List[Dict[str, Any]]) -> str:
        """Format candidate information for task description"""
        formatted = []
        for i, candidate in enumerate(candidates, 1):
            formatted.append(f"""
            Candidate {i}:
            - Name: {candidate.get('name', 'Unknown')}
            - Experience: {candidate.get('experience', 'Not specified')}
            - Skills: {candidate.get('skills', 'Not specified')}
            - Background: {candidate.get('background', 'Not specified')}
            """)
        return "\n".join(formatted)
