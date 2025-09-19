## [Coral-RedditContext-Agent](https://github.com/Coral-Protocol/Coral-Coral-RedditContext-Agent)
 
AI Content Generation Agent specialized in creating engaging Reddit posts with advanced context engineering capabilities. This agent dynamically updates its context based on user requirements to generate highly personalized and targeted content.

## Responsibility
Coral-RedditContext-Agent serves as a Reddit Content Strategist that creates personalized and engaging Reddit post ideas based on user context. It excels at understanding the importance of context in content creation and can adapt suggestions to match different tones, objectives, and niches. The agent uses an innovative context engineering approach where it dynamically updates its understanding based on user requirements, ensuring each generated post is perfectly tailored to the specific context provided.

## Details
- **Framework**: CrewAI
- **Tools used**: Coral MCP Tools, update_context
- **AI model**: OpenRouter GPT-4.1-mini
- **Date added**: September 12, 2025
- **License**: MIT

## Setup the Agent

### 1. Clone & Install Dependencies

<details>  

```bash
# In a new terminal clone the repository:
git clone https://github.com/Coral-Protocol/Coral-RedditContext-Agent.git

# Navigate to the project directory:
cd Coral-RedditContext-Agent

# Download and run the UV installer, setting the installation directory to the current one
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$(pwd) sh

# Create a virtual environment named `.venv` using UV
uv venv .venv

# Activate the virtual environment
source .venv/bin/activate

# install uv
pip install uv

# Install dependencies from `pyproject.toml` using `uv`:
uv sync
```

</details>

### 2. Configure Environment Variables

