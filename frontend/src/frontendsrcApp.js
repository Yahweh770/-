import React, { useState, useEffect } from 'react';
import axios from 'axios';
import React from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Login from './components/Login';
import AdminPanel from './components/AdminPanel';
import FieldForm from './components/FieldForm';
import Notifications from './components/Notifications';

function AppContent() {
  const { token } = useAuth();

  if (!token) {
    return <Login />;
  }

  return (
     <div>
    <h1>Веб-версия: Исполнительная документация</h1>
    <FieldForm />
    <AdminPanel />
    <Notifications /> {/* ✅ Добавлен компонент уведомлений */}
  </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}


export default App;

function App() {
  const [fieldData, setFieldData] = useState([]);
  const [formData, setFormData] = useState({
    object_id: '',
    line_type: '',
    length: '',
    width: '',
    material_used: '',
    notes: ''
  });

  useEffect(() => {
    axios.get('http://localhost:5000/api/field_data')
      .then(res => setFieldData(res.data));
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:5000/api/field_data', formData)
      .then(() => {
        alert('Данные сохранены');
        setFormData({
          object_id: '',
          line_type: '',
          length: '',
          width: '',
          material_used: '',
          notes: ''
        });
      });
  };

  return (
    <div>
      <h1>Веб-версия: Исполнительная документация</h1>
      <form onSubmit={handleSubmit}>
        <input name="line_type" placeholder="Тип линии" value={formData.line_type} onChange={handleChange} required />
        <input name="length" placeholder="Длина" value={formData.length} onChange={handleChange} required />
        <input name="width" placeholder="Ширина" value={formData.width} onChange={handleChange} required />
        <input name="material_used" placeholder="Расход" value={formData.material_used} onChange={handleChange} required />
        <textarea name="notes" placeholder="Заметки" value={formData.notes} onChange={handleChange}></textarea>
        <button type="submit">Сохранить</button>
      </form>

      <h2>Полевые данные</h2>
      <ul>
        {fieldData.map(d => (
          <li key={d.id}>
            {d.line_type} — {d.length} м, {d.material_used} кг — {d.notes}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;