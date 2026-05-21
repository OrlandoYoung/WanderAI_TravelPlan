<!-- 代码已包含 CSS：使用 TailwindCSS , 安装 TailwindCSS 后方可看到布局样式效果 -->
<template>
  <div class="w-[1440px] mx-auto">
    <section class="hero-section h-[800px] relative">
      <video
        class="absolute top-0 left-0 w-full h-full object-cover z-0"
        src="@/videos/island.mp4"
        autoplay
        muted
        loop
        playsinline
      ></video>
       <div class="absolute top-1/2 right-16 transform -translate-y-1/2 z-10 text-right select-none">
        <div class="text-6xl font-extrabold text-white mb-2 drop-shadow-lg" style="font-family: serif;">
         {{ recommendedCities[currentRecommend].name }}
         </div>
        <div class="text-2xl text-white font-medium mb-1 drop-shadow">
         {{ recommendedCities[currentRecommend].feature }}
        </div>
        <div class="text-sm text-white opacity-70 tracking-widest">为你推荐</div>
        </div>
        
      <div class="absolute top-0 left-0 right-0 p-6 flex justify-between items-center z-20">
        <div class="text-white text-3xl" style="font-family: 'Pacifico', cursive;">Travel</div>
        <!-- <button class="text-white text-xl hover:text-gray-200" @click="handleClose">
          <i class="fas fa-times"></i>
        </button> -->
       
        <div>
          <button
            v-if="!isLoggedIn"
            class="text-white text-xl hover:text-gray-200 mr-4"
            @click="$router.push('/login')"
            style="cursor:pointer"
          >
            登录
          </button>
          <button
            v-else
            class="text-white text-xl hover:text-gray-200 mr-4"
            @click="$router.push('/history')" 
            style="cursor:pointer"
          >
            历史记录
          </button>
          <button
            v-if="isLoggedIn"
            class="text-white text-xl hover:text-gray-200"
            @click="logout"
            style="cursor:pointer"
          >
            退出登录
          </button>

        </div>
      </div>

      <div class="relative z-10 h-full flex flex-col justify-center px-20 pl-40 pt-10 pb-20">
        <h1 class="text-white text-6xl font-bold mb-6" style="font-family: 'Alibaba PuHuiTi', 'Source Han Sans SC', 'Microsoft YaHei', 'PingFang SC', sans-serif;">永不停止探索世界</h1>
        <p class="text-white text-xl mb-12 max-w-2xl">让 AI 为您定制完美旅程，从天气到行程，从交通到住宿，一站式智能规划您的旅行体验。</p>
        <div class="bg-white rounded-lg p-8 max-w-2xl">
          <div class="grid grid-cols-2 gap-6 mb-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">出发地</label>
              <div class="relative">
                <i class="fas fa-plane-departure absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                <input v-model="departureCity" type="text" class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-button focus:ring-2 focus:ring-primary focus:border-primary" placeholder="请输入出发城市">
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">目的地</label>
              <div class="relative">
                <i class="fas fa-plane-arrival absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                <input v-model="destinationCity" type="text" class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-button focus:ring-2 focus:ring-primary focus:border-primary" placeholder="请输入目的地">
              </div>
            </div>
          </div>



          
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">旅行日期</label>
            <!-- <div class="relative">
              <i class="fas fa-calendar absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
              <input v-model="travelDate" type="text" class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-button focus:ring-2 focus:ring-primary focus:border-primary" placeholder="选择旅行日期范围">
            </div> -->

            <el-date-picker
              v-model="travelDate"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              class="w-full"
              style="width:100%"
            >
            </el-date-picker>
            
          </div>


          <div class="grid grid-cols-2 gap-6 mb-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">旅行偏好</label>
              <div class="relative">
                <i class="fas fa-heart absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                <input v-model="travelPreference" type="text" class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-button focus:ring-2 focus:ring-primary focus:border-primary" placeholder="如户外冒险、美食之旅">
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">旅行人数</label>
              <div class="relative">
                <i class="fas fa-users absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                <input v-model="travelers" type="number" class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-button focus:ring-2 focus:ring-primary focus:border-primary appearance-none" placeholder="输入旅行人数">
              </div>
            </div>
          </div>

          <button
            :disabled="!isLoggedIn || isPlanning"
            @click="isLoggedIn ? startPlanning() : null"
            :class="[
              'w-full font-semibold py-3 px-6 rounded-button transition duration-300 whitespace-nowrap !rounded-button',
              isLoggedIn
                ? (isPlanning ? 'bg-gray-400 cursor-not-allowed text-white' : 'bg-primary hover:bg-secondary text-white')
                : 'bg-gray-400 cursor-not-allowed text-white'
            ]"
          >
            {{ isLoggedIn ? (isPlanning ? '正在生成中,预计需要3-5分钟' : '开始智能规划') : '请先登录' }}
          </button>

        </div>
      </div>


      

    </section>
  </div>
