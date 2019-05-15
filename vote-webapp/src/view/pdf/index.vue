<template>
  <div>
  	<van-nav-bar
      title="作品预览"
      left-text="返回"
      left-arrow
      @click-left="onClickLeft"
    />
    <pdf :src="pdf_src" :page="1">
    </pdf>
  </div>
</template>

<script>
// var Fly = require("flyio/dist/npm/wx") 
// var fly = new Fly
// 这个是唤起Notify的函数，参照[Vant 文档](https://youzan.github.io/vant-weapp/#/notify)
// import Notify from '@/../static/vant/notify/notify'
// import Toast from '@/../static/vant/toast/toast'
// import Dialog from '@/../static/vant/dialog/dialog'
import { Notify, Dialog, Toast, Loading, Button } from 'vant'
import Vue from 'vue'
Vue.use(Notify)
Vue.use(Button)
Vue.use(Dialog)
Vue.use(Toast)
import { NavBar } from 'vant';

Vue.use(NavBar);
var fly=require("flyio")
export default {
  components: {
    [Notify.name]: Notify,
    [Dialog.name]: Dialog,
    [Toast.name]: Toast,
    [Loading.name]: Loading
  },
  data () {
    return {
    }
  },
  props: {
  	pdf_src: String,
    openid: String,
  },
  mounted: function () {
    
  },
  computed: {
    
  },
  methods: {
    onClickLeft () {
      this.$router.go(-1)
    }
  }
}
</script>

<style>
</style>