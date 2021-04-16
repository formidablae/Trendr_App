export default ($axios) => ({
  /**
   * @desc Get trends for a selected date and location
   * @returns {Promise<any>}
   */
  getTrends(searchParams) {
    return $axios.$get(`/trends?date=${searchParams.date}&woeid=${searchParams.woeid}&page=${searchParams.page}&docperpage=${searchParams.docperpage}`)
  },

  /**
   * @desc Get locations for a selected date
   * @returns {Promise<any>}
   */
  getLocations(date) {
    return $axios.$get(`/locations?date=${date}`)
  },
})