</template>



<script>
  export default {
    name: 'HomePage',
    data() {
      return {
        departureCity: '',
        destinationCity: '',
        travelDate: '',
        travelPreference: '',
        travelers: '',
        isPlanning: false, 
        recommendedCities: [
            { name: '三亚', feature: '阳光沙滩、潜水天堂、热带风情' },
            { name: '丽江', feature: '古城风情、雪山美景、民族文化' },
            { name: '成都', feature: '美食之都、熊猫基地、休闲慢生活' },
            { name: '西安', feature: '历史古都、兵马俑、城墙夜景' },
            { name: '桂林', feature: '山水甲天下、漓江风光、溶洞奇观' }
        ],
        currentRecommend: 0,
        
};
},

computed: {
  isLoggedIn() {
    return !!sessionStorage.getItem('token');
  },
  userName() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    return user.name || '';
  }
},

mounted() {
    this.startRecommendLoop();
    //this.isLoggedIn = !!sessionStorage.getItem('token');
},

methods: {
    startRecommendLoop() {
        this.recommendTimer = setInterval(() => {
        this.currentRecommend = Math.floor(Math.random() * this.recommendedCities.length);
        }, 3000); // 每3秒切换一次
    },
    beforeDestroy() {
        clearInterval(this.recommendTimer);
    },

logout() {
  sessionStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.reload();
},
handleClose() {
// 处理关闭按钮点击事件
},

async startPlanning() {
  if (this.isPlanning) return;
  this.isPlanning = true;
  const payload = {
    departureCity: this.departureCity,
    destinationCity: this.destinationCity,
    travelDate: this.travelDate,
    travelPreference: this.travelPreference,
    travelers: this.travelers
  };
  try {
    const response = await this.$api.trip.generateTrip(payload);
    if (response.data && response.data.success) {
      this.$message && this.$message.success(response.data.message || '提交成功！');
      localStorage.setItem('tripId', response.data.tripId);
      // 保存 travelInfo 到 localStorage
      localStorage.setItem('travelInfo', JSON.stringify(payload));
      this.$router.push('/plan');
    }
  } catch (error) {
    this.$message && this.$message.error('输入不完整，请补全后再提交');
  } finally {
    this.isPlanning = false;
  }
}
},




  filters: {
    dateFormat(val) {
      if (!val) return '';
      const d = new Date(val);
      const y = d.getFullYear();
      const m = (d.getMonth() + 1).toString().padStart(2, '0');
      const day = d.getDate().toString().padStart(2, '0');
      return `${y}-${m}-${day}`;
    }
  }
};
</script>



<style scoped>
.hero-section {
background-image: url('https://mastergo.com/ai/api/search-image?query=aerial view of a beautiful tropical beach with crystal clear turquoise water, palm trees lining the shore, luxury resorts in the background, dramatic lighting, professional photography, ultra high resolution, cinematic composition&width=1440&height=800&orientation=landscape&flag=aae6d95ca933331fc2883547ecf15945');
background-size: cover;
background-position: center;
position: relative;
}
.hero-section::before {
content: '';
position: absolute;
top: 0;
left: 0;
right: 0;
bottom: 0;
background: linear-gradient(to right, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 100%);
z-index: 1;
}
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
-webkit-appearance: none;
margin: 0;
}
</style>