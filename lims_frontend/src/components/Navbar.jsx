import { Avatar, Dropdown, Navbar as FlowbiteNavbar } from "flowbite-react";
import { useNavigate } from "react-router-dom";

export default function AppNavbar({ user, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    // hapus token kalau ada
    localStorage.removeItem("token");
    sessionStorage.removeItem("token");

    if (onLogout) onLogout(); // callback tambahan

    // redirect ke login page
    navigate("/login");
    // atau pakai full reload: window.location.href = "http://localhost:5173/login";
  };

  return (
    <div className="bg-gray-100 flex justify-between items-center p-4">
      <span className="text-xl font-semibold">LIMS</span>
      <div className="flex items-center space-x-4">
        <span>{user?.username}</span>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-3 py-1 rounded"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
