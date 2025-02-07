from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage, default_storage
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView

from app_admin.models import Dish, Category, Announcement, User, Order, OrderItem, Token
from app_admin.serializers import OrderSerializer, UserSerializer, DishSerializer, CategorySerializer, \
    OrderItemSerializer, AnnouncementSerializer


# Create your views here.
def admin_board(request):
    return render(request, "admin_board.html")
def dish_management(request):
    dishes = Dish.objects.all()
    return render(request, "dish_management.html", {"dishes": dishes})
def delete_dish(request, dish_id):
    try:
        dish = Dish.objects.get(id=dish_id)
        print(f"Deleting dish: {dish.name}")  # 调试信息
        
        # 删除封面图
        if dish.cover_image:
            default_storage.delete(dish.cover_image.path)
        
        dish.delete()
        return HttpResponse(status=204)  # 返回空响应，状态码 204 表示成功但无内容
    except Dish.DoesNotExist:
        print(f"Dish with id {dish_id} not found")  # 调试信息
        return HttpResponse(status=404)  # 如果菜品不存在，返回 404
def edit_dish(request, dish_id):
    dish = Dish.objects.get(id=dish_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        dish.name = request.POST.get('name')
        dish.category_id = request.POST.get('category')
        
        if 'cover_image' in request.FILES:
            # 删除旧的封面图
            if dish.cover_image:
                default_storage.delete(dish.cover_image.path)
            
            # 保存新的封面图
            cover_image = request.FILES['cover_image']
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT))
            filename = fs.save(os.path.join('dish_img', cover_image.name), cover_image)
            dish.cover_image = filename
        
        dish.description = request.POST.get('description')
        dish.price = float(request.POST.get('price'))
        dish.stock = int(request.POST.get('stock'))
        dish.status = request.POST.get('status') == 'true'
        dish.is_recommend = request.POST.get('is_recommend') == 'true'
        dish.save()
        return redirect('dish-management')
    
    return render(request, "edit_dish.html", {
        "dish": dish,
        "categories": categories
    })
def add_dish(request):
    categories = Category.objects.all()
    if request.method == 'POST' and request.FILES['cover_image']:
        cover_image = request.FILES['cover_image']
        # 确保路径正确指向 media 目录
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT))
        # 保存文件到 media/dish_img 目录
        filename = fs.save(os.path.join('dish_img', cover_image.name), cover_image)
        dish = Dish(
            name=request.POST.get('name'),
            category_id=request.POST.get('category'),
            cover_image=filename,  # 保存文件名
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            stock=request.POST.get('stock'),
            is_recommend=request.POST.get('is_recommend') == 'true',
            status=request.POST.get('status') == 'true'
        )
        dish.save()
        return redirect('dish-management')
    return render(request, "add_dish.html", {"categories": categories})

def category_management(request):
    categories = Category.objects.all()
    return render(request, "category_management.html", {"categories": categories})


def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return HttpResponse(status=204)  # 返回空响应，状态码 204 表示成功但无内容
    except Category.DoesNotExist:
        print(f"category with id {category_id} not found")  # 调试信息
        return HttpResponse(status=404)  # 如果菜品不存在，返回 404


def edit_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('category-management')
    return render(request, "edit_category.html", {
        "category": category
    })


def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('category-management')
    return render(request, "add_category.html")

def announcement_management(request):
    print("Executing announcement_management view")  # 调试信息
    announcements = Announcement.objects.all()
    return render(request, "announcement_management.html", {"announcements": announcements})

def add_announcement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_active = request.POST.get('is_active') == 'true'
        announcement = Announcement(
            title=title,
            content=content,
            is_active=is_active
        )
        announcement.save()
        return redirect('announcement-management')
    return render(request, "add_announcement.html")

def edit_announcement(request, announcement_id):
    announcement = Announcement.objects.get(id=announcement_id)
    if request.method == 'POST':
        announcement.title = request.POST.get('title')
        announcement.content = request.POST.get('content')
        announcement.is_active = request.POST.get('is_active') == 'true'
        announcement.save()
        return redirect('announcement-management')
    return render(request, "edit_announcement.html", {"announcement": announcement})

