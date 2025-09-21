import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Complaints() {
  const [complaints, setComplaints] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchComplaints = async () => {
      try {
        const res = await api.get("/complaints/");
        setComplaints(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        console.error("Error fetch complaints:", err.response?.data || err.message);
        setError("Gagal memuat data complaints, pastikan sudah login.");
      }
    };

    fetchComplaints();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Daftar Complaints</h1>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      <table className="w-full border">
        <thead className="bg-gray-200">
          <tr>
            <th className="p-2 border">ID</th>
            <th className="p-2 border">Deskripsi</th>
            <th className="p-2 border">Status</th>
          </tr>
        </thead>
        <tbody>
          {complaints.length > 0 ? (
            complaints.map((c) => (
              <tr key={c.id}>
                <td className="p-2 border">{c.id}</td>
                <td className="p-2 border">{c.description}</td>
                <td className="p-2 border">{c.status}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="3" className="text-center p-4 text-gray-500">
                Tidak ada complaint
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
