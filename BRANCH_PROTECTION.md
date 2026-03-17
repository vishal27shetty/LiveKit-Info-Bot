# Branch Protection & Workflow Restrictions

## 🔒 Branch Restrictions

All CI/CD workflows are configured to **ONLY run on the main branch** for security and deployment consistency.

## Why Main Branch Only?

1. **Deployment Consistency**: Ensures only tested, reviewed code is deployed
2. **Security**: Prevents accidental deployments from feature branches
3. **Tracking**: Single source of truth for production deployments
4. **Rollback Safety**: Easy to revert by reverting main branch commits

## Workflows & Branch Enforcement

### 1. Automatic Deployment (`deploy.yml`)

```yaml
on:
  push:
    branches:
      - main  # ✅ Only triggers on main branch pushes
```

**Protection**: Built-in via `branches: [main]` trigger

### 2. Manual Deploy (`manual-deploy.yml`)

```yaml
jobs:
  validate-branch:
    steps:
      - name: Check if main branch
        run: |
          if [ "${{ github.ref }}" != "refs/heads/main" ]; then
            exit 1
          fi
```

**Protection**: 
- Pre-validation job that fails if not on main
- Explicit checkout of main branch
- All jobs depend on validation passing

### 3. Status Check (`status-check.yml`)

```yaml
jobs:
  check-status:
    if: github.ref == 'refs/heads/main' || github.event_name == 'schedule'
```

**Protection**:
- Conditional job execution
- Branch validation for manual triggers
- Forced main branch checkout

## 🚫 What Happens If You Try Other Branches?

### Manual Workflows (`workflow_dispatch`)

If you try to run a manual workflow on a non-main branch:

```
❌ Error: This workflow can only be run on the main branch
Current branch: refs/heads/feature-branch
Please switch to main branch and try again
```

The workflow will **fail immediately** at the validation step.

## ✅ How to Run Workflows Correctly

### For Automatic Deployment

1. Make changes in a feature branch:
   ```bash
   git checkout -b feature/my-changes
   # ... make changes ...
   git commit -am "My changes"
   git push origin feature/my-changes
   ```

2. Create Pull Request to main

3. Review and merge to main

4. **Automatic deployment triggers** when merged to main ✅

### For Manual Workflows

1. **Always select main branch** in the workflow UI:
   ```
   Actions → Select Workflow → Run workflow
   
   Use workflow from: [Branch: main] ← Must be main!
   ```

2. If you're on a different branch locally:
   ```bash
   git checkout main
   git pull origin main
   ```

3. Then trigger the workflow from GitHub UI

## 🔐 Additional GitHub Branch Protection (Recommended)

To further protect your main branch, configure these settings in GitHub:

### Go to: Settings → Branches → Add rule

```
Branch name pattern: main

☑️ Require a pull request before merging
  ☑️ Require approvals (1)
  ☑️ Dismiss stale pull request approvals

☑️ Require status checks to pass before merging
  ☑️ Require branches to be up to date
  - test (select this check)

☑️ Require conversation resolution before merging

☑️ Do not allow bypassing the above settings
```

### What This Does:

- ✅ Prevents direct pushes to main
- ✅ Requires PR review before merge
- ✅ Ensures tests pass before merge
- ✅ Keeps deployment history clean
- ✅ Forces all changes through CI pipeline

## 📋 Deployment Flow with Branch Protection

```
Feature Branch
    ↓
Make Changes
    ↓
Commit & Push
    ↓
Create PR to main
    ↓
Tests run automatically
    ↓
Code review & approval
    ↓
Merge to main
    ↓
✅ Automatic deployment to LiveKit Cloud
```

## 🎯 Best Practices

### DO ✅

- Always merge to main via Pull Requests
- Run manual workflows from main branch only
- Test changes in feature branches locally
- Use `git checkout main` before manual deployments
- Review workflow logs after deployment

### DON'T ❌

- Don't push directly to main (if branch protection enabled)
- Don't run manual workflows from feature branches
- Don't bypass branch validation checks
- Don't modify workflow branch restrictions
- Don't commit sensitive keys to any branch

## 🔍 Verifying Branch Protection

### Check Current Branch
```bash
git branch --show-current
# Should show: main
```

### Check Branch in GitHub UI
When triggering manual workflow:
```
Run workflow
Use workflow from: main  ← Check this dropdown
                   ^^^^
```

### Check in Workflow Logs
Look for:
```
✅ Running on main branch
```

If you see:
```
❌ Error: This workflow can only be run on the main branch
```
You're on the wrong branch!

## 🆘 Troubleshooting

### "This workflow can only be run on the main branch"

**Solution**:
1. Switch to main locally: `git checkout main`
2. Pull latest: `git pull origin main`
3. In GitHub UI, select "main" from branch dropdown
4. Try again

### Manual Workflow Shows Wrong Branch

**Solution**:
1. GitHub UI → Actions → Select Workflow
2. Click "Run workflow" button
3. **Check dropdown** - ensure "main" is selected
4. Change if needed, then click "Run workflow"

### Workflow Triggered on Wrong Branch

**Solution**:
1. Workflow will fail at validation step
2. This is expected behavior (protection working!)
3. Cancel the workflow run
4. Switch to main and retry

### Want to Test Workflow Changes

**Solution**:
```bash
# Create feature branch for workflow changes
git checkout -b feature/update-workflow

# Make changes to .github/workflows/*.yml

# Commit changes
git commit -am "Update workflow"

# Push branch
git push origin feature/update-workflow

# Create PR to main
# Review changes in PR
# Merge to main

# Workflow updates take effect on next run
```

## 📚 Additional Resources

- [GitHub Branch Protection Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Workflow Dispatch](https://docs.github.com/en/actions/using-workflows/manually-running-a-workflow)
- [GitHub Actions Contexts](https://docs.github.com/en/actions/learn-github-actions/contexts)

---

**Key Takeaway**: All deployments must go through the main branch. This ensures quality, security, and consistency in your production environment.
