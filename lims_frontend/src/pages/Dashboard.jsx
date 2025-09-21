import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  FileText,
  Users,
  ClipboardList,
  Package,
  AlertCircle,
  Book,
  FilePlus,
  Archive,
  BarChart,
  ChevronRight,
  X,
} from "lucide-react";

// Dashboard.react.jsx
// Full, self-contained React component (Tailwind CSS assumed available)
// - includes sample data (replace with API fetch)
// - responsive grid, card component, and a right-side drawer "View all"
// - default export

export default function Dashboard({ user, onLogout }) {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [drawer, setDrawer] = useState({ open: false, id: null });

  useEffect(() => {
    if (!user) navigate("/login");
  }, [user, navigate]);

  useEffect(() => {
    // TODO: Replace with fetch to your backend API
    const sampleData = {
      accounts: Array.from({ length: 10 }, (_, i) => `User ${i + 1}`),
      samples: Array.from({ length: 10 }, (_, i) => `Sample ${i + 1}`),
      analysis: Array.from({ length: 10 }, (_, i) => `Analysis Job #${i + 1}`),
      specs: Array.from({ length: 10 }, (_, i) => `Spec ${i + 1}`),
      complaints: Array.from({ length: 10 }, (_, i) => `Complaint ${i + 1}`),
      documents: Array.from({ length: 10 }, (_, i) => `Document ${i + 1}`),
      requests: Array.from({ length: 10 }, (_, i) => `Request ${i + 1}`),
      inventory: Array.from({ length: 10 }, (_, i) => `Stock Item ${i + 1}`),
      reports: Array.from({ length: 10 }, (_, i) => `Report #${i + 1}`),
    };

    // simulate loading
    const t = setTimeout(() => {
      setData(sampleData);
      setLoading(false);
    }, 200);

    return () => clearTimeout(t);
  }, []);

  if (!user) return null;

  if (loading || !data)
    return (
      <div className="p-6 max-w-7xl mx-auto">
        <div className="animate-pulse h-6 w-40 bg-gray-200 rounded mb-4"></div>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="h-28 bg-white rounded-2xl shadow p-4" />
          ))}
        </div>
      </div>
    );

  const cards = [
    { id: "accounts", title: "Accounts", icon: <Users className="w-6 h-6" />, color: "from-indigo-500 to-indigo-600" },
    { id: "samples", title: "Samples", icon: <ClipboardList className="w-6 h-6" />, color: "from-emerald-500 to-emerald-600" },
    { id: "analysis", title: "Analysis", icon: <FileText className="w-6 h-6" />, color: "from-blue-500 to-blue-600" },
    { id: "specs", title: "Specs", icon: <Book className="w-6 h-6" />, color: "from-purple-500 to-purple-600" },
    { id: "complaints", title: "Complaints", icon: <AlertCircle className="w-6 h-6" />, color: "from-rose-500 to-rose-600" },
    { id: "documents", title: "Documents", icon: <Archive className="w-6 h-6" />, color: "from-sky-500 to-sky-600" },
    { id: "requests", title: "Requests", icon: <FilePlus className="w-6 h-6" />, color: "from-green-500 to-green-600" },
    { id: "inventory", title: "Inventory", icon: <Package className="w-6 h-6" />, color: "from-orange-500 to-orange-600" },
    { id: "reports", title: "Reports", icon: <BarChart className="w-6 h-6" />, color: "from-teal-500 to-teal-600" },
  ];

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold">Hi, {user.username} 👋</h1>
          <p className="text-sm text-gray-500">Role: {user.role}</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <input
              aria-label="Search"
              placeholder="Search anything..."
              className="px-4 py-2 rounded-lg border border-gray-200 shadow-sm w-64 focus:outline-none focus:ring-2 focus:ring-indigo-200"
            />
            <button
              onClick={() => navigate('/search')}
              className="absolute right-1 top-1/2 -translate-y-1/2 px-2 text-sm text-indigo-600"
            >
              Search
            </button>
          </div>

          <button
            onClick={() => onLogout?.()}
            className="px-3 py-2 rounded-lg border border-gray-200 text-sm hover:bg-gray-50"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Grid */}
      <section className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {cards.map((c) => (
          <DashboardCard
            key={c.id}
            id={c.id}
            title={c.title}
            icon={c.icon}
            color={c.color}
            items={data[c.id]}
            onViewAll={() => setDrawer({ open: true, id: c.id })}
            onGoto={() => navigate(`/dashboard/${c.id}`)}
          />
        ))}
      </section>

      {/* Drawer / Side panel for "View all" */}
      <AnimatePresence>
        {drawer.open && (
          <motion.aside
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed top-0 right-0 h-full w-full sm:w-96 bg-white shadow-xl z-50 flex flex-col"
            role="dialog"
            aria-modal="true"
          >
            <div className="flex items-center justify-between p-4 border-b">
              <div>
                <h3 className="font-semibold text-lg capitalize">{drawer.id}</h3>
                <p className="text-sm text-gray-500">{data[drawer.id].length} items</p>
              </div>
              <button
                onClick={() => setDrawer({ open: false, id: null })}
                aria-label="Close"
                className="p-2 rounded hover:bg-gray-100"
              >
                <X className="w-5 h-5 text-gray-600" />
              </button>
            </div>

            <div className="p-4 overflow-y-auto h-[calc(100%-64px)]">
              <ul className="space-y-2">
                {data[drawer.id].map((it, idx) => (
                  <li
                    key={idx}
                    className="flex items-center justify-between p-3 rounded bg-gray-50 hover:bg-gray-100"
                  >
                    <div className="truncate pr-4">{it}</div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => alert(`Open ${it}`)}
                        className="text-sm text-indigo-600 hover:underline"
                      >
                        Open
                      </button>
                      <ChevronRight className="w-4 h-4 text-gray-400" />
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>
    </div>
  );
}

function DashboardCard({ id, title, icon, color, items = [], onViewAll, onGoto }) {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="bg-white rounded-2xl shadow p-5 flex flex-col justify-between"
      role="group"
    >
      <div className="flex items-center justify-between">
        <div className={`p-3 rounded-xl bg-gradient-to-r ${color} text-white shadow-sm`}>
          {icon}
        </div>
        <span className="text-2xl font-bold">{items.length}</span>
      </div>

      <h2 className="mt-3 text-lg font-semibold capitalize">{title}</h2>

      <ul className="mt-3 text-sm text-gray-600 space-y-1">
        {items.slice(0, 3).map((it, i) => (
          <li key={i} className="truncate">• {it}</li>
        ))}
      </ul>

      <div className="mt-4 flex items-center justify-between">
        <button
          onClick={onViewAll}
          className="text-sm text-indigo-600 hover:underline"
          aria-label={`View all ${title}`}
        >
          View all →
        </button>

        <button
          onClick={onGoto}
          className="px-3 py-1 rounded bg-indigo-50 text-indigo-700 text-sm flex items-center gap-2"
        >
          Open
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </motion.div>
  );
}
