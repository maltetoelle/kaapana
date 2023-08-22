
<template lang="pug">
  v-layout(row='')
    v-flex.text-xs-left(sm8, d-flex)
      v-card
        v-card-text.text-xs-left
          v-layout
            v-flex(xs12, py-1)
              div(style={'margin': '9px', 'margin-top': '10px'})
                img(src='../../assets/img/floto.png', alt='Vuetify', width='45%')
    v-flex.text-xs-left(sm4 d-flex)
      v-card(width='100%')
        v-card-text.text-xs-left()
          div
            h2 Welcome {{ currentUser.username }}!
            p Drop us an email!
            hr.my-2
        v-card-text
          v-layout(row='', wrap='')
            v-flex(py-1)
              v-card(href="mailto:malte.toelle@med.uni-heidelberg.de?subject=floto%20Support%20Question" elevation=0)
                v-card-title.justify-center
                  v-icon(x-large) mdi-email
                v-card-text
                  span malte.toelle@med.uni-heidelberg.de
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: 'KaapanaWelcome',
  props: {

  },
  computed: {
    ...mapGetters(["commonData", "currentUser"])
  },
  methods:{
    refreshIFrame: function(event){
      this.$refs.iframe.src = this.$refs.iframe.src
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>
