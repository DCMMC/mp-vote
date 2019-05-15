<template>
	<div>
		<div v-if="not_logined">
			<van-dialog
	      v-model="showLoadingDialog"
	      title="正在加载中"
	      :showConfirmButton="false"
	    >
	    </van-dialog>
			<van-panel title="管理员登录" use-footer-slot>
			  <div>
			  	<van-cell-group>
				  <van-field
				    v-model="username"
				    required
				    clearable
				    label="用户名"
				    placeholder="请输入用户名"
				  />

				  <van-field
				    v-model="password"
				    type="password"
				    label="密码"
				    clearable
				    placeholder="请输入密码"
				    required
				    :border="false"
				  />
				</van-cell-group>
			  </div>
			  <div slot="footer">
			    <van-button size="large" type="danger" @click="adminLogin">
			    	登录
					</van-button>
			  </div>
			</van-panel>
		</div>
		<div v-else>
			<div v-if="uploaddiv">
				<van-dialog
					use-slot
				  v-model="showDialog"
				  :show-confirm-button="tipDialog"
				  :show-cancel-button="true"
				  @close="onDialogClose"
				  @confirm="upload_works()"
				  @cancel="onDialogCancel"
				  :title="dialogTitle"
				>
					<div>
					  <div v-if="tipDialog">
					  	<text style="font-size: 18px;">
					  		{{ tips }}
					  	</text>
					  	<text style="color: red; font-size: 20px;">
					  		这将会清空之前所有数据!
					  	</text>
					  </div>
					  <div v-else>
					  	<van-progress :percentage="upload_progress" />
					  	<text></text>
					  </div>
					</div>
				</van-dialog>
				<van-panel title="上传作品表格" use-footer-slot>
				  <div>
				  	<van-cell-group>
						  <van-switch-cell
							  title="是否允许投票多个作品"
							  v-model="multi_votes"
							  @change="onVoteTypeChange"
							/>
							<div v-if="multi_votes">
								<text style="font-size: 20px;">
									请选择每个用户的最大可投票数
								</text>
								<van-stepper
								  v-model="max_votes"
								  integer
								  min="1"
								  input-width="80px"
								  style="font-size: 30px;"
								  @change="onMaxVotesChange"
								/>
							</div>
						</van-cell-group>
				  </div>
				  <div slot="footer">
				  	<van-uploader :after-read="upload_works" accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; application/wps-office.xlsx">
				  		<van-button size="large" type="danger"">
					    	选择表格文件并且上传
							</van-button>
						</van-uploader>
				  </div>
				</van-panel>
			</div>
			<div v-else>
				<van-dialog
		      :show="showContactDialog"
		      show-cancel-button
		      :confirm-button-open-type="'contact'"
		      @close="onContactDialogClose"
		      @cancel="onContactDialogClose"
		      title="提示"
		      message="按确认后转跳到客服界面键入 '投票结果' 下载投票结果 Excel 表格"
		    />
				<div style="padding-bottom: 30px;">
					<van-panel title="导出结果">
					  <div>
					  	<van-cell-group>
					  		<van-button size="large" type="primary"
					  				@click="exportResult()">
							    导出投票结果
								</van-button>
							</van-cell-group>
					  </div>
					</van-panel>
				</div>
				<div style="padding-bottom: 30px;">
					<van-panel title="各作品投票结果" use-footer-slot>
					  <div>
					  	<van-cell-group>
					  		<van-cell
					  			v-for="work in works"
					  			:title="work.tag"
					  			:value="work.votes"
					  			:key="work.tag"
					  			:label="work.title" />
							</van-cell-group>
					  </div>
					</van-panel>
				</div>
			</div>
			<van-tabbar
			  v-model="tabBarActive"
			  @change="onTabBarChange"
			  active-color="#07c160"
			>
			  <van-tabbar-item icon="setting">上传作品</van-tabbar-item>
			  <van-tabbar-item icon="chat">投票结果</van-tabbar-item>
			</van-tabbar>
		</div>
		<!-- <van-notify id="van-notify" /> -->
	</div>
</template>

<script>
import { Notify, Dialog, Toast, Loading, Panel, Button, Field,
	Cell, CellGroup, SwitchCell } from 'vant'
