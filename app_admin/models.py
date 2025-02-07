import uuid

from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='dish_img/')
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    status = models.BooleanField(default=False)
    is_recommend = models.BooleanField(default=False)
    sale_count = models.IntegerField(default=0)

# 公告类
class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    publish_time = models.DateTimeField(default=timezone.now, verbose_name="发布时间")
    is_active = models.BooleanField(default=True, verbose_name="是否有效")

    class Meta:
        verbose_name = "公告"
        verbose_name_plural = "公告"
        ordering = ['-publish_time']  # 按发布时间降序排列

    def __str__(self):
        return self.title

# 自定义用户模型
class User(models.Model):
    username = models.CharField(max_length=150, unique=True, verbose_name="账号")
    password = models.CharField(max_length=128, verbose_name="密码")
    nickname = models.CharField(max_length=128,verbose_name="昵称")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="手机号")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="注册时间")
    is_vip = models.BooleanField(default=False,verbose_name="是否是vip")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"
        ordering = ['-date_joined']  # 按注册时间降序排列

    def __str__(self):
        return self.username

    # 自定义时间格式输出
    def formatted_date_joined(self):
        return self.date_joined.strftime('%Y-%m-%d %H:%M:%S')

# 订单模型
class Order(models.Model):
    # 订单状态选项
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]

    # 订单基本信息
    order_number = models.CharField(max_length=50, unique=True, verbose_name="订单号")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="总金额")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="订单状态")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # 收货信息
    recipient_name = models.CharField(max_length=100, verbose_name="收货人姓名")
    recipient_phone = models.CharField(max_length=15, verbose_name="收货人电话")
    recipient_address = models.CharField(max_length=255, verbose_name="收货地址")

    # 备注
    note = models.TextField(blank=True, null=True, verbose_name="备注")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"
        ordering = ['-created_at']  # 按创建时间降序排列

    def __str__(self):
        return self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            # 生成订单号：ORD + 年月日时分秒的纯数字 + 随机数
            now = timezone.now()
            random_suffix = str(uuid.uuid4().int)[:4]  # 生成4位随机数
            self.order_number = f"ORD{now.strftime('%Y%m%d%H%M')}{random_suffix}"
        super().save(*args, **kwargs)

    # 自定义时间格式输出
    def formatted_created_at(self):
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def formatted_updated_at(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')

# 订单项模型
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="订单")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="菜品")
    quantity = models.PositiveIntegerField(verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="单价")

    class Meta:
        verbose_name = "订单项"
        verbose_name_plural = "订单项"

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"

    def get_subtotal(self):
        return self.quantity * self.price

# Token
class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
    key = models.CharField(max_length=40, unique=True, verbose_name="Token")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"
        ordering = ['-created_at']

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return uuid.uuid4().hex
