<template>
  <div class="tabbar">
    <div class="tabbar__inner">
      <nuxt-link to="/searchingTrends">
        <div class="main-action">
          <i class="el-icon-s-home"></i>
        </div>
      </nuxt-link>
    </div>
  </div>
</template>

<script>
    export default {
        name: 'Tabbar'
    }
</script>

<style lang="scss" scoped>
  @import '@/assets/css/_variables.scss';

  .tabbar {
    @apply fixed bottom-0 bg-white inset-x-0;
    height: $tabbar-height;
    box-shadow: 0px -10px 15px -3px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05);

    &__inner {
      @apply h-full grid grid-cols-5 gap-4 items-center;
      text-align: center;

      a.disabled{
        @apply pointer-events-none opacity-25;
      }

      i {
        font-size: 1.5rem;
        @apply m-auto text-gray-400;
      }

      .nuxt-link-active {
        i {
          color: $theme-color;
        }
      }

      .main-action {
        @apply flex m-auto relative;
        border-radius: 2rem;
        height: 3.5rem;
        width: 3.5rem;
        margin-top: -3rem;
        background-color: $theme-color;
        box-shadow: 0px 20px 25px 15px rgba(0, 0, 0, 0.1),
        0 10px 10px -5px rgba(0, 0, 0, 0.04);

        i {
          @apply h-6 w-6;
        }
      }
    }
  }
</style>

