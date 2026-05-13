## 📂 `data/` – The Agent's Business Logic

This folder holds files that define your agent’s skills, training data, and integrations.

### 📁 Directory Structure:

- **`flows/`**: Rasa CALM flow definitions (step-by-step conversation patterns).
  - `brands_flows.yml`: Business logic for Alazab brands.
  - `general_flows.yml`: Standard conversational patterns (greetings, help).
- **`nlu/`**: Natural Language Understanding data (intents and examples).
  - `brands_nlu.yml`: Intent data for Alazab brands.
  - `general_nlu.yml`: Standard intent data.
  - `generated_refined.yml`: Large-scale generated/refined NLU examples.
- **`rules/`**: Rasa Classic rules (conditional logic).
- **`stories/`**: Rasa Classic stories (example conversation paths).
- **`kb/`**: Knowledge base raw content and services documentation.
- **`integrations/`**: Metadata and scripts for external integrations (e.g., WhatsApp).
- **`prompts/`**: LLM prompts used for command generation and RAG.
- **`system/`**: System-level patterns and configurations.

**Archive**: Outdated or legacy files are stored in the `data/archive/` directory for reference.
