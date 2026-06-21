import React, { useState, useEffect } from 'react';

export function Calculator({ currentUser }: { currentUser: any }) {
  const [history, setHistory] = useState<any[]>([]);
  const [distance, setDistance] = useState('');
  const [vehicle, setVehicle] = useState('Petrol Car');

  useEffect(() => {
    async function fetchHistory() {
      const token = await currentUser?.getIdToken();
      const res = await fetch('http://localhost:8000/api/v1/calculator/', {
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
    if (!distance) return;
    const token = await currentUser?.getIdToken();
    const res = await fetch('http://localhost:8000/api/v1/calculator/', {
      method: 'POST',
      headers: { 
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ distance: parseFloat(distance), vehicle_type: vehicle })
    });
    if (res.ok) {
      const data = await res.json();
      setHistory([data, ...history]);
      setDistance('');
    }
  };

  return (
    <section className="calculator-section" aria-label="Carbon Calculator">
      <div className="section-header">
        <h2>🧮 Carbon Footprint Calculator</h2>
        <p>Calculate emissions for your trips and see sustainable alternatives.</p>
      </div>
      <div className="dashboard-panel">
        <div className="dashboard-grid">
          <div>
            <h3>New Calculation</h3>
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <input type="number" step="0.1" placeholder="Distance (km)" value={distance} onChange={e => setDistance(e.target.value)} required style={{ padding: '8px' }} />
              <select value={vehicle} onChange={e => setVehicle(e.target.value)} style={{ padding: '8px' }}>
                <option value="Petrol Bike">Petrol Bike</option>
                <option value="Petrol Car">Petrol Car</option>
                <option value="Diesel Car">Diesel Car</option>
                <option value="Diesel SUV">Diesel SUV</option>
                <option value="Electric Bike">Electric Bike</option>
                <option value="Electric Car">Electric Car</option>
                <option value="Bus">Bus</option>
                <option value="Train">Train</option>
                <option value="Flight">Flight</option>
              </select>
              <button type="submit" className="btn btn-primary">Calculate</button>
            </form>
          </div>
          <div>
            <h3>History</h3>
            <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
              {history.map(h => (
                <div key={h.id} style={{ background: 'rgba(255,255,255,0.05)', padding: '15px', borderRadius: '8px', marginBottom: '10px' }}>
                  <h4>{h.distance} km by {h.vehicle_type}</h4>
                  <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                    <div className="stat-card" style={{ padding: '10px', flex: 1 }}><span style={{color: '#ef4444'}}>{h.carbon_produced_kg.toFixed(2)} kg</span><br/>Produced</div>
                    <div className="stat-card" style={{ padding: '10px', flex: 1 }}><span style={{color: '#ef4444'}}>₹{h.money_spent.toFixed(2)}</span><br/>Cost</div>
                    <div className="stat-card" style={{ padding: '10px', flex: 1 }}><span style={{color: '#10b981'}}>{h.eco_alternative_savings_kg.toFixed(2)} kg</span><br/>Saved vs Bus</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
