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

// Komponen PrivateRoute: hanya render children kalau user login
function PrivateRoute({ user, children }) {
  if (!user) return <Navigate to="/login" replace />;
  return children;
}

function App() {
  const [user, setUser] = useState(null);

  // Ambil user dari localStorage saat pertama kali load
  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) setUser(JSON.parse(storedUser));
  }, []);

  const handleLogin = (userData) => {
    if (userData?.access) localStorage.setItem("token", userData.access);
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
        {user && <AppSidebar user={user} />}

        <div className="flex-1 p-4">
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login onLogin={handleLogin} />} />
            <Route path="/register" element={<Register />} />

            {/* Private routes */}
            <Route
              path="/dashboard"
              element={
                <PrivateRoute user={user}>
                  <Dashboard user={user} />
                </PrivateRoute>
              }
            />
            <Route
              path="/samples"
              element={
                <PrivateRoute user={user}>
                  <Samples />
                </PrivateRoute>
              }
            />
            <Route
              path="/analysis"
              element={
                <PrivateRoute user={user}>
                  <Analysis />
                </PrivateRoute>
              }
            />
            <Route
              path="/specs"
              element={
                <PrivateRoute user={user}>
                  <Specs />
                </PrivateRoute>
              }
            />
            <Route
              path="/complaints"
              element={
                <PrivateRoute user={user}>
                  <Complaints />
                </PrivateRoute>
              }
            />
            <Route
              path="/documents"
              element={
                <PrivateRoute user={user}>
                  <Documents />
                </PrivateRoute>
              }
            />
            <Route
              path="/requests"
              element={
                <PrivateRoute user={user}>
                  <Requests />
                </PrivateRoute>
              }
            />
            <Route
              path="/inventory"
              element={
                <PrivateRoute user={user}>
                  <Inventory />
                </PrivateRoute>
              }
            />
            <Route
              path="/reports"
              element={
                <PrivateRoute user={user}>
                  <Reports />
                </PrivateRoute>
              }
            />

            {/* Redirect root & unknown */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
