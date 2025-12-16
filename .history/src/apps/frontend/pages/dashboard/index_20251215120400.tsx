import React, { useEffect, useState } from 'react';
import axios from 'axios';
d;
interface Task {
  id: number;
  title: string;
  description: string;
  is_completed: boolean;
}

const Dashboard: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isEditingId, setIsEditingId] = useState<number | null>(null);

  // --- CONFIGURATION ---
  // 1. YOUR REAL ACCOUNT ID
  const ACCOUNT_ID = '693f99e5ca59562f35431332';
  const API_URL = `http://localhost:8080/api/accounts/${ACCOUNT_ID}/tasks`;

  // 2. HELPER: Get Headers with CORRECT Token Name
  const getHeaders = () => {
    // FIX: Changed 'access_token' to 'access-token' to match your browser
    const token = localStorage.getItem('access-token');
    return {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    };
  };

  // 3. Load Tasks
  const fetchTasks = async () => {
    try {
      const response = await axios.get(API_URL, { headers: getHeaders() });
      const data = Array.isArray(response.data)
        ? response.data
        : response.data.data || [];
      setTasks(data);
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  // 4. Add or Update Task
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        title,
        description,
        account_id: ACCOUNT_ID,
      };

      if (isEditingId) {
        await axios.put(`${API_URL}/${isEditingId}`, payload, {
          headers: getHeaders(),
        });
      } else {
        await axios.post(API_URL, payload, { headers: getHeaders() });
      }

      setTitle('');
      setDescription('');
      setIsEditingId(null);
      fetchTasks();
    } catch (error) {
      console.error('Error saving task:', error);
      alert('Error saving task. Check console for details.');
    }
  };

  // 5. Delete Task
  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete this task?')) return;
    try {
      await axios.delete(`${API_URL}/${id}`, { headers: getHeaders() });
      fetchTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  const handleEdit = (task: Task) => {
    setIsEditingId(task.id);
    setTitle(task.title);
    setDescription(task.description);
  };

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 className="text-2xl font-bold mb-4">My Tasks</h1>

      {/* Form */}
      <div
        style={{
          background: '#f4f4f4',
          padding: '20px',
          borderRadius: '8px',
          marginBottom: '20px',
        }}
      >
        <h3 className="font-bold mb-2">
          {isEditingId ? 'Edit Task' : 'New Task'}
        </h3>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            style={{ padding: '8px', flex: 1 }}
          />
          <input
            type="text"
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            style={{ padding: '8px', flex: 2 }}
          />
          <button
            type="submit"
            style={{
              padding: '8px 16px',
              background: '#007bff',
              color: 'white',
              border: 'none',
            }}
          >
            {isEditingId ? 'Save' : 'Add'}
          </button>
        </form>
      </div>

      {/* List */}
      <div>
        {tasks.map((task) => (
          <div
            key={task.id}
            style={{
              borderBottom: '1px solid #eee',
              padding: '15px',
              display: 'flex',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <strong>{task.title}</strong>
              <div style={{ color: '#666' }}>{task.description}</div>
            </div>
            <div>
              <button
                onClick={() => handleEdit(task)}
                style={{ marginRight: '10px', color: 'blue' }}
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(task.id)}
                style={{ color: 'red' }}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
