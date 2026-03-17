# LiveKit Info Bot

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![Flask-RESTX](https://img.shields.io/badge/Flask_RESTX-1.0+-4B8BBE?logo=flask&logoColor=white)
![LiveKit](https://img.shields.io/badge/LiveKit-Real--Time-purple?logo=livekit&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React-20232A?logo=react&logoColor=61DAFB)



---



## Architecture



The project consists of three main components:



1.  **Frontend (`/info-bot`)**: A React/Vite application that handles the UI and connects to the LiveKit room.

2.  **Token Server (`app.py`)**: A Flask-RESTX backend that authenticates users and generates LiveKit access tokens.

3.  **Voice Agent (`agent.py`)**: The core logic powered by the LiveKit Python SDK, managing the conversational loop and LLM integration.



---



## Prerequisites



Before you begin, ensure you have the following installed:



* **Python 3.13**

* **Node.js 18+** & **npm**

* **[uv](https://github.com/astral-sh/uv)** (Python package manager)

    ```bash

    pip install uv

    ```

* **API Keys**:

    * [LiveKit Cloud](https://cloud.livekit.io/) (URL, Key, Secret)

    * [Groq API](https://console.groq.com/)

    * [Google Gemini API](https://aistudio.google.com/)



---



## 🚀 Setup & Installation



### 1. Clone the Repository



```bash

git clone https://github.com/vishal27shetty/LiveKit-Info-Bot.git

cd LiveKit-Info-Bot

```

### 2. Backend Setup (Python)



Initialize the environment and install dependencies using uv.



```bash

# Create virtual environment

python -m venv .venv

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

```

### 3. Sync dependencies

```bash

uv sync

```



**Configure Environment Variables:**



Create a `.env` file in the root directory:



```

LIVEKIT_URL=wss://your-project.livekit.cloud

LIVEKIT_API_KEY=your_api_key

LIVEKIT_API_SECRET=your_api_secret

GROQ_API_KEY=your_groq_api_key

GEMINI_API_KEY=your_gemini_api_key

```



### 4. Frontend Setup (React/Vite)



Navigate to the frontend directory and install dependencies.



```bash

cd info-bot

npm install

```



**Configure Environment Variables:**



Create a `.env` file in the `info-bot` directory:



```

VITE_LIVEKIT_URL=wss://your-project.livekit.cloud

```



## Usage



To run the full application, you will need to run the **Frontend**, **Token Server**, and **Voice Agent** in separate terminals.



### Terminal 1: Frontend Client



Starts the web interface where you can interact with the bot.



```bash

cd info-bot

npm run dev

```



**Access at:** http://localhost:5173/



### Terminal 2: Token Server



Starts the Flask backend to provision access tokens for the frontend.



```bash

# Ensure you are in the root directory and .venv is active

uv run app.py

```



**Running at:** http://127.0.0.1:5000



### Terminal 3: Voice Agent



Starts the AI agent that joins the LiveKit room to listen and respond.



```bash

# Ensure you are in the root directory and .venv is active

uv run agent.py dev

```



## 🚀 Deployment to LiveKit Cloud

This project includes GitHub Actions CI/CD workflows for automatic deployment to LiveKit Cloud.

### Setup GitHub Actions Deployment

1. **Configure Secrets**: Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):
   - `LIVEKIT_URL`: `wss://info-bot-ed21bgbj.livekit.cloud`
   - `LIVEKIT_API_KEY`: `APIezs2YYZ3hb9C`
   - `LIVEKIT_API_SECRET`: Your LiveKit API Secret
   - `GROQ_API_KEY`: Your Groq API Key
   - `GEMINI_API_KEY`: Your Google Gemini API Key

2. **First Time Setup**: 
   - Go to Actions → "Manual Deploy or Create Agent"
   - Select operation: `create`
   - This creates the agent and opens a PR with the configuration
   - Merge the PR

3. **Automatic Deployments**: Push changes to `main` branch and the agent will automatically deploy

For detailed setup instructions, see [GITHUB_SETUP.md](./GITHUB_SETUP.md)

### Available Workflows

- **Automatic Deployment**: Deploys on push to main when agent files change
- **Manual Deploy**: Manually trigger deployment or agent creation
- **Status Monitoring**: Checks agent health every 6 hours

---

## Task Completion Status

| Component | Description | Status |
| :--- | :--- | :---: |
| **PART 1: Core Agent** | `agent.py`: Main conversational logic | ✅ Completed |
| **PART 1.5: API Backend** | `app.py`: Token generation via Flask-RESTX | ✅ Completed |
| **PART 2: User Interface** | `info-bot`: Frontend UI | ✅ Completed |
| **PART 3: Bonus Task** | `custom_llm.py`: Advanced LLM customization | ✅ Completed |
| **CI/CD Pipeline** | GitHub Actions deployment workflows | ✅ Completed |
