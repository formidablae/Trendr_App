import Vue from 'vue';

const vueInstance = new Vue();

function _createNotification(title, message, type = 'error', showClose = true) {
  vueInstance.$notify({
    title,
    message,
    position: 'top-left',
    showClose,
    type,
  });
}

function _createMessage(message, type = 'success', showClose = true) {
  vueInstance.$message({
    message,
    type,
    showClose: true,
  });
}

const NotificationService = {
  error(message, title ='Error', showClose) {
    return _createNotification(title, message, 'error', showClose);
  },
  warning(message, showClose) {
    return _createMessage(message, 'warning', showClose);
  },
  success(message, showClose) {
    return _createMessage(message, 'success', showClose);
  },
  info(message, showClose) {
    return _createMessage(message, 'info', showClose);
  },
};

const Plugin = {
  install(Vue) {
    Vue.prototype.$notificationService = NotificationService;
  },
};

Vue.use(Plugin);
export default Plugin;
