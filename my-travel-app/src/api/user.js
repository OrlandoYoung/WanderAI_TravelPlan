import apiClient from './apiClient';

export default {
  getSavedTrips() {
    // 从 localStorage 获取 user 并解析 id
    const userStr = localStorage.getItem('user');
    let userId = '';
    try {
      userId = JSON.parse(userStr)?.userId || '';
    } catch (e) {
      userId = '';
    }
    return apiClient.get(`/user/saved-trips/${userId}`);
  }
};