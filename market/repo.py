import datetime
from .apps import APP_NAME
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Max, Min,F,Q
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from app.constants import *
from app.enums import *
from app.models import Profile,Comment
from app.persian import PersianCalendar
from app.repo import ProfileRepo
# from leopusher.mypusher import MyPusherChannel
from app.settings import DEBUG
from app.repo import NotificationRepo,ProfileTransactionRepo



class EmployeeRepo():
    def __init__(self,user=None):
        self.user=user
        self.objects=Employee.objects
        self.profile=ProfileRepo(user=user).me
        try:
            self.me = self.objects.get(profile=self.profile)          
        except :
            self.me = None
    def list(self):
        return self.objects.all()
        
    def get(self,employee_id):
        try:
            return self.objects.get(pk=employee_id)
        except :
            return None


class CustomerRepo():
    def __init__(self, user=None):
        self.user = user
        self.objects = Customer.objects
        
        self.profile=ProfileRepo(user=user).me
        try:
            self.me = self.objects.get(profile=self.profile)          
        except :
            self.me = None
    def list(self):
        return self.objects.all()
        
    def add_customer(self,first_name,last_name,username,password):
        # must be replaced
        region = RegionRepo(user=self.user).get(region_id=1)
        user = User.objects.create_user(username = username,email = 'new_user@khafonline.com', password = password)
        if user is not None:
            user.save()
            if user is not None:
                # user=ProfileRepo(user=self.user).register(username=username,password=password,first_name=first_name,last_name=last_name,region_id=region_id).user
                customer = Customer(first_name=first_name,last_name=last_name,user=user,region=region)
                customer.save()
                return customer
        return None
    def get(self,customer_id):
        try:
            return self.objects.get(pk=customer_id)
        except :
            return None



class ProductUnitRepo:
    def get_default(self):
        try:
            adad=self.objects.get(name='عدد')
        except:        
            self.objects.filter(name='عدد').delete()
            ProductUnit(name='عدد',priority=1).save()    
            adad=self.objects.get(name='عدد')
        return adad
    def __init__(self,user=None):
        self.objects=ProductUnit.objects
        self.user=user
    def get_by_name(self,name):
        try:
            return self.objects.get(name=name)
        except :
            return None
    def list(self):
        return self.objects.all()
    def list_for_product(self,product_id):
        product=ProductRepo(user=self.user).get(product_id=product_id)
        if product is not None:
            return product.unit_names.all()

