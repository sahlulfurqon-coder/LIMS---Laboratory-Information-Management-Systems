import { useState } from "react";
import api from "../api/axios";

export default function Reports() {
  const [reportType, setReportType] = useState("samples");
  const [data, setData] = useState([]);

  const fetchReport = async (type) => {
    try {
      const res = await api.get(`/reports/${type}/`);
      setData(res.data); // axios
    } catch (err) {
      console.error("Gagal fetch report:", err);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-4">Reports</h1>
      <div className="flex gap-2 mb-4">
        {["samples", "analysis", "complaints", "inventory", "audit-trail"].map(
          (type) => (
            <button
              key={type}
              onClick={() => {
                setReportType(type);
                fetchReport(type);
              }}
              className="px-4 py-2 border rounded bg-gray-100 hover:bg-gray-200"
            >
              {type}
            </button>
          )
        )}
      </div>

      <pre className="bg-gray-900 text-white p-4 rounded">
        {JSON.stringify(data, null, 2)}
      </pre>
    </div>
  );
}