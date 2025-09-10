"""
Conductor Agent Module
Central orchestrator for coordinating all business operations
"""

import os
import yaml
from crewai import Agent
from typing import Dict, Any

class ConductorAgent:
    """Conductor Agent for orchestrating business operations"""
    
    def __init__(self, config_path: str = "config/agents.yaml"):
        self.config = self._load_config(config_path)
        self.agent = self._create_agent()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load agent configuration from YAML file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                return config.get('conductor', {})
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration if YAML file not found"""
        return {
            'role': 'Business Orchestra Conductor',
            'goal': 'Coordinate and orchestrate all business operations',
            'backstory': 'Central intelligence system for business automation',
            'verbose': True,
            'allow_delegation': True,
            'max_iter': 5,
            'memory': True
        }
    
    def _create_agent(self) -> Agent:
        """Create the Conductor agent with configuration"""
        return Agent(
            role=self.config.get('role'),
            goal=self.config.get('goal'),
            backstory=self.config.get('backstory'),
            verbose=self.config.get('verbose', True),
            allow_delegation=self.config.get('allow_delegation', True),
            max_iter=self.config.get('max_iter', 5),
            memory=self.config.get('memory', True)
        )
    
    def get_agent(self) -> Agent:
        """Return the configured agent"""
        return self.agent
