import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

export default function Notifications() {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const socket = io('http://localhost:5000');

    socket.on('new_notification', (data) => {
      setNotifications(prev => [...prev, data]);
    });

    return () => socket.close();
  }, []);

  return (
    <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '8px', margin: '20px 0', backgroundColor: '#f9f9f9' }}>
      <h3 style={{ color: '#2c3e50', marginBottom: '10px' }}>Уведомления Strod-Service Technology</h3>
      <ul style={{ listStyleType: 'none', padding: 0, maxHeight: '200px', overflowY: 'auto' }}>
        {notifications.map((n, i) => (
          <li key={i} style={{ 
            padding: '8px', 
            margin: '5px 0', 
            backgroundColor: '#fff', 
            border: '1px solid #eee', 
            borderRadius: '4px',
            color: n.type === 'error' ? '#e74c3c' : n.type === 'warning' ? '#f39c12' : '#27ae60' 
          }}>
            {n.message}
          </li>
        ))}
      </ul>
    </div>
  );
}