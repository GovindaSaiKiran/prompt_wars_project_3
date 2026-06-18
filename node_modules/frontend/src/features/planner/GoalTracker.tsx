// purpose: Goal Tracker UI | enforces: Accessibility-first
import React from 'react';

export const GoalTracker: React.FC = () => {
  return (
    <div role="region" aria-label="Sustainability Goals">
      <h2>Your Goals</h2>
      <ul>
        <li>Reduce Energy 10% - <progress value="50" max="100"></progress></li>
      </ul>
    </div>
  );
};
