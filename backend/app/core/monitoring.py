# purpose: Cloud Logging Integration | enforces: Efficiency-first, Quality-first
import logging
import json

# Setup basic logger fallback
logger = logging.getLogger("ecosphere")
logger.setLevel(logging.INFO)

class CloudLogger:
    @staticmethod
    def log_error(error_message: str, metadata: dict = None):
        payload = {"error": error_message, "metadata": metadata or {}}
        # In production, this would use google-cloud-logging
        logger.error(json.dumps(payload))
        
    @staticmethod
    def log_fraud_attempt(user_id: str, details: str):
        payload = {"type": "FRAUD_ATTEMPT", "user_id": user_id, "details": details}
        logger.warning(json.dumps(payload))
