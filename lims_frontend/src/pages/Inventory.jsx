import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Inventory() {
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newItem, setNewItem] = useState({ name: "", stock: "" });
  const [editItem, setEditItem] = useState(null);

  // 🔹 Fetch data
  const fetchInventory = async () => {
    try {
      setLoading(true);
      const res = await api.get("/inventory/");
      setInventory(res.data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  // 🔹 Tambah data
  const addItem = async (e) => {
    e.preventDefault();
    await api.post("/inventory/", newItem);
    setNewItem({ name: "", stock: "" });
    fetchInventory();
  };

  // 🔹 Update data
  const updateItem = async (e) => {
    e.preventDefault();
    await api.put(`/inventory/${editItem.id}/`, editItem);
    setEditItem(null);
    fetchInventory();
  };

  // 🔹 Hapus data
  const deleteItem = async (id) => {
    if (!confirm("Yakin hapus item ini?")) return;
    await api.delete(`/inventory/${id}/`);
    fetchInventory();
  };

  if (loading) return <p className="p-6">Loading...</p>;

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Inventory</h1>

      {/* Form tambah item */}
      <form onSubmit={addItem} className="mb-6 flex gap-2">
        <input
          type="text"
          placeholder="Nama Bahan"
          value={newItem.name}
          onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
          className="border p-2 rounded w-1/2"
          required
        />
        <input
          type="number"
          placeholder="Stok"
          value={newItem.stock}
          onChange={(e) => setNewItem({ ...newItem, stock: e.target.value })}
          className="border p-2 rounded w-1/4"
          required
        />
        <button className="px-4 py-2 bg-green-600 text-white rounded">
          Tambah
        </button>
      </form>

      {/* Tabel data */}
      <table className="w-full border">
        <thead className="bg-gray-200">
          <tr>
            <th className="p-2 border">ID</th>
            <th className="p-2 border">Nama Bahan</th>
            <th className="p-2 border">Stok</th>
            <th className="p-2 border">Aksi</th>
          </tr>
        </thead>
        <tbody>
          {inventory.map((i) => (
            <tr key={i.id}>
              <td className="p-2 border">{i.id}</td>
              <td className="p-2 border">
                {editItem?.id === i.id ? (
                  <input
                    value={editItem.name}
                    onChange={(e) =>
                      setEditItem({ ...editItem, name: e.target.value })
                    }
                    className="border p-1"
                  />
                ) : (
                  i.name
                )}
              </td>
              <td className="p-2 border">
                {editItem?.id === i.id ? (
                  <input
                    type="number"
                    value={editItem.stock}
                    onChange={(e) =>
                      setEditItem({ ...editItem, stock: e.target.value })
                    }
                    className="border p-1 w-20"
                  />
                ) : (
                  i.stock
                )}
              </td>
              <td className="p-2 border flex gap-2">
                {editItem?.id === i.id ? (
                  <>
                    <button
                      onClick={updateItem}
                      className="px-2 py-1 bg-blue-600 text-white rounded"
                    >
                      Simpan
                    </button>
                    <button
                      onClick={() => setEditItem(null)}
                      className="px-2 py-1 bg-gray-500 text-white rounded"
                    >
                      Batal
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      onClick={() => setEditItem(i)}
                      className="px-2 py-1 bg-yellow-500 text-white rounded"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => deleteItem(i.id)}
                      className="px-2 py-1 bg-red-600 text-white rounded"
                    >
                      Hapus
                    </button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
