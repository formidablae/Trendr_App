<template>
  <MainLayout>
    <div class="flex flex-col trending_content h-full">
      <!-- SEARCH SECTION-->
      <el-form
        :model="searchParams"
        :rules="rules"
        :disabled="isLoading"
        hide-required-asterisk
        @keyup.native.enter="search"
        ref="searchForm"
      >
        <!-- DATE SEARCH INPUT-->
        <el-form-item
          prop="date">
          <el-date-picker
            v-model="searchParams.date"
            type="date"
            @change="setDate(searchParams.date)"m
            :picker-options="datePickerOptions"
            placeholder="Choose a date">
          </el-date-picker>
        </el-form-item>

        <!--LOCATION SEARCH INPUT-->
        <el-form-item
          prop="woeid">
          <el-cascader
            filterable
            v-model="searchParams.woeid"
            :options="countriesList"
            :props="props">
            <template slot-scope="{ node, data }">
              <span>{{ data.locations_name }}</span>
              <span v-if="!node.isLeaf &&  data.towns.length> 0"> ({{ data.towns.length }}) </span>
            </template>
          </el-cascader>
        </el-form-item>

        <!-- Filters search and clear button-->
        <div class="mt-4 flex justify-end w-full">
          <el-button type="primary" icon="el-icon-search" size="mini" rounded @click="search">Search</el-button>
          <el-button type="danger" icon="el-icon-close" size="mini" rounded @click="clearSearchInputs">Clear</el-button>
        </div>
      </el-form>
      <p v-if="trends.length > 0" class="text-xl font-bold my-4 capitalize text-primary">Trends list</p>

      <!--TRENDS LIST-->
      <div class="flex flex-col w-full h-full overflow-y-scroll" >
        <div v-if="trends.length > 0">
          <div v-for="(trendItem, $index) in trends" :key="trendItem.name + $index">
            <Loader v-if="isLoading"></Loader>
            <!-- TrendCard is a custom component - check the componenent TrendCard component file on components folder for more details-->
            <TrendCard v-else :trendItem="trendItem" :trendDate="responseData.date"
                       @openDetail="openTrendDetail"></TrendCard>
          </div>
        </div>
        <div v-else class="mt-8">
          <span class="text-center italic text-gray-500">There are no data for the selected search values</span>
        </div>
        <!-- INFINITE LOADING-->
        <InfiniteLoading direction="bottom" :identifier="infiniteId" @infinite="infiniteHandler($event)">
        <span slot="no-results" class="no-result">
          <span></span>
        </span>
          <!-- ADDED EMPTY TO RESET THE END LIST MESSAGE-->
          <div slot="no-more"></div>
        </InfiniteLoading>
      </div>

    </div>
  </MainLayout>
</template>

