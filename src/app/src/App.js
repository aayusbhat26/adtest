import "./App.css";
import { useState } from "react";
import { useTodos } from "./hooks/useTodos";

export function App() {
  const { todos, loading, error, addTodo } = useTodos();
  const [todoText, setTodoText] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const trimmed = todoText.trim();
    if (!trimmed) return;

    const success = await addTodo(trimmed);

    if (success) {
      setTodoText("");
    }
  };

  return (
    <div className="App">
      <div>
        <h1>Todos</h1>
        {error && <p style={{ color: "red", fontWeight: "bold" }}>{error}</p>}
        <ul>
          {todos.map((todo) => (
            <li key={todo._id}>{todo.title}</li>
          ))}
        </ul>
        {todos.length === 0 && !error && <p>No todos yet. Add one below!</p>}
      </div>

      <div>
        <h1>Add a todo</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="todo">Todo: </label>
            <input
              type="text"
              id="todo"
              value={todoText}
              onChange={(e) => setTodoText(e.target.value)}
              placeholder="What needs to be done?"
            />
          </div>
          <div style={{ marginTop: "10px" }}>
            <button type="submit" disabled={loading}>
              {loading ? "Saving..." : "Add todo"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
