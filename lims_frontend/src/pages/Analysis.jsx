import React, { useEffect, useState } from "react";
import api from "../api/axios";

function Analysis({ sampleId }) {
  const [parameters, setParameters] = useState([]);
  const [results, setResults] = useState([]);
  const [value, setValue] = useState("");
  const [selectedParam, setSelectedParam] = useState("");

  useEffect(() => {
    api.get("/analysis/parameters/")
      .then(res => setParameters(res.data))
      .catch(err => console.error(err));

    api.get(`/analysis/results/?sample=${sampleId}`)
      .then(res => setResults(res.data))
      .catch(err => console.error(err));
  }, [sampleId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/analysis/results/", {
        sample: sampleId,
        parameter: selectedParam,
        value: value
      });
      setValue("");
      setSelectedParam("");
      const res = await api.get(`/analysis/results/?sample=${sampleId}`);
      setResults(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold">Analysis for Sample {sampleId}</h2>

      <form onSubmit={handleSubmit} className="flex gap-2 my-4">
        <select
          value={selectedParam}
          onChange={(e) => setSelectedParam(e.target.value)}
          className="border p-2 rounded"
        >
          <option value="">Select Parameter</option>
          {parameters.map(p => (
            <option key={p.id} value={p.id}>{p.name} ({p.unit})</option>
          ))}
        </select>
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Value"
          className="border p-2 rounded"
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Submit
        </button>
      </form>

      <h3 className="font-semibold mb-2">Results</h3>
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="border p-2">Parameter</th>
            <th className="border p-2">Value</th>
            <th className="border p-2">Status</th>
            <th className="border p-2">Analyst</th>
          </tr>
        </thead>
        <tbody>
          {results.map(r => (
            <tr key={r.id}>
              <td className="border p-2">{r.parameter_name}</td>
              <td className="border p-2">{r.value}</td>
              <td className="border p-2">{r.status}</td>
              <td className="border p-2">{r.analyst}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Analysis;
