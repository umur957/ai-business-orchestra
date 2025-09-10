"""
HaruPlate Core Tools
Brand identity, web research, and company-specific utilities.
"""

import os
import logging
import requests
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class HaruPlateTools:
    """Collection of HaruPlate-specific tools and utilities."""
    
    def __init__(self):
        self.brand_identity = {
            "company_name": "HaruPlate",
            "mission": "Providing the best nutrition for children through natural, healthy products",
            "tone": "sincere, healthy, family-oriented",
            "values": [
                "child nutrition excellence",
                "natural product focus",
                "family-first approach", 
                "sincere communication",
                "healthy living promotion"
            ],
            "target_markets": ["Malaysia", "Southeast Asia"],
            "preferred_terminology": {
                "candidates": "teammates",
                "employees": "team family",
                "hiring": "welcoming new family members",
                "job": "mission opportunity",
                "company": "HaruPlate family",
                "customers": "families we serve",
                "products": "nutrition solutions"
            },
            "brand_voice_guidelines": {
                "do_use": [
                    "genuine", "sincere", "family", "natural", "trusted",
                    "mission", "together", "caring", "quality", "transparent"
                ],
                "avoid": [
                    "corporate", "leverage", "synergy", "disrupt", "aggressive",
                    "cheap", "fast", "mass-produced", "artificial"
                ]
            }
        }


