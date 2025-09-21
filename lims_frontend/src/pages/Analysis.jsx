import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Analysis() {
  const [results, setResults] = useState([]);
  const [formData, setFormData] = useState({ parameter: "", value: "" });
  const [editingId, setEditingId] = useState(null);
  const [error, setError] = useState(null);

  // 🔹 Ambil data awal
  const fetchResults = async () => {
    try {
      const res = await api.get("/analysis/results/");
      setResults(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error("Fetch error:", err.response?.data || err.message);
      setError("Gagal mengambil data, mungkin perlu login dulu.");
    }
  };

  useEffect(() => {
    fetchResults();
  }, []);

  // 🔹 Tambah atau update
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingId) {
        // Update
        await api.put(`/analysis/results/${editingId}/`, formData);
      } else {
        // Create
        await api.post("/analysis/results/", formData);
      }
      setFormData({ parameter: "", value: "" });
      setEditingId(null);
      fetchResults();
    } catch (err) {
      console.error("Submit error:", err.response?.data || err.message);
      setError("Gagal menyimpan data.");
    }
  };

  // 🔹 Edit
  const handleEdit = (result) => {
    setFormData({ parameter: result.parameter, value: result.value });
    setEditingId(result.id);
  };

  // 🔹 Hapus
  const handleDelete = async (id) => {
    try {
      await api.delete(`/analysis/results/${id}/`);
      fetchResults();
    } catch (err) {
      console.error("Delete error:", err.response?.data || err.message);
      setError("Gagal menghapus data.");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Hasil Analisa</h1>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      {/* Form Tambah / Edit */}
      <form onSubmit={handleSubmit} className="mb-6 space-y-2">
        <input
          type="text"
          placeholder="Parameter"
          value={formData.parameter}
          onChange={(e) => setFormData({ ...formData, parameter: e.target.value })}
          className="border p-2 w-full"
          required
        />
        <input
          type="text"
          placeholder="Value"
          value={formData.value}
          onChange={(e) => setFormData({ ...formData, value: e.target.value })}
          className="border p-2 w-full"
          required
        />
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded"
        >
          {editingId ? "Update" : "Tambah"}
        </button>
      </form>

      {/* Tabel Data */}
      <table className="w-full border">
        <thead className="bg-gray-200">
          <tr>
            <th className="p-2 border">ID</th>
            <th className="p-2 border">Parameter</th>
            <th className="p-2 border">Result</th>
            <th className="p-2 border">Aksi</th>
          </tr>
        </thead>
        <tbody>
          {results.length > 0 ? (
            results.map((r) => (
              <tr key={r.id}>
                <td className="p-2 border">{r.id}</td>
                <td className="p-2 border">{r.parameter}</td>
                <td className="p-2 border">{r.value}</td>
                <td className="p-2 border space-x-2">
                  <button
                    onClick={() => handleEdit(r)}
                    className="bg-yellow-500 text-white px-2 py-1 rounded"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(r.id)}
                    className="bg-red-500 text-white px-2 py-1 rounded"
                  >
                    Hapus
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" className="text-center p-4 text-gray-500">
                Tidak ada data
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
