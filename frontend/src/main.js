import {createApp} from 'vue'
import App from './App.vue'
import mitt from "mitt";
import apiMixins from "@/mixins/apiMixins";

const emitter = mitt()
const app = createApp(App)

app.mixin(apiMixins);

app.config.globalProperties.emitter = emitter
app.mount('#app')
