// pages/order_list/order_list.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    orders: [], // 订单列表
    orderItems: [],
    loading: true, // 加载状态
    error: null, // 错误信息
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.fetchOrders();
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
    this.fetchOrders();
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
   * 获取订单列表
   */
  fetchOrders() {
    const user = wx.getStorageSync('userInfo');
    if (!user || !user.user_id) {
      this.setData({ error: '用户未登录', loading: false });
      return;
    }

    wx.request({
      url: `http://127.0.0.1:8000/api/orders/?user_id=${user.user_id}`, // 根据用户 ID 获取订单
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({ orders: res.data, loading: false });
          this.fetchOrderItems(this.data.orders)
        } else {
          this.setData({ error: '获取订单失败', loading: false });
        }
      },
      fail: (err) => {
        console.error('获取订单失败', err);
        this.setData({ error: '获取订单失败，请重试', loading: false });
      },
    });
  },
  /**
 * 获取每个订单的 orderitem 项
 */
fetchOrderItems(orders) {
  const promises = orders.map(order => {
      return new Promise((resolve, reject) => {
          wx.request({
              url: `http://127.0.0.1:8000/api/get_orderItems/?order_id=${order.id}`,
              method: 'GET',
              success: (res) => {
                  if (res.statusCode === 200) {
                      resolve({ ...order, items: res.data });
                  } else {
                      reject(new Error('获取订单项失败'));
                  }
              },
              fail: (err) => {
                  reject(err);
              },
          });
      });
  });

  // 等待所有 orderitem 请求完成
  Promise.all(promises)
      .then(ordersWithItems => {
          this.setData({ orders: ordersWithItems, loading: false });
      })
      .catch(err => {
          console.error('获取订单项失败', err);
          this.setData({ error: '获取订单项失败，请重试', loading: false });
      });
  },
})
