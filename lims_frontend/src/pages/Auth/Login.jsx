import { Button, Label, TextInput, Card } from "flowbite-react";
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../../api/axios";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post("/accounts/login/", { username, password });

      // ambil token dan user dari response
      const { access, refresh, user } = res.data;

      // simpan token di localStorage
      localStorage.setItem("token", access);
      localStorage.setItem("refresh_token", refresh);

      // simpan user info di localStorage
      localStorage.setItem("user", JSON.stringify(user));

      // update state user di App.jsx
      if (onLogin) onLogin(user);

      alert(`Login berhasil! Selamat datang, ${user.username} (${user.role_display})`);
      navigate("/dashboard");
    } catch (err) {
      console.error("Login error:", err.response?.data || err.message);
      alert("Login gagal, cek username/password");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-50">
      <Card className="w-96">
        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <div>
            <Label htmlFor="username" value="Username" />
            <TextInput
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div>
            <Label htmlFor="password" value="Password" />
            <TextInput
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <Button type="submit">Login</Button>
        </form>

        {/* Tombol ke halaman Register di luar form */}
        <div className="text-center mt-4">
          <Link to="/register" className="text-blue-600 hover:underline">
            Belum punya akun? Register di sini
          </Link>
        </div>
      </Card>
    </div>
  );
}
