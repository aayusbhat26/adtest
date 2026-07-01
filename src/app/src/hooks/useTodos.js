import { useState, useEffect, useCallback } from "react";
import { createTodo, fetchTodos } from "../api/todoApi";

export function useTodos() {
  const [todos, setTodos] = useState([]);
  const [error, setError] = useState("");

  const [loading, setLoading] = useState(false);

  const loadTodos = useCallback(async () => {
    try {
      const data = await fetchTodos();
      setTodos(data);
      setError("");
    } catch (err) {
      setError("Failed to load todos from the server");
      console.error(err);
    }
  }, []);

  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  const addTodo = async (title) => {
    setLoading(true);
    try {
      await createTodo(title);

      setError("");
      await loadTodos();
      return true;
    } catch (err) {
      setError("Failed to add todo");
      console.error(err);
      return false;
    } finally {
      setLoading(false);
    }
  };

  return {
    todos,
    loading,
    error,
    addTodo,
  };
}
