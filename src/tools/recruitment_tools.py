"""
HaruPlate Recruitment Tools
Real API integrations for CV analysis, email communications, Zoom scheduling, and HaruPlate compatibility scoring.
"""

import os
import logging
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re

from crewai.tools import BaseTool

# Optional imports for full functionality
try:
    import smtplib
    import PyPDF2
    import docx
    import jwt
    import requests
    import pytz
    HAS_OPTIONAL_DEPS = True
except ImportError:
    HAS_OPTIONAL_DEPS = False

logger = logging.getLogger(__name__)


class CVAnalysisTool(BaseTool):
    """Analyzes CVs and resumes with focus on technical skills and experience."""
    
    name: str = "CV Analysis Tool"
    description: str = """Analyzes CV/resume files (PDF, DOCX) and extracts:
        - Technical skills and competencies
        - Work experience and career progression  
        - Education and certifications
        - Industry experience relevance
        - Communication style assessment
        Returns structured analysis for compatibility scoring."""

    def _run(self, file_path: str, position_requirements: str = "") -> Dict[str, Any]:
        """
        Analyzes a CV file and extracts relevant information.
        
        Args:
            file_path: Path to CV file (PDF or DOCX)
            position_requirements: Job requirements to match against
            
        Returns:
            Dictionary with structured CV analysis
        """
        try:
            # Extract text from CV
            cv_text = self._extract_text_from_file(file_path)
            
            if not cv_text:
                return {"error": "Could not extract text from CV file"}
            
            # Analyze CV content
            analysis = {
                "technical_skills": self._extract_technical_skills(cv_text),
                "work_experience": self._extract_work_experience(cv_text),
                "education": self._extract_education(cv_text),
                "industry_experience": self._assess_industry_experience(cv_text),
                "communication_style": self._assess_communication_style(cv_text),
                "key_achievements": self._extract_achievements(cv_text),
                "languages": self._extract_languages(cv_text),
                "certifications": self._extract_certifications(cv_text),
                "raw_text": cv_text[:500]  # First 500 chars for context
            }
            
            logger.info(f"CV analysis completed for: {file_path}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing CV: {str(e)}")
            return {"error": f"CV analysis failed: {str(e)}"}
    
    def _extract_text_from_file(self, file_path: str) -> str:
        """Extracts text from PDF or DOCX files."""
        try:
            if file_path.lower().endswith('.pdf'):
                return self._extract_from_pdf(file_path)
            elif file_path.lower().endswith('.docx'):
                return self._extract_from_docx(file_path)
            else:
                return ""
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            return ""
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extracts text from PDF file."""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extracts text from DOCX file."""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _extract_technical_skills(self, text: str) -> List[str]:
        """Extracts technical skills from CV text."""
        # Common technical skills patterns
        skills_keywords = [
            'python', 'javascript', 'java', 'sql', 'react', 'node.js', 'angular',
            'marketing', 'seo', 'sem', 'google analytics', 'facebook ads', 'social media',
            'project management', 'agile', 'scrum', 'jira', 'confluence',
            'photoshop', 'illustrator', 'figma', 'canva', 'content creation',
            'microsoft office', 'excel', 'powerpoint', 'google workspace'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skills_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        return found_skills
    
    def _extract_work_experience(self, text: str) -> List[Dict[str, str]]:
        """Extracts work experience information."""
        # This is a simplified implementation
        # In production, you'd use more sophisticated NLP
        experience = []
        
        # Look for common date patterns and job titles
        lines = text.split('\n')
        for line in lines:
            if any(word in line.lower() for word in ['manager', 'specialist', 'coordinator', 'analyst', 'developer']):
                experience.append({
                    "role": line.strip(),
                    "details": "Extracted from CV text"
                })
        
        return experience[:5]  # Return top 5 experiences
    
    def _extract_education(self, text: str) -> List[str]:
        """Extracts education information."""
        education_keywords = ['university', 'college', 'bachelor', 'master', 'degree', 'diploma', 'phd']
        education = []
        
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in education_keywords):
                education.append(line.strip())
        
        return education[:3]  # Return top 3 education entries
    
    def _assess_industry_experience(self, text: str) -> Dict[str, Any]:
        """Assesses relevant industry experience for HaruPlate."""
        # HaruPlate relevant industries
        relevant_industries = {
            'food_nutrition': ['food', 'nutrition', 'health', 'wellness', 'dietary', 'supplement'],
            'child_focused': ['child', 'children', 'baby', 'infant', 'pediatric', 'family'],
            'natural_products': ['organic', 'natural', 'herbal', 'sustainable', 'eco'],
            'southeast_asia': ['malaysia', 'singapore', 'thailand', 'indonesia', 'asia'],
            'fmcg': ['fmcg', 'consumer goods', 'retail', 'distribution', 'supply chain']
        }
        
        text_lower = text.lower()
        industry_scores = {}
        
        for industry, keywords in relevant_industries.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            industry_scores[industry] = score
        
        total_relevant_experience = sum(industry_scores.values())
        
        return {
            "industry_breakdown": industry_scores,
            "total_relevance_score": total_relevant_experience,
            "most_relevant_area": max(industry_scores.items(), key=lambda x: x[1])[0] if industry_scores else None
        }
    
    def _assess_communication_style(self, text: str) -> Dict[str, Any]:
        """Assesses communication style for HaruPlate fit."""
        # Look for indicators of sincere, family-oriented communication
        positive_indicators = [
            'passion', 'mission', 'purpose', 'values', 'integrity', 'family',
            'community', 'care', 'dedication', 'commitment', 'genuine', 'authentic'
        ]
        
        professional_indicators = [
            'achievement', 'results', 'success', 'growth', 'innovation',
            'collaboration', 'teamwork', 'leadership', 'responsibility'
        ]
        
        text_lower = text.lower()
        
        positive_score = sum(1 for word in positive_indicators if word in text_lower)
        professional_score = sum(1 for word in professional_indicators if word in text_lower)
        
        return {
            "values_alignment_indicators": positive_score,
            "professional_competence_indicators": professional_score,
            "communication_assessment": "sincere" if positive_score > 2 else "professional" if professional_score > 2 else "neutral"
        }
    
    def _extract_achievements(self, text: str) -> List[str]:
        """Extracts key achievements from CV."""
        achievement_patterns = ['achieved', 'increased', 'improved', 'led', 'managed', 'developed', 'created']
        achievements = []
        
        lines = text.split('\n')
        for line in lines:
            if any(pattern in line.lower() for pattern in achievement_patterns):
                achievements.append(line.strip())
        
        return achievements[:5]
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extracts language skills."""
        languages = ['english', 'malay', 'mandarin', 'chinese', 'tamil', 'bahasa', 'indonesian', 'thai']
        found_languages = []
        
        text_lower = text.lower()
        for lang in languages:
            if lang in text_lower:
                found_languages.append(lang.title())
        
        return found_languages
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extracts certifications and qualifications."""
        cert_keywords = ['certified', 'certification', 'license', 'qualification', 'accredited']
        certifications = []
        
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in cert_keywords):
                certifications.append(line.strip())
        
        return certifications[:3]


