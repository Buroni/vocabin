import Vue from 'vue';
import App from './src/App/App';

const vm = new Vue({
  el: '#app',
  render: h => h(App)
});

export { vm };
