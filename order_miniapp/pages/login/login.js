// pages/login.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    username: '',
    password: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },

  handleLogin() {
    const { username, password } = this.data;
    wx.request({
      url: 'http://127.0.0.1:8000/api/login/',  // Django 登录 API 地址
      method: 'POST',
      data: {
        username,
        password
      },
      success: (res) => {
        if (res.data.status === 'success') {
          console.log(res.data)
          wx.setStorageSync('token', res.data.token);
          wx.setStorageSync('userInfo', res.data);
    
          wx.reLaunch({
            url: '/pages/index/index'
          });
        } else {
          wx.showToast({
            title: '登录失败',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
      }
    });
  },

  handleInput(e) {
    const { field } = e.currentTarget.dataset;
    this.setData({
      [field]: e.detail.value
    });
  }
})