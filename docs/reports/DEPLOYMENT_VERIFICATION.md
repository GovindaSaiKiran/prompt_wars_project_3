# Deployment Verification Report

## Metadata
* **Deployment Timestamp:** 2026-06-18
* **Environment:** Production (Google Cloud Run)
* **Service Name:** prompt-wars-project-3
* **Project ID:** perceptive-bay-493811-c1

## Verification

### Service URL
`https://prompt-wars-project-3-oardwr3raa-uc.a.run.app`

### API Endpoints Verified
1. `GET /api/v1/community/leaderboard`
   * **Status:** 200 OK
   * **Response Sample:** `[{"user_id": "user_456", "total_score": 1200, "rank": 1}, {"user_id": "user_789", "total_score": 950, "rank": 2}]`

2. `POST /api/v1/carbon/calculate`
   * **Payload:** `{"activityType": "electricity", "value": 100, "unit": "kWh"}`
   * **Status:** 200 OK
   * **Response Sample:** `{"co2e_kg": 45.0}`

3. `POST /api/v1/coach/chat`
   * **Payload:** `{"message": "How can I reduce my carbon footprint?"}`
   * **Status:** 200 OK
   * **Response Sample:** `{"recommendation": "Switching to public transport can significantly lower your carbon emissions.", "carbon_reduction_estimate": 18.0, "confidence_score": 0.9}`

4. `POST /api/v1/twin/simulate`
   * **Payload:** `{"variables": {"commute_mode": "bicycle"}}`
   * **Status:** 200 OK
   * **Response Sample:** `{"simulated_reduction": 15.5, "new_projected_score": 850}`

5. `POST /api/v1/planner/goals`
   * **Payload:** `{"title": "Commute less", "target_reduction": 50}`
   * **Status:** 200 OK
   * **Response Sample:** `{"id": "123", "status": "active"}`

## Conclusion
The backend service has been successfully deployed and is returning actual dynamic responses based on the implemented logic services, passing all endpoint health checks.
