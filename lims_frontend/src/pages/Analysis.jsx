import React, { useState, useEffect } from "react";
import api from "../api/axios";

export default function Analysis() {
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [formData, setFormData] = useState({});

  // ambil daftar task analyst
  useEffect(() => {
    api.get("/analysis/results/")
      .then(res => setTasks(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleSelectTask = (task) => {
    setSelectedTask(task);
    const initialData = {};
    ['raw_material','fatblend','finished_product','packaging'].forEach(key => {
      if(task[key]) initialData[key] = task[key];
    });
    initialData.remarks = task.remarks || "";
    setFormData(initialData);
  };

  const handleStartTask = () => {
    api.post(`/analysis/results/${selectedTask.id}/start/`)
      .then(res => setSelectedTask({...selectedTask, status: "in_progress", started_at: res.data.started_at}))
      .catch(err => console.error(err));
  };

  const handleChange = (section, field, value) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const handleSubmit = () => {
    api.post(`/analysis/results/${selectedTask.id}/submit/`, formData)
      .then(res => {
        alert("Task submitted!");
        setTasks(prev => prev.map(t => t.id === res.data.id ? res.data : t));
        setSelectedTask(res.data);
      })
      .catch(err => console.error(err));
  };

  return (
    <div>
      <h1>Analyst Tasks</h1>
      <div style={{display:"flex", gap:"2rem"}}>
        <div style={{flex:1}}>
          <h2>Task List</h2>
          <ul>
            {tasks.map(task => (
              <li key={task.id}>
                <button onClick={() => handleSelectTask(task)}>
                  {task.analysis_type.name} - {task.sample.code} [{task.status}]
                </button>
              </li>
            ))}
          </ul>
        </div>

        {selectedTask && (
          <div style={{flex:2}}>
            <h2>Task Detail: {selectedTask.sample.code}</h2>
            <p>Status: {selectedTask.status}</p>
            {selectedTask.status === "pending" && <button onClick={handleStartTask}>Start Task</button>}

            {selectedTask.status === "in_progress" && (
              <div>
                {['raw_material','fatblend','finished_product','packaging'].map(section => {
                  const sectionData = formData[section] || {};
                  return sectionData && (
                    <div key={section} style={{marginBottom:"1rem"}}>
                      <h3>{section.replace("_"," ").toUpperCase()}</h3>
                      {Object.keys(sectionData).map(field => (
                        <div key={field}>
                          <label>{field}: </label>
                          <input
                            type="text"
                            value={sectionData[field]}
                            onChange={e => handleChange(section, field, e.target.value)}
                          />
                        </div>
                      ))}
                    </div>
                  );
                })}

                <div>
                  <label>Remarks: </label>
                  <textarea
                    value={formData.remarks}
                    onChange={e => setFormData({...formData, remarks: e.target.value})}
                  />
                </div>

                <button onClick={handleSubmit}>Submit Task</button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
