<template>
  <Datepicker
    :id="id"
    :value="value"
    format="dd/MM/yyyy"
    :disabled-dates="disabledDates"
    :name="name"
    :placeholder="placeholder"
    :clear-button="false"
    :calendar-class="calendarClass"
    wrapper-class="wrapper-class"
    :language="it"
    input-class="irc-input gb-input"
    @opened="onOpen"
    @selected="onChange"
  >
  </Datepicker>
</template>
<script>
  import Datepicker from 'vuejs-datepicker'
  import { it } from 'vuejs-datepicker/src/locale'

  export default {
    name: 'DatepickerComponent',
    components: {
      Datepicker,
    },
    props: {
      clear: {
        type: Boolean,
        default: false,
      },
      label: {
        default: '',
        type: String,
      },
      id: {
        default: '',
        type: String,
      },
      name: {
        default: '',
        type: String,
      },
      placeholder: {
        default: '',
        type: String,
      },
      disabledDates: {
        type: Object,
        default: () => {
          return { from: null, to: null }
        },
      },
      value: {
        type: String,
        default: '',
      },
      calendarClass: {
        type: String,
        default: '',
      },
    },
    data() {
      return {
        it,
        config: {
          wrap: true, // set wrap to true only when using 'input-group'
          altFormat: 'd/m/Y',
          altInput: true,
          dateFormat: 'd/m/Y',
        },
      }
    },
    methods: {
      onChange(selectedDates) {
        const date = this.$moment(selectedDates)
        this.$emit('input', date)
        this.$emit('dateChange', date)
      },
      onOpen(selectedDates) {
        this.$emit('datePickerOpen', selectedDates)
      },
    },
  }
</script>
