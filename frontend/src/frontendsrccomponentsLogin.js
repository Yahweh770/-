import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/api/login', { username, password })
      .then(res => {
        login(res.data.token);
        alert('Успешный вход в Strod-Service Technology');
      })
      .catch(err => alert('Ошибка входа в Strod-Service Technology'));
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h2 style={{ textAlign: 'center', color: '#2c3e50' }}>Вход в Strod-Service Technology</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <input 
            style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '16px' }} 
            placeholder="Имя пользователя" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required 
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <input 
            type="password" 
            style={{ width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '16px' }} 
            placeholder="Пароль" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>
        <button 
          type="submit" 
          style={{ 
            width: '100%', 
            padding: '10px', 
            backgroundColor: '#3498db', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px', 
            fontSize: '16px',
            cursor: 'pointer'
          }}
        >
          Войти
        </button>
      </form>
    </div>
  );
}