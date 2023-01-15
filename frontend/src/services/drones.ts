import axios from 'axios';

const API_ROOT = 'http://localhost:5000/';

export const getDrones = () => {
  return axios.get(`${API_ROOT}`).then((res) => res.data);
};
