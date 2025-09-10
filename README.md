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

## 🚀 Quick Start

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

# Run a business scenario
result = orchestra.run_scenario(
    scenario_type="recruitment",
    context="We need to hire a Senior Python Developer"
)

print(result)
```

### Available Scenarios

- **recruitment**: Full recruitment process with candidate evaluation
- **admin_task**: Administrative task handling and process management
- **crisis_management**: Emergency response and crisis handling
- **daily_operations**: Routine business operations coordination

### Command Line Usage

```bash
# Run recruitment scenario
python orchestra.py

# The system will prompt you for scenario type and context
```

## 🏗️ Architecture

The system consists of three main AI agents:

### 👥 HR Agent
- **Role**: Human Resources Specialist
- **Responsibilities**: Recruitment, candidate evaluation, HR policies
- **Tools**: Profile analysis, interview coordination, documentation

### 📋 Admin Agent  
- **Role**: Administrative Coordinator
- **Responsibilities**: Process management, documentation, scheduling
- **Tools**: Task organization, workflow optimization, reporting

### 🎯 Conductor Agent
- **Role**: Orchestra Conductor  
- **Responsibilities**: Agent coordination, task delegation, quality assurance
- **Tools**: Agent communication, workflow orchestration, performance monitoring

## 🔧 Development

### Project Structure

```
ai-business-orchestra/
├── orchestra.py          # Main application
├── requirements.txt      # Full dependencies
├── requirements-clean.txt # Minimal dependencies
├── .env.example         # Environment template
├── LICENSE              # MIT License
└── README.md           # This file
```

### Adding New Scenarios

1. Define the scenario in the `run_scenario` method
2. Create specific tasks for each agent
3. Configure the crew with appropriate agents and tasks
4. Test in simulation mode first

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Examples

### Recruitment Process

```python
orchestra = BusinessOrchestra()
result = orchestra.run_scenario(
    scenario_type="recruitment",
    context="Senior Full-Stack Developer position for fintech startup"
)
```

### Crisis Management

```python
orchestra = BusinessOrchestra()
result = orchestra.run_scenario(
    scenario_type="crisis_management", 
    context="System outage affecting customer transactions"
)
```

### Administrative Task

```python
orchestra = BusinessOrchestra()
result = orchestra.run_scenario(
    scenario_type="admin_task",
    context="Organize quarterly team building event for 50 employees"
)
```

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your API keys are correctly set in `.env`
2. **Import Errors**: Make sure all dependencies are installed
3. **Rate Limiting**: Use simulation mode for testing to avoid API limits

### Debug Mode

Set `USE_SIMULATION=True` in `.env` to run without real API calls for testing.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Umur Kızıldaş**

- GitHub: [@umur957](https://github.com/umur957)

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the amazing multi-agent framework
- [OpenAI](https://openai.com/) for GPT models
- [Google](https://ai.google.dev/) for Gemini models

## 📊 Project Status

This project is actively maintained. Feel free to open issues or contribute!

---

**Made with ❤️ for business automation**
