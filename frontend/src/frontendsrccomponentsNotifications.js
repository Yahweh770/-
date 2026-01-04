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
    <div>
      <h3>Уведомления</h3>
      <ul>
        {notifications.map((n, i) => (
          <li key={i} style={{ color: n.type === 'error' ? 'red' : 'green' }}>
            {n.message}
          </li>
        ))}
      </ul>
    </div>
  );
}