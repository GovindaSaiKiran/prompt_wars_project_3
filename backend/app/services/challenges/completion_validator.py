# purpose: Validate Challenge Proof | enforces: Security-first
class CompletionValidator:
    @staticmethod
    def validate_proof(user_entries: list, challenge_rules: dict) -> bool:
        req_type = challenge_rules.get("required_activity_type")
        req_count = challenge_rules.get("required_count", 1)
        
        matching_entries = [e for e in user_entries if e.get("activityType") == req_type]
        return len(matching_entries) >= req_count
