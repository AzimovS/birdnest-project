import axios from 'axios';

const API_ROOT =
  'https://startlingly-rubber-baboon-penthouse-dev.wayscript.cloud/';

export const getDrones = () => {
  return axios.get(`${API_ROOT}`).then((res) => res.data);
};
