const TODO_API_URL = "http://localhost:8000/todos/";

async function parseJsonResponse(response) {
  const data = await response.json();

  if (!response.ok) {
    const message = data?.error || "Request failed";
    throw new Error(message);
  }

  return data;
}

export async function fetchTodos() {
  const response = await fetch(TODO_API_URL);
  return parseJsonResponse(response);
}

export async function createTodo(title) {
  const response = await fetch(TODO_API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });

  return parseJsonResponse(response);
}
