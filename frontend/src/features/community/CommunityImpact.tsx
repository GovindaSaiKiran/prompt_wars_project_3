// purpose: Community Impact & Leaderboard | enforces: Accessibility-first
import React, { useEffect, useState } from 'react';

interface LeaderboardEntry {
  user_id: string;
  score: number;
  rank: number;
}

export const CommunityImpact: React.FC = () => {
  const [data, setData] = useState<LeaderboardEntry[]>([]);

  useEffect(() => {
    fetch('/api/v1/community/leaderboard')
      .then(res => res.json())
      .then(json => {
        if (json.leaderboard) setData(json.leaderboard);
      })
      .catch(console.error);
  }, []);

  return (
    <div role="region" aria-label="Global Leaderboard">
      <h2>Community Impact</h2>
      <ol>
        {data.length > 0 ? (
          data.map((entry) => (
            <li key={entry.user_id}>
              {entry.user_id} - {entry.score} points (Rank {entry.rank})
            </li>
          ))
        ) : (
          <li>Loading leaderboard...</li>
        )}
      </ol>
    </div>
  );
};
