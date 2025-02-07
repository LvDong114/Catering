// index.js
Page({
  data: {
    userInfo: null,
    swiperList: [
      {
        id: 1,
        imageUrl: 'https://ns-strategy.cdn.bcebos.com/ns-strategy/upload/fc_big_pic/part-00011-4052.jpg',
      },
      {
        id: 2,
        imageUrl: 'https://img2.baidu.com/it/u=3849150747,2094456552&fm=253&fmt=auto&app=138&f=JPEG?w=667&h=500',
      },
      {
        id: 3,
        imageUrl: 'https://img1.baidu.com/it/u=2282509933,2131626414&fm=253&fmt=auto&app=120&f=JPEG?w=1771&h=800',
      },
    ],
    announcements: [],
  },
  bindViewTap() {

  },
  onLoad() {
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.setData({ userInfo });
    }
    this.fetchAnnouncements();
  },
  fetchAnnouncements() {
    wx.request({
      url: 'http://127.0.0.1:8000/api/get_announcements/', // Django 后端 API 地址
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          this.setData({ announcements: res.data });
          console.log('公告数据:', res.data);
          console.log(this.data.announcements[0].title.length)
          console.log(this.data.announcements[0].title.slice(0,3))
        }
      },
      fail: (err) => {
        console.error('获取公告失败', err);
      },
    });
  },
  handleAnnouncementClick(event) {
    const announcementId = event.currentTarget.dataset.id;
    const announcement = this.data.announcements.find(item => item.id === announcementId);
    if (announcement) {
      wx.showModal({
        title: announcement.title,
        content: announcement.content,
        showCancel: false,
      });
    }
  },
  goToOrder(){
    wx.switchTab({
      url: '/pages/order/order',
    })
  }
})
