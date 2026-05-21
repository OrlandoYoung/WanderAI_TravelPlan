<template>
     <section class="px-20 py-16 bg-white">
<div class="mb-12">
<h2 class="text-3xl font-bold mb-6">智能规划进度</h2>
<div class="flex items-center space-x-8 mb-4">
<div v-for="(step, index) in planningSteps" :key="index" class="flex items-center flex-1">
<div class="flex items-center flex-shrink-0">
<div
  :class="[
    'w-8 h-8 rounded-full flex items-center justify-center',
    (currentStep === index || step.completed) ? 'bg-primary' : 'bg-gray-200'
  ]"
>
  <i v-if="step.completed" class="fas fa-check text-white"></i>
  <span v-else class="text-sm text-white">{{ index + 1 }}</span>
</div>
<span class="ml-2 text-sm text-gray-600">{{ step.name }}</span>
</div>
<div v-if="index < planningSteps.length - 1" class="flex-1 h-1 bg-gray-200 ml-4">
<div :class="['h-full bg-primary', step.completed ? 'w-full' : 'w-0']"></div>
</div>
</div>
</div>
</div>
<div class="flex space-x-6">
<div class="flex-1 bg-gray-50 rounded-lg p-6">


<div v-show="currentStep === 0" class="planning-content">
<h3 class="text-xl font-bold mb-4">天气确认</h3>
<div class="space-y-4">
    <div v-if="weatherInfo && weatherInfo.markdown" v-html="weatherHtml" class="prose"></div>
</div>
  <button
    class="mt-6 bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
    @click="nextStep"
    style="float: right"
  >
    下一步
  </button>
</div>

<div v-show="currentStep === 1" class="planning-content">
  <h3 class="text-xl font-bold mb-4">美食推荐</h3>
  <div class="space-y-4">
    <div v-if="foodInfo && foodInfo.markdown" v-html="foodHtml" class="prose"></div>
  </div>
  <div class="flex justify-between mt-6">
    <button
      class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
      @click="prevStep"
    >
      上一步
    </button>
    <button
      class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
      @click="nextStep"
    >
      下一步
    </button>
  </div>
</div>

<div v-show="currentStep === 2" class="planning-content">
<h3 class="text-xl font-bold mb-4">交通安排</h3>
<div class="space-y-4">
    <div v-if="transportInfo && transportInfo.markdown" v-html="transportHtml" class="prose"></div>
</div>
<div class="flex justify-between mt-6">
    <button
      class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
      @click="prevStep"
    >
      上一步
    </button>
    <button
      class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
      @click="nextStep"
    >
      下一步
    </button>
  </div>
</div>

<div v-show="currentStep === 3" class="planning-content">
<h3 class="text-xl font-bold mb-4">酒店预订</h3>
<div class="space-y-4">
    <div v-if="hotelInfo && hotelInfo.markdown" v-html="hotelHtml" class="prose"></div>
</div>
<div class="flex justify-between mt-6">
    <button
      class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
      @click="prevStep"
    >
      上一步
    </button>
    <button
      class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
      @click="nextStep"
    >
      下一步
    </button>
  </div>
</div>

<div v-show="currentStep === 4" class="planning-content">
<h3 class="text-xl font-bold mb-4">行程规划</h3>
<div class="space-y-4">
  <div v-if="itineraryInfo && itineraryInfo.markdown" v-html="itineraryHtml" class="prose"></div>
</div>
<div class="flex justify-between mt-6">
    <button
      class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
      @click="prevStep"
    >
      上一步
    </button>
    <button
      class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
      @click="nextStep"
    >
      下一步
    </button>
  </div>
</div>

<div v-show="currentStep === 5" class="planning-content">
<h3 class="text-xl font-bold mb-4">行程预算</h3>
<div class="space-y-4">
  <div v-if="budgetInfo && budgetInfo.markdown" v-html="budgetHtml" class="prose"></div>
</div>
<div class="flex justify-between mt-6">
    <button
      class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
      @click="prevStep"
    >
      上一步
    </button>
    <button
      class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
      @click="nextStep"
    >
      下一步
    </button>
  </div>
</div>



