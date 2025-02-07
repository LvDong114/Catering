// pages/order/order.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    categories: [], // 用于存储分类数据
    dishes: [], // 用于存储菜品数据
    loading: true, // 加载状态
    error: null, // 错误信息
    activeCategoryId: null, // 当前选中的分类 ID
    cart: [], // 购物车数据
    totalAmount: 0, // 订单总金额
    isCartExpanded: false, // 购物车是否展开
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    this.fetchCategories();
  },

  /**
   * 获取分类数据
   */
  fetchCategories() {
    wx.request({
      url: 'http://127.0.0.1:8000/api/categories/', // Django 后端 API 地址
      method: 'GET',
      success: (res) => {
        if (res.data) {
          this.setData({
            categories: res.data,
            loading: false,
          });
          // 默认加载第一个分类的菜品
          if (res.data.length > 0) {
            this.setData({ activeCategoryId: res.data[0].id });
            this.fetchDishesByCategory(res.data[0].id);
          }
        }
      },
      fail: (err) => {
        console.error('获取分类数据失败', err);
        this.setData({
          error: '获取分类数据失败，请重试',
          loading: false,
        });
      },
    });
  },

  /**
   * 根据分类 ID 获取菜品数据
   */
  fetchDishesByCategory(categoryId) {
    wx.request({
      url: `http://127.0.0.1:8000/api/dishes/?category_id=${categoryId}`, // Django 后端 API 地址
      method: 'GET',
      success: (res) => {
        if (res.data) {
          this.setData({ dishes: res.data });
        }
      },
      fail: (err) => {
        console.error('获取菜品数据失败', err);
      },
    });
  },

  /**
   * 点击分类事件处理
   */
  handleCategoryClick(event) {
    const categoryId = event.currentTarget.dataset.id;
    this.setData({ activeCategoryId: categoryId });
    this.fetchDishesByCategory(categoryId);
  },

  /**
   * 加入购物车
   */
  addToCart(event) {
    const dishId = event.currentTarget.dataset.id;
    const dish = this.data.dishes.find(item => item.id === dishId);
    if (!dish) return;

    let cart = this.data.cart;
    const index = cart.findIndex(item => item.id === dishId);
    if (index >= 0) {
      cart[index].quantity += 1;
    } else {
      cart.push({ ...dish, quantity: 1 });
    }

    const totalAmount = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
    this.setData({
      cart,
      totalAmount,
    });
  },

  /**
   * 切换购物车展开状态
   */
  toggleCart() {
    this.setData({
      isCartExpanded: !this.data.isCartExpanded,
    });
  },
  clearCart(){
    this.setData({cart:[],totalAmount:0});
  },
// 删除购物车项
deleteCartItem(event) {
  const dishId = event.currentTarget.dataset.id;
  let cart = this.data.cart.filter(item => item.id !== dishId); // 过滤掉要删除的项
  const totalAmount = cart.reduce((sum, item) => sum + item.price * item.quantity, 0); // 重新计算总金额
  this.setData({
    cart,
    totalAmount,
  });
  wx.showToast({
    title: '删除成功',
    icon: 'success',
  });
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
   * 跳转到支付页面
   */
  goToPay() {
    const { cart, totalAmount } = this.data;
    if (cart.length === 0) {
      wx.showToast({
        title: '购物车为空',
        icon: 'none',
      });
      return;
    }

    // 跳转到支付页面，并传递购物车数据
    wx.navigateTo({
      url: `/pages/pay/pay?cart=${JSON.stringify(cart)}&totalAmount=${totalAmount}`,
    });
  },
});