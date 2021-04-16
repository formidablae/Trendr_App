import Vue from 'vue';
import Modal from './Modal';

/**
 * Create new modal instance and append to DOM
 *
 * @param propsData
 * @returns {{stopLoading: default.methods.stopLoading, startLoading: default.methods.startLoading, close: *}}
 */
function modal(propsData) {
  // Extend modal
  const instance = Vue.extend(Modal);

  // Create new instance
  let modalInstance = new instance({
    el: document.getElementById('app').appendChild(document.createElement('div')),
    propsData,
  });

  // Return instance of modal
  return {
    'close': modalInstance.close,
    'startLoading': modalInstance.startLoading,
    'stopLoading': modalInstance.stopLoading,
    'getData': modalInstance.getData,
  };
}

const ModalProgrammatic = {

  /**
   * Open modal
   *
   * @returns {{stopLoading: default.methods.stopLoading, startLoading: default.methods.startLoading, close: *}}
   * @param title
   * @param body
   * @param bodyProps
   * @param hasFooter
   * @param onConfirm
   * @param onCancel
   */
  open(title, body, bodyProps, onConfirm, onCancel = () => {
  }, hasFooter = true) {

    return modal({title, body, bodyProps, hasFooter, onConfirm, onCancel});
  },
};

const Plugin = {
  install(Vue) {
    Vue.prototype.$modal = ModalProgrammatic;
  },
};

Vue.use(Plugin);
export default Plugin;
