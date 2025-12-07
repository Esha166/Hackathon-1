import React, { useState, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useLocation } from '@docusaurus/router';
import { UserBackgroundRead } from '../../../backend/schemas'; // Assuming schemas are accessible or re-defined

interface PersonalizeButtonProps {
  chapterId: string; // The ID of the current chapter
  onPersonalize: (personalizedContent: string) => void; // Callback to update chapter content
}

function PersonalizeButton({ chapterId, onPersonalize }: PersonalizeButtonProps) {
  const { siteConfig } = useDocusaurusContext();
  const backendUrl = siteConfig.customFields?.backendUrl || 'http://localhost:8000';
  const [isSurveyCompleted, setIsSurveyCompleted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const location = useLocation();

  useEffect(() => {
    const checkSurveyStatus = async () => {
      const accessToken = localStorage.getItem('access_token');
      if (!accessToken) {
        setIsSurveyCompleted(false);
        return;
      }

      try {
        const response = await fetch(`${backendUrl}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });

        if (response.ok) {
          const userData: UserBackgroundRead = await response.json();
          // Check if all required fields in UserBackgroundRead are present and not empty
          // This is a simplified check; actual implementation might require more specific validation
          const requiredFields: (keyof UserBackgroundRead)[] = ['role', 'programming_level', 'interest_field'];
          const completed = requiredFields.every(field => userData[field] && userData[field] !== '');
          setIsSurveyCompleted(completed);
        } else {
          setIsSurveyCompleted(false);
          console.error('Failed to fetch user data:', await response.json());
        }
      } catch (error) {
        setIsSurveyCompleted(false);
        console.error('Network error checking survey status:', error);
      }
    };

    checkSurveyStatus();
  }, [backendUrl, location.pathname]); // Re-check on path change

  const handlePersonalize = async () => {
    setIsLoading(true);
    setMessage('');
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
      setMessage('Error: Not authenticated.');
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${backendUrl}/personalize/chapter/${chapterId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ chapter_content: 'placeholder content for now' }), // Will be replaced by actual content
      });

      if (response.ok) {
        const data = await response.json();
        onPersonalize(data.personalized_content);
        setMessage('Content personalized successfully!');
      } else {
        const errorData = await response.json();
        setMessage(`Personalization failed: ${errorData.detail || 'Unknown error'}`);
        console.error('Personalization error:', errorData);
      }
    } catch (error) {
      setMessage('Network error during personalization.');
      console.error('Network error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ margin: '20px 0', textAlign: 'center' }}>
      <button
        onClick={handlePersonalize}
        disabled={!isSurveyCompleted || isLoading}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: isSurveyCompleted ? '#007bff' : '#cccccc',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: isSurveyCompleted ? 'pointer' : 'not-allowed',
        }}
      >
        {isLoading ? 'Personalizing...' : 'Personalize Content'}
      </button>
      {!isSurveyCompleted && (
        <p style={{ color: 'red', marginTop: '10px' }}>
          Please complete your <a href="/survey">background survey</a> to enable personalization.
        </p>
      )}
      {message && <p style={{ marginTop: '10px', color: message.includes('failed') || message.includes('Error') ? 'red' : 'green' }}>{message}</p>}
    </div>
  );
}

export default PersonalizeButton;
