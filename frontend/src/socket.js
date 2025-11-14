// src/socket.js
import { io } from "socket.io-client";
import API_URL from "./apiConfig";

// Create a socket connection
export const socket = io(API_URL);

// You can export functions to join/leave rooms if needed
export const joinRoom = (jobId) => {
  socket.emit("join_room", { job_id: jobId });
};
