# purpose: Leaderboard Prep | enforces: Quality-first, Security-first
import hashlib

class LeaderboardPrep:
    @staticmethod
    def export_score(user_id: str, score: int) -> dict:
        anti_gaming_hash = hashlib.sha256(f"{user_id}:{score}:SECRET".encode()).hexdigest()
        return {"user_id": user_id, "score": score, "hash": anti_gaming_hash}