class OrderRepo:
    def __init__(self,user):
        self.objects=Order.objects.order_by('-id')
        self.user=user        
        self.profile=ProfileRepo(user=user).me
    
    def do_pack(self, order_id, description, count_of_packs=1):
        profile = self.profile
        if profile is None:
            return None
        order = self.objects.get(pk=order_id)
        if order.supplier.profile == profile and (order.status == OrderStatusEnum.PACKING or order.status==OrderStatusEnum.ACCEPTED):

            order.count_of_packs = count_of_packs
            if order.description is None:
                order.description = ''
            if description is not None:
                order.description+='<br>   & ' + \
                    order.supplier.title+' : '+str(description)
            order.pack_date = datetime.datetime.now()
            order.status = OrderStatusEnum.PACKED
            order.save()
            if not order.no_ship:
                # MyPusherChannel(user=self.user).pack(order_id=order.id,region_id=order.supplier.region,count_of_packs=order.count_of_packs)
                NotificationRepo(user=self.user).add(title=f'سفارش شماره {order.id} بسته بندی شده است.',url=order.get_absolute_url(),body=f'سفارش  شماره {order.id}  توسط {order.supplier.title} در {order.count_of_packs} بسته آماده ارسال می باشد.',icon='alarm',profile_id=order.customer.profile.pk,color='success',priority=1)
                    
            if order is not None:
                return order

    def cancel_order(self, order_id, description):
        profile = self.profile
        if profile is None:
            return None
        order = Order.objects.get(pk=order_id)
        if order.profile == profile and order.status == OrderStatusEnum.CONFIRMED:
            order.status = OrderStatusEnum.CANCELED
            if order.description is None:
                order.description = ''
            order.cancel_date = datetime.datetime.now()
            if description is not None:
                order.description = order.description+'   @ ' + \
                    order.profile.full_name()+' # انصراف '+PersianCalendar().from_gregorian(order.cancel_date)+' : '+str(description)
            order.save()
            if order is not None:
                return order
    
    def confirm_order(self, order_id, description):
        profile = ProfileRepo(user=self.user).me
        if profile is None:
            return None
        order = Order.objects.get(pk=order_id)
        if order.profile == profile and order.status == OrderStatusEnum.CANCELED:
            order.status = OrderStatusEnum.CONFIRMED
            if order.description is None:
                order.description = ''
            if description is not None:
                order.description = order.description+'   @ ' + \
                    order.profile.full_name()+' # تایید مجدد '+PersianCalendar().from_gregorian(datetime.datetime.now())+' : '+str(description)
            order.save()
            if order is not None:
                return order
    
    def do_ship(self, order_id, description=''):
        shipper = ShipperRepo(user=self.user).me
        
        if shipper is None:
            return None
        order = OrderRepo(user=self.user).get(order_id=order_id)
        if order.status == OrderStatusEnum.PACKED:
            if description is not None:
                order.description += '<br>   & ' + \
                    shipper.title+' : '+description
            order.ship_date = datetime.datetime.now()
            order.status = OrderStatusEnum.SHIPPED
            order.shipper = shipper
            order.save()
            if order is not None:
                NotificationRepo(user=self.user).add(title=f'سفارش شماره {order.id} ارسال شده است.',url=order.get_absolute_url(),body=f'سفارش  شماره {order.id}  توسط {order.shipper.title} ارسال شده است.',icon='alarm',profile_id=order.customer.profile.pk,color='success',priority=1)
                NotificationRepo(user=self.user).add(title=f'سفارش شماره {order.id} ارسال شده است.',url=order.get_absolute_url(),body=f'سفارش  شماره {order.id}  توسط {order.shipper.title} ارسال شده است.',icon='alarm',profile_id=order.supplier.profile.pk,color='success',priority=1)
                 
                return order
        

    def do_deliver(self, order_id, description=''):
        customer = CustomerRepo(user=self.user).me
        if customer is None:
            return None 
        order = OrderRepo(user=self.user).get(order_id=order_id)
        if order.status == OrderStatusEnum.SHIPPED or (order.status == OrderStatusEnum.PACKED and order.no_ship==True):
            if description is not None:
                order.description +='<br>   & '+customer.profile.name()+' : '+description
            order.deliver_date = datetime.datetime.now()
            order.status = OrderStatusEnum.DELIVERED
            order.save()
            if order is not None:
                NotificationRepo(user=self.user).add(title=f'سفارش شماره {order.id} تحویل گرفته شد .',url=order.get_absolute_url(),body=f'سفارش  شماره {order.id} تحویل گرفته شد.',icon='alarm',profile_id=order.supplier.profile.pk,color='success',priority=1)
                
                return order

    def list_for_supplier_temppp(self,supplier_id):
        user=self.user
        supplier = SupplierRepo(user=user).get(supplier_id=supplier_id)
        if supplier.id == self.profile.id or True:
            order_packed=self.objects.filter(supplier=supplier).filter(status=OrderStatusEnum.PACKED)
            order_confirmed=self.objects.filter(supplier=supplier).filter(status=OrderStatusEnum.CONFIRMED)
            order_accepted=self.objects.filter(supplier=supplier).filter(status=OrderStatusEnum.ACCEPTED)
            order_packing=self.objects.filter(supplier=supplier).filter(status=OrderStatusEnum.PACKING)
            orders=[]
            for order in order_packing:
                orders.append({
                    'supplier': {
                        'id': order.supplier.id,
                        'name': order.supplier.name,
                        'get_absolute_url': order.supplier.get_absolute_url(),
                    },
                    'persian_order_date': order.persian_order_date(),
                    'persian_accept_date': order.persian_accept_date(),
                    'persian_pack_date': order.persian_pack_date(),
                    'status': order.status,
                    'ship_fee': order.ship_fee,
                    'total':order.total,
                    'lines_total':order.lines_total,
                    'id': order.id,
                    'can_pack':True,
                    'get_absolute_url':order.get_absolute_url(),

                })
            for order in order_accepted:
                orders.append({
                    'supplier': {
                        'id': order.supplier.id,
                        'name': order.supplier.name,
                        'get_absolute_url': order.supplier.get_absolute_url(),
                    },
                    'persian_order_date': order.persian_order_date(),
                    'persian_accept_date': order.persian_accept_date(),
                    'persian_pack_date': order.persian_pack_date(),
                    'status': order.status,
                    'ship_fee': order.ship_fee,
                    'total':order.total,
                    'lines_total':order.lines_total,
                    'id': order.id,
                    'can_pack':True,
                    'get_absolute_url':order.get_absolute_url(),

                })
            for order in order_confirmed:
                orders.append({
                    'supplier': {
                        'id': order.supplier.id,
                        'name': order.supplier.name,
                        'get_absolute_url': order.supplier.get_absolute_url(),
                    },
                    'persian_order_date': order.persian_order_date(),
                    'persian_accept_date': order.persian_accept_date(),
                    'persian_pack_date': order.persian_pack_date(),
                    'status': order.status,
                    'ship_fee': order.ship_fee,
                    'total':order.total,
                    'lines_total':order.lines_total,
                    'id': order.id,
                    'can_pack':True,
                    'get_absolute_url':order.get_absolute_url(),

                })
            for order in order_packed:
                orders.append({
                    'supplier': {
                        'id': order.supplier.id,
                        'name': order.supplier.name,
                        'get_absolute_url': order.supplier.get_absolute_url(),
                    },
                    'persian_order_date': order.persian_order_date(),
                    'persian_accept_date': order.persian_accept_date(),
                    'persian_pack_date': order.persian_pack_date(),
                    'status': order.status,
                    'ship_fee': order.ship_fee,
                    'total':order.total,
                    'lines_total':order.lines_total,
                    'id': order.id,
                    'can_pack':False,
                    'get_absolute_url':order.get_absolute_url(),

                })
            return orders[:DEFAULT_ORDER_LIST_FOR_SUPPLIER]
    
    def list_for_supplier(self,supplier_id):
        user=self.user
        supplier = SupplierRepo(user=user).get(supplier_id=supplier_id)
        orders=self.objects.filter(supplier=supplier)
        return orders

    def list_for_shipper(self, shipper_id=0):
        user=self.user
        shipper = ShipperRepo(user=self.user).me
        if shipper is None:
            return None
        if shipper is None:
            return None
        region_suppliers=SupplierRepo(user=user).get_by_region(region=shipper.region)
        
        orders_packed = self.objects.filter(supplier__in=region_suppliers).filter(status=OrderStatusEnum.PACKED).filter(no_ship=False)
        orders_shipped = self.objects.filter(status=OrderStatusEnum.SHIPPED).filter(shipper=shipper)
        orders = []
        for order in orders_packed:
            orders.append(order)

        for order in orders_shipped:
            orders.append(order)
        return orders[:DEFAULT_ORDER_LIST_FOR_SHIPPER]

    
    def list_for_customer(self,customer_id):
        customer = CustomerRepo(user=self.user).get(customer_id=customer_id)
        profile=self.profile
        if self.profile is None:
            return []
        if not (customer.profile == profile):
            return []

        orders= self.objects.filter(customer=customer).order_by('-order_date')[:DEFAULT_ORDER_LIST_FOR_USER]
        return orders

    def get(self, order_id,user=None):
        if user is None:
            user=self.user
        profile = self.profile
        
        order = self.objects.get(pk=order_id)
        if not (order.customer.profile==profile or self.user.has_perm('market.view_order') or order.supplier.profile==profile or (order.shipper and order.shipper.profile==profile) ) :
            return None
        
        # lines = OrderLineRepo(user=self.user).get_by_order(order_id=order_id)
        lines = OrderLineRepo(user=self.user).get_by_order(order_id=order_id)
        order.lines =lines 
        if order.customer.id == profile.id:
            order.lines =lines 
        if order.supplier.profile.id == profile.id:
            if order.status == OrderStatusEnum.CONFIRMED:
                order.accept_date = datetime.datetime.now()
                order.status = OrderStatusEnum.ACCEPTED
                order.save()
            if order is not None:
                order.lines = lines
                if not order.customer == profile:
                    order.customer=order.customer
                          
        return order

