import Vue from "vue";
import Vuetify from "vuetify/lib";
import "vuetify/dist/vuetify.min.css";
import "@mdi/font/css/materialdesignicons.css"; // Ensure you are using css-loader
import Notifications from "vue-notification";

import colors from "vuetify/lib/util/colors";

Vue.use(Vuetify);
Vue.use(Notifications);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#004a6f",
        secondary: "#009ee3",
        accent: colors.shades.black,
        error: colors.red.darken2,
      },
      dark: {
        primary: "#009ee3",
        secondary: "#004a6f",
        accent: colors.shades.black,
        error: colors.red.darken2,
      }
    },
  },
  icons: {
    iconfont: "mdi",
  },
});