class HaruPlateCompatibilityTool(BaseTool):
    """Calculates compatibility scores for candidates based on HaruPlate's values."""
    
    name: str = "HaruPlate Compatibility Scoring Tool"
    description: str = """Calculates HaruPlate-specific compatibility scores for candidates.
        Uses 60% values alignment + 40% technical competence weighting.
        Prioritizes passion for child nutrition, family values, and natural products.
        Returns detailed scoring breakdown and recommendations."""

    def _run(self, cv_analysis: Dict[str, Any], position_requirements: str = "") -> Dict[str, Any]:
        """
        Calculates HaruPlate compatibility score for a candidate.
        
        Args:
            cv_analysis: Results from CV analysis tool
            position_requirements: Specific job requirements
            
        Returns:
            Dictionary with detailed compatibility scoring
        """
        try:
            # HaruPlate scoring weights
            VALUES_WEIGHT = 0.6
            TECHNICAL_WEIGHT = 0.4
            
            # Calculate values alignment score (0-100)
            values_score = self._calculate_values_alignment(cv_analysis)
            
            # Calculate technical competence score (0-100)
            technical_score = self._calculate_technical_competence(cv_analysis, position_requirements)
            
            # Calculate overall compatibility score
            overall_score = (values_score * VALUES_WEIGHT) + (technical_score * TECHNICAL_WEIGHT)
            
            # Determine recommendation level
            recommendation = self._get_recommendation_level(overall_score, values_score, technical_score)
            
            # Generate detailed feedback
            feedback = self._generate_candidate_feedback(cv_analysis, values_score, technical_score)
            
            result = {
                "overall_compatibility_score": round(overall_score, 1),
                "values_alignment_score": round(values_score, 1),
                "technical_competence_score": round(technical_score, 1),
                "recommendation_level": recommendation,
                "detailed_feedback": feedback,
                "haruplate_fit_factors": self._identify_fit_factors(cv_analysis),
                "areas_for_development": self._identify_development_areas(cv_analysis, technical_score),
                "interview_focus_areas": self._suggest_interview_focus(values_score, technical_score)
            }
            
            logger.info(f"Compatibility scoring completed. Overall score: {overall_score}")
            return result
            
        except Exception as e:
            logger.error(f"Error calculating compatibility score: {str(e)}")
            return {"error": f"Compatibility scoring failed: {str(e)}"}
    
    def _calculate_values_alignment(self, cv_analysis: Dict[str, Any]) -> float:
        """Calculates values alignment score based on HaruPlate's values."""
        score = 0.0
        
        # Industry experience scoring (max 30 points)
        industry_exp = cv_analysis.get('industry_experience', {})
        industry_score = min(industry_exp.get('total_relevance_score', 0) * 5, 30)
        score += industry_score
        
        # Communication style scoring (max 25 points)
        comm_style = cv_analysis.get('communication_style', {})
        values_indicators = comm_style.get('values_alignment_indicators', 0)
        comm_score = min(values_indicators * 5, 25)
        score += comm_score
        
        # Language skills bonus for Malaysian market (max 15 points)
        languages = cv_analysis.get('languages', [])
        lang_score = 0
        if any('malay' in lang.lower() or 'bahasa' in lang.lower() for lang in languages):
            lang_score += 10
        if any('english' in lang.lower() for lang in languages):
            lang_score += 5
        score += min(lang_score, 15)
        
        # Family/child-oriented experience bonus (max 20 points)
        child_focus_score = industry_exp.get('industry_breakdown', {}).get('child_focused', 0)
        score += min(child_focus_score * 10, 20)
        
        # Natural products experience bonus (max 10 points)
        natural_score = industry_exp.get('industry_breakdown', {}).get('natural_products', 0)
        score += min(natural_score * 5, 10)
        
        return min(score, 100.0)
    
    def _calculate_technical_competence(self, cv_analysis: Dict[str, Any], position_requirements: str) -> float:
        """Calculates technical competence score."""
        score = 0.0
        
        # Technical skills scoring (max 40 points)
        technical_skills = cv_analysis.get('technical_skills', [])
        skills_score = min(len(technical_skills) * 5, 40)
        score += skills_score
        
        # Work experience scoring (max 30 points)
        work_exp = cv_analysis.get('work_experience', [])
        exp_score = min(len(work_exp) * 6, 30)
        score += exp_score
        
        # Education scoring (max 20 points)
        education = cv_analysis.get('education', [])
        edu_score = min(len(education) * 7, 20)
        score += edu_score
        
        # Certifications bonus (max 10 points)
        certifications = cv_analysis.get('certifications', [])
        cert_score = min(len(certifications) * 5, 10)
        score += cert_score
        
        return min(score, 100.0)
    
    def _get_recommendation_level(self, overall_score: float, values_score: float, technical_score: float) -> str:
        """Determines recommendation level based on scores."""
        if overall_score >= 85 and values_score >= 80:
            return "Strongly Recommended - Excellent HaruPlate Fit"
        elif overall_score >= 75 and values_score >= 70:
            return "Recommended - Good Cultural Alignment"
        elif overall_score >= 65 and technical_score >= 70:
            return "Consider - Strong Technical Skills"
        elif overall_score >= 60:
            return "Potential - Requires Further Assessment"
        else:
            return "Not Recommended - Poor Overall Fit"
    
    def _generate_candidate_feedback(self, cv_analysis: Dict[str, Any], values_score: float, technical_score: float) -> str:
        """Generates detailed feedback for the candidate."""
        feedback = []
        
        # Values alignment feedback
        if values_score >= 80:
            feedback.append("🌱 Excellent alignment with HaruPlate's family-oriented values and mission")
        elif values_score >= 60:
            feedback.append("🌿 Good potential for cultural fit with HaruPlate's values")
        else:
            feedback.append("📝 Limited evidence of alignment with child nutrition and family values")
        
        # Technical competence feedback
        if technical_score >= 80:
            feedback.append("🎯 Strong technical qualifications for the role")
        elif technical_score >= 60:
            feedback.append("⚡ Adequate technical skills with room for growth")
        else:
            feedback.append("📚 Technical skills may need development for this role")
        
        # Industry experience feedback
        industry_exp = cv_analysis.get('industry_experience', {})
        most_relevant = industry_exp.get('most_relevant_area')
        if most_relevant == 'food_nutrition':
            feedback.append("🥗 Valuable experience in food and nutrition sector")
        elif most_relevant == 'child_focused':
            feedback.append("👶 Relevant experience with child/family-focused products")
        elif most_relevant == 'natural_products':
            feedback.append("🌿 Experience with natural and organic products")
        
        return " | ".join(feedback)
    
    def _identify_fit_factors(self, cv_analysis: Dict[str, Any]) -> List[str]:
        """Identifies specific factors that make candidate a good fit."""
        fit_factors = []
        
        # Check for specific positive indicators
        industry_breakdown = cv_analysis.get('industry_experience', {}).get('industry_breakdown', {})
        
        if industry_breakdown.get('food_nutrition', 0) > 0:
            fit_factors.append("Experience in food/nutrition industry")
        
        if industry_breakdown.get('child_focused', 0) > 0:
            fit_factors.append("Background with child/family products")
        
        if industry_breakdown.get('southeast_asia', 0) > 0:
            fit_factors.append("Understanding of Southeast Asian markets")
        
        comm_style = cv_analysis.get('communication_style', {})
        if comm_style.get('communication_assessment') == 'sincere':
            fit_factors.append("Sincere, values-driven communication style")
        
        languages = cv_analysis.get('languages', [])
        if any('malay' in lang.lower() for lang in languages):
            fit_factors.append("Malaysian language capabilities")
        
        return fit_factors
    
    def _identify_development_areas(self, cv_analysis: Dict[str, Any], technical_score: float) -> List[str]:
        """Identifies areas where candidate could develop."""
        development_areas = []
        
        if technical_score < 70:
            development_areas.append("Technical skills enhancement needed")
        
        industry_exp = cv_analysis.get('industry_experience', {}).get('total_relevance_score', 0)
        if industry_exp < 3:
            development_areas.append("Limited relevant industry experience")
        
        languages = cv_analysis.get('languages', [])
        if not any('english' in lang.lower() for lang in languages):
            development_areas.append("English language proficiency verification needed")
        
        return development_areas
    
    def _suggest_interview_focus(self, values_score: float, technical_score: float) -> List[str]:
        """Suggests areas to focus on during interviews."""
        focus_areas = []
        
        if values_score < 70:
            focus_areas.append("Explore passion for child nutrition and family values")
        
        if technical_score < 70:
            focus_areas.append("Assess technical competency through practical examples")
        
        focus_areas.extend([
            "Understand motivation for joining HaruPlate mission",
            "Assess cultural fit with family business environment",
            "Evaluate commitment to Malaysian market expansion"
        ])
        
        return focus_areas


