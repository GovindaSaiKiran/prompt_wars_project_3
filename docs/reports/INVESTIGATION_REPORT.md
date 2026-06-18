# Investigation Report
**Timestamp:** 2026-06-18T16:11:15.277587Z
**Tool versions:** Git, npm, pip
**Commands executed:** `git status`, manual code review
**Findings:** The repository contains a deployed frontend via Firebase Hosting. However, the backend (FastAPI) is NOT deployed. The GitHub Actions pipeline only deploys Firebase Hosting.
**Evidence paths:** `.github/workflows/ci.yml`
**Status:** FAIL
