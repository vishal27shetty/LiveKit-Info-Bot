# LiveKit-Info-Bot

**Eightfold.ai Assignment Submission**  
An intelligent Voice AI agent that helps search employee email id and an answer general knowledge questions.

## Setup Instructions

### Prerequisites

- **Python 3.13** 
- **Node.js 18+** and npm
- API Keys:
  - Livekit API
  - Groq API
  - Google Gemini API

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/vishal27shetty/LiveKit-Info-Bot.git
   cd LiveKit-Info-Bot
   ```
2. **Create virtual environment**
  ```bash
    python -m venv .venv
    source .venv/bin/activate
  ```
3. Sync the dependencies
   ```bash
   uv sync
   ```

4. Set .env file in root directory
   ```bash
    LIVEKIT_URL=YOUR_LIVEKIT_URL
    LIVEKIT_API_KEY=YOUR_LIVEKIT_API_KEY
    LIVEKIT_API_SECRET=YOUR_LIVEKIT_API_SECRET
    GROQ_API_KEY =YOUR_GROQ_API_KEY
    GEMINI_API_KEY= YOUR_GEMINI_API_KEY
    ```
5. Set .env file in frontend directory
    ```bash
    VITE_LIVEKIT_URL=YOUR_LIVEKIT_URL
    ```
6. Run the frontend
    ```bash
    cd info-bot
    npm install
    npm run dev
    ```
    The frontend will be running on http://localhost:5173/
7. Run the backend
  ```bash
    uv run app.py
  ```
  The backend will be running on http://127.0.0.1:5000
  
8. Run the livekit voice agent
   ```bash
    uv run agent.py dev
    ```

## Task Success Criteria

### Part 1: The Core Agent (Backend/LiveKit Agent Logic)
 It has been completed in the agent.py file


### Part 1.5: API Backend for Token Generation (Flask-RESTX)
 It has been completed in the agent.py file


### Part 2: The User Interface (Frontend)
 It has been completed in the info-bot


### Part 3: Advanced Customization (Bonus Task)
 It has been completed in the custom.llm


  




