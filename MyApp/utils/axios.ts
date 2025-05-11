import axios from 'axios';
//this api will be imported in any screen later on that needs to make api requests

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // replace with your actual backend URL
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
