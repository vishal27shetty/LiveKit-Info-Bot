# 📋 Pre-Deployment Checklist

Before deploying to LiveKit Cloud, ensure all items are completed:

## ✅ Local Setup Complete

- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`uv sync`)
- [ ] `.env` file configured with all API keys
- [ ] Employee embeddings built (`employee_embeddings.npy` exists)
- [ ] Agent runs successfully locally (`uv run agent.py dev`)
- [ ] Token server works (`uv run app.py`)
- [ ] Frontend connects successfully

## ✅ Repository Prepared

- [ ] All code committed to repository
- [ ] `.gitignore` excludes sensitive files (`.env`, `.venv/`)
- [ ] `livekit.toml` configuration file exists
- [ ] `Dockerfile` exists and is valid
- [ ] `.dockerignore` excludes unnecessary files
- [ ] `employee_embeddings.npy` is committed (or will be built)

## ✅ GitHub Secrets Configured

Go to: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

- [ ] `LIVEKIT_URL` = `wss://info-bot-ed21bgbj.livekit.cloud`
- [ ] `LIVEKIT_API_KEY` = `APIezs2YYZ3hb9C`
- [ ] `LIVEKIT_API_SECRET` = `rwrw3i9DkmunvrrC1c1eU82I5KJdZ1rANgzByhxPYrW`
- [ ] `GROQ_API_KEY` = Your Groq API key
- [ ] `GEMINI_API_KEY` = Your Google Gemini API key

## ✅ GitHub Workflows Ready

- [ ] `.github/workflows/deploy.yml` exists (automatic deployment)
- [ ] `.github/workflows/manual-deploy.yml` exists (manual operations)
- [ ] `.github/workflows/status-check.yml` exists (health monitoring)

## ✅ Data Files Ready

- [ ] `data.json` contains valid employee directory data
- [ ] `employee_embeddings.npy` exists (run `uv run build_embeddings.py`)
- [ ] JSON structure validated

## 🚀 Deployment Steps

### Option 1: First Time (Create Agent)

1. Go to **Actions** tab in GitHub
2. Select **"Manual Deploy or Create Agent"**
3. Click **"Run workflow"**
4. Select operation: **create**
5. Click **"Run workflow"**
6. Wait for PR to be created with agent ID
7. Review and merge the PR
8. ✅ Agent is now deployed and running!

### Option 2: Update Existing Agent

1. Make your code changes locally
2. Test locally: `uv run agent.py dev`
3. Commit and push to main:
   ```bash
   git add .
   git commit -m "Update agent logic"
   git push origin main
   ```
4. ✅ Automatic deployment triggered!

## 🔍 Post-Deployment Verification

- [ ] GitHub Actions workflow completed successfully (green checkmark)
- [ ] Run "Monitor Agent Status" workflow to check health
- [ ] Visit LiveKit Cloud dashboard to see agent status
- [ ] Test agent by connecting from frontend application
- [ ] Verify agent responds to voice queries
- [ ] Check that tool calling works (employee directory lookup)

## ⚠️ Important Notes

### Must Build Embeddings First

If `employee_embeddings.npy` doesn't exist, run locally:

```bash
# Ensure GEMINI_API_KEY is in .env
uv run build_embeddings.py
git add employee_embeddings.npy
git commit -m "Add pre-built employee embeddings"
git push
```

### Agent ID

- After first deployment with "create", the agent ID is written to `livekit.toml`
- This ID is used for all subsequent deployments
- Don't modify the agent ID manually

### API Keys Security

- Never commit API keys to the repository
- Use GitHub Secrets for all sensitive credentials
- The SECRET_LIST in workflows passes keys to the agent securely

### Deployment Time

- First deployment: 3-5 minutes (includes building Docker image)
- Subsequent deployments: 2-3 minutes
- Status check: Up to 5 minutes (waits for "Running" state)

## 🆘 Troubleshooting

### "employee_embeddings.npy not found" error
**Solution**: Run `uv run build_embeddings.py` locally and commit the file

### "GEMINI_API_KEY not set" error
**Solution**: Add `GEMINI_API_KEY` to GitHub Secrets

### Deployment succeeds but agent doesn't respond
**Solution**: 
1. Check agent logs in LiveKit Cloud dashboard
2. Verify all API keys are correct in GitHub Secrets
3. Run "Monitor Agent Status" workflow

### Tests fail on GitHub Actions
**Solution**:
1. Run tests locally first: `python -m py_compile agent.py`
2. Validate JSON: `python -c "import json; json.load(open('data.json'))"`
3. Check workflow logs for specific error

## 📚 Additional Resources

- [GitHub Setup Guide](./GITHUB_SETUP.md) - Detailed secrets configuration
- [CI/CD Guide](./CI_CD_GUIDE.md) - Complete CI/CD reference
- [LiveKit Deploy Action](https://github.com/livekit/deploy-action) - Official documentation
- [LiveKit Cloud Dashboard](https://cloud.livekit.io/) - View agent status

---

**Ready to Deploy?** 🚀

If all checkboxes are complete, you're ready to deploy to LiveKit Cloud!
