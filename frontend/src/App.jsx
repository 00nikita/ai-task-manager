import {useState, useEffect} from "react"


function App() {

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [tasks, setTasks] = useState([]);

  const [title, setTitle] = useState("");

useEffect(() => {
  async function fetchTasks() {
    try {
      const response = await fetch("http://localhost:8000/tasks");

      if (!response.ok) {
        throw new Error("Failed to fetch tasks");
      }

      const data = await response.json();
      setTasks(data);

    } catch (err) {
      setError(err.message);

    } finally {
      setLoading(false);
    }
  }

  fetchTasks();
}, []);

async function addTask() {
  const response = await fetch("http://localhost:8000/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: title,
      completed: false,
    }),
  });

  const newTask = await response.json();
  setTasks((prevTasks) => [...prevTasks, newTask]);
}

async function toggleTask(task) {
  const response = await fetch(
    `http://localhost:8000/tasks/${task.id}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        completed: !task.completed
      })
    }
  );

  const updatedTask = await response.json();

  setTasks((prevTasks) =>
    prevTasks.map((t) =>
      t.id === task.id ? updatedTask : t
    )
  );
}

async function deleteTask(id) {
  const response = await fetch(
    `http://localhost:8000/tasks/${id}`,
    {
      method: "DELETE"
    }
  );

  if (!response.ok) {
    console.error("Failed to delete task");
    return;
  }

  setTasks((prevTasks) =>
    prevTasks.filter((task) => task.id !== id)
  );
}

  return(
    <div>
      <h1>Task Manager</h1>
      <input
        type="text"
        placeholder="Enter Task title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        style={{
          backgroundColor: "white",
          color: "black",
          border: "2px solid red",
          padding: "12px",
          width: "300px"
        }}
      />
      <button onClick={addTask} >
        Add Task
      </button>

      {loading && <p>Loading tasks...</p>}

      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul>
        {tasks.map((task) => (
          <li key={task.id}>
            <input
              type="checkbox"
              checked={task.completed}
            onChange={() => toggleTask(task)}
          />
          <span>{task.title}</span>
          <button onClick={() => deleteTask(task.id)}>
            Delete
          </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;