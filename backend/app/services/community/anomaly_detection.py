# purpose: Detect Impossible Score Jumps | enforces: Security-first
class AnomalyDetector:
    @staticmethod
    def is_anomalous_jump(old_score: int, new_score: int) -> bool:
        if new_score - old_score > 500:
            return True
        return False
