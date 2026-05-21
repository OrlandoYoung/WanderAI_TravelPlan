import apiClient from './apiClient';

export default {
  // 生成旅行计划
  generateTrip(data) {
    // 格式化日期为 YYYY-MM-DD
    const formatDate = d => {
      if (!d) return '';
      // 如果已经是字符串且格式正确，直接返回
      if (typeof d === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(d)) return d;
      // 否则尝试转为 Date 对象
      const dateObj = new Date(d);
      if (isNaN(dateObj)) return '';
      return dateObj.toISOString().slice(0, 10);
    };
    let userId = '';
    try {
      userId = JSON.parse(localStorage.getItem('user'))?.userId || '';
    } catch (e) {
      userId = '';
    }
    return apiClient.post('/trip/generate', {
      origin: data.departureCity,
      destination: data.destinationCity,
      startDate: formatDate(data.travelDate[0]),
      endDate: formatDate(data.travelDate[1]),
      interests: data.travelPreference,
      numPeople: data.travelers,
      userId: userId
    });
  },
  // 获取天气准备信息
  getWeatherInfo(tripId) {
    return apiClient.get(`/trip/${tripId}/weather-md`);
  },
  // 获取交通安排信息
  getTransportInfo(tripId) {
    return apiClient.get(`/trip/${tripId}/transport-md`);
  },
  // 获取住宿选择信息
  getHotelInfo(tripId) {
    return apiClient.get(`/trip/${tripId}/hotel-md`);
  },
  // 获取本地美食信息
  getFoodInfo(tripId) {
    return apiClient.get(`/trip/${tripId}/food-md`);
  },
  // 获取每日行程信息
  getItineraryInfo(tripId) {
    return apiClient.get(`/trip/${tripId}/itinerary-md`);
  },
  // 获取预算明细信息
  getBudgetInfo(tripId) {
    return apiClient.get(`/trip/${tripId}/budget-md`);
  },

  // 下载旅行计划
  downloadTrip(tripId, format = 'md') {
    return apiClient.get(`/trip/${tripId}/download`, {
      responseType: 'blob'
    })
    .then(response => {
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${tripId}.${format}`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  },

  // 修订旅行计划
  revisePlan(tripId) {
    let userId = '';
    try {
      userId = JSON.parse(localStorage.getItem('user'))?.userId || '';
    } catch (e) {
      userId = '';
    }
    return apiClient.post(`/trip/revise/${tripId}`, {
      userId: userId
    });
  },
    getTripSummary(tripId) {
    return apiClient.get(`/trip/${tripId}/summary`);
  }
};