class CartRepo:
    def __init__(self,user=None):
        self.objects=CartLine.objects
        self.user=user
        self.profile=ProfileRepo(user=user).me
       
    def get_user_cart_for_api(self):
        user=self.user
        if user.is_authenticated:
            profile = ProfileRepo(user=self.user).me
            if profile is not None:                
                orders=[]
                cart_total=0
                cart_lines_total=0
                cart_lines = CartLine.objects.filter(profile=profile)
                shops = Shop.objects.filter(
                    id__in=cart_lines.values('shop_id'))
                for supplier in Supplier.objects.filter(id__in=shops.values('supplier_id')):
                    order = Order()
                    order.supplier = supplier
                    order.ship_fee = supplier.ship_fee

                    lines_total = 0
                    for line in cart_lines:
                        if line.shop.supplier == supplier:
                            lines_total = lines_total+(line.quantity*line.shop.price)
                    order.lines_total = lines_total
                    total = lines_total+supplier.ship_fee
                    order.total = total
                    cart_total=cart_total+total
                    cart_lines_total=cart_lines_total+lines_total
                    orders.append(order)
                return {'lines':cart_lines,'orders':orders,'total':cart_total,'lines_total':cart_lines_total}

    def get_by_customer(self,customer_id=0):
        if customer_id==0 :
            user=self.user
            customer_id=self.profile.id
    
        customer = CustomerRepo(user=self.user).get(customer_id=customer_id)
        if customer is not None:            
            cart_lines = self.objects.filter(customer=customer)
            if cart_lines is None or len(cart_lines)<1:
                return None
            orders=self.get_cart_orders(customer_id=customer_id)
            total=0
            for order in orders:
                total+=order.total
            cart = {'lines': cart_lines,'customer':customer, 'orders': orders,'total':total}            
            return cart
    
    def get_cart_orders(self,customer_id=0,no_ship=None):
        if no_ship is None:
            no_ship=False
        if customer_id ==0:
            customer=CustomerRepo(user=self.user).me
        else:
            customer=CustomerRepo(user=self.user).get(customer_id=customer_id)
        cart_lines = self.objects.filter(customer=customer)
        if len(cart_lines)==0:
            return None
        shops =ShopRepo(user=self.user).get_by_cart(cart_lines=cart_lines)
        orders=[]
        for supplier in Supplier.objects.filter(id__in=shops.values('supplier_id')):
            order = Order()
            order.supplier = supplier
            order.customer_id = customer_id
            if no_ship:
                order.ship_fee = 0
            else:
                order.ship_fee = supplier.ship_fee
            order.status = OrderStatusEnum.CONFIRMED
            order.description = ''
            order.address = ''
            order.no_ship = no_ship
            order.total=order.ship_fee
            order.lines=[]
            if order is not None:
                for cart_line in cart_lines:
                    if cart_line.shop.supplier == supplier:
                        order_line=OrderLine(order=order, product=cart_line.shop.product, quantity=cart_line.quantity,
                                    price=cart_line.shop.price, unit_name=cart_line.shop.unit_name)
                        order.lines.append(order_line)
                        order.total+=cart_line.shop.price*cart_line.quantity
                
                orders.append(order)
        
        return orders

    def submit(self, address, description=None,customer_id=None,no_ship=False,supplier_id=0):
        user=self.user
        if customer_id is None:
            customer=CustomerRepo(user=self.user).me
        else:
            customer = CustomerRepo(user=self.user).get(customer_id=customer_id)
            
        if customer is not None:
            cart_lines = self.objects.filter(customer=customer)
            shops = ShopRepo(user=self.user).get_by_cart(cart_lines=cart_lines)
            orders=[]
            if supplier_id==0:
                suppliers=Supplier.objects.filter(id__in=shops.values('supplier_id'))
            else:
                suppliers=[SupplierRepo(user=self.user).get(supplier_id=supplier_id)]
            for supplier in suppliers:
                order = Order()
                order.supplier_id = supplier.id
                order.customer = customer
                if no_ship:
                    order.ship_fee = 0
                else:
                    order.ship_fee = supplier.ship_fee
                order.status = OrderStatusEnum.CONFIRMED
                order.description = description
                order.address = address
                order.no_ship = no_ship
                order.order_date =  datetime.datetime.now()
                order.save()
                if order is not None:
                    orders.append(order)
                    for cart_line in cart_lines:
                        if cart_line.shop.supplier == supplier:
                            order_line=OrderLine(order=order, product=cart_line.shop.product,
                                quantity=cart_line.quantity,
                                price=cart_line.shop.price,
                                #product_name=cart_line.shop.product.name,
                                unit_name=cart_line.shop.unit_name)
                            order_line.save()
                            cart_line.delete()
                    # order=OrderRepo(user=self.user).get(order_id=order.pk)
                    # MyPusherChannel(user=self.user).submit(order_id=order.id,total=order.total(),supplier_id=order.supplier.id)
                    NotificationRepo(user=self.user).add(title='سفارش تایید شده',body=f'سفارش تایید شده به مبلغ {order.total()} تومان',url=order.get_absolute_url(),icon='alarm',profile_id=order.supplier.profile.pk,color='danger',priority=1)
                    ProfileTransactionRepo(user=self.user).add(
                        from_profile_id=order.supplier.id,
                        to_profile_id=order.customer.id,title=f'فاکتور شماره {order.id}',amount=order.total(),cash_type='',description='description')
                    
            
            return orders

    def get_count(self,user):
        if user.is_authenticated:
            profile = ProfileRepo(user=self.user).me
            if profile is not None:
                return len(CartLine.objects.filter(profile=profile))

    def remove_from_cart(self,shop_id):
        user=self.user
        if user.is_authenticated:
            customer = CustomerRepo(user=user).me
            if customer is None:
                return None
            try:
                shop = Shop.objects.get(pk=shop_id)
            except:
                pass
            if shop is not None:
                CartLine.objects.filter(customer_id=customer.id).filter(shop=shop).delete()
                return True
        return False

    def add_to_cart(self, shop_id, quantity,customer_id=None):
        user=self.user
        if customer_id is None:
            customer=CustomerRepo(user=self.user).me
        else:
            customer=CustomerRepo(user=self.user).get(customer_id=customer_id)
        if customer is None:    
            result={'result':'error','error_message':'حساب مشتری فعال نیست',}       
            return result
        try:
            shop = Shop.objects.get(pk=shop_id)
        except:
            return None
        self.objects.filter(customer_id=customer.id).filter(
            shop_id=shop_id).delete()
        cart_line = CartLine(customer=customer, shop=shop, quantity=quantity)
        cart_line.save()
        return cart_line

