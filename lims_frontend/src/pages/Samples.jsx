import { useEffect, useState } from "react";
import { Button, Label, TextInput, Select, Card } from "flowbite-react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Samples() {
  const [samples, setSamples] = useState([]);
  const [loading, setLoading] = useState(false);

  // pilihan dari backend
  const [rawMaterials, setRawMaterials] = useState([]);
  const [fatBlends, setFatBlends] = useState([]);
  const [finishedProducts, setFinishedProducts] = useState([]);

  // form state
  const [type, setType] = useState("");
  const [tank, setTank] = useState("");
  const [date, setDate] = useState("");
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [fatBlendId, setFatBlendId] = useState("");
  const [finishedId, setFinishedId] = useState("");

  // filter state
  const [filterType, setFilterType] = useState("");

  const navigate = useNavigate();

  // ===== API =====
  const fetchSamples = async () => {
    try {
      let url = "/samples/";
      if (filterType) {
        url += `?type=${filterType}`;
      }
      const res = await api.get(url);
      setSamples(Array.isArray(res.data) ? res.data : res.data.results || []);
    } catch (error) {
      console.error("Gagal mengambil data samples:", error);
    }
  };

  const fetchOptions = async () => {
    try {
      const [rm, fb, fp] = await Promise.all([
        api.get("/raw-materials/"),
        api.get("/fat-blends/"),
        api.get("/finished-products/"),
      ]);
      setRawMaterials(rm.data);
      setFatBlends(fb.data);
      setFinishedProducts(fp.data);
    } catch (error) {
      console.error("Gagal ambil data pilihan:", error);
    }
  };

  useEffect(() => {
    fetchSamples();
    fetchOptions();
  }, [filterType]);

  // generate kode otomatis untuk raw material
  useEffect(() => {
    if (type === "raw_material" && tank && date) {
      const d = new Date(date);
      const dd = String(d.getDate()).padStart(2, "0");
      const mm = String(d.getMonth() + 1).padStart(2, "0");
      const yy = String(d.getFullYear()).slice(-2);
      setCode(`${tank}${dd}${mm}${yy}`);
    }
  }, [type, tank, date]);

  // ===== Actions =====
  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await api.post("/samples/", {
        type,
        code,
        name,
        related_fatblend: fatBlendId || null,
        related_finished: finishedId || null,
      });
      // reset
      setType("");
      setTank("");
      setDate("");
      setCode("");
      setName("");
      setFatBlendId("");
      setFinishedId("");
      fetchSamples();
    } catch (error) {
      console.error("Gagal register sample:", error.response?.data || error);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Yakin mau hapus sampel ini?")) return;
    try {
      setLoading(true);
      await api.delete(`/samples/${id}/`);
      fetchSamples();
    } catch (error) {
      console.error("Gagal hapus sample:", error.response?.data || error);
    } finally {
      setLoading(false);
    }
  };

  // ===== Render =====
  return (
    <div className="p-4">
      {/* Filter */}
      <div className="mb-4 flex gap-4 items-center">
        <Label value="Filter Jenis" />
        <Select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
        >
          <option value="">Semua</option>
          <option value="raw_material">Raw Material</option>
          <option value="fat_blend">Fat Blend</option>
          <option value="finished_product">Finished Product</option>
        </Select>
      </div>

      {/* Form Registrasi */}
      <Card className="mb-6">
        <form onSubmit={handleRegister} className="flex flex-col gap-4">
          <div>
            <Label value="Jenis Sampel" />
            <Select value={type} onChange={(e) => setType(e.target.value)}>
              <option value="">Pilih jenis</option>
              <option value="raw_material">Raw Material</option>
              <option value="fat_blend">Fat Blend</option>
              <option value="finished_product">Finished Product</option>
            </Select>
          </div>

          {type === "raw_material" && (
            <>
              <div>
                <Label value="Tangki" />
                <Select value={tank} onChange={(e) => setTank(e.target.value)}>
                  <option value="">Pilih Tangki</option>
                  {["J2","J3","J4","J5","TA","TB","TC","TD","TE","TF"].map((t) => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </Select>
              </div>
              <div>
                <Label value="Tanggal" />
                <TextInput
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                />
              </div>
            </>
          )}

          {type === "fat_blend" && (
            <div>
              <Label value="Pilih Fat Blend" />
              <Select
                value={fatBlendId}
                onChange={(e) => setFatBlendId(e.target.value)}
              >
                <option value="">-- pilih --</option>
                {fatBlends.map((fb) => (
                  <option key={fb.id} value={fb.id}>
                    {fb.name}
                  </option>
                ))}
              </Select>
            </div>
          )}

          {type === "finished_product" && (
            <div>
              <Label value="Pilih Finished Product" />
              <Select
                value={finishedId}
                onChange={(e) => setFinishedId(e.target.value)}
              >
                <option value="">-- pilih --</option>
                {finishedProducts.map((fp) => (
                  <option key={fp.id} value={fp.id}>
                    {fp.name} ({fp.batch_code})
                  </option>
                ))}
              </Select>
            </div>
          )}

          <div>
            <Label value="Nama Sampel" />
            <TextInput
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          {code && (
            <p className="text-sm text-gray-600">
              Kode Sampel: <b>{code}</b>
            </p>
          )}

          <Button type="submit">Simpan</Button>
        </form>
      </Card>

      {/* Daftar Sampel */}
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 border">
          <thead className="bg-gray-100">
            <tr>
              <th className="px-4 py-2 text-left">ID</th>
              <th className="px-4 py-2 text-left">Kode Sampel</th>
              <th className="px-4 py-2 text-left">Jenis</th>
              <th className="px-4 py-2 text-left">Nama</th>
              <th className="px-4 py-2 text-left">Tanggal</th>
              <th className="px-4 py-2 text-left">Aksi</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {samples.map((s) => (
              <tr key={s.id}>
                <td className="px-4 py-2">{s.id}</td>
                <td className="px-4 py-2">{s.code}</td>
                <td className="px-4 py-2">{s.type}</td>
                <td className="px-4 py-2">{s.name}</td>
                <td className="px-4 py-2">{s.registered_at?.slice(0,10)}</td>
                <td className="px-4 py-2 flex gap-2">
                  <Button
                    size="xs"
                    color="info"
                    onClick={() => navigate(`/analysis/${s.id}`)}
                  >
                    Analyze
                  </Button>
                  <Button
                    size="xs"
                    color="failure"
                    onClick={() => handleDelete(s.id)}
                    disabled={loading}
                  >
                    {loading ? "..." : "Delete"}
                  </Button>
                </td>
              </tr>
            ))}
            {samples.length === 0 && (
              <tr>
                <td colSpan="6" className="text-center py-4 text-gray-500">
                  Belum ada sampel terdaftar.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
