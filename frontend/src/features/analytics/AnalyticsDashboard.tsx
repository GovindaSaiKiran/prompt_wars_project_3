import React, { useState, useEffect } from 'react';

export function AnalyticsDashboard({ currentUser }: { currentUser: any }) {
  const [trends, setTrends] = useState<any>(null);
  const [daily, setDaily] = useState<any>(null);
  const [monthly, setMonthly] = useState<any>(null);

  useEffect(() => {
    async function fetchData() {
      const token = await currentUser?.getIdToken();
      const headers = { 'Authorization': `Bearer ${token}` };
      
      const [tRes, dRes, mRes] = await Promise.all([
        fetch('http://localhost:8000/api/v1/analytics/trends', { headers }),
        fetch('http://localhost:8000/api/v1/analytics/daily', { headers }),
        fetch('http://localhost:8000/api/v1/analytics/monthly', { headers })
      ]);
      
      if (tRes.ok) setTrends(await tRes.json());
      if (dRes.ok) setDaily(await dRes.json());
      if (mRes.ok) setMonthly(await mRes.json());
    }
    fetchData();
  }, [currentUser]);

  if (!trends || !daily || !monthly) return <div style={{padding: '20px'}}>Loading Analytics...</div>;

  return (
    <section className="analytics-section" aria-label="Personal Emissions Analytics">
      <div className="section-header">
        <h2>📈 Personal Emissions Analytics</h2>
        <p>Track your footprint over time and view AI insights.</p>
      </div>

      <div className="stats-bar" style={{ marginBottom: '20px' }}>
        <div className="stat-card">
          <div className="stat-value" style={{color: '#10b981'}}>{daily.totalCarbonSavedKg.toFixed(1)} kg</div>
          <div className="stat-label">Saved Today</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{monthly.totalCarbonProducedKg.toFixed(1)} kg</div>
          <div className="stat-label">Produced This Month</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{trends.trend_percent > 0 ? '+' : ''}{trends.trend_percent.toFixed(1)}%</div>
          <div className="stat-label">Trend vs Last Week</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{daily.sustainabilityScore.toFixed(0)}</div>
          <div className="stat-label">Daily Eco Score</div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3>🤖 AI Insights</h3>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {trends.insights.map((insight: string, idx: number) => (
              <li key={idx} style={{ marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span>💡</span> {insight}
              </li>
            ))}
          </ul>
        </div>

        <div className="glass-panel" style={{ padding: '20px' }}>
          <h3>Top Impact Areas (Current Week)</h3>
          <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #333', paddingBottom: '10px', marginBottom: '10px' }}>
            <span>Highest Emission Source:</span>
            <strong style={{color: '#ef4444', textTransform: 'capitalize'}}>{trends.current_week.topEmissionSource}</strong>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>Highest Saving Source:</span>
            <strong style={{color: '#10b981'}}>{trends.current_week.topSavingSource}</strong>
          </div>
        </div>
      </div>
    </section>
  );
}