class ShopRepo:
    def remove(self,shop_id):
        self.objects.filter(pk=shop_id).delete()
    def get(self,shop_id):
        return self.objects.get(pk=shop_id)
    def get_by_cart(self,cart_lines):        
        return self.objects.filter(id__in=cart_lines.values('shop_id'))
    def get_by_supplier(self,supplier_id):
        return self.objects.filter(supplier_id=supplier_id)
    def __init__(self,user=None):
        self.objects=Shop.objects
        self.user=user
        self.profile=ProfileRepo(user=user).me
       
    def get_units_names(self):
        return ProductUnit.objects.order_by('priority')
    def list(self,product_id):
        if self.profile is not None:
            region_suppliers=SupplierRepo(user=self.user).get_by_region(region=self.profile.region)
            shops = self.objects.filter(supplier__in=region_suppliers).filter(product_id=product_id)
            return shops
        return None

    def add(self, product_id,  unit_name, price,available=None,supplier_id=None):
        user=self.user
        supplier = SupplierRepo(self.user).get(supplier_id=supplier_id)

        
        if price ==0:
            self.objects.filter(supplier=supplier).filter(
                product_id=product_id).filter(unit_name=unit_name).delete()
            return True

        else:
            if available is None:
                available = DEFAULT_AVAILABLE_PRODUCT_FOR_SHOP
            self.objects.filter(supplier=supplier).filter(
                product_id=product_id).filter(unit_name=unit_name).delete()
            shop = Shop(supplier=supplier, product_id=product_id,
                        available=available, unit_name=unit_name, price=price)
            shop.save()           
            return shop