class HaruPlateWebResearchTool(BaseTool):
    """Researches HaruPlate's web presence and competitor landscape."""
    
    name: str = "HaruPlate Web Research Tool"
    description: str = """Conducts web research about HaruPlate's online presence,
        competitor analysis, and market intelligence for the natural child nutrition
        sector in Malaysia and Southeast Asia."""

    def _run(self, research_topic: str, market_focus: str = "Malaysia") -> Dict[str, Any]:
        """
        Conducts web research on HaruPlate-related topics.
        
        Args:
            research_topic: What to research about
            market_focus: Geographic market to focus on
            
        Returns:
            Dictionary with research findings and insights
        """
        try:
            # Simulate comprehensive research results
            # In production, this would use real web scraping or search APIs
            
            research_results = {
                "research_topic": research_topic,
                "market_focus": market_focus,
                "findings": self._generate_research_findings(research_topic, market_focus),
                "competitive_landscape": self._analyze_competitive_landscape(market_focus),
                "market_opportunities": self._identify_market_opportunities(research_topic, market_focus),
                "brand_positioning_insights": self._analyze_brand_positioning(research_topic),
                "recommendations": self._generate_recommendations(research_topic, market_focus)
            }
            
            logger.info(f"Web research completed for: {research_topic} in {market_focus}")
            return research_results
            
        except Exception as e:
            logger.error(f"Error conducting web research: {str(e)}")
            return {"error": f"Web research failed: {str(e)}"}
    
    def _generate_research_findings(self, topic: str, market: str) -> List[Dict[str, str]]:
        """Generates simulated research findings based on topic."""
        
        if "job" in topic.lower() or "recruitment" in topic.lower():
            return [
                {
                    "source": "LinkedIn Malaysia Jobs",
                    "finding": "High demand for digital marketing specialists with food industry experience",
                    "relevance": "Direct competitor for talent acquisition"
                },
                {
                    "source": "JobStreet Malaysia",
                    "finding": "Average salary for marketing roles in FMCG sector: RM4,500-7,000",
                    "relevance": "Market rate for competitive compensation"
                },
                {
                    "source": "Glassdoor Reviews",
                    "finding": "Candidates value company mission and work-life balance over pure salary",
                    "relevance": "Supports HaruPlate's values-first approach"
                }
            ]
        elif "market" in topic.lower() or "competitor" in topic.lower():
            return [
                {
                    "source": "Euromonitor Malaysia Baby Food Report",
                    "finding": "Natural/organic baby food segment growing 15% annually",
                    "relevance": "Strong market tailwind for HaruPlate positioning"
                },
                {
                    "source": "Local parenting forums",
                    "finding": "Malaysian parents increasingly concerned about artificial additives",
                    "relevance": "Validates HaruPlate's natural product focus"
                },
                {
                    "source": "Retail distribution analysis",
                    "finding": "Premium positioning requires strong online and specialty retail presence",
                    "relevance": "Distribution strategy implications"
                }
            ]
        else:
            return [
                {
                    "source": "Industry publications",
                    "finding": f"Research insights relevant to {topic}",
                    "relevance": "Market intelligence for strategic decisions"
                }
            ]
    
    def _analyze_competitive_landscape(self, market: str) -> Dict[str, Any]:
        """Analyzes competitive landscape in the specified market."""
        
        if market.lower() == "malaysia":
            return {
                "direct_competitors": [
                    {
                        "name": "Nestlé Malaysia",
                        "strengths": ["Market leader", "Distribution network", "Brand recognition"],
                        "weaknesses": ["Large corporation feel", "Less focus on natural ingredients"],
                        "positioning": "Mainstream nutrition solutions"
                    },
                    {
                        "name": "Abbott Malaysia", 
                        "strengths": ["Medical backing", "Premium positioning"],
                        "weaknesses": ["High price point", "Limited natural focus"],
                        "positioning": "Medical nutrition approach"
                    }
                ],
                "indirect_competitors": [
                    {
                        "name": "Local organic food brands",
                        "strengths": ["Natural focus", "Local connection"],
                        "weaknesses": ["Limited distribution", "Smaller scale"],
                        "positioning": "Artisanal natural products"
                    }
                ],
                "market_gaps": [
                    "Family-oriented natural nutrition brand",
                    "Sincere, non-corporate communication",
                    "Local understanding with international quality"
                ]
            }
        else:
            return {
                "analysis": f"Competitive landscape analysis for {market}",
                "note": "Market-specific competitive intelligence would be gathered here"
            }
    
    def _identify_market_opportunities(self, topic: str, market: str) -> List[str]:
        """Identifies market opportunities based on research topic."""
        
        opportunities = [
            "Growing demand for natural child nutrition products",
            "Increasing parental awareness of ingredient quality",
            "Gap for family-oriented brand communication in the sector"
        ]
        
        if "recruitment" in topic.lower():
            opportunities.extend([
                "Attract talent who value meaningful work over pure compensation",
                "Appeal to professionals interested in child welfare",
                "Leverage family business culture as competitive advantage"
            ])
        
        if market.lower() == "malaysia":
            opportunities.extend([
                "Strong local market presence as expansion base",
                "Cultural understanding advantage over international brands",
                "Government support for local food innovation"
            ])
        
        return opportunities
    
    def _analyze_brand_positioning(self, topic: str) -> Dict[str, Any]:
        """Analyzes brand positioning insights."""
        
        return {
            "current_positioning": "Family-first natural nutrition specialist",
            "differentiators": [
                "Sincere, non-corporate communication style",
                "Focus on child nutrition rather than just general health",
                "Family business values and transparency",
                "Natural product specialization"
            ],
            "brand_strengths": [
                "Authentic family business story",
                "Clear mission alignment with customer values",
                "Growing natural products market trend"
            ],
            "positioning_recommendations": [
                "Emphasize local understanding with international quality standards",
                "Highlight family business authenticity vs corporate competitors",
                "Focus on partnership with parents rather than just product sales"
            ]
        }
    
    def _generate_recommendations(self, topic: str, market: str) -> List[str]:
        """Generates actionable recommendations based on research."""
        
        recommendations = []
        
        if "recruitment" in topic.lower():
            recommendations.extend([
                "Emphasize mission and values in job descriptions",
                "Use local job platforms popular in Malaysia",
                "Leverage employee referrals from mission-aligned team members",
                "Highlight work-life balance and family-first culture"
            ])
        
        if "market" in topic.lower():
            recommendations.extend([
                "Develop content marketing strategy around child nutrition education",
                "Partner with local parenting influencers and pediatricians",
                "Establish presence in premium retail and online channels",
                "Create parent community engagement programs"
            ])
        
        recommendations.extend([
            f"Maintain authentic communication style when expanding in {market}",
            "Regularly research competitor activities and market trends",
            "Build strategic partnerships with complementary family-focused businesses"
        ])
        
        return recommendations


