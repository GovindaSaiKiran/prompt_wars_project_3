# purpose: Verify Cryptographic Score Hash | enforces: Security-first
import hashlib

class RankingValidator:
    @staticmethod
    def is_valid_score(user_id: str, score: int, provided_hash: str) -> bool:
        expected_hash = hashlib.sha256(f"{user_id}:{score}:SECRET".encode()).hexdigest()
        return expected_hash == provided_hash
