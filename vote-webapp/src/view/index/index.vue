<template>
  <div style="height: 100%;">
    <!-- <van-notify id="van-notify" /> -->
      <van-button size="large" type="primary" style="position:absolute;top:50%; width: 100%;" @click="getUserInfo">
        使用微信账号身份登录
      </van-button>
    <van-button size="large" style="position:absolute;top:80%;width: 100%;" @click="toAdmin()">
    管理员登录
    </van-button>
    <van-dialog
      v-model="showDialog"
      title="正在登录中"
      :showConfirmButton="false"
    >
      <van-loading type="spinner" color="white" />
    </van-dialog>
  </div>
</template>

<script>
// var Fly = require("flyio/dist/npm/wx") 
// var fly = new Fly
var fly=require("flyio")
import Vue from 'vue'
// 这个是唤起Notify的函数，参照[Vant 文档](https://youzan.github.io/vant-weapp/#/notify)
// import Notify from '@/../static/vant/notify/notify'
// import Toast from '@/../static/vant/toast/toast'
// import Dialog from '@/../static/vant/dialog/dialog';
import { Notify, Dialog, Toast, Loading, Button } from 'vant'
Vue.use(Dialog)
export default {
  components: {
    [Notify.name]: Notify,
    [Dialog.name]: Dialog,
    [Toast.name]: Toast,
    [Loading.name]: Loading,
    [Button.name]: Button
  },
  data () {
    return {
      // Test
      deploy_domain: 'https://vote.ilingyue.cn',
      // deploy_domain: 'http://142.93.185.148:8888',
      userId: undefined,
      showPopup: false,
      selectedWorkTag: '',
      showDetailAction: false,
      showContactDialog: false,
      // 进入客服界面之前的提示信息
      subname: '',
      showDialog: false,
      openid: ''
    }
  },
  mounted: function () {
    this.openid = this.$route.query['openid']
    // if (this.openid === '' || this.openid === undefined || this.openid === null) {
    //   this.login_href = this.deploy_domain + '/login'
    // }
    // Notify(this.openid)
    // console.log(this.openid)
  },
  computed: {
    detailActions: function () {
      return [
        {
          name: '小程序内查看',
          subname: '在小程序内打开作品的 pdf 版本介绍'
        },
        {
          name: '作品链接',
          subname: '在客服号中回复 "' + this.selectedWorkTag
            + '" 获得作品链接'
        }
      ]
    }
  },
  methods: {
    toAdmin () {
      // wx.navigateTo({
      //   url: '../admin/main'
      // })
      this.$router.push('admin')
    },
    getUserInfo (e) {
      // Notify(this.$route.query['openid'])
      if (this.openid !== '') {
        this.$router.push({ name: 'vote', params: {userId: this.openid}})
      } else {
        Notify('还未登录')
        window.location = this.deploy_domain + '/login'
      }
      
      // if (e.target.errMsg.includes('fail')) {
      //   Notify('必须同意获取用户数据才能投票!')
      // } else {
      //   //调用微信登录接口  
      //   // wx.showLoading({
      //   //   title: '正在登录中',
      //   // })
      //   this.showDialog = true
      //   var _this = this
      //   wx.login({
      //       success: function (loginCode) {
      //       	// 毫无安全性的行为, 直接把 appid 放进去
      //       	// 希望 ctfer/hacker 手下留情, 反正就是一个很简陋的小程序
      //           var appid = 'wxfd7ef8735b0528b6'; //填写微信小程序appid  
      //           var secret = '4b19a6d11634f66eb533326e9b50146d'; //填写微信小程序secret  

      //           //调用request请求api转换登录凭证  
      //           wx.request({
      //               url: 'https://api.weixin.qq.com/sns/jscode2session?appid='+appid+'&secret='+secret+'&grant_type=authorization_code&js_code=' + loginCode.code,
      //               header: {
      //                   'content-type': 'application/json'
      //               },
      //               success: function (res) {
      //                   console.log('######### opendid' + JSON.stringify(res)) //获取openid
      //                   wx.hideLoading()
      //                   _this.userId = res['data']['openid']
      //                   // debug
      //                   // _this.userId = '_____adminTestId'
      //                   wx.navigateTo({
      //                     url: '../vote/main?userId=' + _this.userId
      //                   })
      //               },
      //               fail: function (e) {
      //                 wx.hideLoading()
      //                 Notify('openid 获取失败')
      //                 console.log('openid 获取失败')
      //                 console.log(e)
      //               }
      //           })
      //       },
      //       fail: function (e) {
      //         wx.hideLoading()
      //         Notify('login 失败')
      //         console.log('login 失败')
      //         console.log(e)
      //       }
      //   })
      //   console.log(e)
      // }
    }
  }
}
</script>

<style>
</style>
