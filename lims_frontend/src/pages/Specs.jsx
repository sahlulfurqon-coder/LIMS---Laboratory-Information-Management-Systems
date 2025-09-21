import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Specs() {
  const [specs, setSpecs] = useState([]);

  useEffect(() => {
    const fetchSpecs = async () => {
      try {
        const res = await api.get("/specs/");
        setSpecs(res.data);
      } catch (error) {
        console.error("Gagal mengambil data specs:", error);
      }
    };

    fetchSpecs();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Spesifikasi Produk</h1>
      <ul className="space-y-2">
        {specs.map((s) => (
          <li key={s.id} className="p-4 border rounded bg-white shadow">
            <h2 className="font-semibold">{s.name}</h2>
            <p>Kriteria: {s.criteria}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}