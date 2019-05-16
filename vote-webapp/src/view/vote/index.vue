<template>
  <div>
  	<van-dialog
      v-model="showLoadingDialog"
      title="正在下载中"
      :showConfirmButton="false"
    >
	</van-dialog>
    <van-card
      :tag="work.tag + ' 号'"
      :desc="work.desc"
      :title="work.title"
      v-for="work in works"
      :key="work.tag"
      :thumb="work.imageURL"
    >
      <div slot="footer">
        <van-button size="small" type="danger"
          @click="show_confirm_vote()"
          :disabled="disable_all || work.voted"
          round style="padding-right: 5px;">
          去投票
        </van-button>
        <van-button size="small" type="primary"
          @click="show_detail(work.tag)"
          round style="padding-left: 5px;">查看详情</van-button>
      </div>
    </van-card>
    <van-dialog id="van-dialog" />
    <van-dialog
      :show="showContactDialog"
      show-cancel-button
      :confirm-button-open-type="'contact'"
      @close="onContactDialogClose"
      @cancel="onContactDialogClose"
      title="提示"
      :message="subname"
    />
    <van-actionsheet v-model="showDetailAction" title="选择查看详情方式"
        @close="onActionClose()">
        <div>
          <van-button
            v-for="action in detailActions"
            :key="action.name"
            @click="onActionSelect(action.name, action.subname)"
            size="large">
            <!-- :open-type="action.name === '作品链接' ? 'contact' : ''"> -->
            {{ action.name }}
          </van-button>
        </div>
    </van-actionsheet>
    <van-notify id="van-notify" />
    <van-toast id="van-toast" />
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
import { Actionsheet } from 'vant';

Vue.use(Actionsheet);
import { Card } from 'vant';

