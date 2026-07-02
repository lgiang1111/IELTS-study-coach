# Rollback Plan: v1.0.0

## Trigger Conditions
- High failure rate in Streamlit app (e.g., Streamlit fails to load, or throws 500 error on launch).
- Critical security breach or leaked API keys in repository history.
- Regression in Genetic Algorithm core logic that breaks scheduling behavior for users.

## Steps
1. **Identify Previous Stable Commit**: Find the last working commit hash in the git history.
2. **Revert or Reset Branch**:
   ```bash
   # Revert the current HEAD commit
   git revert HEAD --no-edit
   ```
3. **Push to Remote**:
   ```bash
   # Push the reverted commit to the main branch on GitHub
   git push origin main
   ```
   *Streamlit Community Cloud automatically triggers a redeployment when the remote branch is updated.*
4. **Invalidate Cache**: If package dependency issues occurred, go to the Streamlit Community Cloud dashboard, click the app's settings dropdown, select **"Rerun"** or **"Delete"** and redeploy.

## Verification
- [ ] Access the Streamlit URL (e.g., https://ielts-study-coach.streamlit.app/) and verify the web interface loads in the browser.
- [ ] Confirm no trace log or terminal error outputs are shown in the logs console.
- [ ] Run the test suite: `PYTHONPATH=. pytest` to ensure all tests pass.

## Post-Rollback
- [ ] Open an issue/ticket detailing the root cause of the deployment failure.
- [ ] Create a fix/patch branch to resolve the issue before attempting another deployment.