<div v-show="currentStep === 6" class="planning-content">
  <h3 class="text-xl font-bold mb-4">行程文档导出</h3>
  <div class="space-y-4">
    <div v-if="summaryInfo && summaryInfo.markdown" v-html="summaryHtml" class="prose"></div>
    <div v-else class="text-gray-400">正在加载行程汇总...</div>
    <div class="mt-8 p-4 bg-gray-100 rounded">
      <label class="block mb-2 font-semibold">不满意？请输入意见，将重新为您生成旅行计划：</label>
      <textarea
        v-model="regenerateOpinion"
        class="w-full p-2 border rounded mb-4"
        rows="3"
        placeholder="请输入您的意见"
      ></textarea>
      <button
        class="font-semibold py-2 px-6 rounded-button transition duration-300"
        :class="isRegenerating
          ? 'bg-gray-400 cursor-not-allowed text-white'
          : 'bg-primary hover:bg-secondary text-white'"
        @click="handleRegenerate"
        :disabled="isRegenerating"
      >
        {{ isRegenerating ? '正在重新生成......' : '重新生成' }}
      </button>
    </div>

  
    <div class="flex justify-between mt-6">
      <button
        class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
        @click="prevStep"
      >
        上一步
      </button>
      <div class="flex space-x-4">
        <button
          @click="downloadMarkdown"
          class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-4 rounded-button transition duration-300 whitespace-nowrap !rounded-button"
        >
          <i class="fas fa-download mr-2"></i>下载行程文档
        </button>
        <button
          class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-8 rounded-button transition duration-300"
          @click="$router.push('/')"
        >
          返回主页
        </button>
      </div>
    </div>
  
  </div>
  <!-- <button
    class="bg-primary hover:bg-secondary text-white font-semibold py-2 px-6 rounded-button transition duration-300"
    @click="prevStep"
  >
    上一步
  </button>
  <button @click="downloadMarkdown" class="mt-6 bg-primary hover:bg-secondary text-white font-semibold py-2 px-4 rounded-button transition duration-300 whitespace-nowrap !rounded-button">
      <i class="fas fa-download mr-2"></i>下载行程文档
    </button> -->
</div>

</div>

<div class="w-80 bg-gray-50 rounded-lg p-6">
<h3 class="font-semibold mb-4">旅行信息概览</h3>
<div class="space-y-4">
<div v-for="(info, index) in travelInfo" :key="index">
<p class="text-sm text-gray-500">{{ info.label }}</p>
<p class="font-medium">{{ info.value }}</p>
</div>
</div>
</div>

</div>
</section>
<!-- <router-view /> -->
<!-- </div> -->
</template>

