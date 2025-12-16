import React, { useEffect, useState } from 'react';
import axios from 'axios';

// 1. Define what a Task looks like
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

  // 2. Function to load tasks (FIXED URL)
  const fetchTasks = async () => {
    try {
      // Changed /api/tasks to http://localhost:8080/tasks
      const response = await axios.get('http://localhost:8080/tasks');
      setTasks(response.data);
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  };

  // Load tasks when the page opens
  useEffect(() => {
    fetchTasks();
  }, []);

  // 3. Function to Add or Update a task
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (isEditingId) {
        // Update existing task (FIXED URL)
        await axios.put(`http://localhost:8080/api/tasks/${isEditingId}`, {
          title,
          description,
        });
      } else {
        // Create new task (FIXED URL)
        await axios.post('http://localhost:8080/tasks', { title, description });
      }

      setTitle('');
      setDescription('');
      setIsEditingId(null);
      fetchTasks();
    } catch (error) {
      console.error('Error saving task:', error);
      alert('Error saving task. Check backend terminal for details.');
    }
  };

  // 4. Function to Delete a task
  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete this task?')) return;
    try {
      // Delete task (FIXED URL)
      await axios.delete(`http://localhost:8080/tasks/${id}`);
      fetchTasks();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  // 5. Setup Form for Editing
  const handleEdit = (task: Task) => {
    setIsEditingId(task.id);
    setTitle(task.title);
    setDescription(task.description);
  };

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 className="text-2xl font-bold mb-4">Task Manager</h1>

      {/* --- The Form --- */}
      <div
        style={{
          background: '#f4f4f4',
          padding: '20px',
          borderRadius: '8px',
          marginBottom: '20px',
        }}
      >
        <h3 className="font-bold mb-2">
          {isEditingId ? 'Edit Task' : 'Add New Task'}
        </h3>
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            placeholder="Task Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            style={{
              padding: '8px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              flex: 1,
            }}
          />
          <input
            type="text"
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            style={{
              padding: '8px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              flex: 2,
            }}
          />
          <button
            type="submit"
            style={{
              padding: '8px 16px',
              background: '#007bff',
              color: 'white',
              borderRadius: '4px',
              border: 'none',
              cursor: 'pointer',
            }}
          >
            {isEditingId ? 'Update' : 'Add'}
          </button>

          {isEditingId && (
            <button
              type="button"
              onClick={() => {
                setIsEditingId(null);
                setTitle('');
                setDescription('');
              }}
              style={{
                padding: '8px 16px',
                background: '#ccc',
                borderRadius: '4px',
                border: 'none',
                cursor: 'pointer',
              }}
            >
              Cancel
            </button>
          )}
        </form>
      </div>

      {/* --- The List --- */}
      <div>
        {tasks.length === 0 ? <p>No tasks found. Add one above!</p> : null}

        {tasks.map((task) => (
          <div
            key={task.id}
            style={{
              borderBottom: '1px solid #eee',
              padding: '15px 0',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <div>
              <div style={{ fontWeight: 'bold', fontSize: '1.1em' }}>
                {task.title}
              </div>
              <div style={{ color: '#666' }}>{task.description}</div>
            </div>
            <div>
              <button
                onClick={() => handleEdit(task)}
                style={{
                  marginRight: '10px',
                  color: '#007bff',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  textDecoration: 'underline',
                }}
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(task.id)}
                style={{
                  color: 'red',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  textDecoration: 'underline',
                }}
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
