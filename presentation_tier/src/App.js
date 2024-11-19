// import React, { useState, useEffect } from 'react';
// import './App.css';

// const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';

// function App() {
//   const [todos, setTodos] = useState([]);
//   const [newTodo, setNewTodo] = useState('');
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     fetchTodos();
//   }, []);

//   const fetchTodos = async () => {
//     try {
//       const response = await fetch(`${API_URL}/todos`);
//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }
//       const data = await response.json();
//       setTodos(Array.isArray(data) ? data : []);
//       setError(null);
//     } catch (error) {
//       console.error('Error fetching todos:', error);
//       setError('Failed to fetch todos. Please try again later.');
//       setTodos([]);
//     }
//   };

//   const addTodo = async () => {
//     if (newTodo.trim() === '') return;
//     try {
//       const response = await fetch(`${API_URL}/todos`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ task: newTodo }),
//       });
//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }
//       const data = await response.json();
//       setTodos(prevTodos => [...prevTodos, data]);
//       setNewTodo('');
//       setError(null);
//     } catch (error) {
//       console.error('Error adding todo:', error);
//       setError('Failed to add todo. Please try again later.');
//     }
//   };

//   const deleteTodo = async (id) => {
//     try {
//       const response = await fetch(`${API_URL}/todos/${id}`, { method: 'DELETE' });
//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }
//       setTodos(prevTodos => prevTodos.filter(todo => todo.id !== id));
//       setError(null);
//     } catch (error) {
//       console.error('Error deleting todo:', error);
//       setError('Failed to delete todo. Please try again later.');
//     }
//   };

//   return (
//     <div className="App">
//       <h1>Todo App</h1>
//       {error && <p style={{color: 'red'}}>{error}</p>}
//       <div>
//         <input
//           type="text"
//           value={newTodo}
//           onChange={(e) => setNewTodo(e.target.value)}
//           placeholder="Enter a new todo"
//         />
//         <button onClick={addTodo}>Add Todo</button>
//       </div>
//       <ul>
//         {todos.map((todo) => (
//           <li key={todo.id}>
//             {todo.task}
//             <button onClick={() => deleteTodo(todo.id)}>Delete</button>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// export default App;

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      // const response = await axios.post('http://44.211.61.254:3000/upload', formData, {

      const response = await axios.post(' http://localhost:3000/upload', formData, {



        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setMessage('File uploaded successfully: ' + response.data.file_url);
    } catch (error) {
      setMessage('Error uploading file: ' + error.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>File Upload</h1>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Upload</button>
        </form>
        {message && <p>{message}</p>}
      </header>
    </div>
  );
}

export default App;