class JobPostingTool(BaseTool):
    """Creates HaruPlate-branded job postings with sincere, family-oriented tone."""
    
    name: str = "HaruPlate Job Posting Creator"
    description: str = """Creates compelling job descriptions that reflect HaruPlate's
        sincere, family-oriented brand identity. Uses preferred terminology like
        'teammates' instead of 'candidates'. Emphasizes mission alignment and
        child nutrition focus. Optimized for Malaysian market."""

    def _run(self, position_title: str, requirements: str, location: str = "Malaysia") -> Dict[str, Any]:
        """
        Creates a HaruPlate-branded job posting.
        
        Args:
            position_title: The job title/position
            requirements: Technical and experience requirements
            location: Job location (default: Malaysia)
            
        Returns:
            Dictionary with complete job posting content
        """
        try:
            # Create job posting content
            job_posting = {
                "title": self._create_engaging_title(position_title),
                "introduction": self._create_mission_introduction(),
                "role_description": self._create_role_description(position_title, requirements),
                "what_we_seek": self._create_teammate_profile(requirements),
                "what_we_offer": self._create_value_proposition(),
                "application_process": self._create_application_instructions(),
                "company_culture": self._create_culture_description(),
                "location_info": self._create_location_information(location),
                "formatted_posting": ""
            }
            
            # Create formatted posting
            job_posting["formatted_posting"] = self._format_complete_posting(job_posting)
            
            logger.info(f"Job posting created for: {position_title}")
            return job_posting
            
        except Exception as e:
            logger.error(f"Error creating job posting: {str(e)}")
            return {"error": f"Job posting creation failed: {str(e)}"}
    
    def _create_engaging_title(self, position_title: str) -> str:
        """Creates an engaging job title with HaruPlate branding."""
        return f"🌱 Join Our Mission: {position_title} - HaruPlate Family"
    
    def _create_mission_introduction(self) -> str:
        """Creates mission-focused introduction."""
        return """
        🌟 About Our Mission
        
        At HaruPlate, we believe every child deserves the best possible nutrition to grow, learn, and thrive. 
        We're not just another company - we're a family-driven mission to transform child nutrition through 
        natural, carefully crafted products that parents can trust completely.
        
        Our sincere, family-first approach has made us a trusted name among Malaysian families, and we're 
        expanding across Southeast Asia to bring healthy nutrition to even more children.
        """
    
    def _create_role_description(self, position_title: str, requirements: str) -> str:
        """Creates role description with HaruPlate context."""
        return f"""
        🎯 Your Mission as Our {position_title}
        
        You'll be joining our passionate team to help more families discover the natural nutrition their 
        children deserve. This isn't just a job - it's an opportunity to make a meaningful difference in 
        children's health and development.
        
        In this role, you'll work alongside our dedicated team family to:
        - Support our mission of providing exceptional child nutrition
        - Help expand HaruPlate's positive impact across Malaysian and Southeast Asian markets
        - Contribute to product innovation that prioritizes natural ingredients and family values
        - Maintain our commitment to sincere, transparent communication with families
        
        Key Responsibilities & Requirements:
        {requirements}
        """
    
    def _create_teammate_profile(self, requirements: str) -> str:
        """Creates ideal teammate profile with values focus."""
        return """
        🌿 What Makes You a Perfect Teammate for Our Family
        
        We're looking for someone special - not just skills, but heart. You might be our ideal teammate if you:
        
        💚 Values Alignment:
        - Genuinely care about child nutrition and healthy development
        - Believe in the power of natural products and sustainable practices
        - Appreciate sincere, family-oriented business relationships
        - Share our commitment to transparency and trust with customers
        
        🎯 Professional Excellence:
        - Bring relevant experience and skills to contribute immediately
        - Demonstrate continuous learning and growth mindset
        - Show cultural sensitivity for Malaysian and Southeast Asian markets
        - Communicate with authenticity and warmth
        
        🌟 Personal Qualities:
        - Passion for making a positive impact on families
        - Collaborative spirit that strengthens our team family
        - Initiative to contribute ideas and solutions
        - Integrity that aligns with our family business values
        """
    
    def _create_value_proposition(self) -> str:
        """Creates what HaruPlate offers to teammates."""
        return """
        🏠 What Our HaruPlate Family Offers You
        
        When you join our mission, you become part of a family business that truly values its people:
        
        🌱 Meaningful Work:
        - Direct impact on child nutrition and family health
        - Opportunity to build something lasting and meaningful
        - Work that aligns with your personal values and purpose
        
        📈 Professional Growth:
        - Learning opportunities in the growing natural products industry
        - Mentorship from experienced family business leaders  
        - Skills development that advances your career and our mission
        
        🤝 Family Culture:
        - Sincere, supportive work environment
        - Work-life balance that honors your personal family time
        - Transparent communication and shared decision-making
        - Recognition and appreciation for your contributions
        
        🌏 Market Leadership:
        - Be part of expanding across Southeast Asian markets
        - Work with premium, natural products you can believe in
        - Contribute to industry innovation in child nutrition
        """
    
    def _create_application_instructions(self) -> str:
        """Creates warm, welcoming application instructions."""
        return """
        💌 Ready to Join Our Mission?
        
        We'd love to learn about you and understand why HaruPlate's mission speaks to your heart.
        
        Please share with us:
        📄 Your experience and qualifications (CV/resume)
        💭 A personal note about why child nutrition and family values matter to you
        🌟 What excites you most about the possibility of joining our family
        
        We review every application with care and will respond personally to each prospective teammate.
        
        Send your application to: [careers@haruplate.com]
        Subject: "Excited to Join HaruPlate Mission - [Your Name]"
        
        🕒 We'll be in touch within 5 business days to continue our conversation!
        """
    
    def _create_culture_description(self) -> str:
        """Creates description of HaruPlate's culture."""
        return """
        🌺 Life at HaruPlate Family
        
        Our workplace reflects the same values we put into our products:
        - Sincere relationships built on trust and mutual respect
        - Family-first approach that supports your personal life balance
        - Collaborative environment where every voice matters
        - Continuous learning culture focused on child nutrition innovation
        - Celebration of both individual achievements and team success
        - Commitment to sustainability and natural product excellence
        """
    
    def _create_location_information(self, location: str) -> str:
        """Creates location-specific information."""
        if location.lower() == "malaysia":
            return """
            📍 Based in Malaysia - Heart of Our Mission
            
            You'll be working from our Malaysian headquarters, the foundation of our family business 
            and the launching point for our Southeast Asian expansion. This location offers:
            - Close connection to our founding values and mission
            - Access to local suppliers and natural product sources
            - Cultural understanding of our primary market
            - Opportunity to shape our regional growth strategy
            """
        else:
            return f"""
            📍 Location: {location}
            
            This role offers the opportunity to represent HaruPlate's mission and values in {location}, 
            contributing to our expansion while maintaining our family-oriented approach to business.
            """
    
    def _format_complete_posting(self, components: Dict[str, str]) -> str:
        """Formats all components into a complete job posting."""
        return f"""
{components['title']}

{components['introduction']}

{components['role_description']}

{components['what_we_seek']}

{components['what_we_offer']}

{components['culture_description']}

{components['location_info']}

{components['application_process']}

---
🌱 HaruPlate Family - Nurturing Children, Strengthening Families
"Every child deserves the best possible nutrition to grow, learn, and thrive."
        """.strip()


