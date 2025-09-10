# 🌱 HaruPlate HR & Admin Intelligence Orchestra

**"Like the founders of HaruPlate, managers should dedicate their time to strategic thinking, product development, and the brand vision—not to repetitive, time-consuming HR and administrative tasks."**

## 🎼 Project Overview

The HaruPlate HR & Admin Intelligence Orchestra is a comprehensive AI-powered business process automation system designed specifically for HaruPlate's sincere, family-oriented approach to business. This system embodies our core philosophy by automating routine tasks while maintaining the authentic, values-driven communication style that makes HaruPlate special.

### 🎯 Core Mission

Transform how HaruPlate's management spends their time by creating an AI orchestra that handles:
- **HR Processes**: Finding teammates who truly believe in our child nutrition mission
- **Administrative Tasks**: Managing finances, documents, and operations seamlessly
- **Strategic Support**: Providing insights that honor our family business values

## 🏗️ System Architecture

### 🎭 The Orchestra Conductor
The single point of contact that analyzes requests, delegates to expert teams, and ensures human approval at critical decision points.

### 👥 HR Expert Crew
- **Recruitment Strategist**: Creates HaruPlate-branded job descriptions with sincere, family-oriented tone
- **Profile Analyst**: Scores candidates on values alignment (60%) + technical skills (40%)
- **Communications Coordinator**: Drafts warm, personalized emails and schedules Zoom interviews
- **Quality Control Specialist**: Ensures all outputs authentically represent HaruPlate's brand

### 📊 Admin Expert Crew
- **Financial Document Processor**: Automates invoice processing with Malaysian supplier focus
- **Digital Archivist**: Organizes documents supporting regulatory compliance and decision-making
- **Meeting Assistant**: Prepares strategic briefings with market intelligence
- **Data Analyst**: Answers natural language questions about business data

## 🚀 Key Features

### ✨ Human-in-the-Loop Workflows
- **Approval Points**: Critical decisions always involve management review
- **Family Business Style**: Warm, collaborative approval processes, not corporate bureaucracy
- **Values Integration**: Every decision considers HaruPlate's mission and values

### 🌿 HaruPlate Brand Identity Integration
- **Terminology**: Uses "teammates" not "candidates", "HaruPlate family" not "company"
- **Tone**: Maintains sincere, family-oriented communication in all outputs
- **Values Scoring**: Prioritizes alignment with child nutrition and natural product focus
- **Cultural Sensitivity**: Optimized for Malaysian market and Southeast Asian expansion

### 🔧 Real API Integrations
- **Gmail**: Automated invoice retrieval and candidate communication
- **Google Drive**: Document archival and organization
- **Google Sheets**: Financial tracking and data management
- **Zoom**: Interview scheduling and coordination
- **Google Calendar**: Meeting preparation and research

## 📁 Project Structure

```
ai-business-orchestra/
├── 🎼 haruplate_orchestra_main.py          # Main application entry point
├── 🧪 test_haruplate_orchestra.py          # Comprehensive test suite
├── 📋 requirements-haruplate.txt           # Dependencies
├── 📖 README_HARUPLATE.md                  # This documentation
│
├── 🎵 src/
│   ├── flows/
│   │   └── orchestra_conductor.py          # Main orchestration logic
│   ├── crews/
│   │   ├── hr_crew.py                      # HR expert team
│   │   └── admin_crew.py                   # Admin expert team
│   └── tools/
│       ├── haruplate_tools.py              # Brand identity & web research
│       ├── recruitment_tools.py            # CV analysis, job posting, email
│       ├── financial_tools.py              # Invoice processing, sheets integration
│       ├── document_tools.py               # Document management
│       ├── meeting_tools.py                # Meeting preparation
│       └── data_analysis_tools.py          # Business intelligence
│
└── 🔧 config/
    ├── haruplate_agents.yaml              # Agent definitions
    └── haruplate_tasks.yaml               # Task configurations
```

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements-haruplate.txt
```

### 2. Configure Environment Variables
Create a `.env` file:
```env
# LLM API Keys
OPENAI_API_KEY=your_openai_key_here
GOOGLE_AI_API_KEY=your_gemini_key_here

# Google APIs (Gmail, Drive, Sheets)
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret

# Zoom API
ZOOM_API_KEY=your_zoom_key
ZOOM_API_SECRET=your_zoom_secret

# Optional: Simulation Mode (if no API keys)
SIMULATION_MODE=true
```

### 3. Google API Setup
1. Enable Gmail, Drive, Sheets APIs in Google Cloud Console
2. Download `credentials.json` to project root
3. Run initial authentication flow

### 4. Test Installation
```bash
python test_haruplate_orchestra.py
```

## 🎯 Usage Examples

### 👥 HR Request Example
```python
from haruplate_orchestra_main import HaruPlateOrchestra

orchestra = HaruPlateOrchestra()

# Example: Recruitment request
result = orchestra.process_request(
    request_text="Tell the HR team we need to find an experienced 'Digital Marketing Specialist' for the Malaysian market. Have them start the process.",
    requester="Founder",
    priority="high"
)

# Handle human approval
if result.get("human_approval_required"):
    print(result["approval_message"])
    
    # After management review
    approval_result = orchestra.handle_approval_response(
        request_id=result["session_info"]["request_id"],
        approved=True,
        feedback="Approved to proceed with candidate search"
    )
```

### 📊 Admin Request Example
```python
# Example: Financial processing
result = orchestra.process_request(
    request_text="Process this month's invoices from Malaysian suppliers and update our financial tracking systems.",
    requester="Operations Manager",
    priority="normal"
)

