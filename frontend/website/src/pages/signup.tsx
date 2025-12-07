import React from 'react';
import Layout from '@theme/Layout';
import SignupForm from '../components/Auth/SignupForm';

function Signup() {
  return (
    <Layout
      title="Sign Up"
      description="Sign up for an account to access personalized content.">
      <main>
        <SignupForm />
      </main>
    </Layout>
  );
}

export default Signup;
