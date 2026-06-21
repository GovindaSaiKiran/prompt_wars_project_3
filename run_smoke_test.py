import requests
import json
from datetime import datetime

def check_endpoint(url, expected_status=200):
    try:
        res = requests.get(url, timeout=5)
        return res.status_code == expected_status
    except Exception as e:
        return False

def check_post_endpoint(url, payload, expected_status=200):
    try:
        res = requests.post(url, json=payload, timeout=5)
        return res.status_code == expected_status
    except Exception as e:
        return False

def generate_smoke_test_report():
    report = "# Smoke Test Report\n\n"
    report += f"**Timestamp:** {datetime.utcnow().isoformat()}Z\n\n"
    report += "## Endpoints Verification\n\n"
    
    endpoints = {
        "Database Health (/api/v1/system/db-health)": ("GET", "http://localhost:8000/api/v1/system/db-health", 200),
        "Leaderboard API (/api/v1/leaderboard/)": ("GET", "http://localhost:8000/api/v1/leaderboard/", 200),
        "Community API (/api/v1/community/)": ("GET", "http://localhost:8000/api/v1/community/", 200),
    }
    
    all_passed = True
    for name, (method, url, expected) in endpoints.items():
        if method == "GET":
            passed = check_endpoint(url, expected)
        
        status_text = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        report += f"- **{name}:** {status_text} (Expected {expected})\n"
        
    report += "\n## Summary\n"
    if all_passed:
        report += "All critical systems are functional. The application passes the smoke test.\n"
    else:
        report += "Some critical systems failed the smoke test. Investigation required.\n"

    with open("SMOKE_TEST_REPORT.md", "w") as f:
        f.write(report)
        
    print("SMOKE_TEST_REPORT.md generated.")

if __name__ == "__main__":
    generate_smoke_test_report()
