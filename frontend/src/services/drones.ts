import axios from 'axios';

const API_ROOT =
  'https://octopus-app-yobck.ondigitalocean.app/';

export const getDrones = () => {
  return axios.get(`${API_ROOT}`).then((res) => res.data);
};
