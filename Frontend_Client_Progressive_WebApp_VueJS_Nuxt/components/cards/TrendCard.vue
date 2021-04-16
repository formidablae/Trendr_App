<template>
  <BaseCard>
    <!-- Trend content -->
    <div class="w-10/12 flex flex-row ml-4 justify-between w-full">
      <div class="flex w-9/12">
        <div class="flex-col">
          <p class="truncate"><strong>{{trendItem.name}}</strong></p>
          <p class="text-sm text-gray-600" v-if="trendItem.tweetvolume">Tweet volume: {{trendItem.tweetvolume}}</p>
        </div>
      </div>
      <div class="w-3/12 text-right cursor-pointer" @click="goToTrendDetail">
        <i class="el-icon-arrow-right p-0"></i>
      </div>
    </div>
  </BaseCard>
</template>

<script>
  import BaseCard from "./BaseCard";

  export default {
    name: 'TrendCard',
    props: {
      trendItem: {
        type: Object,
        required: true
      },
      trendDate: {
        type: String
      },
      components: {
        BaseCard
      }
    },
    methods: {
      goToTrendDetail() {
        this.$emit('openDetail', this.trendItem.url )
      }

    }
  }
</script>

<style lang="scss" scoped>
  i {
    font-size: 2rem;
    @apply pr-3;
  }
</style>
