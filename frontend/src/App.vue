<template>
  <DashboardViewer/>
</template>

<script>
import DashboardViewer from './components/Dashboard.vue'

export default {
  name: 'App',
  components: {
    DashboardViewer
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
