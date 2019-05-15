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
      <view slot="footer">
        <van-button size="small" type="danger"
          @click="show_confirm_vote(work.tag, work.title, disable_all, work.voted)"
          :disabled="disable_all || work.voted"
          round style="padding-right: 5px;">
          {{ work.btn_text }}
        </van-button>
        <van-button size="small" type="primary"
          @click="show_detail(work.tag)"
          round style="padding-left: 5px;">查看详情</van-button>
      </view>
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
    <van-action-sheet :show="showDetailAction" title="选择查看详情方式"
        @close="onActionClose()">
        <view>
          <van-button
            v-for="action in detailActions"
            :key="action.name"
            @click="onActionSelect(action.name, action.subname)"
            size="large">
            <!-- :open-type="action.name === '作品链接' ? 'contact' : ''"> -->
            {{ action.name }}
          </van-button>
        </view>
    </van-action-sheet>
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
      showLoadingDialog: false,
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
        Notify('获取作品失败')
      }
    }).catch(function (error) {
      console.log(error);
      Notify('获取作品失败: ' + error);
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
    show_confirm_vote (tag, title, disable_all, voted) {
      if (disable_all) {
        Notify('您已经使用完了所有票数(' + this.voted + ' 张)')
      } else if (voted) {
        Notify('您已经投票了该作品')
      } else {
        Dialog.confirm({
          title: '确认投票',
          message: '是否确认为作品 "' + title + '"(' + tag + ') 投票, 投票后不能撤销!'
        }).then(() => {
          // TODO
          fly.post(this.deploy_domain + '/vote', {
            user_id: this.userId,
            tag: tag
          })
          .then(function (response) {
            console.log(response);
            Notify('作品 "' + title + '"( ' + tag + ') 投票成功');
          })
          .catch(function (error) {
            console.log(error);
            Notify('作品 "' + title + '"( ' + tag + ') 投票失败');
          });
          this.voted = this.voted + 1
          Notify('作品 "' + title + '"( ' + tag + ') 投票成功, 剩余可投票数 ' + (this.max_votes - this.voted) + ' 张')
          this.$set(this.works[tag], 'voted', true)
          this.$set(this.works[tag], 'btn_text', '已投票')
          if (this.max_votes <= this.voted) {
            this.disable_all = true
          }
        }).catch(() => {
          Toast('取消投票')
        });
      }
    },
    show_detail (tag) {
      this.selectedWorkTag = tag
      this.showDetailAction = true
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
      if (actionName === '小程序内查看') {
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
        this.subname = subname
        this.showContactDialog = true
      }
      this.selectedWorkTag = ''
    }
  }
}
</script>

<style>
</style>