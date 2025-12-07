import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SurveyForm() {
  const [role, setRole] = useState('');
  const [programmingLevel, setProgrammingLevel] = useState('');
  const [hardwareSpecs, setHardwareSpecs] = useState('');
  const [softwareExperience, setSoftwareExperience] = useState('');
  const [interestField, setInterestField] = useState('');
  const [preferredLanguage, setPreferredLanguage] = useState('');
  const [goals, setGoals] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setMessage('Submitting survey...');

    const surveyData = {
      role,
      programming_level: programmingLevel,
      hardware_specs: hardwareSpecs,
      software_experience: softwareExperience,
      interest_field: interestField,
      preferred_language: preferredLanguage,
      goals,
    };

    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      setMessage('Error: Not authenticated. Please sign in again.');
      navigate('/signin');
      return;
    }

    // Assuming user ID is part of the token payload or retrieved separately after login
    // For now, let's assume we can get it from a /users/me endpoint or decode the token
    // For simplicity, let's try to fetch user info from the backend or decode token for userId
    let userId = localStorage.getItem('user_id'); // This would ideally be set during login
    if (!userId) {
        // Fallback: Make a call to /users/me or decode JWT. For hackathon, assume stored or fixed for now
        // TODO: Implement a proper way to get user_id after login.
        // For demonstration, let's use a dummy UUID if not available
        userId = "00000000-0000-0000-0000-000000000001"; // Dummy UUID for testing if not set
        console.warn("Using dummy user_id for survey submission. Implement proper user_id retrieval.");
    }


    try {
      const response = await fetch(`http://localhost:8000/users/${userId}/background`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify(surveyData),
      });

      if (response.ok) {
        setMessage('Survey submitted successfully! Redirecting...');
        console.log('Survey success:', surveyData);
        navigate('/'); // Redirect to home page
      } else {
        const errorData = await response.json();
        setMessage(`Survey submission failed: ${errorData.detail || 'Unknown error'}`);
        console.error('Survey error:', errorData);
      }
    } catch (error) {
      setMessage('Network error during survey submission.');
      console.error('Network error:', error);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: 'auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
      <h2>Background Survey</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="role" style={{ display: 'block', marginBottom: '5px' }}>Current Role:</label>
          <select id="role" value={role} onChange={(e) => setRole(e.target.value)} required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}>
            <option value="">Select your role</option>
            <option value="Student">Student</option>
            <option value="Developer">Developer</option>
            <option value="Engineer">Engineer</option>
            <option value="Beginner">Beginner</option>
            <option value="Researcher">Researcher</option>
          </select>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="programmingLevel" style={{ display: 'block', marginBottom: '5px' }}>Programming Experience Level:</label>
          <select id="programmingLevel" value={programmingLevel} onChange={(e) => setProgrammingLevel(e.target.value)} required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}>
            <option value="">Select your level</option>
            <option value="None">None</option>
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="hardwareSpecs" style={{ display: 'block', marginBottom: '5px' }}>Hardware Setup (e.g., Laptop specs / GPU availability / OS):</label>
          <textarea id="hardwareSpecs" value={hardwareSpecs} onChange={(e) => setHardwareSpecs(e.target.value)} rows={3}
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}></textarea>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="softwareExperience" style={{ display: 'block', marginBottom: '5px' }}>Software Tools Experience (e.g., Python, ROS2, Gazebo, Unity, Isaac Sim):</label>
          <textarea id="softwareExperience" value={softwareExperience} onChange={(e) => setSoftwareExperience(e.target.value)} rows={3}
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}></textarea>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="interestField" style={{ display: 'block', marginBottom: '5px' }}>Field of Interest:</label>
          <select id="interestField" value={interestField} onChange={(e) => setInterestField(e.target.value)} required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}>
            <option value="">Select your field</option>
            <option value="Robotics">Robotics</option>
            <option value="AI Agents">AI Agents</option>
            <option value="Vision">Vision</option>
            <option value="Humanoids">Humanoids</option>
            <option value="Embedded">Embedded</option>
          </select>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="preferredLanguage" style={{ display: 'block', marginBottom: '5px' }}>Preferred Language:</label>
          <select id="preferredLanguage" value={preferredLanguage} onChange={(e) => setPreferredLanguage(e.target.value)} required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}>
            <option value="">Select your language</option>
            <option value="English">English</option>
            <option value="Urdu">Urdu</option>
          </select>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label htmlFor="goals" style={{ display: 'block', marginBottom: '5px' }}>Future Goals (e.g., Career path or specialization):</label>
          <textarea id="goals" value={goals} onChange={(e) => setGoals(e.target.value)} rows={3}
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}></textarea>
        </div>

        <button type="submit" style={{ width: '100%', padding: '10px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>Submit Survey</button>
      </form>
      {message && <p style={{ marginTop: '15px', color: message.includes('failed') || message.includes('error') ? 'red' : 'green' }}>{message}</p>}
    </div>
  );
}

export default SurveyForm;