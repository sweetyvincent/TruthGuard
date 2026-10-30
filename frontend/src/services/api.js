import axios from 'axios';
const api = axios.create({baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api'});
export const getDocs = () => api.get('/documents').then(r=>r.data);
export const uploadDoc = file => {const f=new FormData();f.append('file',file);return api.post('/documents/upload',f).then(r=>r.data)};
export const deleteDoc = id => api.delete(`/documents/${id}`);
export const ask = question => api.post('/query',{question}).then(r=>r.data);
export const getHistory = () => api.get('/history').then(r=>r.data);
