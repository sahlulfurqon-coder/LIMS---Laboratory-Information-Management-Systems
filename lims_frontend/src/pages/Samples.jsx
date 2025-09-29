import { useEffect, useState } from "react";
import { Button, Label, TextInput, Select, Card } from "flowbite-react";
import api from "../api/axios";

export default function Samples() {
  const [samples, setSamples] = useState([]);
  const [loading, setLoading] = useState(false);

  // pilihan dari backend
  const [sampleTypes, setSampleTypes] = useState([]);
  const [rawMaterials, setRawMaterials] = useState([]);

  // form state
  const [type, setType] = useState("");
  const [rawMatType, setRawMatType] = useState("");
  const [tank, setTank] = useState("");
  const [name, setName] = useState("");
  const [date, setDate] = useState("");

  // ===== API =====
  const fetchSamples = async () => {
    try {
      const res = await api.get("/samples/");
      setSamples(Array.isArray(res.data) ? res.data : res.data.results || []);
    } catch (error) {
      console.error("Gagal mengambil data samples:", error);
    }
  };

  const fetchOptions = async () => {
    try {
      const [st, rm] = await Promise.all([
        api.get("/sample-types/"),
        api.get("/raw-materials/"),
      ]);
      setSampleTypes(st.data);
      setRawMaterials(rm.data);
    } catch (error) {
      console.error("Gagal ambil data pilihan:", error);
    }
  };

  useEffect(() => {
    fetchSamples();
    fetchOptions();
  }, []);

  // ===== Actions =====
  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        type, // ID SampleType
        detail: rawMatType || null, // ID RawMaterial kalau ada
        tank: tank || null,
        name: name || "",
      };

      const res = await api.post("/samples/", payload);

      alert(`Sample berhasil dibuat. Kode: ${res.data.code}`);

      // reset
      setType("");
      setRawMatType("");
      setTank("");
      setDate("");
      setName("");
      fetchSamples();
    } catch (error) {
      console.error("Gagal register sample:", error.response?.data || error);
      alert("Gagal menyimpan sampel. Cek console untuk detail.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 space-y-8">
      {/* Form Input */}
      <Card>
        <form onSubmit={handleRegister} className="flex flex-col gap-4">
          <div>
            <Label htmlFor="type" value="Jenis Sampel" />
            <Select
              id="type"
              value={type}
              onChange={(e) => setType(e.target.value)}
            >
              <option value="">Pilih jenis</option>
              {sampleTypes.map((st) => (
                <option key={st.id} value={st.id}>
                  {st.name}
                </option>
              ))}
            </Select>
          </div>

          {type &&
            sampleTypes.find((st) => st.id === parseInt(type))?.name ===
              "Raw Material" && (
              <>
                <div>
                  <Label htmlFor="rawMatType" value="Jenis Minyak (Olein, Stearin, dll)" />
                  <Select
                    id="rawMatType"
                    value={rawMatType}
                    onChange={(e) => setRawMatType(e.target.value)}
                  >
                    <option value="">-- pilih --</option>
                    {rawMaterials.map((rm) => (
                      <option key={rm.id} value={rm.id}>
                        {rm.name} {rm.variant}
                      </option>
                    ))}
                  </Select>
                </div>

                <div>
                  <Label htmlFor="tank" value="Tangki" />
                  <Select
                    id="tank"
                    value={tank}
                    onChange={(e) => setTank(e.target.value)}
                  >
                    <option value="">Pilih</option>
                    {[
                      "J2","J3","J4","J5","J6","J7","J8","J9","J10","J11","J12","J13",
                      "TA","TB","TC","TD","TE","TF"
                    ].map((t) => (
                      <option key={t} value={t}>{t}</option>
                    ))}
                  </Select>
                </div>
              </>
            )}

          <div>
            <Label htmlFor="name" value="Nama Sampel" />
            <TextInput
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div>
            <Label htmlFor="date" value="Tanggal Pengisian" />
            <TextInput
              id="date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>

          <Button type="submit" disabled={loading}>
            {loading ? "Menyimpan..." : "Simpan"}
          </Button>
        </form>
      </Card>

      {/* Tabel Samples */}
      <Card>
        <h2 className="text-lg font-semibold mb-4">Daftar Sampel</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-300">
            <thead className="bg-gray-100">
              <tr>
                <th className="border px-2 py-1 text-left">Kode</th>
                <th className="border px-2 py-1 text-left">Nama</th>
                <th className="border px-2 py-1 text-left">Jenis</th>
                <th className="border px-2 py-1 text-left">Status</th>
              </tr>
            </thead>
            <tbody>
              {samples.length > 0 ? (
                samples.map((s) => (
                  <tr key={s.id} className="bg-white">
                    <td className="border px-2 py-1 font-medium">{s.code}</td>
                    <td className="border px-2 py-1">{s.name}</td>
                    <td className="border px-2 py-1">{sampleTypes.find((st) => st.id === s.type)?.name || "-"}</td>
                    <td className="border px-2 py-1">
                      <span
                        className={`px-2 py-1 rounded text-xs font-semibold ${
                          s.status === "registered"
                            ? "bg-blue-100 text-blue-700"
                            : s.status === "in_progress"
                            ? "bg-yellow-100 text-yellow-700"
                            : "bg-green-100 text-green-700"
                        }`}
                      >
                        {s.status}
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={4} className="text-center border px-2 py-1">
                    Belum ada sampel
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
