import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { isLoggedIn, getUserRole } from '../auth';

export default function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    if (isLoggedIn()) {
      const role = getUserRole();
      if (role === 'admin' || role === 'tech') {
        navigate('/admin');
      } else {
        navigate('/dashboard');
      }
    }
  }, []); // ✅ empty array = run once on mount

  return (
    <div>
      <h1>Welcome to Luxe RMA Tracker</h1>
      <p>Please <a href="/login">log in</a> or <a href="/register">create an account</a>.</p>
    </div>
  );
}
