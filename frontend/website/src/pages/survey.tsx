import React from 'react';
import Layout from '@theme/Layout';
import SurveyForm from '../components/Auth/SurveyForm';

function SurveyPage() {
  return (
    <Layout
      title="Background Survey"
      description="Complete your background survey for personalized content.">
      <main>
        <SurveyForm />
      </main>
    </Layout>
  );
}

export default SurveyPage;