class BrandComplianceTool(BaseTool):
    """Ensures all content complies with HaruPlate's brand identity and values."""
    
    name: str = "HaruPlate Brand Compliance Checker"
    description: str = """Reviews content for compliance with HaruPlate's brand identity,
        tone of voice, and values. Checks terminology usage, cultural sensitivity,
        and alignment with family-oriented positioning."""

    def __init__(self):
        super().__init__()
        self.haruplate_tools = HaruPlateTools()
        self.brand_identity = self.haruplate_tools.brand_identity

    def _run(self, content: str, content_type: str = "general") -> Dict[str, Any]:
        """
        Checks content compliance with HaruPlate brand guidelines.
        
        Args:
            content: Content to check
            content_type: Type of content ('job_posting', 'email', 'marketing', 'general')
            
        Returns:
            Dictionary with compliance analysis and recommendations
        """
        try:
            compliance_results = {
                "content_type": content_type,
                "overall_compliance_score": 0,
                "compliance_checks": {
                    "terminology_check": self._check_terminology(content),
                    "tone_analysis": self._analyze_tone(content),
                    "values_alignment": self._check_values_alignment(content),
                    "cultural_sensitivity": self._check_cultural_sensitivity(content),
                    "brand_voice": self._check_brand_voice(content)
                },
                "issues_found": [],
                "recommendations": [],
                "approved": False
            }
            
            # Calculate overall compliance score
            compliance_results["overall_compliance_score"] = self._calculate_overall_score(
                compliance_results["compliance_checks"]
            )
            
            # Generate issues and recommendations
            compliance_results["issues_found"] = self._identify_issues(compliance_results["compliance_checks"])
            compliance_results["recommendations"] = self._generate_compliance_recommendations(
                compliance_results["compliance_checks"], content_type
            )
            
            # Determine if content is approved
            compliance_results["approved"] = compliance_results["overall_compliance_score"] >= 80
            
            logger.info(f"Brand compliance check completed. Score: {compliance_results['overall_compliance_score']}")
            return compliance_results
            
        except Exception as e:
            logger.error(f"Error checking brand compliance: {str(e)}")
            return {"error": f"Brand compliance check failed: {str(e)}"}
    
    def _check_terminology(self, content: str) -> Dict[str, Any]:
        """Checks if content uses HaruPlate's preferred terminology."""
        
        content_lower = content.lower()
        preferred_terms = self.brand_identity["preferred_terminology"]
        
        terminology_issues = []
        correct_usage = []
        
        for old_term, new_term in preferred_terms.items():
            if old_term in content_lower:
                terminology_issues.append({
                    "issue": f"Uses '{old_term}' instead of '{new_term}'",
                    "recommendation": f"Replace '{old_term}' with '{new_term}'"
                })
            elif new_term in content_lower:
                correct_usage.append(new_term)
        
        score = max(0, 100 - (len(terminology_issues) * 20))  # Deduct 20 points per issue
        
        return {
            "score": score,
            "correct_usage": correct_usage,
            "issues": terminology_issues,
            "total_issues": len(terminology_issues)
        }
    
    def _analyze_tone(self, content: str) -> Dict[str, Any]:
        """Analyzes if content matches HaruPlate's sincere, family-oriented tone."""
        
        content_lower = content.lower()
        
        # Positive tone indicators
        positive_words = [
            'family', 'sincere', 'genuine', 'care', 'trust', 'together',
            'mission', 'values', 'heart', 'meaningful', 'passionate'
        ]
        
        # Negative tone indicators (too corporate)
        negative_words = [
            'leverage', 'synergy', 'disrupt', 'aggressive', 'dominate',
            'exploit', 'maximize', 'optimize', 'competitive advantage'
        ]
        
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        # Calculate tone score
        if negative_count > 0:
            score = max(0, 60 - (negative_count * 20))  # Penalty for corporate language
        else:
            score = min(100, 60 + (positive_count * 10))  # Bonus for family-oriented language
        
        return {
            "score": score,
            "positive_indicators": positive_count,
            "negative_indicators": negative_count,
            "tone_assessment": "family-oriented" if positive_count > negative_count else "corporate" if negative_count > 0 else "neutral"
        }
    
    def _check_values_alignment(self, content: str) -> Dict[str, Any]:
        """Checks alignment with HaruPlate's core values."""
        
        content_lower = content.lower()
        values = self.brand_identity["values"]
        
        values_mentioned = []
        for value in values:
            # Check for key words from each value
            if "child nutrition" in value and any(word in content_lower for word in ['child', 'nutrition', 'health']):
                values_mentioned.append("child nutrition excellence")
            elif "natural product" in value and any(word in content_lower for word in ['natural', 'organic', 'pure']):
                values_mentioned.append("natural product focus")
            elif "family" in value and any(word in content_lower for word in ['family', 'parent', 'together']):
                values_mentioned.append("family-first approach")
            elif "sincere" in value and any(word in content_lower for word in ['sincere', 'genuine', 'honest']):
                values_mentioned.append("sincere communication")
            elif "healthy living" in value and any(word in content_lower for word in ['healthy', 'wellness', 'wellbeing']):
                values_mentioned.append("healthy living promotion")
        
        score = min(100, (len(values_mentioned) / len(values)) * 100 + 20)  # Base score + values bonus
        
        return {
            "score": score,
            "values_mentioned": values_mentioned,
            "values_coverage": f"{len(values_mentioned)}/{len(values)} values addressed"
        }
    
    def _check_cultural_sensitivity(self, content: str) -> Dict[str, Any]:
        """Checks cultural sensitivity for Malaysian and Southeast Asian markets."""
        
        content_lower = content.lower()
        
        # Positive cultural indicators
        cultural_positives = [
            'malaysia', 'malaysian', 'local', 'community', 'tradition',
            'respect', 'understanding', 'inclusive', 'diverse'
        ]
        
        # Potential cultural issues
        cultural_warnings = [
            'western', 'american', 'european', 'foreign', 'imported',
            'superior', 'advanced', 'modern vs traditional'
        ]
        
        positive_indicators = sum(1 for word in cultural_positives if word in content_lower)
        warning_indicators = sum(1 for word in cultural_warnings if word in content_lower)
        
        score = min(100, 80 + (positive_indicators * 10) - (warning_indicators * 15))
        
        return {
            "score": score,
            "cultural_awareness": positive_indicators,
            "potential_issues": warning_indicators,
            "assessment": "culturally sensitive" if warning_indicators == 0 and positive_indicators > 0 else "needs review"
        }
    
    def _check_brand_voice(self, content: str) -> Dict[str, Any]:
        """Checks adherence to HaruPlate's brand voice guidelines."""
        
        content_lower = content.lower()
        voice_guidelines = self.brand_identity["brand_voice_guidelines"]
        
        do_use_words = voice_guidelines["do_use"]
        avoid_words = voice_guidelines["avoid"]
        
        good_words_used = sum(1 for word in do_use_words if word in content_lower)
        bad_words_used = sum(1 for word in avoid_words if word in content_lower)
        
        score = min(100, 70 + (good_words_used * 5) - (bad_words_used * 15))
        
        return {
            "score": score,
            "recommended_words_used": good_words_used,
            "words_to_avoid_used": bad_words_used,
            "voice_assessment": "on-brand" if bad_words_used == 0 and good_words_used > 0 else "needs improvement"
        }
    
    def _calculate_overall_score(self, checks: Dict[str, Any]) -> float:
        """Calculates overall compliance score."""
        
        scores = [check["score"] for check in checks.values()]
        overall_score = sum(scores) / len(scores)
        
        return round(overall_score, 1)
    
    def _identify_issues(self, checks: Dict[str, Any]) -> List[str]:
        """Identifies specific compliance issues."""
        
        issues = []
        
        # Terminology issues
        term_issues = checks["terminology_check"]["issues"]
        for issue in term_issues:
            issues.append(f"Terminology: {issue['issue']}")
        
        # Tone issues
        if checks["tone_analysis"]["tone_assessment"] == "corporate":
            issues.append("Tone: Content sounds too corporate, needs more family-oriented language")
        
        # Values alignment issues
        if checks["values_alignment"]["score"] < 60:
            issues.append("Values: Content doesn't clearly reflect HaruPlate's core values")
        
        # Cultural sensitivity issues
        if checks["cultural_sensitivity"]["assessment"] == "needs review":
            issues.append("Cultural: Content may need cultural sensitivity review for Malaysian market")
        
        # Brand voice issues
        if checks["brand_voice"]["voice_assessment"] == "needs improvement":
            issues.append("Voice: Content uses words that don't align with HaruPlate's brand voice")
        
        return issues
    
    def _generate_compliance_recommendations(self, checks: Dict[str, Any], content_type: str) -> List[str]:
        """Generates specific recommendations for improvement."""
        
        recommendations = []
        
        # Terminology recommendations
        term_issues = checks["terminology_check"]["issues"]
        for issue in term_issues:
            recommendations.append(issue["recommendation"])
        
        # Tone recommendations
        if checks["tone_analysis"]["score"] < 80:
            recommendations.append("Add more warm, family-oriented language to reflect HaruPlate's sincere approach")
        
        # Values recommendations
        if checks["values_alignment"]["score"] < 70:
            recommendations.append("Include more references to child nutrition, natural products, or family values")
        
        # Cultural recommendations
        if checks["cultural_sensitivity"]["score"] < 80:
            recommendations.append("Review content for cultural appropriateness in Malaysian context")
        
        # Brand voice recommendations
        if checks["brand_voice"]["score"] < 80:
            recommendations.append("Use more words from HaruPlate's preferred vocabulary (genuine, family, mission, etc.)")
        
        # Content type specific recommendations
        if content_type == "job_posting":
            recommendations.append("Ensure job posting emphasizes mission alignment and family culture")
        elif content_type == "email":
            recommendations.append("Make email communication more personal and warm")
        elif content_type == "marketing":
            recommendations.append("Focus on how content serves families and supports child nutrition")
        
        return recommendations


