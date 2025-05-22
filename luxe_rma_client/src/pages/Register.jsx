import React, { useState } from 'react';
import axios from 'axios';

export default function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    try {
      const res = await axios.post('http://localhost:5000/auth/register', formData);
      setMessage(res.data.message || 'Registered successfully!');
    } catch (err) {
      if (err.response) {
        setMessage(`Error: ${err.response.data.message}`);
      } else {
        setMessage('Error connecting to server.');
      }
    }
  };

  return (
    <div>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Name:<br />
          <input type="text" name="name" value={formData.name} onChange={handleChange} required />
        </label><br /><br />

        <label>
          Email:<br />
          <input type="email" name="email" value={formData.email} onChange={handleChange} required />
        </label><br /><br />

        <label>
          Password:<br />
          <input type="password" name="password" value={formData.password} onChange={handleChange} required />
        </label><br /><br />

        <button type="submit">Register</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}
