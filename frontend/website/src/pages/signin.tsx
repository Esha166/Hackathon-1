import React from 'react';
import Layout from '@theme/Layout';
import SigninForm from '../components/Auth/SigninForm';

function Signin() {
  return (
    <Layout
      title="Sign In"
      description="Sign in to your account to access personalized content.">
      <main>
        <SigninForm />
      </main>
    </Layout>
  );
}

export default Signin;
