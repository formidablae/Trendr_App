<template>
    <div class="main-layout">
        <header v-if="hasHeader">
          <template>
            <div class="flex flex-row items-center justify-between">
              <div class="text-center m-auto font-bold">
                <img src="@/assets/img/logo.png" alt="" class="h-8 w-18">
              </div>
            </div>
          </template>
        </header>
        <main>
            <slot />
        </main>
    </div>
</template>

<script>
  export default {
    name: 'MainLayout',
    components: {},
    props: {
      hasHeader: {
        type: Boolean,
        default: true
      },
      hasTabbar: {
        type: Boolean,
        default: true
      }
    }

  }
</script>

<style lang="scss" scoped>
  @import '@/assets/css/_variables.scss';

  .main-layout {
    @apply flex flex-col w-full overflow-visible;
    background-color: $background-color;

    header {
      @apply px-4 py-5;
      background-color: $background-color;
    }

    main {
      border-top-left-radius: 1.25rem;
      border-top-right-radius: 1.25rem;
      height: calc(100% - 63px) !important;
      @apply p-6 bg-white;
    }
  }
</style>