class SupplierRepo:
    def get(self,supplier_id):
        try:
            return self.objects.get(pk=supplier_id)
        except:
            return None

    def __init__(self,user=None):
        self.objects=Supplier.objects
        self.user=user
        self.profile=ProfileRepo(user=self.user).me
        if self.profile is not None:
            try:
                self.me=self.objects.get(profile_id=self.profile.id)
            except:                
                self.me=None
        else:
            self.me=None
    def list(self):
        suppliers= Supplier.objects.order_by('priority')
        for supplier in suppliers:
            supplier.rest=ProfileTransactionRepo(user=self.user).rest(supplier.id)
        return suppliers
    
    def get_by_region(self,region=None):
        if region is not None:
            return Supplier.objects.filter(region=region)
        if self.profile is not None:
            return self.objects.filter(region=self.profile.region)
    

 
class BrandRepo:
    def brand(self,brand_id):
        try:
            return self.objects.get(pk=brand_id)
        except:
            return None

    def __init__(self,user=None):
        self.objects=Brand.objects
        self.user=user
        self.profile=ProfileRepo(user=self.user).me
        if self.profile is not None:
            try:
                self.me=self.objects.get(profile_id=self.profile.id)
            except:                
                self.me=None
        else:
            self.me=None
    def list(self):
        brands= self.objects.order_by('priority')
        return brands
    
 
