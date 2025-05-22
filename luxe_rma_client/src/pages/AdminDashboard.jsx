import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { isLoggedIn } from '../auth';
import { Navigate } from 'react-router-dom';
import { getUserRole } from '../auth';


export default function AdminDashboard() {
  const [rmas, setRmas] = useState([]);
  const [error, setError] = useState('');
  const [selectedRmaId, setSelectedRmaId] = useState(null);
  const [repairForm, setRepairForm] = useState({
    description: '',
    diagnosis: '',
    cost: '',
    warranty: false,
    repair_date: ''
  });
  const [repairMessage, setRepairMessage] = useState('');
  const [serialSearch, setSerialSearch] = useState('');
  const [searchedMarker, setSearchedMarker] = useState(null);
  const [markerError, setMarkerError] = useState('');

  const token = localStorage.getItem('token');

  useEffect(() => {
    if (!token) return;

    axios
      .get('http://localhost:5000/rma/all', {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => setRmas(res.data))
      .catch(() => setError('Failed to fetch RMAs.'));
  }, []);

  const handleRepairChange = (e) => {
    const { name, value } = e.target;
    setRepairForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSerialSearch = async (e) => {
    e.preventDefault();
    setMarkerError('');
    setSearchedMarker(null);

    try {
      const res = await axios.get(
        `http://localhost:5000/marker/search/${serialSearch}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSearchedMarker(res.data);
    } catch (err) {
      setMarkerError('Marker not found.');
    }
  };

  const toggleStolen = async () => {
    try {
      const res = await axios.post(
        `http://localhost:5000/marker/toggle-stolen`,
        { serial_number: searchedMarker.serial_number },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSearchedMarker(prev => ({ ...prev, status: res.data.status }));
    } catch {
      alert('Failed to update status');
    }
  };

  const handleRepairSubmit = async (e, rma) => {
    e.preventDefault();
    setRepairMessage('');

    try {
      await axios.post(
        'http://localhost:5000/repair/log',
        {
          marker_id: rma.marker_id || rma.id || 1, // ensure backend returns marker ID
          tech_id: localStorage.getItem('user_id'),
          description: repairForm.description,
          diagnosis: repairForm.diagnosis,
          cost: parseFloat(repairForm.cost),
          warranty: repairForm.warranty,
          repair_date: repairForm.repair_date,
          status: 'completed'
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      setRepairMessage('Repair logged successfully.');
      setSelectedRmaId(null);
    } catch (err) {
      setRepairMessage('Error logging repair.');
    }
  };

  if (!isLoggedIn()) return <Navigate to="/login" />;

  const role = getUserRole();
  if (role !== 'admin' && role !== 'tech') {
    return <Navigate to="/dashboard" />;
  }

  return (
    <div>
      <h2>Admin Dashboard (Technician View)</h2>
      {error && <p>{error}</p>}

      <h3>Search Marker by Serial</h3>
      <form onSubmit={handleSerialSearch}>
        <input
          type="text"
          placeholder="Enter serial number"
          value={serialSearch}
          onChange={e => setSerialSearch(e.target.value)}
          required
        />
        <button type="submit">Search</button>
      </form>

      {markerError && <p>{markerError}</p>}

      {searchedMarker && (
        <div>
          <h4>Marker Info</h4>
          <p>Serial: {searchedMarker.serial_number}</p>
          <p>Model: {searchedMarker.model}</p>
          <p>Color: {searchedMarker.color}</p>
          <p>Status: {searchedMarker.status}</p>
          <button onClick={toggleStolen}>
            {searchedMarker.status === 'stolen'
              ? 'Unflag as Stolen'
              : 'Flag as Stolen'}
          </button>
        </div>
      )}

      <h3>All RMA Requests</h3>
      <ul>
        {rmas.map(rma => (
          <li key={rma.rma_number}>
            <strong>RMA #{rma.rma_number}</strong>
            <br />
            Marker SN: {rma.serial_number}
            <br />
            Model: {rma.model}
            <br />
            Owner: {rma.owner_name} ({rma.owner_email})
            <br />
            Status: {rma.status}
            <br />

            <button onClick={() => setSelectedRmaId(rma.rma_number)}>
              Log Repair
            </button>

            {selectedRmaId === rma.rma_number && (
              <form onSubmit={e => handleRepairSubmit(e, rma)}>
                <label>
                  Description:
                  <br />
                  <input
                    type="text"
                    name="description"
                    onChange={handleRepairChange}
                    required
                  />
                </label>
                <br /><br />

                <label>
                  Diagnosis:
                  <br />
                  <input
                    type="text"
                    name="diagnosis"
                    onChange={handleRepairChange}
                    required
                  />
                </label>
                <br /><br />

                <label>
                  Cost:
                  <br />
                  <input
                    type="number"
                    name="cost"
                    onChange={handleRepairChange}
                    required
                  />
                </label>
                <br /><br />

                <label>
                  Warranty?
                  <br />
                  <input
                    type="checkbox"
                    name="warranty"
                    onChange={e =>
                      setRepairForm(prev => ({
                        ...prev,
                        warranty: e.target.checked
                      }))
                    }
                  />
                </label>
                <br /><br />

                <label>
                  Repair Date (YYYY-MM-DD):
                  <br />
                  <input
                    type="text"
                    name="repair_date"
                    onChange={handleRepairChange}
                    required
                  />
                </label>
                <br /><br />

                <button type="submit">Submit Repair</button>
              </form>
            )}
            <br /><br />
          </li>
        ))}
      </ul>
    </div>
  );
}