def delete_announcement(request, announcement_id):
    print(f"Deleting announcement with ID: {announcement_id}")  # 调试信息
    try:
        announcement = Announcement.objects.get(id=announcement_id)
        announcement.delete()
        return HttpResponse(status=204)  # 返回空响应，状态码 204 表示成功但无内容
    except Announcement.DoesNotExist:
        print(f"Announcement with id {announcement_id} not found")  # 调试信息
        return HttpResponse(status=404)  # 如果公告不存在，返回 404

# 用户管理视图
def user_management(request):
    users = User.objects.all()
    return render(request, "user_management.html", {"users": users})

# 删除用户视图
def delete_user(request, user_id):
    print(f"Deleting user with ID: {user_id}")  # 调试信息
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponse(status=204)  # 返回空响应，状态码 204 表示成功但无内容
    except User.DoesNotExist:
        print(f"User with id {user_id} not found")  # 调试信息
        return HttpResponse(status=404)  # 如果用户不存在，返回 404

# 订单管理视图
def order_management(request):
    status = request.GET.get('status', '')  # 获取状态参数
    orders = Order.objects.all().order_by('-created_at')

    # 根据状态筛选订单
    if status:
        orders = orders.filter(status=status)

    return render(request, "order_management.html", {"orders": orders})

# 删除订单视图
def delete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        order.delete()
        return HttpResponse(status=204)  # 返回空响应，状态码 204 表示成功但无内容
    except Order.DoesNotExist:
        return HttpResponse(status=404)  # 如果订单不存在，返回 404

# 订单详情视图
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_detail.html", {"order": order})

# 更新订单状态视图
@csrf_exempt
def update_order_status(request, order_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order = Order.objects.get(id=order_id)
            order.status = data.get('status')
            order.save()
            return JsonResponse({'success': True})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': '订单不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': '无效的请求方法'}, status=400)

# 获取订单列表
@api_view(['GET'])
def get_orders(request):
    user_id = request.query_params.get('user_id')
    if user_id:
        orders = Order.objects.filter(user_id=user_id)
    else:
        orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
@api_view(['GET'])
def get_orderItems_by_order_id(request):
    order_id = request.query_params.get('order_id')
    if order_id:
       orderItems  = OrderItem.objects.filter(order_id=order_id)
    else:
        orderItems = OrderItem.objects.all()
    serializer = OrderItemSerializer(orderItems, many=True)
    return Response(serializer.data)

# 小程序登陆
@api_view(['POST'])
@permission_classes([AllowAny])
def mini_program_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
        if user.password == password:  # 使用自定义的密码验证
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': 'success',
                'token': token.key,
                'user_id': user.id,
                'username': user.username,
                'nickname': user.nickname,
                'phone': user.phone,
                'is_vip': user.is_vip,
            })
        else:
            return Response({'status': 'error', 'message': 'Invalid credentials'}, status=401)
    except User.DoesNotExist:
      return Response({'status': 'error', 'message': 'User not found'}, status=404)

def verify_token(request):
    token_key = request.headers.get('Authorization')
    if not token_key:
        return JsonResponse({'status': 'error', 'message': 'Token is required'}, status=401)
    
    try:
        token = Token.objects.get(key=token_key)
        return JsonResponse({'status': 'success', 'user_id': token.user.id})
    except Token.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid token'}, status=401)

# 获取菜单分类
@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_dishes_by_category(request):
    category_id = request.query_params.get('category_id')
    dishes = Dish.objects.filter(category_id=category_id)
    serializer = DishSerializer(dishes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_announcements(request):
    # 按照发布时间降序排列，并只获取最新的三条公告
    announcements = Announcement.objects.filter(is_active=True).order_by('-publish_time')[:3]
    serializer = AnnouncementSerializer(announcements, many=True)
    return Response(serializer.data)


class AddOrdersView(APIView):
    def post(self, request):
        # 获取请求数据
        data = request.data

        # 验证数据
        required_fields = ['user_id', 'items', 'total_amount', 'recipient_address', 'recipient_name', 'recipient_phone']
        if not all(key in data for key in required_fields):
            print(data)  # 打印接收到的数据
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

        # 创建订单
        try:
            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
