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
    <div>
      <h2>Админ-панель</h2>
      <ul>
        {users.map(u => (
          <li key={u.id}>{u.username} — {u.role}</li>
        ))}
      </ul>
    </div>
  );
}