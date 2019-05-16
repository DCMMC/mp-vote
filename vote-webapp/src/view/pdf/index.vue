<template>
  <div>
  	<!-- <van-nav-bar
      title="作品预览"
      left-text="返回"
      left-arrow
      @click-left="onClickLeft"
    /> -->
    <van-dialog
      v-model="showLoadingDialog"
      title="正在下载中, 请耐心等待"
      :showConfirmButton="false"
    >
  </van-dialog>
    <pdf :src="pdf_src" :page="1" @progress="loading">
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
// import pdf from 'pdfvuer'
import pdf from 'vue-pdf'

export default {
  components: {
    [Notify.name]: Notify,
    [Dialog.name]: Dialog,
    [Toast.name]: Toast,
    [Loading.name]: Loading,
    pdf
  },
  data () {
    return {
      showLoadingDialog: true,
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
    },
    loading (e) {
      console.log(e)
      this.showLoadingDialog = (('' + e) !== '1')
    }
  }
}
</script>

<style>
</style>