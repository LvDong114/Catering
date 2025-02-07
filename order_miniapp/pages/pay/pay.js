// pages/pay/pay.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    user: null, // 用户信息

    cart: [], // 购物车数据
    totalAmount: 0, // 总金额
    address: '', // 收货地址
    note: '', // 备注
    phone:'',
    recipient_name:'',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    // 从本地存储中获取用户信息
    const user = wx.getStorageSync('userInfo');
    console.log(user.user_id)
    if (user.id) {
        this.setData({ user });
    }
    // 解析购物车数据
    const cart = JSON.parse(options.cart);
    const totalAmount = parseFloat(options.totalAmount);
    this.setData({ user,cart, totalAmount });
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

  /**
   * 处理收货地址输入
   */
  handleAddressInput(e) {
    this.setData({ address: e.detail.value });
  },

  /**
   * 处理备注输入
   */
  handleNoteInput(e) {
    this.setData({ note: e.detail.value });
  },
  handlePhoneInput(e) {
    this.setData({ phone: e.detail.value });
  },
  handleRecipientNameInput(e) {
    this.setData({ recipient_name: e.detail.value });
  },

  /**
   * 处理支付
   */
  handlePay() {
    const { user, cart, totalAmount, address, note } = this.data;
    console.log(user.user_id)
    if (!cart || cart.length === 0) {
        wx.showToast({
            title: '购物车为空',
            icon: 'none',
        });
        return;
    }

    if (!totalAmount || totalAmount <= 0) {
        wx.showToast({
            title: '总金额无效',
            icon: 'none',
        });
        return;
    }

    if (!address) {
        wx.showToast({
            title: '请输入收货地址',
            icon: 'none',
        });
        return;
    }

    // 构造订单数据
    console.log("id:"+user.user_id)
    const order = {
        user_id: user.user_id,  // 确保使用 user_id
        items: cart.map(item => ({
            dish: item.id,
            quantity: item.quantity,
            price: item.price,
        })),
        total_amount: totalAmount,
        recipient_address: address,  // 修改为 recipient_address
        recipient_name: this.data.recipient_name || user.username,  // 使用用户名作为收货人姓名
        recipient_phone: this.data.phone || user.phone,  // 使用用户手机号作为收货人电话
        note: note || '',  // 如果备注为空，设置为空字符串
    };

    // 打印订单数据
    console.log('订单数据:', order);

    // 发送订单数据到 Django 后台
    wx.request({
        url: 'http://127.0.0.1:8000/api/add_orders/',
        method: 'POST',
        data: order,
        success: (res) => {
            if (res.statusCode === 201) {
                wx.showToast({
                    title: '支付成功',
                    icon: 'success',
                });
                wx.switchTab({
                  url: '/pages/order_list/order_list', // 跳转到订单列表页面
                });
            } else {
                wx.showToast({
                    title: '支付失败，请重试',
                    icon: 'none',
                });
                console.error('支付失败:', res.data);  // 打印错误信息
            }
        },
        fail: (err) => {
            console.error('支付失败', err);
            wx.showToast({
                title: '支付失败，请重试',
                icon: 'none',
            });
        },
    });
  },
})