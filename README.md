# 🎼 AI Business Orchestra

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.177.0-orange.svg)](https://github.com/joaomdmoura/crewAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*"Intelligent Multi-Agent Business Automation System"*

A comprehensive AI-powered business automation system that enables management to focus on strategic thinking, product development, and business vision while AI handles repetitive HR and administrative tasks.

**Author: UMUR KIZILDAS**

## 🌱 Project Philosophy

**Core Mission:** Business leaders should dedicate their time to strategic thinking, product development, and business vision—not to repetitive, time-consuming HR and administrative tasks.

This project embodies modern business automation principles:
- **Professional communication** standards
- **Flexible industry adaptation** capabilities
- **Cultural sensitivity** configurations
- **Customizable terminology** and workflows
- **Configurable scoring systems** for various business needs

## 🎼 Orchestra Architecture

### Orchestra Conductor (Main Orchestrator)
The brain of the system using **CrewAI Flows** for workflow orchestration:
- Analyzes requests in natural language
- Routes to appropriate expert crews (HR or Admin)
- Manages human-in-the-loop approval workflows
- Consolidates results with configurable business compliance

### 👥 HR Expert Crew (4 Specialized Agents)
Based on [crewAI-examples/recruitment](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment) patterns:

1. **Recruitment Strategist** - Creates job descriptions reflecting company values
2. **Profile Analyst** - Configurable scoring system (values alignment + technical skills)
3. **Communications Coordinator** - Professional outreach via Gmail/Zoom
4. **Quality Control Specialist** - Business compliance and quality assurance

### 🏢 Admin Expert Crew (4 Specialized Agents)
Based on [umur957](https://github.com/umur957) automation patterns:

1. **Financial Document Processor** - Invoice automation and processing → Google Sheets
2. **Digital Archivist** - AI-powered document organization (inspired by [Custodian](https://github.com/umur957/Custodian))
3. **Meeting Assistant** - Strategic briefings for industry meetings
4. **Data Analyst** - Market insights and business data analysis

## 🔧 Real API Integrations

Based on [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) integration patterns:

- **Gmail API** - Invoice processing and recruitment communications
- **Google Sheets** - Financial data and expense categorization
- **Zoom API** - Interview scheduling and meeting coordination
- **Google Drive** - Document archival and organization

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- CrewAI framework
- API credentials for Google services and Zoom (optional - runs in simulation mode)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/umur957/ai-business-orchestra.git
   cd ai-business-orchestra
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional for real API integration)
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

### Quick Start

Run the AI Business Orchestra:

```bash
python business_orchestra_main.py
```

## 💡 Usage Examples

### HR Scenario: Digital Marketing Specialist Recruitment
```python
request = "We need to find an experienced Digital Marketing Specialist for our target market."
result = orchestra.process_request(request)
```

### Admin Scenario: Invoice Processing
```python
request = "Process the latest invoices from our suppliers and organize them in Google Sheets."
result = orchestra.process_request(request)
```

### Meeting Preparation
```python
request = "Prepare a briefing for tomorrow's strategy meeting about expanding our products in new markets."
result = orchestra.process_request(request)
```

### Data Analysis
```python
request = "Which was our most popular product in the target market this quarter?"
result = orchestra.process_request(request)
```

## 📁 Project Structure

```
ai-business-orchestra/
├── business_orchestra_main.py          # Main entry point
├── src/
│   ├── flows/
│   │   └── business_orchestra_flow.py   # CrewAI Flow orchestration
│   ├── crews/
│   │   ├── hr_crew.py                   # HR Expert Crew
│   │   └── admin_crew.py                # Admin Expert Crew
│   └── tools/
│       └── real_api_integrations.py     # Gmail, Zoom, Sheets, Drive APIs
├── config/
│   ├── hr_agents.yaml                   # HR agent configurations
│   ├── hr_tasks.yaml                    # HR task definitions
│   ├── admin_agents.yaml                # Admin agent configurations
│   └── admin_tasks.yaml                 # Admin task definitions
└── requirements.txt                     # Project dependencies
```

## 🎯 Key Features

### Business-Focused Implementation
- **Brand Compliance**: Automatic checking for company tone and terminology
- **Market Adaptability**: Cultural sensitivity and supplier prioritization
- **Configurable Scoring**: Customizable values alignment + technical skills for recruitment
- **Professional Communication**: Consistent, professional tone in all outreach
- **Industry Flexibility**: Adaptable industry-specific knowledge and categorization

### Technical Excellence
- **CrewAI Flows**: Modern workflow orchestration with state management
- **Human-in-the-Loop**: Strategic decisions require management approval
- **Real API Integration**: Production-ready connections to business tools
- **Simulation Mode**: Full testing without external API dependencies
- **Configuration-Driven**: YAML-based agent and task management

## 📊 Test Results

**Latest Test Score: 83.3% (GOOD - Minor improvements needed)**

- ✅ HR Expert Crew: PASS
- ✅ Admin Expert Crew: PASS
- ✅ API Integrations: PASS
- ✅ API Functionality: PASS
- ✅ Main Orchestra: PASS
- ⚠️ Flow Integration: Needs refinement

## 🏗️ Architecture Inspiration

This project is built using proven patterns from leading repositories:

- **[crewAI-examples/flows](https://github.com/crewAIInc/crewAI-examples/tree/main/flows)** - Orchestration workflows
- **[crewAI-examples/recruitment](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment)** - HR processes
- **[umur957/n8n-invoice-automation](https://github.com/umur957/n8n-invoice-automation)** - Financial automation
- **[umur957/Custodian](https://github.com/umur957/Custodian)** - Document management
- **[awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)** - API integration patterns

## 🤝 Contributing

This is an open-source business automation system. Contributions are welcome! Please see the project patterns above for implementation guidance.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CrewAI framework for multi-agent orchestration
- **Author**: UMUR KIZILDAS
- Open source community for integration patterns and tools

---

*Built with ❤️ for intelligent business automation.*