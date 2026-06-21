import React, { useState, useEffect } from 'react';

export function RoutineAnalyzer({ currentUser }: { currentUser: any }) {
  const [history, setHistory] = useState<any[]>([]);
  const [routineText, setRoutineText] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchHistory() {
      const token = await currentUser?.getIdToken();
      const res = await fetch('http://localhost:8000/api/v1/routine-analyzer/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        setHistory(await res.json());
      }
    }
    fetchHistory();
  }, [currentUser]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!routineText) return;
    setLoading(true);
    const token = await currentUser?.getIdToken();
    try {
      const res = await fetch('http://localhost:8000/api/v1/routine-analyzer/', {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: routineText })
      });
      if (res.ok) {
        const data = await res.json();
        setHistory([data, ...history]);
        setRoutineText('');
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="routine-section" aria-label="Daily Routine Analyzer">
      <div className="section-header">
        <h2>📅 Daily Routine Carbon Analyzer</h2>
        <p>Describe your day in natural language, and AI will extract the carbon impact.</p>
      </div>
      <div className="dashboard-panel">
        <div className="dashboard-grid">
          <div>
            <h3>Analyze New Routine</h3>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <textarea 
                rows={5} 
                placeholder="e.g. I woke up at 7 AM, drove 10km to work in my petrol car, used AC for 5 hours, and ate chicken biryani for lunch..." 
                value={routineText} 
                onChange={e => setRoutineText(e.target.value)} 
                required 
                style={{ padding: '10px', borderRadius: '8px', background: 'rgba(255,255,255,0.05)', color: 'white', border: '1px solid #333' }} 
              />
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Analyzing with Gemini...' : 'Analyze Impact'}
              </button>
            </form>
          </div>
          <div>
            <h3>Analysis History</h3>
            <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
              {history.map(h => (
                <div key={h.id} style={{ background: 'rgba(255,255,255,0.05)', padding: '15px', borderRadius: '8px', marginBottom: '10px' }}>
                  <p style={{fontStyle: 'italic', fontSize: '0.9rem', color: '#ccc'}}>"{h.original_text}"</p>
                  <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                    <div className="stat-card" style={{ padding: '10px', flex: 1 }}>{h.estimated_carbon_kg.toFixed(1)} kg<br/><span style={{fontSize:'0.8rem'}}>Total Carbon</span></div>
                    <div className="stat-card" style={{ padding: '10px', flex: 1 }}>{h.eco_score.toFixed(0)} / 100<br/><span style={{fontSize:'0.8rem'}}>Eco Score</span></div>
                  </div>
                  <div style={{ marginTop: '10px' }}>
                    <strong>Breakdown:</strong> Transport: {h.transport_impact}kg | Food: {h.food_impact}kg | Energy: {h.electricity_impact}kg | Other: {h.other_impact}kg
                  </div>
                  {h.recommendations && h.recommendations.length > 0 && (
                    <div style={{ marginTop: '10px', background: 'rgba(16, 185, 129, 0.1)', padding: '10px', borderRadius: '5px' }}>
                      <strong style={{color: '#10b981'}}>AI Recommendations:</strong>
                      <ul style={{margin: '5px 0 0 15px', fontSize: '0.9rem'}}>
                        {h.recommendations.map((r: string, idx: number) => <li key={idx}>{r}</li>)}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
