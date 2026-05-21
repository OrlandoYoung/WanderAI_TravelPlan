// store/index.js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    travelData: null // 存储提交的数据
  },
  mutations: {
    setTravelData(state, data) {
      state.travelData = data;
    }
  }
});