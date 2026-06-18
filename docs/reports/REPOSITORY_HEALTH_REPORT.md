# Repository Health Report
**Timestamp:** 2026-06-18T16:11:15.277587Z
**Tool versions:** N/A
**Commands executed:** Manual Audit
**Findings:**

| Area | Status | Findings |
| ---- | ------ | -------- |
| package.json consistency | PASS | Workspaces configured correctly |
| lockfiles | PASS | package-lock.json present |
| dependency duplication | PASS | Minimal duplication |
| unused dependencies | FAIL | Many dependencies in backend unused |
| unused files | FAIL | Scaffold test files cover dummy components |
| dead code | FAIL | Mocked state in frontend not wired to backend |
| environment variables | FAIL | .env files missing required remote vars |
| broken API contracts | FAIL | Frontend calls `/api/v1/coach/chat` which returns 404 on live |

**Status:** FAIL
**Remediation:** Wire frontend to real backend API and deploy backend to Cloud Run.