import Vue from 'vue'
Vue.use(Notify)
Vue.use(Panel)
Vue.use(Button)
Vue.use(Dialog)
Vue.use(Field)
Vue.use(Cell).use(CellGroup).use(SwitchCell)
import { Tabbar, TabbarItem } from 'vant';

Vue.use(Tabbar).use(TabbarItem);
import { Stepper } from 'vant';
Vue.use(Stepper);
import { Uploader } from 'vant';

Vue.use(Uploader);
const axios = require('axios');

export default {
	components: {
	    [Notify.name]: Notify,
	    [Dialog.name]: Dialog,
	    [Toast.name]: Toast,
	    [Loading.name]: Loading,
	    // [Button.name]: Button
	  },
	data () {
		return {
			username: '',
			password: '',
			uploaddiv: true,
			not_logined: true,
			multi_votes: false,
			showContactDialog: false,
			max_votes: 1,
			showDialog: false,
			tipDialog: true,
			tips: '从聊天内容中选择文件, 请选择 ".xls" 或 ".xlsx" 格式的 Excel 表格文件.',
			upload_progress: 0,
			uploadTask: undefined,
			dialogTitle: '提示',
			tabBarActive: 0,
			works: undefined,
			showLoadingDialog: false,
			// Test
			// deploy_domain: 'http://vote.ilingyue.cn:8888',
			deploy_domain: 'http://142.93.185.148:8888',
		}
	},
	computed: {

	},
	methods: {
		adminLogin () {
			// wx.showLoading({
   //      title: '正在登录中',
   //    })
			var _this = this
			axios.post(this.deploy_domain + '/adminLogin', {
		    username: this.username,
		    password: this.password
		  }).then(function (response) {
		    console.log(response);
		    if (response.data.code === 'success') {
		    	// wx.setStorageSync("admin_sessionid",
		    	// 	response.headers["set-cookie"][0])
		    	// wx.hideLoading()
		    	Notify('登录成功')
		    	_this.not_logined = false
		    }
		    else {
		    	// wx.hideLoading()
		      Notify('账号或密码错误')
		    }
		  }).catch(function (error) {
		    console.log(error);
		    // wx.hideLoading()
		    Notify('登录失败');
		  });
		},
		confirm_upload () {
			this.showDialog = true
		},
		upload_works (file, detail) {
			console.log(file)
			if (file.file.name.endsWith('.xlsx')) {
				let data = new FormData()
				data.set('max_votes', this.max_votes)
				data.append('file', file.file)
				axios.post(this.deploy_domain + '/upload',
				  data,
				  {
				    headers: {
				        'Content-Type': 'multipart/form-data',
				        'accept': 'application/json'
				    }
				  }
				).then(function(){
					Notify('文件 "' + file.file.name + '" 上传成功')
				})
				.catch(function(e){
					Notify('文件 "' + file.file.name + '" 上传失败: ' + JSON.stringify(e))
				});
			} else {
				Notify('文件 "' + file.file.name + '" 不是表格文件(xlsx)')
			}
			// wx.chooseMessageFile({
			//   count: 1,
			//   type: 'file',
			//   success(res) {
			//     if (res.errMsg === 'chooseMessageFile:ok') {
			// 			_this.dialogTitle = '上传进度'
			// 			_this.showDialog = true
			//     	const tempFilePath = res.tempFiles[0]['path']
			//     	const fileName = res.tempFiles[0]['name']
			//     	if (fileName.endsWith('.xlsx')) {
				   //  	_this.uploadTask = wx.uploadFile({
					  //   	// TODO
					  //     url: _this.deploy_domain + '/upload',
					  //     filePath: tempFilePath,
					  //     name: fileName,
					  //     formData: {
					  //       max_votes: _this.max_votes
					  //     },
					  //     header: {
					  //       "Content-Type": "multipart/form-data",
					  //       'accept': 'application/json',
					  //       'cookie': wx.getStorageSync("admin_sessionid")
					  //     },
					  //     success(res) {
					  //     	console.log(res)
					  //       // const data = res.data
					  //       let data = JSON.parse(res.data)
					  //       if (data['code'] === 'success') {
					  //       	Notify('上传文件成功, 成功导入 ' + data['data'])
					  //       } else {
					  //       	Notify('上传文件失败, ' + data['data'])
					  //       }
					  //       _this.showDialog = false
					  //     		setTimeout(() => {
							//       	_this.tipDialog = true
							//       	_this.uploadTask = undefined
							//       	_this.dialogTitle = '提示'
					  //     		}, 300)
					  //     },
					  //     fail (res) {
					  //     	console.log(JSON.stringify(res))
					  //     	// TODO
					  //     	// debug
					  //     	// _this.upload_progress = 30
					  //     	// setTimeout(() => {
				   //    		_this.showDialog = false
				   //    		Notify('上传文件失败')
				   //    		setTimeout(() => {
						 //      	_this.tipDialog = true
						 //      	_this.uploadTask = undefined
						 //      	_this.dialogTitle = '提示'
				   //    		}, 300)
					  //     	// }, 2000)
					  //     }
					  //   })
					  //   _this.uploadTask.onProgressUpdate((res) => {
							//   _this.upload_progress = res.progress
							//   // console.log('已经上传的数据长度', res.totalBytesSent)
							//   // console.log('预期需要上传的数据总长度', res.totalBytesExpectedToSend)
							// })
			    // 	} else {
			    // 		_this.showDialog = false
		     //  		setTimeout(() => {
				   //    	_this.tipDialog = true
				   //    	_this.uploadTask = undefined
				   //    	_this.dialogTitle = '提示'
		     //  		}, 300)
		     //  		Notify('文件 "' + fileName + '" 不是表格文件(xlsx)')
			    // 	}
			    // } else {
			    // 	console.log(res)
			    // 	_this.showDialog = false
	      // 		setTimeout(() => {
			    //   	_this.tipDialog = true
			    //   	_this.uploadTask = undefined
			    //   	_this.dialogTitle = '提示'
	      // 		}, 300)
			    // 	Notify('读取文件失败')
			    // }
			//   },
			//   fail (res) {
			//   	_this.showDialog = false
   //    		setTimeout(() => {
		 //      	_this.tipDialog = true
		 //      	_this.uploadTask = undefined
		 //      	_this.dialogTitle = '提示'
   //    		}, 300)
			//   	Notify('读取文件失败')
			//   	console.log(JSON.stringify(res))
			//   }
			// })
		},
		onVoteTypeChange (e) {
			console.log(e)
		},
		onMaxVotesChange (e) {
		},
		onDialogClose (e) {
		},
		onDialogCancel (e) {
			this.showDialog = false
			if (this.uploadTask !== undefined) {
				this.showDialog = false
    		setTimeout(() => {
	      	this.tipDialog = true
	      	this.uploadTask = undefined
	      	this.dialogTitle = '提示'
    		}, 300)
    		Notify('取消上传文件')
			}
		},
		exportResult () {
			this.showContactDialog = true
		},
    onContactDialogClose() {
      this.showContactDialog = false
    },
		onTabBarChange (e) {
			this.uploaddiv = (this.tabBarActive === 0)
			// this.showLoadingDialog = true
			var _this = this
			// TODO 下载数据
			if (this.tabBarActive === 1) {
				// wx.showLoading({
    //       title: '下载数据中',
    //     })
        axios.post(this.deploy_domain + '/get_results', {}, {
        	headers: {
        		'accept': 'application/json'
        	}
        }).then(function (response) {
			    console.log(response);
			    // _this.showLoadingDialog = false
			    if (response.data.code === 'success') {
			    	// wx.hideLoading()
			    	Notify('获取成功')
			    	_this.works = response.data.data
			    }
			    else {
			    	// wx.hideLoading()
			      Notify('获取出错 ' + response.data.data)
			    }
			  }).catch(function (error) {
			    console.log(error)
			    // _this.showLoadingDialog = false
			    // wx.hideLoading()
			    Notify('获取失败')
			  });
        // setTimeout(() => {
        // 	var works = {}
        // 	for (var i = 1; i <= 20; i++) {
        // 		works['' + i] = {
        // 			title: '作品 ' + i,
        // 			tag: '' + i,
        // 			votes: Math.floor(Math.random() * Math.floor(40))
        // 		}
        // 	}
        // 	this.works = works
        // 	wx.hideLoading()
        // }, 400)
			}
		}
	}
}
</script>