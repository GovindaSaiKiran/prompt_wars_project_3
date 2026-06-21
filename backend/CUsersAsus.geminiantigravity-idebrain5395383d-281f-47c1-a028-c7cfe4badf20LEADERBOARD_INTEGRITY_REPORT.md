# Leaderboard Integrity Verification Gate

## 1. Security Architecture
- **Score Source of Truth:** Backend Database (PostgreSQL)
- **Tamper Protection:** HMAC-SHA256 Signatures
- **Authentication:** Firebase ID Tokens

## 2. Integrity Testing

### Test Case A: Valid HMAC Signature
**Input:** Score=850.5, Streak=7
**Calculated Signature:** `4751d69a4c1f1b00556395c4cc7b2fcbdd4abe8a1dacab9d9b9a511b8a50b07e`
**Result Status:** 200
**Result Body:** `{"id":"test_user_123","user_id":"test_user_123","username":"ValidUser","score":850.5,"reduction_pct":-10.5,"streak":7,"region":"Global","emoji":"🌿","rank":0}`
**Status:** PASS

### Test Case B: Tampered Score Payload (Invalid HMAC)
**Input:** Score=9999.0, Streak=7 (Client attempts to cheat)
**Provided Signature:** `4751d69a4c1f1b00556395c4cc7b2fcbdd4abe8a1dacab9d9b9a511b8a50b07e` (Stolen from previous valid payload)
**Result Status:** 403
**Result Body:** `{"detail":"Invalid HMAC signature. Data tampered."}`
**Status:** PASS

## 3. Conclusion
The Leaderboard API correctly verifies HMAC signatures and successfully rejects payloads where the score or streak has been tampered with by the client.