<script>
  import TrendCard from '@/components/cards/TrendCard'
  import moment from 'moment'
  import Loader from "./trendingLoader"
  import InfiniteLoading from 'vue-infinite-loading'

  export default {
    name: 'Trendr',
    head () {
      return {
        title: 'Trendr',
      }
    },
    components: { TrendCard, Loader, InfiniteLoading },
    data() {
      return {
        isLoading: false,
        hasLoadMoreButton: false,
        responseData: [],
        trends: [],
        defaultLocation: {
          locations_name: "Worldwide",
          locations_woeid: 1,
        },
        searchParams: {
          woeid: 1,
          date: moment().format('YYYY-MM-DD'),
          page: 1,
          docperpage: 15
        },
        currentDate: moment().format('YYYY-MM-DD'),
        datePickerOptions: {
          disabledDate: this.disabledDate
        },
        countriesList: [{
          locations_name: "Worldwide",
          locations_woeid: 1
        }],
        props: {
          value: 'locations_woeid',
          label: 'locations_name',
          checkStrictly: true,
          children: 'towns' },

        rules: {
          date: {
              required: true,
              message: "Date is required",
              trigger: 'change'
            },
          woeid: {
            required: true,
            message: "Location",
            trigger: 'change'
          }
        },
        infiniteId: +new Date()
      }
    },
    created() {
      this.getLocationsByDate()
    },
    mounted() {
      this.$router.push('/');
      /**
       * @description Before the template is being rendered get all the information for trends by passign the default values for country id (worldwide) and today as date
       */
      // this.getTrendsByDateAndLocation()
    },
    methods:{
      /**
       * @desc Fetch trends
       * @returns {Promise<void>}
       */
      async getTrendsByDateAndLocation() {
        this.isLoading = true
        try {
          this.searchParams.date =  moment(this.searchParams.date).format('YYYY-MM-DD')
          this.searchParams.woeid =  Array.isArray(this.searchParams.woeid) ? this.searchParams.woeid[this.searchParams.woeid.length -1] : this.searchParams.woeid
          this.responseData = (await this.$services.trends.getTrends(this.searchParams)).body
          this.trends.push(...this.responseData.trends)
          this.hasLoadMoreButton =this.responseData.trends.length === this.searchParams.docperpage
        } catch (e) {
          // this.$notificationService.error(e)
        } finally {
          this.isLoading = false
        }
      },
      /**
       * @desc Load trends on scroll
       * @param state
       */
      async infiniteHandler($state) {
        const vm = this
        try {
          vm.searchParams.date =  moment(vm.searchParams.date).format('YYYY-MM-DD')
          vm.searchParams.woeid =  Array.isArray(vm.searchParams.woeid) ? vm.searchParams.woeid[vm.searchParams.woeid.length -1] : vm.searchParams.woeid
          vm.responseData = (await vm.$services.trends.getTrends(vm.searchParams)).body
          if(vm.responseData.trends.length > 0) {
            $state.loaded()
            vm.trends.push(...vm.responseData.trends)
            vm.searchParams.page++
          } else {
            $state.complete()
          }
        } catch (e) {
          $state.complete()
          // this.$notificationService.error(e)
        }
      },

      /**
       * @desc Search for trends on button click
       */
      async search() {
        try {
          await this.$refs.searchForm.validate()
        } catch (e) {
          return
        }
        this.trends = []
        this.infiniteId += 1
        this.searchParams.page = 1
        this.getTrendsByDateAndLocation()
      },
      /**
       * @description getLocationsByDate method
       */
      async getLocationsByDate(date) {
        try {
          this.countriesList = [{
            locations_name: "Worldwide",
            locations_woeid: 1
          }]
          let response = (await this.$services.trends.getLocations(date ? moment(date).format('YYYY-MM-DD') : this.currentDate)).body
          let responseData = response.locations[0].locations.countries
          responseData.sort((a, b) => (a.locations_name > b.locations_name) ? 1 : ((b.locations_name > a.locations_name) ? -1 : 0));
          responseData.forEach((country) => {
            if (country.towns && country.towns.length === 0) {
              delete country.towns
            } else {
              country.towns.sort((a, b) => (a.locations_name > b.locations_name) ? 1 : ((b.locations_name > a.locations_name) ? -1 : 0));
            }
          })
          response.locations.length > 0 ? this.countriesList.push(...responseData) : [this.defaultLocation]
        } catch (e) {
          // this.$notificationService.error(this.$t('errors.fetch'))
        } finally {
          this.isLoading = false
        }
      },

      /**
       * @description Clear input filters
       */
      clearSearchInputs() {
        this.searchParams = {
          woeid: 1,
          date: moment().format('YYYY-MM-DD'),
          page: 1,
          docperpage: 15
        }
        this.trends = []
        this.infiniteId += 1
        this.getLocationsByDate(this.searchParams.date)
        this.getTrendsByDateAndLocation()
      },
      openTrendDetail(url) {
        window.open(url,'_blank');
      },
      disabledDate(date) {
        const startDate = new Date("2020-08-13")
        return !(date >= startDate  && date <= new Date())
      },
      setDate(date) {
        this.searchParams.woeid = 1
        this.countriesList= [{
          locations_name: "Worldwide",
          locations_woeid: 1,
          towns: []
        }]
        this.getLocationsByDate(this.searchParams.date)
      }
    }
  }
</script>

<style lang="scss" scoped>
  .el-cascader {
    width: 100%;
  }

  .el-date-editor.el-input, .el-date-editor.el-input__inner {
    width: 100%;
  }

  .trending_content {
    height: 100%  !important;
  }
</style>
