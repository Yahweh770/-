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
        alert('Успешный вход');
      })
      .catch(err => alert('Ошибка входа'));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input placeholder="Имя пользователя" value={username} onChange={(e) => setUsername(e.target.value)} required />
      <input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} required />
      <button type="submit">Войти</button>
    </form>
  );
}