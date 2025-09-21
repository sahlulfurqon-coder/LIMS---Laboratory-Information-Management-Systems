import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import AppNavbar from "./components/Navbar";
import AppSidebar from "./components/Sidebar";

import Login from "./pages/Auth/Login";
import Register from "./pages/Auth/Register";
import Dashboard from "./pages/Dashboard";
import Samples from "./pages/Samples";
import Analysis from "./pages/Analysis";
import Specs from "./pages/Specs";
import Complaints from "./pages/Complaints";
import Documents from "./pages/Documents";
import Requests from "./pages/Requests";
import Inventory from "./pages/Inventory";
import Reports from "./pages/Reports";

function App() {
  const [user, setUser] = useState(null);

  // Ambil user dari localStorage saat pertama kali load
  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    if (userData?.access) {
      localStorage.setItem("token", userData.access);
    }
    localStorage.setItem("user", JSON.stringify(userData));
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    setUser(null);
  };

  return (
    <BrowserRouter>
      <AppNavbar user={user} onLogout={handleLogout} />

      <div className="flex min-h-screen">
        {/* Sidebar hanya muncul jika user sudah login */}
        {user && <AppSidebar user={user} />}

        <div className="flex-1 p-4">
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />

            {!user ? (
              <>
                <Route path="/login" element={<Login onLogin={handleLogin} />} />
                <Route path="/register" element={<Register />} />
              </>
            ) : (
              <>
                <Route path="/dashboard" element={<Dashboard user={user} />} />
                <Route path="/samples" element={<Samples />} />
                <Route path="/analysis" element={<Analysis />} />
                <Route path="/specs" element={<Specs />} />
                <Route path="/complaints" element={<Complaints />} />
                <Route path="/documents" element={<Documents />} />
                <Route path="/requests" element={<Requests />} />
                <Route path="/inventory" element={<Inventory />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </>
            )}
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