Vue.use(Card);
var fly=require("flyio")
export default {
  components: {
    [Notify.name]: Notify,
    [Dialog.name]: Dialog,
    [Toast.name]: Toast,
    [Loading.name]: Loading,
    [Actionsheet.name]: Actionsheet,
  },
  data () {
    return {
      showLoadingDialog: true,
      // Test
      deploy_domain: 'https://vote.ilingyue.cn',
      // deploy_domain: 'http://142.93.185.148:8888',
      // userId: undefined,
      selectedWorkTag: '',
      showDetailAction: false,
      showContactDialog: false,
      disable_all: false,
      max_votes: 3,
      voted: 0,
      // 进入客服界面之前的提示信息
      subname: '',
      vote_url: 'https://mp.weixin.qq.com/s/xBss_zKOtVrYdyfcZDU0Yg',
      // 作品, 先不用分页和懒加载
      works: {
        // '1': {
        //   title: '作品 1',
        //   tag: '1',
        //   desc: '作品 1 的描述, TODO. 这只是简略表述, 每个作品还有一个图标, 图标有一个默认的占位符.',
        //   // 指向后端存储的作品 pdf 渲染
        //   pdf_url: 'https://media.nips.cc/Conferences/NIPS2018/Styles/nips_2018.pdf',
        //   // 这个是后台机器人回复该内容可以获得一个链接指向微信推送之类的地方去
        //   origin_url: '',
        //   imageURL: "https://avatars2.githubusercontent.com/u/8016514",
        //   voted: false,
        // },
        // '2': {
        //   title: '作品 2',
        //   tag: '2',
        //   desc: '作品 2 的描述, TODO. 这只是简略表述, 每个作品还有一个图标, 图标有一个默认的占位符.',
        //   // 指向后端存储的作品 pdf 渲染
        //   // TODO: 到时候这些 url 只能用站内 url
        //   pdf_url: 'https://media.nips.cc/Conferences/NIPS2018/Styles/nips_2018.pdf',
        //   // 这个是后台机器人回复该内容可以获得一个链接指向微信推送之类的地方去
        //   origin_url: '',
        //   imageURL: "https://avatars2.githubusercontent.com/u/8016514",
        //   voted: true,
        // },
        // '3': {
        //   title: '作品 3',
        //   tag: '3',
        //   desc: '作品 3 的描述, TODO. 这只是简略表述, 每个作品还有一个图标, 图标有一个默认的占位符.',
        //   // 指向后端存储的作品 pdf 渲染
        //   pdf_url: 'https://media.nips.cc/Conferences/NIPS2018/Styles/nips_2018.pdf',
        //   // 这个是后台机器人回复该内容可以获得一个链接指向微信推送之类的地方去
        //   origin_url: '',
        //   imageURL: "https://avatars2.githubusercontent.com/u/8016514",
        //   voted: false,
        // }
      }
    }
  },
  props: {
  	userId: String
  },
  onLoad (options) {
    // this.userId = this.$root.$mp.query.userId
  },
  mounted: function () {
    // this.$nextTick(function () {
    Notify('登录成功: ' + this.userId)
    // Notify('登录成功')
    // })
    // TODO
    var _this = this
    fly.post(this.deploy_domain + '/getWorks', {
      userId: this.userId
    }).then(function (response) {
      console.log(response);
      _this.showLoadingDialog = false
      if (response['data']['code'] === 'success') {
        // console.log(response['data']['data'])
        _this.works = response['data']['data']['works']
        _this.max_votes = response['data']['data']['max_votes']
        Notify('获取作品成功')
        var voted = 0
        var works = _this.works
        for (var w in _this.works) {
          if (works[w]['voted']) {
            voted += 1
            works[w]['btn_text'] = '已投票'
          } else {
            works[w]['btn_text'] = '直接投票'
          }
        }
        if (voted >= _this.max_votes) {
          _this.disable_all = true
        }
        _this.voted = voted
        _this.works = works
      }
      else {
        Notify('获取作品失败' + response['data']['data'])
      }
    }).catch(function (error) {
      console.log(error);
      _this.showLoadingDialog = false
      Notify('获取作品失败: ' + JSON.stringify(error));
    });
  },
  computed: {
    detailActions: function () {
      return [
        {
          name: 'pdf 查看',
          subname: '在小程序内打开作品的 pdf 版本介绍'
        },
        {
          name: '作品链接',
          subname: '查看作品原始链接'
        }
      ]
    }
  },
  methods: {
    show_confirm_vote () {
    	window.open(this.vote_url, '_blank')
    },
    show_detail (tag) {
      this.selectedWorkTag = tag
      this.showLoadingDialog = true
      var url = this.works[this.selectedWorkTag]['pdf_url']
      this.$router.push({ name: 'pdf', params: {
      	pdf_src: url,
      	// openid: this.openid
      }})
      this.showLoadingDialog = false
      // this.showDetailAction = true
    },
    onActionClose () {
      this.showDetailAction = false
      this.selectedWorkTag = ''
      Toast('取消查看详情')
    },
    onContactDialogClose() {
      this.showContactDialog = false
    },
    onActionSelect(actionName, subname) {
      this.showDetailAction = false
      if (actionName === 'pdf 查看') {
        // wx.showLoading({
        //   title: '文件下载中',
        // })
        this.showLoadingDialog = true
        var url = this.works[this.selectedWorkTag]['pdf_url']
        this.$router.push({ name: 'pdf', params: {
        	pdf_src: url,
        	openid: this.openid
        }})
        this.showLoadingDialog = false
        // wx.downloadFile({
        //   url: ,
        //   success(res) {
        //     const filePath = res.tempFilePath
        //     wx.openDocument({
        //       filePath,
        //       success(res) {
        //         wx.hideLoading()
        //         console.log(res)
        //         console.log('打开文档成功')
        //       },
        //       fail(res) {
        //         wx.hideLoading()
        //         console.log(res)
        //         Notify('打开文件失败')
        //       }
        //     })
        //   },
        //   fail(res) {
        //     wx.hideLoading()
        //     console.log(res)
        //     Notify('下载文件失败')
        //   }
        // })
      } else if (actionName === '作品链接') {
        // this.subname = subname
        // this.showContactDialog = true
        Notify('正在转跳到作品链接')
        var url = this.works[this.selectedWorkTag]['origin_url']
        window.open(url, '_blank')
      }
      this.selectedWorkTag = ''
    }
  }
}
</script>

<style>
</style>