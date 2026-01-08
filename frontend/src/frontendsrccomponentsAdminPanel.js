import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function AdminPanel() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    axios.get('http://localhost:5000/api/users', {
      headers: { Authorization: token }
    })
    .then(res => setUsers(res.data))
    .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', margin: '20px 0' }}>
      <h2 style={{ color: '#2c3e50', borderBottom: '2px solid #3498db', paddingBottom: '10px' }}>Админ-панель Strod-Service Technology</h2>
      <p>Управление пользователями системы</p>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {users.map(u => (
          <li key={u.id} style={{ padding: '8px', borderBottom: '1px solid #eee' }}>
            <strong>{u.username}</strong> — <span style={{ color: u.role === 'admin' ? '#e74c3c' : '#27ae60' }}>{u.role}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}