class ShipperRepo:
    def get(self,shipper_id):
        try:
            return self.objects.get(pk=shipper_id)
        except:
            return None
    def __init__(self,user=None):
        self.user=user
        self.objects=Shipper.objects
        self.profile=ProfileRepo(user=self.user).me
        if self.profile is not None:
            try:
                self.me=self.objects.get(profile_id=self.profile.id)
            except:                
                self.me=None
        else:
            self.me=None
    def list(self):
        return Shipper.objects.order_by('priority')
    

class ShopRegionRepo:
    def __init__(self,user=None):
        self.user=user
        self.objects=ShopRegion.objects
    def list(self):
        return self.objects.all()

class CommentRepo:
    def __init__(self,object_type=None,user=None):
        if object_type=='Product':
            self.objects=Product.objects
        self.user=user
        self.profile=ProfileRepo(user=user).me
    def add(self,text,object_id):
        
        object_=self.objects.get(pk=object_id) or None
        my_comment=Comment.objects.create(profile=self.profile,text=text)
        my_comment.save()
        object_.comments.add(my_comment)
        return my_comment

    def delete(self,comment_id):
        try:
            comment=Comment.objects.get(pk=comment_id)
            if comment.profile==self.profile:
                comment.delete()
                return True
        except:
            pass
        return False
    def count(self,object_id):
        object_=self.objects.get(pk=object_id) or None
        if object_ is not None:
            try:
                comments_count=len(object_.comments.all())
                return comments_count
            except:
                pass
   
