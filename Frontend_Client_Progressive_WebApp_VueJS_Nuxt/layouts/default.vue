<template>
  <div id="app">
    <div class="main-container flex lg:w-2/5 md:w-3/5 md:m-auto">
      <Nuxt/>
    </div>
  </div>
</template>
<script>
  export default {
    head() {
      return {
        title: 'Trendr',
        meta: [
          { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1' }
        ]
      }
    },
    name: 'default'
  }
</script>
<style lang="scss" scoped>
  @import '@/assets/css/_variables.scss';

  #app {
    @apply bg-gray-300;
    @apply flex flex-col min-h-screen w-full;
  }

  .main-container {
    height: 100vh;
  }
</style>
