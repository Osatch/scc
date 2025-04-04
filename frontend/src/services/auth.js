import jwt_decode from "jwt-decode";

export function isAuthenticated() {
  const token = localStorage.getItem("access");
  if (!token) return false;

  try {
    const decoded = jwt_decode(token);
    return decoded.exp > Date.now() / 1000;
  } catch (e) {
    return false;
  }
}

export async function refreshToken() {
  const refresh = localStorage.getItem("refresh");
  if (!refresh) return null;

  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh })
    });

    if (!res.ok) throw new Error("Token refresh failed");
    const data = await res.json();
    localStorage.setItem("access", data.access);
    return data.access;
  } catch (err) {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    return null;
  }
}