class WareHouseRepo:
    def get(self,ware_house_id):
        try:
            return self.objects.get(pk=ware_house_id)
        except:
            return None

    def __init__(self,user=None):
        self.objects=WareHouse.objects
        self.user=user  
   
class ProductRepo:
    # def top_products(self,category_id):
    #     category_repo=CategoryRepo(user=self.user)
        
    #     products=list(self.list(category_id=category_id).values('id','name'))
    #     for child in category_repo.list(parent_id=category_id):
    #         products+=(self.top_products(child.id))
    #     return products
    def __init__(self,user=None):
        self.objects=Product.objects
        self.user=user        
        self.profile=ProfileRepo(user=self.user).me
        self.customer=CustomerRepo(user=self.user).me
        self.supplier=SupplierRepo(user=self.user).me
    def list_by_supplier(self,supplier_id):
        shops=ShopRepo(user=self.user).get_by_supplier(supplier_id=supplier_id)
        products=self.objects.filter(pk__in=shops.values('product_id'))
        return products
   
    def my_list(self):
        
        my_list=CustomerRepo(user=self.user).me.favorites.all()
        products=self.objects.filter(pk__in=my_list.values('id'))
        return products
    def add_like(self,product_id):       
        product=self.objects.get(pk=product_id)         
        if self.customer is not None and product is not None:
            if self.is_my_favorite(product.pk):
                self.customer.favorites.remove(product)
                return False
            else :
                self.customer.favorites.add(product.pk)
                return True
    
    def is_my_favorite(self,product_id):
        if self.customer is not None:
            products=self.customer.favorites.filter(pk=product_id)
            if products is None or len(products)<1:
                return False
            else:
                return True
    def comments(self,product_id):
        return ProductComment.objects.filter(product_id=product_id).order_by('-id')
    def add_comment(self,product_id,comment):
        profile=ProfileRepo(user=self.user).me
        if profile is not None:
            product_comment=ProductComment()
            product_comment.profile=profile
            product_comment.product=self.objects.get(pk=product_id)
            product_comment.comment=comment;
            product_comment.save()
            return product_comment
    def del_comment(self,comment_id):
        comment=ProductComment.objects.get(pk=comment_id)
        if self.profile.id==comment.profile.id:
            comment.delete()
            return True
        return False

    def search(self,search_for):
        user=self.user
        region=None
        if user is not None:
            profile=ProfileRepo(user=self.user).me        
            if profile is not None:
                region=profile.region

        products=self.objects.filter(name__contains=search_for)
        for product in products:
            product.price=Shop.objects.filter(product_id=product.id).filter(supplier__in=Supplier.objects.filter(region=region)).aggregate(Min('price'))['price__min']
        categories=Category.objects.filter(name__contains=search_for)
        suppliers=Supplier.objects.filter(title__contains=search_for)
        return {'products':products,'categories':categories,'suppliers':suppliers}
    def related(self,product_id):
        product=self.get(product_id=product_id)
        user=self.user
        region=None
        if user is not None:
            profile=ProfileRepo(user=self.user).me     
            if profile is not None:
                region=profile.region
        products=product.related.all()
        for product in products:
            product.price=Shop.objects.filter(product_id=product.id).filter(supplier__in=Supplier.objects.filter(region=region)).aggregate(Min('price'))['price__min']
        return products
    
    def edit_product(self,id,name,unit_name,image,short_description,description):
        origin_product=self.objects.filter(pk=id)
        if len(origin_product)==1:
            origin_product=origin_product[0]
            user=self.user
            if user.has_perm('leohypermarket.change_product') or origin_product.adder==self.profile:
                origin_product.name=name
                if image is not None and image:
                    origin_product.image=image
                origin_product.unit_name=unit_name
                origin_product.description=description
                origin_product.short_description=short_description
                origin_product.save()
                return True
        return False
    
    def delete_product(self,product_id):
        user=self.user
        origin_product=self.objects.filter(pk=product_id)
        if len(origin_product)==1:
            origin_product=origin_product[0]
            user=self.profile.user
            if user.has_perm('leohypermarket.delete_product') or origin_product.adder==self.profile:
                origin_product.delete()
                return True
        return False

    def list_all(self):
        user=self.user
        return self.objects.all().order_by('priority')

    def list_for_home(self):
        user=self.user
        return self.objects.filter(for_home=True).order_by('priority')

    def list(self,category_id=0):
        user=self.user
        region=None
        if user is not None:
            profile=ProfileRepo(user=self.user).me          
            if profile is not None:
                region=profile.region
            
        if category_id == 0:
            return []
        products=self.objects.filter(category_id=category_id).order_by('priority')
        for product in products:
            product.price=Shop.objects.filter(product_id=product.id).filter(supplier__in=Supplier.objects.filter(region=region)).aggregate(Min('price'))['price__min']
        return products


    def get(self,product_id):
        user=self.user
        region=None
        if user is not None:
            profile=ProfileRepo(user=self.user).me            
            if profile is not None:
                region=profile.region
        try:
            product = self.objects.get(pk=product_id)
            product.category=CategoryRepo(user=user).get(category_id=product.category_id)
            product.price=Shop.objects.filter(product_id=product.id).filter(supplier__in=Supplier.objects.filter(region=region)).aggregate(Min('price'))['price__min']
        except ObjectDoesNotExist:
            product = None
        return product

    def add(self, name,category_id,unit_name=None):
        user=self.user
        product = Product(name=name, category_id=category_id)
        default_unit=ProductUnitRepo(user=self.user).get_by_name(name=unit_name) if ProductUnitRepo(user=self.user).get_by_name(name=unit_name) is not None else ProductUnitRepo(user=self.user).get_default()
        if user.has_perm(f'{APP_NAME}.add_product'):
            if category_id == 0:
                return None
            else:
                product.category = CategoryRepo(user=user).get(category_id=category_id)
                product.adder = ProfileRepo(user=self.user).me
                product.save()
                product.unit_names.add(default_unit)
                product.save()
            return product
        return None

    def remove(self, product):
        user=self.user
        return None

