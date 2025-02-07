from rest_framework import serializers
from django.conf import settings
from .models import Order, User, OrderItem, Category, Dish, Announcement


class DishSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ['id', 'name', 'cover_image', 'price', 'description']

    def get_cover_image(self, obj):
        if obj.cover_image:
            # 返回完整的图片 URL
            return f"{settings.BASE_URL}{obj.cover_image.url}"
        return None
        return None

class OrderItemSerializer(serializers.ModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), write_only=True)  # 反序列化时使用 ID
    dish_detail = DishSerializer(source='dish', read_only=True)  # 序列化时使用 DishSerializer

    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'dish_detail', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)  # 反序列化时使用
    items_detail = OrderItemSerializer(source='items', many=True, read_only=True)  # 序列化时使用
    user_id = serializers.IntegerField(write_only=True)
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'order_number', 'total_amount', 'recipient_address', 'recipient_name', 'recipient_phone', 'note', 'status', 'status_display', 'items', 'items_detail','created_at']
        extra_kwargs = {
            'user_id': {'required': True},
            'order_number': {'required': False},  # order_number 是可选的，因为会自动生成
            'total_amount': {'required': True},
            'recipient_address': {'required': True},
            'recipient_name': {'required': True},
            'recipient_phone': {'required': True},
            'note': {'required': False},  # 备注是可选的
            'status': {'required': False, 'default': 'pending'},  # 状态默认为 pending
            'status_display': {'required': False},
            'created_at': {'required': False},
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user_id = validated_data.pop('user_id')
        user = User.objects.get(id=user_id)
        order = Order.objects.create(user=user, **validated_data)

        # 创建订单项
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def get_status_display(self, obj):
        """使用 Django 内置的 get_status_display() 获取中文状态"""
        return obj.get_status_display()  # ✅ 直接调用 Django 的内置方法

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'phone','is_vip']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AnnouncementSerializer(serializers.ModelSerializer):
    publish_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M')  # 自定义时间格式
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'publish_time']

