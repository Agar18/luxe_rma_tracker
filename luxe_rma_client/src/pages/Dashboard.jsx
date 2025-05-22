import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { logout } from '../auth';
import { useNavigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../AuthContext';


export default function Dashboard() {
  const [userId, setUserId] = useState(null);
  const [markers, setMarkers] = useState([]);
  const [rmas, setRmas] = useState([]);
  const [error, setError] = useState('');
  const [registerMessage, setRegisterMessage] = useState('');
  const [rmaMessage, setRmaMessage] = useState('');
  const navigate = useNavigate();
  const { role } = useContext(AuthContext);


  const token = localStorage.getItem('token');

  useEffect(() => {
    const id = localStorage.getItem('user_id');
    if (!token || !id) {
      setError('You must be logged in to view the dashboard.');
      return;
    }

    setUserId(id);

    const headers = {
      Authorization: `Bearer ${token}`
    };

    // Fetch markers
    axios.get(`http://localhost:5000/marker/user/${id}`, { headers })
      .then(res => setMarkers(res.data))
      .catch(() => setError('Could not fetch markers.'));

    // Fetch RMAs
    axios.get(`http://localhost:5000/rma/user/${id}`, { headers })
      .then(res => setRmas(res.data))
      .catch(() => setError('Could not fetch RMAs.'));
  }, []);

  const handleRegisterMarker = async (e) => {
    e.preventDefault();
    setRegisterMessage('');

    const form = e.target;
    const newMarker = {
      serial_number: form.serial_number.value,
      model: form.model.value,
      color: form.color.value,
      date_made: form.date_made.value,
      user_id: userId,
      purchased_from: form.purchased_from.value,
      purchase_date: form.purchase_date.value
    };

    try {
      await axios.post('http://localhost:5000/marker/register-marker', newMarker, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRegisterMessage('Marker registered successfully!');
      form.reset();
    } catch (err) {
      if (err.response) {
        setRegisterMessage(`Error: ${err.response.data.message}`);
      } else {
        setRegisterMessage('Server error while registering marker.');
      }
    }
  };

  const handleRmaSubmit = async (e) => {
    e.preventDefault();
    setRmaMessage('');

    const marker_id = e.target.marker_id.value;

    try {
      const res = await axios.post('http://localhost:5000/rma/create', {
        marker_id: marker_id,
        user_id: userId
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      setRmaMessage(`RMA Submitted! RMA #${res.data.rma_number}`);
    } catch (err) {
      if (err.response) {
        setRmaMessage(`Error: ${err.response.data.message}`);
      } else {
        setRmaMessage('Failed to submit RMA.');
      }
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (error) return <p>{error}</p>;

  return (
    <div>
    <button onClick={handleLogout} style={{ float: 'right' }}>Logout</button>
    <h2>Dashboard</h2>
    <p>Welcome, User #{userId}</p>

      <h2>Dashboard</h2>
      <p>Welcome, User #{userId}</p>

      <h3>Your Registered Markers</h3>
      <ul>
        {markers.map(marker => (
          <li key={marker.serial_number}>
            {marker.serial_number} — {marker.model} ({marker.color})
          </li>
        ))}
      </ul>

      <h3>Your RMA Requests</h3>
      <ul>
        {rmas.map(rma => (
          <li key={rma.rma_number}>
            RMA #{rma.rma_number} - Status: {rma.status}
          </li>
        ))}
      </ul>

  
      {(role === 'admin' || role === 'tech') ? (
  <>
    <h3>Register a New Marker</h3>
    <form onSubmit={handleRegisterMarker}>
      <label>
        Serial Number:<br />
        <input type="text" name="serial_number" required />
      </label><br /><br />

      <label>
        Model:<br />
        <input type="text" name="model" required />
      </label><br /><br />

      <label>
        Color:<br />
        <input type="text" name="color" required />
      </label><br /><br />

      <label>
        Date Made (YYYY-MM-DD):<br />
        <input type="text" name="date_made" required />
      </label><br /><br />

      <label>
        Purchased From:<br />
        <input type="text" name="purchased_from" required />
      </label><br /><br />

      <label>
        Purchase Date (YYYY-MM-DD):<br />
        <input type="text" name="purchase_date" required />
      </label><br /><br />

      <button type="submit">Register Marker</button>
    </form>

    {registerMessage && <p>{registerMessage}</p>}
  </>
) : (
  <p><em></em></p>
)}


      <h3>Submit a New RMA</h3>
      <form onSubmit={handleRmaSubmit}>
        <label>
          Select Marker:<br />
          <select name="marker_id" required>
            {markers.map(marker => (
              <option key={marker.id} value={marker.id}>
                {marker.serial_number} — {marker.model}
              </option>
            ))}
          </select>
        </label><br /><br />

        <button type="submit">Submit RMA</button>
      </form>

      {rmaMessage && <p>{rmaMessage}</p>}
    </div>
  );
}
