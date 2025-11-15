import { io } from "socket.io-client";
import API_URL from "./apiConfig";

export const socket = io(API_URL);

export const joinRoom = (jobId) => {
  socket.emit("join_room", { job_id: jobId });
};
