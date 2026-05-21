<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航栏 -->
    <header class="fixed top-0 left-0 right-0 bg-white shadow-sm z-50">
      <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <div class="flex items-center">
          <button class="!rounded-button whitespace-nowrap text-gray-600 
          hover:text-gray-900 mr-4" @click="$router.push('/')">
            <i class="fas fa-arrow-left"></i>
          </button>
          <h1 class="text-xl font-medium">我的行程记录</h1>
        </div>

      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="max-w-7xl mx-auto px-4 pt-24 pb-8">
      <!-- 有数据时显示的列表 -->
      <div v-if="trips.length > 0" class="space-y-4">
        <div v-for="trip in trips" :key="trip.tripId" 
          class="bg-white rounded-lg shadow-sm p-6 transform transition-all duration-300 hover:shadow-md">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-4">
              <div class="flex items-center">
                <span class="text-lg font-medium">{{ trip.origin }}</span>
                <i class="fas fa-arrow-right mx-3 text-gray-400"></i>
                <span class="text-lg font-medium">{{ trip.destination }}</span>
              </div>
            </div>
            <button
              class="!rounded-button whitespace-nowrap text-gray-400 hover:text-gray-600"
              @click="toggleTripSummary(trip.tripId)"
            >
              <i :class="expandedTripId === trip.tripId ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
            </button>
          </div>
          <div class="flex items-center text-gray-500 text-sm">
            <i class="far fa-calendar-alt mr-2"></i>
            <span>{{ trip.dateRange }}</span>
          </div>
          <div class="mt-2 text-xs text-gray-400">
            保存于 {{ formatDate(trip.savedAt) }}
          </div>

          <!-- 下拉markdown展示区 -->
          <div v-if="expandedTripId === trip.tripId" class="mt-4 p-4 bg-gray-50 rounded">
            <div v-if="tripSummaries[trip.tripId]?.loading" class="text-blue-500">正在加载行程汇总...</div>
            <div v-else v-html="marked(tripSummaries[trip.tripId]?.markdown || '')" class="prose"></div>
          </div>
        </div>
      </div>

      <!-- 空状态展示 -->
      <div v-else class="text-center py-16">
        <div class="w-64 h-64 mx-auto mb-6 overflow-hidden">
          <img :src="emptyStateImage" alt="暂无行程" class="w-full h-full object-cover">
        </div>
        <h3 class="text-gray-600 mb-4">暂无保存的行程</h3>
        <button
          class="!rounded-button whitespace-nowrap bg-blue-600 text-white px-6 py-2 hover:bg-blue-700"
          @click="$router.push('/')"
        >
          去规划行程
        </button>
      </div>
    </main>
  </div>
</template>

<script>
import { marked } from 'marked';
export default {
  name:'HistoryPage',
  data() {
    return {
      currentUser: '',
      trips: [],
      expandedTripId: null, // 当前展开的行程id
      tripSummaries: {}, 
      //emptyStateImage: 'https://img.alicdn.com/imgextra/i4/6000000000427/O1CN01Q5Qn2g1Yw7QwZ0TOg_!!6000000000427-2-tps-512-512.png'
    };
  },
  mounted(){
    // this.getCurrentUser();
    this.fetchTrips();
  },
  methods: {
    marked(md) {
      return marked(md || '');
    },
    async toggleTripSummary(tripId) {
      if (this.expandedTripId === tripId) {
        // 再次点击则收起
        this.expandedTripId = null;
        return;
      }
      this.expandedTripId = tripId;
      // 如果已缓存则不再请求
      if (!this.tripSummaries[tripId]) {
        this.$set(this.tripSummaries, tripId, { loading: true, markdown: '' });
        try {
          const res = await this.$api.trip.getTripSummary(tripId);
          if (res.data && res.data.success) {
            this.$set(this.tripSummaries, tripId, { loading: false, markdown: res.data.markdown });
          } else {
            this.$set(this.tripSummaries, tripId, { loading: false, markdown: '未能获取行程汇总内容' });
          }
        } catch (e) {
          this.$set(this.tripSummaries, tripId, { loading: false, markdown: '获取行程汇总失败' });
        }
      }
    },
    // getCurrentUser() {
    //   this.currentUser = localStorage.getItem('username') || '未登录';
    // },
    async fetchTrips() {
      try {
        const res = await this.$api.user.getSavedTrips();
        // 取 saved_trips，并格式化日期
        this.trips = (res.data.savedTrips || []).map(trip => ({
          ...trip,
          dateRange: `${trip.startDate} 至 ${trip.endDate}`
        }));
      } catch (e) {
        this.$message && this.$message.error('获取行程记录失败');
        this.trips = [];
      }
    },
    refreshData() {
      // 刷新数据的逻辑
      // this.getCurrentUser(); // 刷新时重新获取用户信息
      this.fetchTrips();
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    }
  }
};
</script>

<style scoped>
.trip-card-enter-active,
.trip-card-leave-active {
  transition: all 0.3s ease;
}

/* 如果需要调整按钮内元素的间距 */
.fa-sync-alt {
  margin-right: 4px;
}

.trip-card-enter,
.trip-card-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>

