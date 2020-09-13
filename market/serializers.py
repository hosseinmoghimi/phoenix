from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from app.serializers import ProfileSerializer

class ShopRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model=ShopRegion
        fields=['id','name','server_address']      

class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=DeliveryAddress
        fields=['id','title','agent','mobile','street','region','tel']      

class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = ['product_name', 'product_image',
                  'product_id', 'quantity', 'price', 'unit_name']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'profile', 'image', 'priority','get_absolute_url',
                  'address', 'mobile', 'body', 'ship_fee']


class ShipperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipper
        fields = ['id', 'name', 'profile', 'image',
                  'priority', 'address', 'tel', 'mobile', 'body']

class ProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = ['id', 'name','priority']


class ShopSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializer()
    class Meta:
        model = Shop
        fields = ['id', 'supplier_id','supplier', 'unit_name','get_absolute_url',
                  'available', 'price', 'product_id', 'product_name', 'product_image']



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id',
                  'supplier_name',
                  'shipper_name',
                  'status',
                  'address',
                  'persian_order_date',
                  'persian_ship_date',
                  'persian_deliver_date',
                  'persian_cancel_date',
                  'persian_accept_date',
                  'persian_pack_date',
                  'description',
                  'supplier_id', 'shipper_id', 'count_of_packs', 'total', 'lines_total', 'ship_fee']


class CartLineSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()

    class Meta:
        model = CartLine
        fields = ['id', 'quantity', 'shop', 'persian_time_added']

class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductComment
        fields=['id','name','comment','persian_time_added','image','profile_id']
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id','get_edit_url', 'name', 'image', 'thumbnail', 'priority',
                  'price', 'short_description', 'category_id','get_absolute_url']

class ProductBriefSerialize(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    # products=ProductSerializer(many=True,read_only=True,)

    class Meta:
        model = Category
        fields = ['id','icon', 'name', 'image', 'priority', 'parent_id','get_edit_url']

class EmployeeSerializer(ProfileSerializer):
    pass