class CategoryRepo:
    objects=Category.objects
    def __init__(self,user=None):
        self.user=user        
        self.profile=ProfileRepo(user=self.user).me
        
    def list_all(self):
        return self.objects.all().order_by('priority')
    def list_master(self):
        return self.objects.all().filter(parent=None).order_by('priority')

    def get(self,category_id):
        user=self.user
        try:
            category = self.objects.get(pk=category_id)
            
        except ObjectDoesNotExist:
            category = None
        return category

    def list(self,parent_id):
        user=self.user
        if parent_id == 0:
            return self.objects.filter(parent=None).order_by('priority')
        return self.objects.filter(parent_id=parent_id).order_by('priority')

    def add(self, name, parent_id=None):
        category = Category(name=name, parent_id=parent_id)
        if self.user.has_perm(f'{APP_NAME}.add_category'):
            if parent_id is not None:
                category.parent = self.objects.get(pk=category.parent_id)
            category.save()
            return category
        return None

    def remove(self,user, category):
        return None

    def update(self,user, category):
        return None


  

class OrderLineRepo:
    def __init__(self,user):
        self.objects=OrderLine.objects
        self.user=user        
        self.profile=ProfileRepo(user=self.user).me
    def get_by_order(self,order_id):
        return self.objects.filter(order_id=order_id)