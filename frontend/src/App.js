import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, FlatList, Alert } from 'react-native';
import axios from 'axios';

export default function App() {
  const [token, setToken] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fieldData, setFieldData] = useState([]);
  const [formData, setFormData] = useState({
    object_id: '',
    line_type: '',
    length: '',
    width: '',
    material_used: '',
    notes: ''
  });

  const login = () => {
    axios.post('http://localhost:5000/api/login', { username, password })
      .then(res => {
        setToken(res.data.token);
        Alert.alert('Успешный вход');
      })
      .catch(err => Alert.alert('Ошибка входа'));
  };

  const fetchFieldData = () => {
    axios.get('http://localhost:5000/api/field_data', {
      headers: { Authorization: token }
    })
    .then(res => setFieldData(res.data))
    .catch(err => console.error(err));
  };

  const submitFieldData = () => {
    axios.post('http://localhost:5000/api/field_data', formData, {
      headers: { Authorization: token }
    })
    .then(() => {
      Alert.alert('Данные сохранены');
      setFormData({
        object_id: '',
        line_type: '',
        length: '',
        width: '',
        material_used: '',
        notes: ''
      });
    })
    .catch(err => console.error(err));
  };

  return (
    <View style={{ padding: 20 }}>
      {!token ? (
        <>
          <TextInput placeholder="Имя пользователя" value={username} onChangeText={setUsername} />
          <TextInput placeholder="Пароль" value={password} onChangeText={setPassword} secureTextEntry />
          <Button title="Войти" onPress={login} />
        </>
      ) : (
        <>
          <TextInput placeholder="Тип линии" value={formData.line_type} onChangeText={(v) => setFormData({...formData, line_type: v})} />
          <TextInput placeholder="Длина" value={formData.length} onChangeText={(v) => setFormData({...formData, length: v})} />
          <TextInput placeholder="Ширина" value={formData.width} onChangeText={(v) => setFormData({...formData, width: v})} />
          <TextInput placeholder="Расход" value={formData.material_used} onChangeText={(v) => setFormData({...formData, material_used: v})} />
          <TextInput placeholder="Заметки" value={formData.notes} onChangeText={(v) => setFormData({...formData, notes: v})} />
          <Button title="Сохранить" onPress={submitFieldData} />
          <Button title="Загрузить данные" onPress={fetchFieldData} />
          <FlatList
            data={fieldData}
            keyExtractor={(item) => item.id.toString()}
            renderItem={({ item }) => (
              <Text>{item.line_type} — {item.length} м, {item.material_used} кг</Text>
            )}
          />
        </>
      )}
    </View>
  );
}