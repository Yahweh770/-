import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, FlatList, Alert, StyleSheet, ScrollView } from 'react-native';
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
  const [activeTab, setActiveTab] = useState('dashboard');
  const [objects, setObjects] = useState([]);
  const [materials, setMaterials] = useState([]);

  const login = () => {
    axios.post('http://localhost:5000/api/login', { username, password })
      .then(res => {
        setToken(res.data.token);
        Alert.alert('Успешный вход в Strod-Service Technology');
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

  const fetchObjects = () => {
    axios.get('http://localhost:5000/api/objects', {
      headers: { Authorization: token }
    })
    .then(res => setObjects(res.data))
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
      fetchFieldData(); // Обновить данные после добавления
    })
    .catch(err => console.error(err));
  };

  useEffect(() => {
    if (token) {
      fetchFieldData();
      fetchObjects();
    }
  }, [token]);

  const renderDashboard = () => (
    <View style={styles.container}>
      <Text style={styles.title}>Strod-Service Technology</Text>
      <Text style={styles.subtitle}>Система управления проектами</Text>
      
      <View style={styles.featuresContainer}>
        <Text style={styles.sectionTitle}>Основные возможности:</Text>
        <Text style={styles.feature}>• Управление объектами и их характеристиками</Text>
        <Text style={styles.feature}>• Учет материалов и норм расхода</Text>
        <Text style={styles.feature}>• Отслеживание типов линий и их параметров</Text>
        <Text style={styles.feature}>• Ведение учета полевых данных и отчетов</Text>
        <Text style={styles.feature}>• Управление подрядчиками и документами</Text>
        <Text style={styles.feature}>• Формирование отчетов и анализ данных</Text>
        <Text style={styles.feature}>• Загрузка и просмотр фотоотчетов</Text>
        <Text style={styles.feature}>• Хранение и управление файлами</Text>
        <Text style={styles.feature}>• Интеграция с внешними API</Text>
        <Text style={styles.feature}>• Уведомления и оповещения</Text>
      </View>
      
      <View style={styles.navButtons}>
        <Button title="Объекты" onPress={() => setActiveTab('objects')} />
        <Button title="Полевые данные" onPress={() => setActiveTab('fieldData')} />
        <Button title="Добавить данные" onPress={() => setActiveTab('addData')} />
      </View>
    </View>
  );

  const renderObjects = () => (
    <View style={styles.container}>
      <Text style={styles.title}>Объекты</Text>
      <Button title="Назад" onPress={() => setActiveTab('dashboard')} />
      
      <FlatList
        data={objects}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.itemCard}>
            <Text style={styles.itemName}>{item.name}</Text>
            <Text style={styles.itemLocation}>Местоположение: {item.location}</Text>
          </View>
        )}
      />
    </View>
  );

  const renderFieldData = () => (
    <View style={styles.container}>
      <Text style={styles.title}>Полевые данные</Text>
      <Button title="Обновить" onPress={fetchFieldData} />
      <Button title="Назад" onPress={() => setActiveTab('dashboard')} />
      
      <FlatList
        data={fieldData}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.itemCard}>
            <Text style={styles.itemName}>Тип линии: {item.line_type}</Text>
            <Text>Длина: {item.length} м</Text>
            <Text>Ширина: {item.width} м</Text>
            <Text>Расход материала: {item.material_used} кг</Text>
            <Text>Заметки: {item.notes}</Text>
            <Text>Дата: {new Date(item.date).toLocaleDateString()}</Text>
          </View>
        )}
      />
    </View>
  );

  const renderAddData = () => (
    <View style={styles.container}>
      <Text style={styles.title}>Добавить полевые данные</Text>
      <Button title="Назад" onPress={() => setActiveTab('dashboard')} />
      
      <View style={styles.formContainer}>
        <TextInput 
          style={styles.input} 
          placeholder="ID объекта" 
          value={formData.object_id} 
          onChangeText={(v) => setFormData({...formData, object_id: v})} 
          keyboardType="numeric"
        />
        <TextInput 
          style={styles.input} 
          placeholder="Тип линии" 
          value={formData.line_type} 
          onChangeText={(v) => setFormData({...formData, line_type: v})} 
        />
        <TextInput 
          style={styles.input} 
          placeholder="Длина (м)" 
          value={formData.length} 
          onChangeText={(v) => setFormData({...formData, length: v})} 
          keyboardType="numeric"
        />
        <TextInput 
          style={styles.input} 
          placeholder="Ширина (м)" 
          value={formData.width} 
          onChangeText={(v) => setFormData({...formData, width: v})} 
          keyboardType="numeric"
        />
        <TextInput 
          style={styles.input} 
          placeholder="Расход материала (кг)" 
          value={formData.material_used} 
          onChangeText={(v) => setFormData({...formData, material_used: v})} 
          keyboardType="numeric"
        />
        <TextInput 
          style={styles.input} 
          placeholder="Заметки" 
          value={formData.notes} 
          onChangeText={(v) => setFormData({...formData, notes: v})} 
          multiline
        />
        <Button title="Сохранить данные" onPress={submitFieldData} />
      </View>
    </View>
  );

  return (
    <View style={styles.mainContainer}>
      {!token ? (
        <View style={styles.loginContainer}>
          <Text style={styles.loginTitle}>Вход в Strod-Service Technology</Text>
          <TextInput 
            style={styles.input} 
            placeholder="Имя пользователя" 
            value={username} 
            onChangeText={setUsername} 
          />
          <TextInput 
            style={styles.input} 
            placeholder="Пароль" 
            value={password} 
            onChangeText={setPassword} 
            secureTextEntry 
          />
          <Button title="Войти" onPress={login} />
        </View>
      ) : (
        <View style={{ flex: 1 }}>
          {activeTab === 'dashboard' && renderDashboard()}
          {activeTab === 'objects' && renderObjects()}
          {activeTab === 'fieldData' && renderFieldData()}
          {activeTab === 'addData' && renderAddData()}
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loginContainer: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#fff',
  },
  loginTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 20,
    color: '#333',
  },
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 10,
    color: '#2c3e50',
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 20,
    color: '#7f8c8d',
  },
  featuresContainer: {
    marginBottom: 20,
    padding: 15,
    backgroundColor: '#ecf0f1',
    borderRadius: 8,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#2c3e50',
  },
  feature: {
    fontSize: 14,
    marginBottom: 5,
    color: '#34495e',
  },
  navButtons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
  },
  formContainer: {
    marginTop: 10,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    padding: 10,
    marginBottom: 10,
    borderRadius: 4,
    fontSize: 16,
  },
  itemCard: {
    backgroundColor: '#fff',
    padding: 15,
    marginBottom: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  itemName: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
    color: '#2c3e50',
  },
  itemLocation: {
    fontSize: 14,
    color: '#7f8c8d',
    marginBottom: 5,
  },
});