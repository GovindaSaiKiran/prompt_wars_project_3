import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';

export function Login() {
  const { loginWithGoogle, loginWithEmail, registerWithEmail, resetPassword } = useAuth();
  const [error, setError] = useState('');
  const [msg, setMsg] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);

  const handleGoogleLogin = async () => {
    try {
      setError('');
      await loginWithGoogle();
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleEmailAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setError('');
      setMsg('');
      if (isRegistering) {
        await registerWithEmail(email, password);
      } else {
        await loginWithEmail(email, password);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleReset = async () => {
    if (!email) {
      setError('Please enter your email to reset password.');
      return;
    }
    try {
      setError('');
      await resetPassword(email);
      setMsg('Password reset email sent!');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="login-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', background: '#0f172a', color: 'white' }}>
      <div style={{ padding: '2rem', background: '#1e293b', borderRadius: '8px', textAlign: 'center', maxWidth: '400px', width: '100%' }}>
        <h2>EcoSphere AI</h2>
        <p style={{ marginBottom: '2rem', color: '#94a3b8' }}>Sign in to track your carbon footprint</p>
        
        {error && <div style={{ color: '#ef4444', marginBottom: '1rem' }}>{error}</div>}
        {msg && <div style={{ color: '#22c55e', marginBottom: '1rem' }}>{msg}</div>}
        
        <form onSubmit={handleEmailAuth} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1rem' }}>
          <input 
            type="email" 
            placeholder="Email address" 
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
            style={{ padding: '0.75rem', borderRadius: '4px', border: 'none', background: '#334155', color: 'white' }}
          />
          <input 
            type="password" 
            placeholder="Password" 
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
            style={{ padding: '0.75rem', borderRadius: '4px', border: 'none', background: '#334155', color: 'white' }}
          />
          <button 
            type="submit"
            style={{ width: '100%', padding: '0.75rem', background: '#10b981', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '1rem', fontWeight: 'bold' }}
          >
            {isRegistering ? 'Register' : 'Sign in with Email'}
          </button>
        </form>

        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem', fontSize: '0.85rem' }}>
          <button onClick={() => setIsRegistering(!isRegistering)} style={{ background: 'none', border: 'none', color: '#38bdf8', cursor: 'pointer' }}>
            {isRegistering ? 'Already have an account? Login' : 'Need an account? Register'}
          </button>
          <button onClick={handleReset} style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
            Forgot password?
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', margin: '1rem 0' }}>
          <div style={{ flex: 1, height: '1px', background: '#475569' }}></div>
          <span style={{ margin: '0 10px', color: '#94a3b8' }}>OR</span>
          <div style={{ flex: 1, height: '1px', background: '#475569' }}></div>
        </div>

        <button 
          onClick={handleGoogleLogin}
          style={{ width: '100%', padding: '0.75rem', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontSize: '1rem', fontWeight: 'bold' }}
        >
          Sign in with Google
        </button>
      </div>
    </div>
  );
}
