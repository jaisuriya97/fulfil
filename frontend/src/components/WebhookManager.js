import React, { useState, useEffect } from "react";
import axios from "axios";
import API_URL from "../apiConfig";

function WebhookManager() {
  const [webhooks, setWebhooks] = useState([]);
  const [newUrl, setNewUrl] = useState("");
  const [testResults, setTestResults] = useState({});

  const fetchWebhooks = async () => {
    try {
      const res = await axios.get(`${API_URL}/api/webhooks`);
      setWebhooks(res.data);
    } catch (err) {
      console.error("Error fetching webhooks:", err);
    }
  };

  useEffect(() => {
    fetchWebhooks();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!newUrl) return;
    try {
      await axios.post(`${API_URL}/api/webhooks`, { url: newUrl });
      setNewUrl("");
      fetchWebhooks();
    } catch (err) {
      console.error("Error adding webhook:", err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API_URL}/api/webhooks/${id}`);
      fetchWebhooks();
    } catch (err) {
      console.error("Error deleting webhook:", err);
    }
  };

  const handleTest = async (id) => {
    try {
      setTestResults((prev) => ({ ...prev, [id]: "Testing..." }));
      const res = await axios.post(`${API_URL}/api/webhooks/test/${id}`);
      setTestResults((prev) => ({
        ...prev,
        [id]: `Test OK (Status: ${res.data.dummy_response.status})`,
      }));
    } catch (err) {
      setTestResults((prev) => ({ ...prev, [id]: "Test Failed" }));
    }
  };

  return (
    <div className="card">
      <h3>Story 4: Webhook Management</h3>
      <form onSubmit={handleAdd}>
        <input
          type="url"
          value={newUrl}
          onChange={(e) => setNewUrl(e.target.value)}
          placeholder="Enter new webhook URL"
        />
        <button type="submit">Add Webhook</button>
      </form>

      <ul>
        {webhooks.map((w) => (
          <li key={w.id}>
            <span>{w.url}</span>
            <div>
              <button onClick={() => handleTest(w.id)}>Test</button>
              <button
                onClick={() => handleDelete(w.id)}
                className="small-danger"
              >
                Delete
              </button>
            </div>
            {testResults[w.id] && <small>{testResults[w.id]}</small>}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default WebhookManager;
