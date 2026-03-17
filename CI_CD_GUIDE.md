# CI/CD Quick Reference

## 🚀 Quick Start

### First Time Deployment

1. **Add GitHub Secrets** (Settings → Secrets and variables → Actions):
   ```
   LIVEKIT_URL=wss://info-bot-ed21bgbj.livekit.cloud
   LIVEKIT_API_KEY=APIezs2YYZ3hb9C
   LIVEKIT_API_SECRET=rwrw3i9DkmunvrrC1c1eU82I5KJdZ1rANgzByhxPYrW
   GROQ_API_KEY=<your-groq-key>
   GEMINI_API_KEY=<your-gemini-key>
   ```

2. **Create Agent** (GitHub → Actions → "Manual Deploy or Create Agent"):
   - Click "Run workflow"
   - Select operation: `create`
   - Wait for PR to be created
   - Merge the PR with agent ID

3. **Automatic Deployments**: Now enabled on push to `main`!

---

## 📋 Workflow Files

| File | Trigger | Purpose |
|------|---------|---------|
| `deploy.yml` | Push to main (auto) | Runs tests + deploys agent |
| `manual-deploy.yml` | Manual only | Create or deploy agent manually |
| `status-check.yml` | Every 6 hours / Manual | Monitor agent health |

---

## 🔄 Common Operations

### Deploy Changes
```bash
git add .
git commit -m "Update agent logic"
git push origin main
# ✅ Automatic deployment triggered!
```

### Manual Deployment
1. Go to **Actions** tab
2. Select **"Manual Deploy or Create Agent"**
3. Click **"Run workflow"**
4. Choose operation: `deploy`
5. Click **"Run workflow"**

### Check Agent Status
1. Go to **Actions** tab
2. Select **"Monitor Agent Status"**
3. Click **"Run workflow"**
4. Check logs for status

---

## 🧪 What Gets Tested

Before deployment, the CI runs:
- ✅ Python syntax validation
- ✅ Dependencies installation check
- ✅ JSON data validation
- ✅ Linting checks

---

## 📦 What Gets Deployed

The deployment includes:
- `agent.py` - Main agent logic
- `custom_llm.py` - Custom LLM wrapper
- `build_embeddings.py` - Embeddings builder
- `data.json` - Employee directory data
- `employee_embeddings.npy` - Pre-built embeddings
- `pyproject.toml` - Dependencies
- `livekit.toml` - Agent configuration

---

## 🔍 Troubleshooting

### Deployment Fails

**Check 1**: Are all secrets set correctly?
```
Settings → Secrets and variables → Actions
Verify all 5 secrets are present
```

**Check 2**: Is `livekit.toml` configured?
```bash
cat livekit.toml
# Should have valid agent ID after first creation
```

**Check 3**: Review workflow logs
```
Actions → Select failed workflow → View logs
```

### Agent Not Responding

**Check 1**: Agent status
```
Run "Monitor Agent Status" workflow
```

**Check 2**: LiveKit Cloud Dashboard
```
Visit: https://cloud.livekit.io/
Check agent status in dashboard
```

**Check 3**: Dependencies
```
Ensure pyproject.toml has all required packages:
- livekit-agents[groq,silero,turn-detector]
- livekit-plugins-noise-cancellation
- google-genai
- numpy
- python-dotenv
```

### Test Failures

**Check**: Validate files locally
```bash
# Activate virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Test imports
python -c "import agent"
python -c "import custom_llm"

# Validate JSON
python -c "import json; json.load(open('data.json'))"
```

---

## 🎯 Best Practices

1. **Test Locally First**
   ```bash
   uv run agent.py dev
   # Verify agent works before pushing
   ```

2. **Small Commits**: Deploy incremental changes for easier debugging

3. **Monitor Status**: Check agent health after deployment

4. **Use Branches**: Test major changes in feature branches first

5. **Review Logs**: Always check deployment logs for warnings

---

## 📊 Monitoring

### View Deployment Status
```
GitHub → Actions → Recent workflow runs
```

### View Agent Logs
```
LiveKit Cloud Dashboard → Agents → View Logs
```

### Check Agent Health
```
Run "Monitor Agent Status" workflow manually
```

---

## 🆘 Need Help?

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **LiveKit Deploy Action**: https://github.com/livekit/deploy-action
- **LiveKit Cloud**: https://cloud.livekit.io/
- **LiveKit Docs**: https://docs.livekit.io/

---

## 🎉 Success Indicators

After successful deployment, you should see:

✅ Green checkmark on GitHub Actions workflow
✅ Agent status: "Running" in status check
✅ Agent visible in LiveKit Cloud dashboard
✅ Agent responds to voice requests in your app

---

**Last Updated**: March 2026
