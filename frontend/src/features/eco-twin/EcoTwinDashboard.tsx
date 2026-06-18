// purpose: Eco Twin Viz with Explainability | enforces: Accessibility-first, Transparency
import React, { useState } from 'react';

export const EcoTwinDashboard: React.FC = () => {
  const [footprint, setFootprint] = useState<number | null>(null);
  const [diff, setDiff] = useState<number | null>(null);

  const runSimulation = () => {
    fetch('/api/v1/twin/simulate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ variables: {} })
    })
      .then(res => res.json())
      .then(data => {
        setFootprint(data.simulated_co2e);
        setDiff(data.difference);
      })
      .catch(console.error);
  };

  return (
    <div role="region" aria-label="Eco Twin Dashboard">
      <h2>Your Eco Twin</h2>
      {footprint !== null ? (
        <p>Simulated Footprint: {footprint} kg CO2e (Difference: {diff})</p>
      ) : (
        <p>Current Footprint: 1000 kg CO2e</p>
      )}
      <button onClick={runSimulation}>Run Simulation</button>
      
      <div className="explainability-panel" aria-label="Explainability Dashboard">
        <h3>Simulation Details</h3>
        <ul>
          <li><strong>Assumptions:</strong> Assumes average mpg for internal combustion engine.</li>
          <li><strong>Emission Factors:</strong> 0.2 kg CO2e / km (Source: EPA)</li>
          <li><strong>Methodology:</strong> CO2e = Distance * Emission Factor</li>
        </ul>
      </div>
    </div>
  );
};
