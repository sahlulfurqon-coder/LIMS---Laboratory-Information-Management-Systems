import { Button, Label, TextInput, Card, Select } from "flowbite-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/axios";

export default function Register() {
  const [formData, setFormData] = useState({
    username: "", email: "", first_name: "", last_name: "",
    password: "", password2: "", role: "analyst", phone: "", department: ""
  });
  const navigate = useNavigate();

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/accounts/register/", formData);
      alert("User berhasil diregister!");
      navigate("/login");
    } catch (err) {
      console.error("Register error:", err.response?.data || err.message);
      alert("Gagal register! Cek input atau hak akses");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <Card className="w-96">
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Label value="Username" />
          <TextInput name="username" value={formData.username} onChange={handleChange} required />
          <Label value="Email" />
          <TextInput name="email" type="email" value={formData.email} onChange={handleChange} required />
          <Label value="First Name" />
          <TextInput name="first_name" value={formData.first_name} onChange={handleChange} />
          <Label value="Last Name" />
          <TextInput name="last_name" value={formData.last_name} onChange={handleChange} />
          <Label value="Password" />
          <TextInput name="password" type="password" value={formData.password} onChange={handleChange} required />
          <Label value="Confirm Password" />
          <TextInput name="password2" type="password" value={formData.password2} onChange={handleChange} required />
          <Label value="Role" />
          <Select name="role" value={formData.role} onChange={handleChange} required>
            <option value="analyst">Analyst</option>
            <option value="rnd">RnD</option>
            <option value="qa_supervisor">QA Supervisor</option>
            <option value="qa_manager">QA Manager</option>
            <option value="admin">Admin</option>
          </Select>
          <Label value="Phone" />
          <TextInput name="phone" value={formData.phone} onChange={handleChange} />
          <Label value="Department" />
          <TextInput name="department" value={formData.department} onChange={handleChange} />
          <Button type="submit">Register</Button>
        </form>
      </Card>
    </div>
  );
}
