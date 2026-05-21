import apiClient from './apiClient';

export function login(credentials) {
  return apiClient.post('/auth/login', credentials);
}

export function register(userData) {
  return apiClient.post('/auth/register', userData);
}
export function sendEmailCode(email) {
  return apiClient.post('/auth/send_email_code', { email });
}
export default {
  login,
  register,
  sendEmailCode
};
