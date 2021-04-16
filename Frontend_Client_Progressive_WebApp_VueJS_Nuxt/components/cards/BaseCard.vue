<template>
  <div class="base-card">
    <div class="base-card__inner">
      <slot>
      </slot>
    </div>
  </div>
</template>

<script>

  export default {
    name: 'BaseCard'
  }
</script>

<style lang="scss" scoped>
  .base-card {
    @apply bg-gray-200 w-full rounded-lg;
    @apply mb-4;
    &__inner {
      @apply flex flex-row items-center px-4 py-3;
    }
  }
</style>