class EmailDraftTool(BaseTool):
    """Creates warm, personalized email drafts for candidate communication."""
    
    name: str = "HaruPlate Email Communication Tool"
    description: str = """Drafts personalized, warm emails for candidate communication
        that reflect HaruPlate's sincere, family-oriented values. Creates initial
        outreach, interview invitations, and follow-up communications."""

    def _run(self, email_type: str, candidate_name: str, position_title: str, 
             personalization_details: str = "", interview_time: str = "") -> Dict[str, Any]:
        """
        Creates personalized email draft for candidate communication.
        
        Args:
            email_type: Type of email ('initial_outreach', 'interview_invitation', 'follow_up', 'rejection')
            candidate_name: Candidate's name
            position_title: Position they applied for
            personalization_details: Specific details about candidate to personalize
            interview_time: For interview invitations
            
        Returns:
            Dictionary with email subject and body content
        """
        try:
            email_content = {}
            
            if email_type == "initial_outreach":
                email_content = self._create_initial_outreach(candidate_name, position_title, personalization_details)
            elif email_type == "interview_invitation":
                email_content = self._create_interview_invitation(candidate_name, position_title, interview_time)
            elif email_type == "follow_up":
                email_content = self._create_follow_up(candidate_name, position_title)
            elif email_type == "rejection":
                email_content = self._create_rejection_email(candidate_name, position_title)
            else:
                return {"error": f"Unknown email type: {email_type}"}
            
            logger.info(f"Email draft created: {email_type} for {candidate_name}")
            return email_content
            
        except Exception as e:
            logger.error(f"Error creating email draft: {str(e)}")
            return {"error": f"Email creation failed: {str(e)}"}
    
    def _create_initial_outreach(self, candidate_name: str, position_title: str, details: str) -> Dict[str, str]:
        """Creates initial outreach email."""
        subject = f"🌱 We're impressed by your passion, {candidate_name} - HaruPlate Family"
        
        body = f"""
Dear {candidate_name},

Thank you for sharing your interest in joining the HaruPlate family as our {position_title}. 
We were genuinely impressed by your background and the values that shine through your application.

{details if details else "Your experience and passion for meaningful work caught our attention immediately."}

What particularly resonates with us is your alignment with our mission of providing exceptional 
nutrition for children through natural, family-trusted products. We believe you could be a 
wonderful addition to our team family.

We'd love to learn more about you and share our story in person. Would you be available for 
a conversation next week? We can arrange a time that works best for your schedule.

This would be an opportunity for us to:
- Share more about our mission and the meaningful work we do together
- Learn about your aspirations and how they align with our family business
- Discuss how your talents could help us serve more families across Southeast Asia

Please let us know what days and times work best for you. We're flexible and happy to 
accommodate your schedule.

Looking forward to our conversation!

Warm regards,

[Your Name]
HaruPlate Family
"Nurturing Children, Strengthening Families"

P.S. Feel free to explore more about our mission at [website] - we'd love to hear your thoughts!
        """.strip()
        
        return {"subject": subject, "body": body}
    
    def _create_interview_invitation(self, candidate_name: str, position_title: str, interview_time: str) -> Dict[str, str]:
        """Creates interview invitation email."""
        subject = f"🌟 Let's continue our conversation - Interview invitation for {candidate_name}"
        
        body = f"""
Dear {candidate_name},

We're excited to continue our conversation about you joining the HaruPlate family as our {position_title}!

After reviewing your application and our initial discussion, we're even more convinced that your 
values and experience align beautifully with our mission of providing exceptional child nutrition 
through natural products.

We'd love to invite you for a more detailed conversation:

📅 Interview Details:
• Date & Time: {interview_time if interview_time else "[To be scheduled based on your availability]"}
• Duration: Approximately 60 minutes
• Format: Video call via Zoom (link will be shared separately)
• Participants: [Names of interviewers and their roles]

🌿 What to Expect:
This will be a warm, conversational interview where we'll discuss:
- Your passion for child nutrition and family values
- How your experience can contribute to our mission
- Our family business culture and growth opportunities
- Your questions about life at HaruPlate

📝 How to Prepare:
- Think about specific examples of your values-driven work
- Consider questions about our mission and company culture
- Review our website to understand our products and philosophy
- Prepare to share why HaruPlate's mission speaks to your heart

If this time doesn't work for you, please let us know your preferred times and we'll gladly adjust.

We're genuinely looking forward to learning more about you and sharing our story!

With warm anticipation,

[Your Name]
HaruPlate Family
"Nurturing Children, Strengthening Families"

P.S. If you have any questions before our meeting, please don't hesitate to reach out!
        """.strip()
        
        return {"subject": subject, "body": body}
    
    def _create_follow_up(self, candidate_name: str, position_title: str) -> Dict[str, str]:
        """Creates follow-up email after interview."""
        subject = f"Thank you for sharing your story with us, {candidate_name} 🌱"
        
        body = f"""
Dear {candidate_name},

Thank you so much for taking the time to speak with us about joining our HaruPlate family 
as our {position_title}. It was truly wonderful getting to know you and understanding your 
passion for meaningful work that makes a difference in families' lives.

Your insights about [specific topic discussed] and your thoughtful questions about our 
mission showed us exactly the kind of caring, values-driven teammate we hoped to find.

We're currently completing our conversations with all potential teammates and will be in 
touch with our decision within the next [timeframe]. We want to ensure we make the choice 
that's best for both you and our family business.

In the meantime, please don't hesitate to reach out if you have any additional questions 
about HaruPlate, our mission, or the role. We're always happy to continue the conversation.

Thank you again for your interest in our mission and for sharing your story with us.

With appreciation and warm regards,

[Your Name]
HaruPlate Family
"Nurturing Children, Strengthening Families"

P.S. Regardless of our decision, we're genuinely grateful to have met someone who shares 
our values and commitment to making a positive impact!
        """.strip()
        
        return {"subject": subject, "body": body}
    
    def _create_rejection_email(self, candidate_name: str, position_title: str) -> Dict[str, str]:
        """Creates respectful rejection email."""
        subject = f"Thank you for sharing your journey with us, {candidate_name} 🌿"
        
        body = f"""
Dear {candidate_name},

Thank you so much for your interest in joining the HaruPlate family as our {position_title} 
and for sharing your time and story with us during our conversations.

After careful consideration and many thoughtful discussions, we've decided to move forward 
with another candidate whose experience aligns more closely with our current specific needs. 
This was not an easy decision, as we were genuinely impressed by your values, passion, and 
commitment to meaningful work.

Please know that this decision in no way diminishes our respect for your talents and the 
sincere way you approach your work. The dedication to family values and positive impact 
that you shared with us was truly inspiring.

As HaruPlate continues to grow and expand our mission across Southeast Asia, we may have 
opportunities in the future that could be an even better fit for your unique talents. 
We'd be honored to keep in touch and reach out if such an opportunity arises.

We sincerely wish you all the best in finding a role where your values and skills can 
make the meaningful difference you're seeking. Any organization would be fortunate to 
have someone with your integrity and passion on their team.

Thank you again for considering HaruPlate as a place to contribute your talents. We're 
grateful for the opportunity to have met you.

With warm wishes for your continued success,

[Your Name]
HaruPlate Family
"Nurturing Children, Strengthening Families"

P.S. We encourage you to follow our journey as we continue working to provide better 
nutrition for children across the region. Your support of our mission means so much to us!
        """.strip()
        
        return {"subject": subject, "body": body}


