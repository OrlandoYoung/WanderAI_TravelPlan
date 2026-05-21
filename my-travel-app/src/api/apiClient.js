import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 300000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器 - 添加认证token
apiClient.interceptors.request.use(config => {
  const token = sessionStorage.getItem('aaatoken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截器 - 统一错误处理
apiClient.interceptors.response.use(
  response => response,
  error => {
    const errorMessage = error.response?.data?.error?.message ||
      error.response?.data?.message ||
      '请求失败，请稍后重试';
    return Promise.reject(new Error(errorMessage));
  }
);

export default apiClient;