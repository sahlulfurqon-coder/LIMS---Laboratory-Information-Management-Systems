// src/components/AppSidebar.jsx
import { NavLink } from "react-router-dom";
import {
  FlaskConical,
  Home,
  ClipboardList,
  CheckSquare,
  Box,
  AlertCircle,
  FileText,
  Package,
  BarChart2,
  Layers,
} from "lucide-react";

const menuConfig = {
  all: [
    { path: "/dashboard", label: "Dashboard", icon: Home },
    { path: "/samples", label: "Samples", icon: ClipboardList },
    { path: "/analysis", label: "Analysis", icon: CheckSquare },
    { path: "/specs", label: "Specs", icon: Box },
    { path: "/complaints", label: "Complaints", icon: AlertCircle },
    { path: "/documents", label: "Documents", icon: FileText },
    { path: "/requests", label: "Requests", icon: Layers },
    { path: "/inventory", label: "Inventory", icon: Package },
    { path: "/reports", label: "Reports", icon: BarChart2 },
  ],
  analyst: [
    { path: "/dashboard", label: "Dashboard", icon: Home },
    { path: "/samples", label: "Samples", icon: ClipboardList },
    { path: "/analysis", label: "Analysis", icon: CheckSquare },
    { path: "/reports", label: "Reports", icon: BarChart2 },
  ],
};

export default function AppSidebar({ user }) {
  if (!user) return null;

  const role = user.role?.toLowerCase();
  const fullAccessRoles = ["admin", "qa_supervisor", "qa_manager"];
  console.log("Role dari backend:", user.role);

  const menus = fullAccessRoles.includes(role)
    ? menuConfig.all
    : menuConfig[role] || [];

  return (
    <aside className="w-64 bg-gray-900 text-gray-200 flex flex-col min-h-screen shadow-lg">
      {/* Logo Section */}
      <div className="flex items-center gap-3 p-4 border-b border-gray-700">
        <div className="bg-blue-600 p-2 rounded-lg">
          <FlaskConical size={28} className="text-white" />
        </div>
        <div>
          <h2 className="text-lg font-bold text-white">LIMS</h2>
          <p className="text-xs text-gray-400">Laboratory System</p>
        </div>
      </div>

      {/* Role Info */}
      <div className="px-4 py-2 border-b border-gray-700 text-sm text-gray-400">
        Role: <span className="font-medium text-white">{role}</span>
      </div>

      {/* Menu List */}
      <nav className="flex-1 p-2">
        <ul className="space-y-1">
          {menus.map(({ path, label, icon: Icon }) => (
            <li key={path}>
              <NavLink
                to={path}
                className={({ isActive }) =>
                  `flex items-center gap-2 px-4 py-2 rounded-md transition ${
                    isActive
                      ? "bg-blue-600 text-white font-medium"
                      : "text-gray-300 hover:bg-gray-700 hover:text-white"
                  }`
                }
              >
                <Icon size={18} />
                <span>{label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-700 text-xs text-gray-500">
        © 2025 LIMS
      </div>
    </aside>
  );
}
