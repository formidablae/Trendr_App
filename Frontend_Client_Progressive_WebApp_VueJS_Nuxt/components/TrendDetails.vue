<template>
  <div class="flex flex-col px-6 py-4">
    <div class="flex flex-col justify-between my-6">
      <div class="font-bold text-xl mb-2">{{ bodyData.trendData.name }}</div>
      <div v-if="bodyData.trendData.url" class="text-sm text-primary">
        For more information go to: <br><br>
        <strong> <a target="_blank" class="text-primary" :href="bodyData.trendData.url"> {{bodyData.trendData.url}}</a></strong>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    data() {
      return {};
    },
    computed: {},
    props: {
      bodyData: { type: Object, },
    },
    methods: {
      close() {

      }
    }
  };
</script>
<style lang="scss">
</style>
