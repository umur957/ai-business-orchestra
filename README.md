# 🎼 AI Business Orchestra

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.177.0-orange.svg)](https://github.com/joaomdmoura/crewAI)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/umur957/ai-business-orchestra/graphs/commit-activity)

A powerful multi-agent AI system for business automation using CrewAI framework. Transform your business operations with intelligent agents that can handle HR processes, administrative tasks, and complex decision-making scenarios.

## ✨ Features

- **🤖 Multi-Agent System**: Coordinated AI agents working together
- **👥 HR Agent**: Recruitment, candidate evaluation, and HR processes
- **📋 Admin Agent**: Administrative tasks and process management  
- **🎯 Conductor Agent**: Orchestrates and coordinates agent activities
- **🔄 Dual Mode**: Simulation mode for testing + real AI mode for production
- **🔧 Easy Configuration**: Simple environment variable setup
- **📊 Detailed Reporting**: Comprehensive task execution reports

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- OpenAI API key or Google Gemini API key

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
   # For minimal installation
   pip install -r requirements-clean.txt
   
   # For full development environment
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

### Configuration

Edit the `.env` file with your API credentials:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Google Gemini Configuration  
GOOGLE_API_KEY=your_google_api_key_here

# System Configuration
USE_SIMULATION=False  # Set to True for testing without real AI calls
DEFAULT_LLM=openai    # Options: openai, gemini
```

## 💼 Usage

### Basic Usage

```python
from orchestra import BusinessOrchestra

# Initialize the orchestra
orchestra = BusinessOrchestra()

# Process different types of requests
hr_result = orchestra.process_request("We need to hire a Senior Python Developer")
admin_result = orchestra.process_request("Process this week's invoices")
```

### Scenario-Based Usage

```python
# Use specific scenarios for targeted responses
recruitment = orchestra.run_scenario("recruitment", 
    "Senior AI Engineer - 5+ years ML experience required")

admin_task = orchestra.run_scenario("admin_task", 
    "Organize quarterly board meeting for 50 attendees")

crisis = orchestra.run_scenario("crisis_management", 
    "Critical system outage affecting customer payments")

daily_ops = orchestra.run_scenario("daily_operations", 
    "Coordinate today's schedule and priority tasks")
```

### Command Line Usage

```bash
# Run the built-in demo
python orchestra.py

# Test all functionality
python -c "from orchestra import BusinessOrchestra; o=BusinessOrchestra(); print(o.process_request('Test system'))"
```

## 🎯 Supported Scenarios

| Scenario Type | Description | Use Cases |
|---------------|-------------|-----------|
| `recruitment` | HR and talent acquisition | Job postings, candidate evaluation, hiring strategy |
| `admin_task` | Administrative operations | Document processing, meeting organization, data analysis |
| `crisis_management` | Emergency response | System outages, customer issues, urgent situations |
| `daily_operations` | Routine coordination | Task scheduling, priority management, team coordination |

## 🔧 Architecture

```
AI Business Orchestra
├── 🎯 Conductor Agent     # Main coordinator and orchestrator
├── 👥 HR Specialist       # Recruitment and human resources
└── 📋 Admin Specialist    # Administrative and operational tasks
```

### Agent Responsibilities

- **Conductor**: Analyzes requests, delegates tasks, ensures alignment with company values
- **HR Specialist**: Handles recruitment, job descriptions, candidate evaluation
- **Admin Specialist**: Manages documents, finances, meetings, and operational tasks

## 🛠️ Configuration Options

### Environment Variables

```env
# Core Settings
COMPANY_NAME=Your Company Name
COMPANY_CULTURE_VALUES=professional, innovative, customer-focused
COMPANY_TONE_OF_VOICE=professional, friendly, solution-oriented

# AI Configuration
OPENAI_API_KEY=sk-your-openai-key
GOOGLE_API_KEY=your-google-api-key
USE_SIMULATION=True|False
DEFAULT_LLM=openai|gemini

# Advanced Settings
CREWAI_VERBOSE=True|False
PROCESS_TYPE=sequential|hierarchical
```

### Simulation Mode

For testing without API costs:

```env
USE_SIMULATION=True
```

This provides realistic mock responses without calling external AI APIs.

## 📦 Dependencies

### Minimal Requirements (`requirements-clean.txt`)
- `crewai==0.177.0` - Multi-agent framework
- `openai==1.57.2` - OpenAI API client
- `google-generativeai==0.8.3` - Google Gemini API
- `python-dotenv==1.0.1` - Environment configuration

### Full Development (`requirements.txt`)
All minimal requirements plus development and testing tools.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Umur Kızıldaş** ([@umur957](https://github.com/umur957))

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [OpenAI](https://openai.com/) for GPT models
- [Google](https://ai.google.dev/) for Gemini models

## 📈 Roadmap

- [ ] Web interface for easy interaction
- [ ] Integration with popular business tools (Slack, Notion, etc.)
- [ ] Custom workflow creation
- [ ] Advanced reporting and analytics
- [ ] Multi-language support

---

*Transform your business operations with intelligent automation. Let the AI Business Orchestra handle routine tasks while you focus on strategic growth.*
