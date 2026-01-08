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
     <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ color: '#2c3e50', textAlign: 'center', borderBottom: '2px solid #3498db', paddingBottom: '10px' }}>Strod-Service Technology - Система управления проектами</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', marginTop: '20px' }}>
        <div style={{ flex: '1', minWidth: '300px' }}>
          <FieldForm />
        </div>
        <div style={{ flex: '1', minWidth: '300px' }}>
          <AdminPanel />
          <Notifications /> {/* ✅ Добавлен компонент уведомлений */}
        </div>
      </div>
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

function AppWeb() {
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
        alert('Данные сохранены в Strod-Service Technology');
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
    <div style={{ fontFamily: 'Arial, sans-serif', padding: '20px' }}>
      <h1>Strod-Service Technology - Веб-версия: Исполнительная документация</h1>
      <form onSubmit={handleSubmit} style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <div style={{ marginBottom: '10px' }}>
          <input name="line_type" placeholder="Тип линии" value={formData.line_type} onChange={handleChange} required 
                 style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '200px' }} />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input name="length" placeholder="Длина" value={formData.length} onChange={handleChange} required 
                 style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '200px' }} />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input name="width" placeholder="Ширина" value={formData.width} onChange={handleChange} required 
                 style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '200px' }} />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input name="material_used" placeholder="Расход" value={formData.material_used} onChange={handleChange} required 
                 style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '200px' }} />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <textarea name="notes" placeholder="Заметки" value={formData.notes} onChange={handleChange}
                   style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '300px', height: '60px' }}></textarea>
        </div>
        <button type="submit" style={{ padding: '10px 20px', backgroundColor: '#3498db', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Сохранить</button>
      </form>

      <h2>Полевые данные Strod-Service Technology</h2>
      <ul style={{ listStyleType: 'none', padding: 0 }}>
        {fieldData.map(d => (
          <li key={d.id} style={{ padding: '10px', marginBottom: '5px', backgroundColor: '#f9f9f9', border: '1px solid #eee', borderRadius: '4px' }}>
            <strong>Тип линии:</strong> {d.line_type} — <strong>Длина:</strong> {d.length} м, <strong>Расход:</strong> {d.material_used} кг — {d.notes}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AppWeb;