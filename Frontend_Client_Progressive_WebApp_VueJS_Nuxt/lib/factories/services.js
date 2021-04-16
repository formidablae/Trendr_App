import trendsService from '~/lib/services/trendsService'

export default ($axios) => ({
  trends: trendsService($axios),
})
