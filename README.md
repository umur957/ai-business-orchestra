# 🎼 HaruPlate HR & Admin Intelligence Orchestra

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.177.0-orange.svg)](https://github.com/joaomdmoura/crewAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*"Sincere, Family-Oriented AI for Child Nutrition Business Excellence"*

A comprehensive AI-powered business automation system specifically designed for HaruPlate - enabling management to focus on strategic thinking, product development, and brand vision while AI handles repetitive HR and administrative tasks.

## 🌱 Project Philosophy

**HaruPlate's Core Mission:** Like the founders of HaruPlate, managers should dedicate their time to strategic thinking, product development, and the brand vision—not to repetitive, time-consuming HR and administrative tasks.

This project embodies HaruPlate's values:
- **Sincere, family-oriented** approach to all communications
- **Child nutrition and natural products** mission focus
- **Malaysian market** cultural sensitivity
- **"Teammates"** terminology (not "candidates" or "employees")
- **Values-first** compatibility scoring (60% values + 40% technical skills)

## 🎼 Orchestra Architecture

### Orchestra Conductor (Main Orchestrator)
The brain of the system using **CrewAI Flows** for workflow orchestration:
- Analyzes requests in natural language
- Routes to appropriate expert crews (HR or Admin)
- Manages human-in-the-loop approval workflows
- Consolidates results with HaruPlate brand compliance

### 👥 HR Expert Crew (4 Specialized Agents)
Based on [crewAI-examples/recruitment](https://github.com/crewAIInc/crewAI-examples/tree/main/crews/recruitment) patterns:

1. **Recruitment Strategist** - Creates job descriptions reflecting HaruPlate's values
2. **Profile Analyst** - 60/40 scoring system (values alignment + technical skills)
3. **Communications Coordinator** - Warm, family-oriented outreach via Gmail/Zoom
4. **Quality Control Specialist** - Brand compliance ("teammates" not "candidates")

### 🏢 Admin Expert Crew (4 Specialized Agents)
Based on [umur957](https://github.com/umur957) automation patterns:

1. **Financial Document Processor** - Malaysian supplier invoice automation → Google Sheets
2. **Digital Archivist** - AI-powered document organization (inspired by [Custodian](https://github.com/umur957/Custodian))
3. **Meeting Assistant** - Strategic briefings for child nutrition industry meetings
4. **Data Analyst** - Singapore/Malaysia market insights from business data

## 🔧 Real API Integrations

Based on [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps) integration patterns:

- **Gmail API** - Invoice processing and recruitment communications
- **Google Sheets** - Financial data and expense categorization with Malaysian supplier focus
- **Zoom API** - Interview scheduling and meeting coordination
- **Google Drive** - Document archival and HaruPlate-compliant organization

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
   pip install -r requirements-haruplate.txt
   ```

4. **Set up environment variables** (optional for real API integration)
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

### Quick Start

Run the HaruPlate Orchestra:

```bash
python haruplate_orchestra.py
```

Or run the comprehensive test:

```bash
python test_haruplate_complete.py
```

## 💡 Usage Examples

### HR Scenario: Digital Marketing Specialist Recruitment
```python
request = "We need to find an experienced Digital Marketing Specialist for the Malaysian market who understands child nutrition."
result = orchestra.process_request(request)
```

### Admin Scenario: Invoice Processing
```python
request = "Process the latest invoices from our Malaysian suppliers and organize them in Google Sheets."
result = orchestra.process_request(request)
```

### Meeting Preparation
```python
request = "Prepare a briefing for tomorrow's strategy meeting about expanding our child nutrition products in Singapore."
result = orchestra.process_request(request)
```

### Data Analysis
```python
request = "Which was our most popular child nutrition product in Singapore this quarter?"
result = orchestra.process_request(request)
```

## 📁 Project Structure

```
ai-business-orchestra/
├── haruplate_orchestra.py          # Main entry point
├── test_haruplate_complete.py      # Comprehensive test suite
├── src/
│   ├── flows/
│   │   └── haruplate_orchestra_flow.py  # CrewAI Flow orchestration
│   ├── crews/
│   │   ├── haruplate_hr_crew.py         # HR Expert Crew
│   │   └── haruplate_admin_crew.py      # Admin Expert Crew
│   └── tools/
│       └── real_api_integrations.py     # Gmail, Zoom, Sheets, Drive APIs
├── config/
│   ├── haruplate_hr_agents.yaml        # HR agent configurations
│   ├── haruplate_hr_tasks.yaml         # HR task definitions
│   ├── haruplate_admin_agents.yaml     # Admin agent configurations
│   └── haruplate_admin_tasks.yaml      # Admin task definitions
└── requirements-haruplate.txt          # Project dependencies
```

## 🎯 Key Features

### HaruPlate-Specific Implementation
- **Brand Compliance**: Automatic checking for HaruPlate tone and terminology
- **Malaysian Market Focus**: Cultural sensitivity and local supplier prioritization
- **Values-Based Scoring**: 60% values alignment + 40% technical skills for recruitment
- **Family-Oriented Communication**: Warm, sincere tone in all outreach
- **Child Nutrition Focus**: Industry-specific knowledge and categorization

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

This is a specialized system for HaruPlate's business needs. For general business automation, see the base project patterns above.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- CrewAI framework for multi-agent orchestration
- HaruPlate team for business requirements and values
- Open source community for integration patterns and tools

---

*Built with ❤️ for HaruPlate's mission of providing sincere, family-oriented child nutrition solutions.*
