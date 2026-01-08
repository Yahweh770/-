import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function FieldForm() {
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
    const token = localStorage.getItem('token');
    axios.get('http://localhost:5000/api/field_data', {
      headers: { Authorization: token }
    })
    .then(res => setFieldData(res.data))
    .catch(err => console.error(err));
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    
    axios.post('http://localhost:5000/api/field_data', formData, {
      headers: { Authorization: token }
    })
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
      
      // Refresh data
      axios.get('http://localhost:5000/api/field_data', {
        headers: { Authorization: token }
      })
      .then(res => setFieldData(res.data));
    })
    .catch(err => alert('Ошибка при сохранении данных'));
  };

  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px', marginBottom: '20px' }}>
      <h2 style={{ color: '#2c3e50', borderBottom: '2px solid #3498db', paddingBottom: '10px' }}>Добавить полевые данные</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <div style={{ marginBottom: '10px' }}>
          <input 
            name="object_id" 
            placeholder="ID объекта" 
            value={formData.object_id} 
            onChange={handleChange} 
            required
            style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '200px' }} 
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input 
            name="line_type" 
            placeholder="Тип линии" 
            value={formData.line_type} 
            onChange={handleChange} 
            required
            style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '200px' }} 
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input 
            name="length" 
            placeholder="Длина" 
            value={formData.length} 
            onChange={handleChange} 
            required
            style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '200px' }} 
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input 
            name="width" 
            placeholder="Ширина" 
            value={formData.width} 
            onChange={handleChange} 
            required
            style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '200px' }} 
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <input 
            name="material_used" 
            placeholder="Расход" 
            value={formData.material_used} 
            onChange={handleChange} 
            required
            style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '200px' }} 
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <textarea 
            name="notes" 
            placeholder="Заметки" 
            value={formData.notes} 
            onChange={handleChange}
            style={{ padding: '8px', marginRight: '10px', border: '1px solid #ccc', borderRadius: '4px', width: '300px', height: '60px' }}
          ></textarea>
        </div>
        <button 
          type="submit" 
          style={{ 
            padding: '10px 20px', 
            backgroundColor: '#27ae60', 
            color: 'white', 
            border: 'none', 
            borderRadius: '4px', 
            cursor: 'pointer' 
          }}
        >
          Сохранить данные
        </button>
      </form>

      <h3 style={{ color: '#2c3e50', marginTop: '20px' }}>Полевые данные</h3>
      <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
        {fieldData.length > 0 ? (
          <ul style={{ listStyleType: 'none', padding: 0 }}>
            {fieldData.map(d => (
              <li key={d.id} style={{ 
                padding: '10px', 
                marginBottom: '5px', 
                backgroundColor: '#f9f9f9', 
                border: '1px solid #eee', 
                borderRadius: '4px' 
              }}>
                <strong>Тип линии:</strong> {d.line_type} — <strong>Длина:</strong> {d.length} м, <strong>Ширина:</strong> {d.width} м, <strong>Расход:</strong> {d.material_used} кг — {d.notes}
              </li>
            ))}
          </ul>
        ) : (
          <p>Нет данных для отображения</p>
        )}
      </div>
    </div>
  );
}