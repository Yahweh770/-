import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [files, setFiles] = useState([]);
  const [input, setInput] = useState('');
  const [username, setUsername] = useState('user1');
  const [file, setFile] = useState(null);

  useEffect(() => {
    const socket = io('http://localhost:5000');

    socket.on('new_message', (data) => {
      setMessages(prev => [...prev, data]);
    });

    socket.on('new_file', (data) => {
      setFiles(prev => [...prev, data]);
    });

    return () => socket.close();
  }, []);

  const sendMessage = () => {
    if (input.trim()) {
      const socket = io('http://localhost:5000');
      socket.emit('send_message', { username, message: input });
      setInput('');
    }
  };

  const sendFile = () => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      const socket = io('http://localhost:5000');
      socket.emit('send_file', { username, file: formData });
      setFile(null);
    }
  };

  return (
    <div>
      <h3>Чат</h3>
      <div>
        {messages.map((msg, i) => (
          <div key={i}>
            <strong>{msg.username}</strong>: {msg.message} ({msg.timestamp})
          </div>
        ))}
        {files.map((f, i) => (
          <div key={i}>
            <strong>{f.username}</strong> отправил файл: <a href={f.url} target="_blank">{f.filename}</a> ({f.timestamp})
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Введите сообщение..."
      />
      <button onClick={sendMessage}>Отправить</button>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={sendFile}>Отправить файл</button>
    </div>
  );
}