class HaruPlateConfigTool(BaseTool):
    """Manages HaruPlate-specific configuration and settings."""
    
    name: str = "HaruPlate Configuration Manager"
    description: str = """Manages HaruPlate-specific settings, brand guidelines,
        and configuration parameters for consistent application across all systems."""

    def __init__(self):
        super().__init__()
        self.haruplate_tools = HaruPlateTools()

    def _run(self, config_type: str, setting_name: str = "", new_value: str = "") -> Dict[str, Any]:
        """
        Manages HaruPlate configuration settings.
        
        Args:
            config_type: Type of configuration ('brand_identity', 'terminology', 'values')
            setting_name: Specific setting to retrieve or update
            new_value: New value if updating a setting
            
        Returns:
            Dictionary with configuration information
        """
        try:
            if config_type == "brand_identity":
                return self._get_brand_identity(setting_name)
            elif config_type == "terminology":
                return self._get_terminology_guide()
            elif config_type == "values":
                return self._get_company_values()
            elif config_type == "voice_guidelines":
                return self._get_voice_guidelines()
            else:
                return {"error": f"Unknown configuration type: {config_type}"}
                
        except Exception as e:
            logger.error(f"Error accessing configuration: {str(e)}")
            return {"error": f"Configuration access failed: {str(e)}"}
    
    def _get_brand_identity(self, setting_name: str = "") -> Dict[str, Any]:
        """Returns HaruPlate's brand identity information."""
        
        brand_identity = self.haruplate_tools.brand_identity
        
        if setting_name:
            return {
                "setting": setting_name,
                "value": brand_identity.get(setting_name, "Setting not found")
            }
        else:
            return {
                "full_brand_identity": brand_identity
            }
    
    def _get_terminology_guide(self) -> Dict[str, Any]:
        """Returns HaruPlate's preferred terminology guide."""
        
        return {
            "terminology_guide": self.haruplate_tools.brand_identity["preferred_terminology"],
            "usage_instructions": [
                "Always use 'teammates' instead of 'candidates' or 'employees'",
                "Refer to 'HaruPlate family' rather than just 'company'",
                "Call positions 'mission opportunities' rather than just 'jobs'",
                "Use 'families we serve' instead of 'customers' or 'consumers'",
                "Describe hiring as 'welcoming new family members'"
            ]
        }
    
    def _get_company_values(self) -> Dict[str, Any]:
        """Returns HaruPlate's core values and their applications."""
        
        return {
            "core_values": self.haruplate_tools.brand_identity["values"],
            "value_applications": {
                "child_nutrition_excellence": "Prioritize child health and development in all decisions",
                "natural_product_focus": "Choose natural ingredients and sustainable practices",
                "family_first_approach": "Support work-life balance and family relationships",
                "sincere_communication": "Be genuine, honest, and transparent in all communications",
                "healthy_living_promotion": "Encourage and enable healthy lifestyle choices"
            }
        }
    
    def _get_voice_guidelines(self) -> Dict[str, Any]:
        """Returns HaruPlate's brand voice and communication guidelines."""
        
        return {
            "brand_voice": self.haruplate_tools.brand_identity["brand_voice_guidelines"],
            "tone_description": self.haruplate_tools.brand_identity["tone"],
            "communication_principles": [
                "Speak from the heart, not from corporate scripts",
                "Use warm, inclusive language that welcomes people",
                "Avoid jargon and speak in terms families understand",
                "Show genuine care for the people we're communicating with",
                "Be transparent about our mission and values",
                "Maintain professionalism while being authentically human"
            ]
        }


if __name__ == "__main__":
    # Example usage
    web_research = HaruPlateWebResearchTool()
    brand_compliance = BrandComplianceTool()
    
    # Test web research
    research_result = web_research._run("job market analysis", "Malaysia")
    print("🔍 Web Research Result:", research_result)
    
    # Test brand compliance
    sample_content = "We are looking for candidates to join our company and leverage synergies to disrupt the market."
    compliance_result = brand_compliance._run(sample_content, "job_posting")
    print("✅ Brand Compliance Result:", compliance_result)