print(f"Processed: {result['results']['deliverables']}")
```

### 🎭 Mixed Workflow Example
```python
# Example: Complex coordinated request
result = orchestra.process_request(
    request_text="Prepare for Q2 planning: hire 2 marketing specialists for Malaysian expansion and analyze Q1 sales performance data.",
    requester="Management Team",
    priority="urgent"
)

# Always requires approval for complex workflows
print(result["approval_message"])
```

## 🔄 Workflow Types

### 1. HR Workflow
**Triggers**: "hire", "find", "recruit", "team member"
- Creates job descriptions with HaruPlate branding
- Develops recruitment strategy for Malaysian market
- Analyzes candidates with values-alignment scoring
- Prepares warm, personalized communications
- Ensures brand compliance throughout process

### 2. Admin Workflow
**Triggers**: "invoice", "document", "meeting", "data analysis"
- Processes financial documents and updates tracking
- Organizes regulatory and business documents
- Prepares strategic meeting briefings
- Answers natural language business intelligence questions

### 3. Mixed Workflow
**Triggers**: Multiple workflow indicators in single request
- Coordinates both HR and Admin teams
- Always requires human approval
- Provides integrated strategic recommendations

## 🎨 HaruPlate Brand Integration

### Preferred Terminology
- ✅ "Teammates" → ❌ "Candidates" or "Employees"
- ✅ "HaruPlate family" → ❌ "Company" or "Organization"
- ✅ "Mission opportunity" → ❌ "Job" or "Position"
- ✅ "Families we serve" → ❌ "Customers" or "Consumers"
- ✅ "Welcoming new family members" → ❌ "Hiring"

### Core Values Integration
1. **Child Nutrition Excellence** - Prioritized in all decision-making
2. **Natural Product Focus** - Emphasized in supplier relationships
3. **Family-First Approach** - Reflected in communication style
4. **Sincere Communication** - Authentic, non-corporate tone
5. **Healthy Living Promotion** - Integrated into all messaging

### Cultural Considerations
- Malaysian market expertise and sensitivity
- Southeast Asian expansion readiness
- Local language preferences (English, Bahasa Malaysia)
- Cultural business practices and relationship-building

## 🔍 Quality Assurance

### Brand Compliance Checking
- Automatic tone and terminology validation
- Cultural sensitivity verification
- Values alignment confirmation
- Self-evaluation loops for content refinement

### Compatibility Scoring Algorithm
**For HR candidates:**
- Technical Competence: 40%
- Values Alignment: 60%
  - Child nutrition passion
  - Natural product interest
  - Family business culture fit
  - Malaysian market understanding

## 📈 Performance Monitoring

### Key Metrics
- **HR Efficiency**: Time from job posting to quality candidate shortlist
- **Admin Automation**: Percentage of routine tasks handled without human intervention
- **Brand Compliance**: Approval rate for AI-generated content
- **Values Alignment**: Compatibility scores for new team members

### Success Indicators
- Management time freed for strategic activities
- Improved candidate quality and cultural fit
- Streamlined financial and document processes
- Maintained authentic HaruPlate communication style

## 🔧 Configuration

### Agent Customization
Edit `config/haruplate_agents.yaml` to adjust:
- Agent personalities and backstories
- HaruPlate brand context
- Preferred terminology and values
- Market focus areas

### Task Templates
Modify `config/haruplate_tasks.yaml` for:
- Workflow definitions
- Expected outputs
- Quality control criteria
- Approval point configuration

## 🚨 Security & Privacy

### Data Protection
- No sensitive data stored in logs
- API keys managed through environment variables
- Email and document access controlled through Google OAuth
- All processing maintains audit trail

### Compliance
- GDPR-ready data handling
- Malaysian personal data protection compliance
- Secure credential management
- Privacy-first document processing

## 🌱 Future Enhancements

### Planned Features
- **Multilingual Support**: Full Bahasa Malaysia integration
- **Advanced Analytics**: Predictive insights for HR and finance
- **Mobile Interface**: On-the-go management approvals
- **Integration Expansion**: CRM, accounting software, job boards
- **AI Training**: Custom models trained on HaruPlate data

### Expansion Opportunities
- **Regional Scaling**: Singapore, Thailand, Indonesia support
- **Product Categories**: Specialized agents for new product lines
- **Regulatory Automation**: Enhanced compliance monitoring
- **Customer Insights**: Integration with customer service data

## 🤝 Contributing

### Development Guidelines
1. Maintain HaruPlate's sincere, family-oriented tone in all code comments
2. Test brand compliance for any new content generation features
3. Ensure Malaysian market cultural sensitivity
4. Follow family business values in technical decisions

### Code Standards
- Clear, readable code that reflects HaruPlate values
- Comprehensive testing with real-world scenarios
- Documentation that speaks to business users
- Error handling that maintains user trust

## 📞 Support

For technical support or business questions about the HaruPlate Orchestra:
- 📧 Email: tech@haruplate.com
- 📱 WhatsApp: +60-xxx-xxx-xxxx (Malaysian hours)
- 🌐 Internal Documentation: confluence.haruplate.com/orchestra

## 📜 License

This system is proprietary to HaruPlate and contains confidential business processes and brand intellectual property. 

**© 2025 HaruPlate Sdn Bhd - "Nurturing Children, Strengthening Families"**

---

*Built with ❤️ for the HaruPlate family by teammates who believe in our mission of providing the best nutrition for children through natural, healthy products.*