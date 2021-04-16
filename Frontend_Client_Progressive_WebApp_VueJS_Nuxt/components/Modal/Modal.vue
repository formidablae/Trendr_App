<template>
  <el-dialog
    :visible.sync="isOpen"
    :title="title"
    :before-close="onCancelPressed"
    @closed="close()"
  >
    <div>
      <component
        :is="body"
        v-loading="isLoading"
        :body-data="bodyProps"
        @validate="onValidate"
        @change="onChange"
        @click="onConfirmPressed"
      />
    </div>
    <!--<span-->
    <!--v-if="hasFooter"-->
    <!--slot="footer"-->
    <!--class="dialog-footer"-->
    <!--&gt;-->
    <!--<el-button-->
    <!--:loading="isLoading"-->
    <!--@click="onCancelPressed"-->
    <!--&gt;{{ cancelButtonText }}</el-button>-->
    <!--<el-button-->
    <!--:disabled="!isValid"-->
    <!--:loading="isLoading"-->
    <!--type="primary"-->
    <!--@click="onConfirmPressed"-->
    <!--&gt;{{ confirmButtonText }}</el-button>-->
    <!--</span>-->
  </el-dialog>
</template>

<script>
  export default {
    name: 'Modal',
    props: {
      title: {
        type: String,
        default: '',
      },
      body: {
        type: Object,
        default: null,
      },
      bodyProps: {
        type: Object,
        default: null,
      },
      confirmButtonText: {
        type: String,
        default: () => {
          return 'Conferma';
        },
      },
      cancelButtonText: {
        type: String,
        default: 'Annulla',
      },
      hasFooter: {
        type: Boolean,
        default: false,
      },
      onConfirm: {
        type: Function,
        required: true,
        default: () => {
          this.onConfirmPressed();
        },
      },
      onCancel: {
        type: Function,
        default: () => {
          this.close();
        },
      },
    },
    data() {
      return {
        isOpen: false,
        isValid: true,
        isLoading: false,
        bodyData: null,
      };
    },
    mounted() {
      this.isOpen = true;
    },
    methods: {
      /**
       * Callback for dynamic component validation event
       *
       * @param isValid
       */
      onValidate(isValid) {
        this.isValid = isValid;
      },
      /**
       * Callback for dynamic component data change
       *
       * @param data
       */
      onChange(data) {
        this.bodyData = data;
      },
      /**
       * Callback for confirmation event
       *
       * for the moment it will return the instance and data directly in callback
       * but you should use getData,startLoading etc if you need them by assign it to a variable
       *  - this.modalCallback = this.$modal.open('Lorem ipsum dolor', ProductForm, this.onConfirm, this.onCancel);
       *  and then
       *  this.modalCallback.getData() or this.modalCallback.startLoading()
       */
      onConfirmPressed() {
        this.close();
        this.onConfirm({
          instance: this,
          data: this.bodyData,
        });
      },
      /**
       * Callback for confirmation event
       *
       * for the moment it will return the instance and data directly in callback
       * but you should use getData,startLoading etc if you need them by assign it to a variable
       *  - this.modalCallback = this.$modal.open('Lorem ipsum dolor', ProductForm, this.onConfirm, this.onCancel);
       *  and then
       *  this.modalCallback.getData() or this.modalCallback.startLoading()
       */
      onCancelPressed() {
        this.onCancel({
          instance: this,
          data: this.bodyData,
        });
        this.close();
      },
      /**
       * Set modal as loading
       */
      startLoading() {
        this.isLoading = true;
      },
      /**
       * Stop modal from loading
       */
      stopLoading() {
        this.isLoading = false;
      },
      getData() {
        return this.bodyData;
      },
      /**
       * Close modal
       */
      close() {
        this.isOpen = false;
      },
    },
  };
</script>

<style lang="scss">
  .el-dialog {
    // margin-top: 25vh !important;
    /*height: 70%;*/
    margin-bottom: 0;
    width: 100%;
    border-radius: 20px 20px 0px 0px;
    @apply absolute;
    @apply bottom-0;

    &__header {
      // @apply border-b;
      @apply border-gray-200;
      @apply p-4;

      .el-dialog__headerbtn {
        top: 16px;
        visibility: unset;
      }
    }

    &__body {
      max-height: 70vh;
      overflow: auto;
      padding: unset;
      width: 100%;
    }

    &__footer {
      @apply border-t;
      @apply border-gray-200;
      @apply p-4;
    }
  }
</style>
