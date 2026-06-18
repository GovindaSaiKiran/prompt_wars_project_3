# purpose: Detect Duplicate Logging | enforces: Security-first
import time

class FraudDetector:
    _recent_logs = {}  # In-memory sliding window for dummy check

    @staticmethod
    def is_duplicate_activity(user_id: str, activity_hash: str) -> bool:
        current_time = time.time()
        key = f"{user_id}:{activity_hash}"
        
        # Rate limit to 1 identical activity per 24 hours (86400s)
        if key in FraudDetector._recent_logs:
            if current_time - FraudDetector._recent_logs[key] < 86400:
                return True
        
        FraudDetector._recent_logs[key] = current_time
        return False
