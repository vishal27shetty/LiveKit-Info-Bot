# GitHub Secrets Setup Guide

To use the GitHub Actions CI/CD workflows, you need to configure the following secrets in your GitHub repository.

## How to Add Secrets

1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret below

## Required Secrets

### LiveKit Cloud Credentials

```
LIVEKIT_URL=wss://info-bot-ed21bgbj.livekit.cloud
LIVEKIT_API_KEY=APIezs2YYZ3hb9C
LIVEKIT_API_SECRET=rwrw3i9DkmunvrrC1c1eU82I5KJdZ1rANgzByhxPYrW
```

### API Keys

```
GROQ_API_KEY=your_groq_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

## Summary of Secrets to Add

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `LIVEKIT_URL` | LiveKit Cloud WebSocket URL | `wss://info-bot-ed21bgbj.livekit.cloud` |
| `LIVEKIT_API_KEY` | LiveKit API Key | `APIezs2YYZ3hb9C` |
| `LIVEKIT_API_SECRET` | LiveKit API Secret | `rwrw3i9D...` |
| `GROQ_API_KEY` | Groq API Key for LLM | `gsk_...` |
| `GEMINI_API_KEY` | Google Gemini API Key for embeddings | `AIza...` |

## Optional: GitHub Environment Setup

For additional security, you can create a `production` environment:

1. Go to **Settings** → **Environments**
2. Click **New environment**
3. Name it `production`
4. Add protection rules if desired (e.g., required reviewers)

## Verify Setup

After adding secrets, you can verify by:

1. Go to **Actions** tab
2. Select **Manual Deploy or Create Agent**
3. Click **Run workflow**
4. Choose operation: `deploy`
5. Check the workflow logs

---

## Workflows Available

### 1. **Automatic Deployment** (`deploy.yml`)
- Triggers on push to `main` branch when agent files change
- Runs tests first, then deploys if tests pass

### 2. **Manual Deploy** (`manual-deploy.yml`)
- Manually trigger deployment or agent creation
- Go to Actions → Manual Deploy or Create Agent → Run workflow

### 3. **Status Monitoring** (`status-check.yml`)
- Automatically checks agent health every 6 hours
- Can be manually triggered anytime

## First Time Setup

If this is your first deployment:

1. Add all secrets to GitHub
2. Go to Actions → Manual Deploy or Create Agent
3. Select operation: `create`
4. This will create a new agent and open a PR with the agent ID
5. Merge the PR
6. Future deployments will use the `deploy` operation

## Troubleshooting

- **Deployment fails**: Check that all secrets are correctly set
- **Agent not starting**: Verify `data.json` and `employee_embeddings.npy` are in the repository
- **Missing dependencies**: Ensure `pyproject.toml` includes all required packages
