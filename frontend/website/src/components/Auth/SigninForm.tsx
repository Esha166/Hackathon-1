import React, { useState } from 'react';

function SigninForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setMessage('Signing in...');

    try {
      const response = await fetch('http://localhost:8000/auth/jwt/login', { // TODO: Replace with dynamic backend URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded', // fastapi-users login expects form urlencoded
        },
        body: new URLSearchParams({ username: email, password: password }).toString(),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage('Signin successful!');
        console.log('Signin success, token:', data.access_token);
        // Here you would typically store the token (e.g., in localStorage or context)
        localStorage.setItem('access_token', data.access_token);
      } else {
        const errorData = await response.json();
        setMessage(`Signin failed: ${errorData.detail || 'Unknown error'}`);
        console.error('Signin error:', errorData);
      }
    } catch (error) {
      setMessage('Network error during signin.');
      console.error('Network error:', error);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px', marginTop: '20px' }}>
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="email" style={{ display: 'block', marginBottom: '5px' }}>Email:</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="password" style={{ display: 'block', marginBottom: '5px' }}>Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>
        <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Sign In</button>
      </form>
      {message && <p style={{ marginTop: '15px', color: message.includes('failed') || message.includes('error') ? 'red' : 'green' }}>{message}</p>}
    </div>
  );
}

export default SigninForm;
