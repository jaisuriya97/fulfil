// src/components/FileUpload.js
import React, { useState, useEffect } from "react";
import axios from "axios";
import API_URL from "../apiConfig";
import { socket, joinRoom } from "../socket";

function FileUpload() {
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [jobId, setJobId] = useState(null);

  useEffect(() => {
    // Listen for progress updates
    socket.on("progress_update", (data) => {
      setProgress(data.progress);
      setStatus(data.status);
      setError("");
    });

    // Listen for task completion
    socket.on("task_complete", (data) => {
      setStatus(data.status);
      setProgress(100);
      setJobId(null); // Reset for next upload
    });

    // Listen for task failure
    socket.on("task_failed", (data) => {
      setError(`Error: ${data.error}`);
      setStatus("Upload Failed");
      setJobId(null); // Reset
    });

    // Clean up listeners on component unmount
    return () => {
      socket.off("progress_update");
      socket.off("task_complete");
      socket.off("task_failed");
    };
  }, []); // Only run once on mount

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setProgress(0);
    setStatus("");
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setStatus("Uploading...");
      const res = await axios.post(`${API_URL}/api/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const newJobId = res.data.job_id;
      setJobId(newJobId);
      joinRoom(newJobId); // Join the socket room for this job
      setStatus("Processing... (0%)");
    } catch (err) {
      setError("File upload failed.");
      setStatus("");
    }
  };

  return (
    <div className="card">
      <h3>Story 1: Product Importer</h3>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".csv" onChange={handleFileChange} />
        <button type="submit" disabled={jobId !== null}>
          {jobId ? "Processing..." : "Upload Products"}
        </button>
      </form>
      {status && (
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${progress}%` }}
          ></div>
          <span>
            {status}{" "}
            {progress > 0 && progress < 100 ? `${Math.round(progress)}%` : ""}
          </span>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default FileUpload;
