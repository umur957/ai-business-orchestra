"""
Admin Agent Module  
Specialized agent for administrative and operational tasks
"""

import os
import yaml
from crewai import Agent
from typing import Dict, Any

class AdminAgent:
    """Administrative Specialist Agent for operational tasks"""
    
    def __init__(self, config_path: str = "config/agents.yaml"):
        self.config = self._load_config(config_path)
        self.agent = self._create_agent()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load agent configuration from YAML file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                return config.get('admin_specialist', {})
        except FileNotFoundError:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Default configuration if YAML file not found"""
        return {
            'role': 'Administrative Operations Specialist',
            'goal': 'Manage all administrative tasks efficiently',
            'backstory': 'Expert administrative professional with operational expertise',
            'verbose': True,
            'allow_delegation': False,
            'max_iter': 3,
            'memory': True
        }
    
    def _create_agent(self) -> Agent:
        """Create the Admin agent with configuration"""
        return Agent(
            role=self.config.get('role'),
            goal=self.config.get('goal'),
            backstory=self.config.get('backstory'),
            verbose=self.config.get('verbose', True),
            allow_delegation=self.config.get('allow_delegation', False),
            max_iter=self.config.get('max_iter', 3),
            memory=self.config.get('memory', True)
        )
    
    def get_agent(self) -> Agent:
        """Return the configured agent"""
        return self.agent