Get the API Key:
[OpenRouter](https://openrouter.ai/keys) or your preferred LLM provider

<details>

```bash
# Create .env file in project root
cp -r .env.example .env
```

Configure the following environment variables in your `.env` file:

```bash
# Coral Server Configuration
CORAL_SSE_URL=your_coral_sse_url_here
CORAL_AGENT_ID=your_agent_id_here

# Model Configuration
MODEL_PROVIDER=openrouter/openai
MODEL_NAME=gpt-4.1-mini
MODEL_API_KEY=your_model_api_key_here
MODEL_BASE_URL=https://openrouter.ai/api/v1
```

</details>

## Run the Agent

You can run in either of the below modes to get your system running.  

- The Executable Model is part of the Coral Protocol Orchestrator which works with [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio).  
- The Dev Mode allows the Coral Server and all agents to be seperately running on each terminal without UI support.  

### 1. Executable Mode

Checkout: [How to Build a Multi-Agent System with Awesome Open Source Agents using Coral Protocol](https://github.com/Coral-Protocol/existing-agent-sessions-tutorial-private-temp) and update the file: `coral-server/src/main/resources/application.yaml` with the details below, then run the [Coral Server](https://github.com/Coral-Protocol/coral-server) and [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio). You do not need to set up the `.env` in the project directory for running in this mode; it will be captured through the variables below.

<details>

For Linux or MAC:

```bash
# PROJECT_DIR="/PATH/TO/YOUR/PROJECT"

applications:
  - id: "app"
    name: "Default Application"
    description: "Default application for testing"
    privacyKeys:
      - "default-key"
      - "public"
      - "priv"

registry:
  context_engineering_agent:
    options:
      - name: "MODEL_PROVIDER"
        type: "string"
        description: "Model provider (e.g., openrouter/openai)"
      - name: "MODEL_NAME"
        type: "string"
        description: "Model name (e.g., gpt-4.1-mini)"
      - name: "MODEL_API_KEY"
        type: "string"
        description: "API key for the model provider"
      - name: "MODEL_BASE_URL"
        type: "string"
        description: "Base URL for the model provider API"
    runtime:
      type: "executable"
      command: ["bash", "-c", "${PROJECT_DIR}/run_agent.sh main.py"]
      environment:
        - name: "MODEL_PROVIDER"
          from: "MODEL_PROVIDER"
        - name: "MODEL_NAME"
          from: "MODEL_NAME"
        - name: "MODEL_API_KEY"
          from: "MODEL_API_KEY"
        - name: "MODEL_BASE_URL"
          from: "MODEL_BASE_URL"

```

For Windows, create a powershell command (run_agent.ps1) and run:

```bash
command: ["powershell","-ExecutionPolicy", "Bypass", "-File", "${PROJECT_DIR}/run_agent.ps1","main.py"]
```

</details>

### 2. Dev Mode

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system and run below command in a separate terminal.

<details>

```bash
# Run the agent using `uv`:
uv run main.py
```

You can view the agents running in Dev Mode using the [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio) by running it separately in a new terminal.

</details>


## Example

<details>


```bash
# Input:
Interface Agent: Generate me reddit post about ai in healthcare

# Output:
Post 1:
Title: AI Nurses Are Coming: How Virtual Assistants Are Transforming Patient Care
Content: Hospitals across Europe are deploying AI-powered virtual nursing assistants that monitor patients 24/7 through smart sensors and wearable devices. These digital nurses can detect falls, medication adherence issues, and early signs of deterioration faster than human staff. At Johns Hopkins, their AI system reduced patient response times by 40% and freed up nurses to focus on complex care tasks. The technology isn't replacing human touch—it's amplifying it.
Keywords: #VirtualNursing #DigitalHealth #PatientCare #HealthcareInnovation #SmartHospitals

Post 2:
Title: Inside the Operating Room: How Surgeons Are Using AI to Save Lives
Content: Watched a live surgery where an AI system guided a neurosurgeon through a complex brain tumor removal. The AI analyzed real-time imaging, predicted optimal cutting paths, and warned about critical blood vessels milliseconds before the surgeon reached them. What used to be a 6-hour procedure was completed in 3.5 hours with zero complications. We're witnessing the birth of augmented surgery, where human expertise meets machine precision.
Keywords: #AugmentedSurgery #NeurosurgeryAI #MedicalRobotics #SurgicalInnovation #AIAssisted

Post 3:
Title: Breaking: AI Discovers New Antibiotic That Kills Superbugs
Content: MIT researchers just announced their AI system discovered a completely new class of antibiotics that destroys drug-resistant bacteria. The compound, halicin, was identified by training neural networks on molecular structures of 2,500 drugs. In lab tests, it killed every superbug thrown at it, including MRSA and C. diff. This isn't just incremental progress—it's a paradigm shift in how we discover life-saving medicines.
Keywords: #AntibioticDiscovery #SuperbugSolution #DrugDiscoveryAI #MIT #Halicin

Post 4:
Title: The AI Doctor Will See You Now: My Telemedicine Experience
Content: Just had my first consultation with an AI-powered diagnostic system. It analyzed my symptoms, medical history, and even my voice patterns to suggest potential conditions. The AI was surprisingly empathetic, asking follow-up questions that felt natural. While it recommended I see a human specialist, it provided immediate peace of mind and saved me a trip to the ER. The future of primary care is here, and it's more accessible than ever.
Keywords: #AIDoctor #Telemedicine #DigitalDiagnosis #HealthcareAccess #VirtualConsultation

Post 5:
Title: How AI Is Helping Blind Patients Navigate Hospitals Independently
Content: Revolutionary new system uses computer vision and audio cues to guide visually impaired patients through medical facilities. Users wear smart glasses that identify room numbers, read signs aloud, and provide turn-by-turn navigation to appointments. Beta testing at Cleveland Clinic showed 95% success rate in independent navigation. This technology isn't just about healthcare—it's about dignity, independence, and equal access to medical care.
Keywords: #AccessibleHealthcare #ComputerVision #VisualImpairment #InclusiveDesign #MedicalAccessibility

Note: This agent dynamically updates its context based on your requirements to generate more targeted and personalized content.
```
</details>


## Creator Details
- **Name**: Ahsen Tahir
- **Affiliation**: Coral Protocol
- **Contact**: [Discord](https://discord.com/invite/Xjm892dtt3)