<script>
import {marked} from 'marked';
  export default {
    name: 'HomePage',
    data() {
      return {
        tripId: '', 
        currentStep: 0,
        currentRecommend: 0,
        weatherInfo: null,
        transportInfo: null,
        hotelInfo: null,
        foodInfo: null,
        itineraryInfo: null,
        budgetInfo: null,
        isRegenerating: false,
        summaryInfo: null,
        regenerateOpinion: '', 
        planningSteps: [
          { name: '天气确认', completed: false },
          { name: '美食推荐', completed: false },
          { name: '交通安排', completed: false },
          { name: '酒店预订', completed: false },
          { name: '行程规划', completed: false },
          { name: '行程预算', completed: false },
          { name: '导出文档', completed: false }
        ],
        
};
},

computed: {
  weatherHtml() {
  if (!this.weatherInfo || !this.weatherInfo.markdown) return '';
    return marked(this.weatherInfo.markdown);
  },
  foodHtml() {
    if (!this.foodInfo || !this.foodInfo.markdown) return '';
    return marked(this.foodInfo.markdown);
  },
  transportHtml() {
    if (!this.transportInfo || !this.transportInfo.markdown) return '';
    return marked(this.transportInfo.markdown);
  },
  hotelHtml() {
    if (!this.hotelInfo || !this.hotelInfo.markdown) return '';
    return marked(this.hotelInfo.markdown);
  },
  itineraryHtml() {
    if (!this.itineraryInfo || !this.itineraryInfo.markdown) return '';
    return marked(this.itineraryInfo.markdown);
  },
  budgetHtml() {
    if (!this.budgetInfo || !this.budgetInfo.markdown) return '';
    return marked(this.budgetInfo.markdown);
  },
  summaryHtml() {
    if (!this.summaryInfo || !this.summaryInfo.markdown) return '';
    return marked(this.summaryInfo.markdown);
  },
  travelInfo() {
    // 从 localStorage 获取 travelInfo
    const info = JSON.parse(localStorage.getItem('travelInfo') || '{}');
    return [
      { label: '出发地', value: info.departureCity || '未填写' },
      { label: '目的地', value: info.destinationCity || '未填写' },
      { label: '日期', value: (info.travelDate && info.travelDate.length === 2)
        ? `${this.$options.filters.dateFormat(info.travelDate[0])} 至 ${this.$options.filters.dateFormat(info.travelDate[1])}`
        : '未选择' },
      { label: '人数', value: info.travelers || '未填写' },
      { label: '偏好', value: info.travelPreference || '未填写' }
    ];
  }
},

mounted() {
    this.tripId = localStorage.getItem('tripId') || '';
    this.startInfoGeneration();
    this.weatherInfo = JSON.parse(localStorage.getItem('weatherInfo') || 'null');
    this.transportInfo = JSON.parse(localStorage.getItem('transportInfo') || 'null');
    this.hotelInfo = JSON.parse(localStorage.getItem('hotelInfo') || 'null');
    this.foodInfo = JSON.parse(localStorage.getItem('foodInfo') || 'null');
    this.itineraryInfo = JSON.parse(localStorage.getItem('itineraryInfo') || 'null');
    this.budgetInfo = JSON.parse(localStorage.getItem('budgetInfo') || 'null');
},

methods: {
  async fetchTripSummary() {
    try {
      const res = await this.$api.trip.getTripSummary(this.tripId);
      if (res.data && res.data.success) {
        this.summaryInfo = { markdown: res.data.markdown };
      } else {
        this.summaryInfo = { markdown: '未能获取行程汇总内容' };
      }
    } catch (e) {
      this.summaryInfo = { markdown: '获取行程汇总失败' };
    }
  },
  async handleRegenerate() {
    if (!this.regenerateOpinion || !this.regenerateOpinion.trim()) {
      this.$message.error('请输入您的意见后再重新生成');
      return;
    }
    this.isRegenerating = true;
    this.summaryMarkdown = '请稍等，正在为您重新规划';
    try {
      await this.$api.trip.revisePlan(this.tripId, this.regenerateOpinion);

      // 只需重新获取 summary，不跳转页面
      await this.fetchTripSummary();

      this.$message.success('已为您重新生成规划！');
      // 不再 this.currentStep = 0;
    } catch (e) {
      this.summaryMarkdown = '重新生成失败，请稍后重试';
      this.$message.error('重新生成失败，请稍后重试');
    } finally {
      this.isRegenerating = false;
      this.regenerateOpinion = '';
    }
  },
  startInfoGeneration() {

    (async () => {
      try {
        const [
          weatherRes,
          transportRes,
          hotelRes,
          foodRes,
          itineraryRes,
          budgetRes
        ] = await Promise.all([
          this.$api.trip.getWeatherInfo(this.tripId),
          this.$api.trip.getTransportInfo(this.tripId),
          this.$api.trip.getHotelInfo(this.tripId),
          this.$api.trip.getFoodInfo(this.tripId),
          this.$api.trip.getItineraryInfo(this.tripId),
          this.$api.trip.getBudgetInfo(this.tripId)
        ]);

        // 保存到 localStorage
        localStorage.setItem('weatherInfo', JSON.stringify(weatherRes.data));
        this.weatherInfo = weatherRes.data;
        localStorage.setItem('transportInfo', JSON.stringify(transportRes.data));
        this.transportInfo = transportRes.data;
        localStorage.setItem('hotelInfo', JSON.stringify(hotelRes.data));
        this.hotelInfo = hotelRes.data;
        localStorage.setItem('foodInfo', JSON.stringify(foodRes.data));
        this.foodInfo = foodRes.data;
        localStorage.setItem('itineraryInfo', JSON.stringify(itineraryRes.data));
        this.itineraryInfo = itineraryRes.data;
        localStorage.setItem('budgetInfo', JSON.stringify(budgetRes.data));
        this.budgetInfo = budgetRes.data;
      } catch (e) {
        this.weatherStatus = '获取失败';
        this.transportStatus = '获取失败';
      }
    })();
  },

nextStep() {
  if (this.currentStep < this.planningSteps.length - 1) {
    this.currentStep++;
    this.planningSteps[this.currentStep - 1].completed = true;
    // 进入导出文档步骤时获取 summary
    if (this.currentStep === 6) {
      this.fetchTripSummary();
    }
  }
},
prevStep() {
  if (this.currentStep > 0) {
    this.planningSteps[this.currentStep - 1].completed = false;
    this.currentStep--;
  }
},
async downloadMarkdown() {
  try {
    // 假设 tripId 已经有值
    const response = await this.$api.trip.downloadTrip(this.tripId, 'md');
    const blob = new Blob([response.data], { type: 'text/markdown' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = '旅行计划.md';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (e) {
     //this.$message && this.$message.error('下载失败，请重试');
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