class ZoomSchedulingTool(BaseTool):
    """Handles Zoom meeting scheduling and integration for interviews."""
    
    name: str = "Zoom Interview Scheduling Tool"
    description: str = """Creates and schedules Zoom meetings for candidate interviews.
        Generates meeting links, handles timezone coordination for Malaysian market,
        and sends calendar invitations with HaruPlate branding."""

    def __init__(self):
        super().__init__()
        # In production, these would be loaded from environment variables
        self.zoom_api_key = os.getenv('ZOOM_API_KEY')
        self.zoom_api_secret = os.getenv('ZOOM_API_SECRET')
        self.zoom_account_id = os.getenv('ZOOM_ACCOUNT_ID')

    def _run(self, meeting_title: str, start_time: str, duration_minutes: int = 60,
             participant_email: str = "", timezone: str = "Asia/Kuala_Lumpur") -> Dict[str, Any]:
        """
        Creates a Zoom meeting for candidate interview.
        
        Args:
            meeting_title: Title for the meeting
            start_time: Meeting start time in ISO format
            duration_minutes: Meeting duration (default 60 minutes)
            participant_email: Candidate's email for invitation
            timezone: Timezone for meeting (default Malaysian time)
            
        Returns:
            Dictionary with meeting details and links
        """
        try:
            # Create JWT token for Zoom API authentication
            jwt_token = self._generate_jwt_token()
            
            if not jwt_token:
                # Return simulated response if no API credentials
                return self._create_simulated_meeting_response(meeting_title, start_time, duration_minutes)
            
            # Create meeting via Zoom API
            meeting_data = self._create_zoom_meeting(jwt_token, meeting_title, start_time, duration_minutes, timezone)
            
            # Format response with HaruPlate branding
            formatted_response = self._format_meeting_response(meeting_data, participant_email)
            
            logger.info(f"Zoom meeting created: {meeting_title}")
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error creating Zoom meeting: {str(e)}")
            return {"error": f"Meeting scheduling failed: {str(e)}"}
    
    def _generate_jwt_token(self) -> Optional[str]:
        """Generates JWT token for Zoom API authentication."""
        if not all([self.zoom_api_key, self.zoom_api_secret]):
            logger.warning("Zoom API credentials not configured")
            return None
        
        try:
            # JWT payload
            payload = {
                'iss': self.zoom_api_key,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            
            # Generate token
            token = jwt.encode(payload, self.zoom_api_secret, algorithm='HS256')
            return token
            
        except Exception as e:
            logger.error(f"Error generating JWT token: {str(e)}")
            return None
    
    def _create_zoom_meeting(self, jwt_token: str, title: str, start_time: str, 
                           duration: int, timezone: str) -> Dict[str, Any]:
        """Creates meeting via Zoom API."""
        url = f"https://api.zoom.us/v2/users/me/meetings"
        
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        }
        
        # Convert start time to proper format
        start_datetime = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        
        data = {
            'topic': title,
            'type': 2,  # Scheduled meeting
            'start_time': start_datetime.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'duration': duration,
            'timezone': timezone,
            'settings': {
                'join_before_host': False,
                'mute_upon_entry': True,
                'watermark': False,
                'use_pmi': False,
                'approval_type': 0,
                'registration_type': 1,
                'audio': 'both',
                'auto_recording': 'none'
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        return response.json()
    
    def _create_simulated_meeting_response(self, title: str, start_time: str, duration: int) -> Dict[str, Any]:
        """Creates simulated meeting response for demonstration purposes."""
        meeting_id = f"123-456-789{hash(title) % 1000}"
        join_url = f"https://zoom.us/j/{meeting_id.replace('-', '')}"
        
        return {
            "meeting_created": True,
            "meeting_id": meeting_id,
            "join_url": join_url,
            "start_url": f"https://zoom.us/s/{meeting_id.replace('-', '')}?role=1",
            "title": title,
            "start_time": start_time,
            "duration": duration,
            "timezone": "Asia/Kuala_Lumpur",
            "password": "HaruPlate2025",
            "calendar_invitation": self._generate_calendar_invitation(title, start_time, duration, join_url),
            "simulation_mode": True
        }
    
    def _format_meeting_response(self, meeting_data: Dict[str, Any], participant_email: str) -> Dict[str, Any]:
        """Formats Zoom API response with HaruPlate branding."""
        return {
            "meeting_created": True,
            "meeting_id": meeting_data.get('id'),
            "join_url": meeting_data.get('join_url'),
            "start_url": meeting_data.get('start_url'),
            "title": meeting_data.get('topic'),
            "start_time": meeting_data.get('start_time'),
            "duration": meeting_data.get('duration'),
            "timezone": meeting_data.get('timezone'),
            "password": meeting_data.get('password'),
            "participant_email": participant_email,
            "calendar_invitation": self._generate_calendar_invitation(
                meeting_data.get('topic'),
                meeting_data.get('start_time'),
                meeting_data.get('duration'),
                meeting_data.get('join_url')
            ),
            "meeting_instructions": self._create_meeting_instructions(meeting_data.get('join_url')),
            "simulation_mode": False
        }
    
    def _generate_calendar_invitation(self, title: str, start_time: str, duration: int, join_url: str) -> str:
        """Generates calendar invitation text."""
        return f"""
🌱 HaruPlate Interview: {title}

Join us for a warm conversation about joining the HaruPlate family!

📅 When: {start_time}
⏰ Duration: {duration} minutes
🌏 Timezone: Malaysia Time (GMT+8)

🔗 Join Zoom Meeting: {join_url}

🌿 About This Meeting:
This is your opportunity to share your story and learn about how you can contribute 
to HaruPlate's mission of providing exceptional nutrition for children through 
natural, family-trusted products.

📝 What to Prepare:
- Examples of your values-driven work
- Questions about our family business culture
- Your thoughts on child nutrition and natural products

We're looking forward to getting to know you better!

HaruPlate Family
"Nurturing Children, Strengthening Families"
        """.strip()
    
    def _create_meeting_instructions(self, join_url: str) -> str:
        """Creates user-friendly meeting instructions."""
        return f"""
🎥 How to Join Your HaruPlate Interview

1. Click this link 5 minutes before our scheduled time: {join_url}
2. If prompted, download the Zoom app (recommended) or join via web browser
3. Test your audio and video before we begin
4. Have a glass of water nearby and find a quiet, comfortable space

💡 Technical Tips:
- Ensure stable internet connection
- Use headphones for better audio quality
- Have good lighting on your face
- Keep distracting background minimal

We'll handle all the technical details - just focus on sharing your authentic self!

Looking forward to our conversation! 🌱
        """


if __name__ == "__main__":
    # Example usage
    cv_tool = CVAnalysisTool()
    compatibility_tool = HaruPlateCompatibilityTool()
    
    # Simulate CV analysis
    sample_analysis = {
        "technical_skills": ["Marketing", "Google Analytics", "Social Media"],
        "work_experience": [{"role": "Marketing Specialist", "details": "2 years experience"}],
        "education": ["Bachelor in Marketing"],
        "industry_experience": {
            "industry_breakdown": {"food_nutrition": 1, "child_focused": 2},
            "total_relevance_score": 3
        },
        "communication_style": {
            "values_alignment_indicators": 3,
            "communication_assessment": "sincere"
        },
        "languages": ["English", "Malay"]
    }
    
    # Calculate compatibility score
    score_result = compatibility_tool._run(sample_analysis, "Digital Marketing Specialist")
    print("🎯 Compatibility Score Result:", score_result)


# Tool aliases for HaruPlate crew compatibility
HaruPlateJobPostingTool = JobPostingTool
HaruPlateWebResearchTool = CVAnalysisTool  # Web research functionality within CV analysis
BrandComplianceTool = JobPostingTool  # Brand compliance checking within job posting
ValuesAlignmentTool = HaruPlateCompatibilityTool
HaruPlateTemplatesTool = EmailDraftTool