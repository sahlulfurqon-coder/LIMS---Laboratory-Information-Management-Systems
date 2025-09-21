import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Requests() {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    const fetchRequests = async () => {
      try {
        const res = await api.get("/requests/external/");
        setRequests(res.data); 
      } catch (err) {
        console.error("Gagal fetch requests:", err);
      }
    };

    fetchRequests();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Requests Eksternal</h1>
      <table className="w-full border">
        <thead className="bg-gray-200">
          <tr>
            <th className="p-2 border">ID</th>
            <th className="p-2 border">Requester</th>
            <th className="p-2 border">Jenis</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((r) => (
            <tr key={r.id}>
              <td className="p-2 border">{r.id}</td>
              <td className="p-2 border">{r.requester}</td>
              <td className="p-2 border">{r.type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}