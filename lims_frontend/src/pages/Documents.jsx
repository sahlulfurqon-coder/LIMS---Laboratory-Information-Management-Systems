import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Documents() {
  const [docs, setDocs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDocs = async () => {
      try {
        const res = await api.get("/documents/");
        setDocs(Array.isArray(res.data) ? res.data : []);
      } catch (err) {
        console.error("Error fetch documents:", err.response?.data || err.message);
        setError("Gagal memuat dokumen, pastikan sudah login.");
      }
    };

    fetchDocs();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Dokumen</h1>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      <ul className="space-y-2">
        {docs.length > 0 ? (
          docs.map((d) => (
            <li key={d.id} className="p-4 border rounded shadow bg-white">
              <a
                href={d.file}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 underline"
              >
                {d.name}
              </a>
            </li>
          ))
        ) : (
          <p className="text-gray-500">Tidak ada dokumen.</p>
        )}
      </ul>
    </div>
  );
}
