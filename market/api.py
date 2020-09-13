from django.urls import path
from rest_framework.views import APIView
from .forms import *
from .serializers import *
from .repo import *
from app.forms import AddCommentForm
from app.serializers import CommentSerializer
from django.http import JsonResponse
from app.settings import SITE_URL
import json
def getContext(request):
    context={}
    context['request']=request
    context['SITE_URL']=SITE_URL
    return context


     
def auth_user(request):
    if request.user.is_authenticated:
        return request.user
    token = str(request.headers.get('token'))
    try:
        token = Token.objects.get(key=token)
        if token is not None:
            user = token.user
            if user is not None:
                return user
    except:
        pass
    try:
        username = str(request.data['username'])
        password = str(request.data['password'])
        user = ProfileRepo(user=request.user).authenticate_user(
            username=username, password=password)
        if user is not None:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return user
    except:
        pass
    return None


class OrderApi(APIView):
     #serializer_class = OrderSerializer

    def post(self, request):
        request.user=auth_user(request)
        user=request.user
        if user is None:
            return JsonResponse({'message': 'auth problem'}) 
        action=str(request.headers.get('action'))
        if action=='MY_ORDERS':
            return self.my_orders(request)        
        if action=='DETAIL':
            return self.detail(request)        
    def my_orders(self, request):        
        user=request.user                    
        context = {'request': request}
        orders=OrderRepo().list_for_user(user)
        orders_s=OrderSerializer(orders,many=True,context=context).data
        return JsonResponse({'orders':orders_s})        

    def detail(self,request):
        order_id=request.data['id']
        order=OrderRepo().get(request.user,order_id)
        lines=order.lines
        lines_s=OrderLineSerializer(lines,many=True,context={'request':request}).data
        order_s=OrderSerializer(order,context={'request':request}).data
        order_s['lines']=lines_s
        return JsonResponse({'order':order_s})



class Basic_api(APIView):
    def delete_comment(self,request,*args, **kwargs):
        user=request.user
        if request.method=='POST' and user and user.is_authenticated:
            delete_comment_form=DeleteCommentForm(request.POST)
            if delete_comment_form.is_valid():
                comment_id=delete_comment_form.cleaned_data['comment_id']                
                comment_repo=CommentRepo(user=user)
                done=comment_repo.delete(comment_id=comment_id)
                return JsonResponse({'done':done})


    def add_comment(self,request):
        user=request.user
        if request.method=='POST':
            add_comment_form=AddCommentForm(request.POST)
            if add_comment_form.is_valid():
                object_id=add_comment_form.cleaned_data['object_id']
                text=add_comment_form.cleaned_data['text']
                object_type=add_comment_form.cleaned_data['object_type']
                comment_repo=CommentRepo(user=request.user,object_type=object_type)
                my_comment=comment_repo.add(object_id=object_id,text=text)
                comments_count=comment_repo.count(object_id=object_id)
                my_comment_s=CommentSerializer(my_comment).data
                return JsonResponse({'my_comment':my_comment_s,'comments_count':comments_count})

                return JsonResponse({'result':'2'})
                    
            return JsonResponse({'result':'3'})
        return JsonResponse({'result':'4'}) 
class ProductApi(APIView):
    def add_comment(self,request):
        user=request.user
        if request.method=='POST':
            add_product_comment_form=AddProductCommentForm(request.POST)
            if add_product_comment_form.is_valid():
                product_id=add_product_comment_form.cleaned_data['product_id']
                comment=add_product_comment_form.cleaned_data['comment']
                product_comment=ProductRepo(user=request.user).add_comment(product_id=product_id,comment=comment)
                if product_comment is not None:
                    product_comments=ProductRepo(user=user).comments(product_id=product_id)
                    product_comments=ProductCommentSerializer(product_comments,many=True).data
                    return JsonResponse({'product_comments':product_comments})
                    
                return JsonResponse({'result':'2'})
                    
            return JsonResponse({'result':'3'})
        return JsonResponse({'result':'4'}) 
    def del_comment(self,request):
        user=request.user
        if request.method=='POST':
            del_product_comment_form=DeleteProductCommentForm(request.POST)
            if del_product_comment_form.is_valid():
                comment_id=del_product_comment_form.cleaned_data['comment_id']
                done=ProductRepo(user=request.user).del_comment(comment_id=comment_id)
                if done is not None and done:
                    return JsonResponse({'result':'1'})
                    
                return JsonResponse({'result':'2'})
                    
            return JsonResponse({'result':'3'})
        return JsonResponse({'result':'4'}) 
    def list_all(self,request):
        user=request.user
        request.user=auth_user(request)
        products = ProductRepo(user=user).list_all()
        context =getContext(request)
        products_s = ProductSerializer(products, many=True, context=context).data
        return JsonResponse({'products':products_s},safe=False)

    def detail(self,request,product_id):
        pass

    def list(self, request, format=None,category_id=0):
        user=request.user
        request.user=auth_user(request)
        products = ProductRepo(user=user).list(category_id=category_id)
        context = {'request': request}
        serializer = ProductSerializer(products, many=True, context=context)
        return JsonResponse({'products':serializer.data},safe=False)

    # def post(self, request, format=None):
    #     context = {'request': request}
    #     serializer = ProductSerializer(data=request.data, context=context)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    #     return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def post(self, request, product_id, format=None):
        request.user=auth_user(request)
        user=request.user
        product = ProductRepo(user=user).get(product_id=product_id)
        context = {'request': request}
        serializer = ProductSerializer(instanse=product, context=context)
        product_s = serializer.data
        category_s= CategorySerializer(product.category, context=context).data
        shops_s=ShopSerializer(ShopRepo(user=user).list(user,product_id=product.id),many=True,context=context).data
        related_s=ProductSerializer(ProductRepo(user=user).related(product),many=True,context=context).data
        return JsonResponse({'product':product_s,'category':category_s,'shops':shops_s,'products':related_s})


class CategoryList(APIView):
   

    def get(self, request, format=None):
        user=request.user
        categories = CategoryRepo(user=user).list_all(user)
        context = {'request': request}
        serializer = CategorySerializer(categories, many=True, context=context)
        data = serializer.data

        return JsonResponse({'categories':data}, safe=False)

    def post(self, request, format=None):
        context = {'request': request}
        serializer = CategorySerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopApi(APIView):
    def add_category(self,request):
        user=request.user
        if request.method=='POST':
            add_category_form=AddCategoryForm(request.POST)
            if add_category_form.is_valid():
                parent_id=add_category_form.cleaned_data['parent_id']
                name=add_category_form.cleaned_data['name']
                category=CategoryRepo(user=request.user).add(name=name,parent_id=parent_id)
                context={}
                if category is not None:
                    context['done']=SUCCEED
                
                categories_s=CategorySerializer(CategoryRepo(user=user).list(parent_id=parent_id),many=True).data
                context['categories']=categories_s
                return JsonResponse(context)
    
    
    def add_product(self,request):        
        user=request.user
        if request.method=='POST':
            add_product_form=AddProductForm(request.POST)
            if add_product_form.is_valid():
                category_id= add_product_form.cleaned_data['category_id']
                name=add_product_form.cleaned_data['name']
                product=ProductRepo(user=user).add(name=name,category_id=category_id)
                context={}
                if product is not None:
                    context['done']=SUCCEED
                products_s=ProductSerializer(ProductRepo(user=user).list(category_id=category_id),many=True).data
                context['products']=products_s
                return JsonResponse(context)
       
    def get_shop(self,request,parent_id=0):
        context={}
        user=request.user
        category_repo=CategoryRepo(user=user)

        
        categories=category_repo.list(parent_id=parent_id)
        if len(categories)>0:
            categories_s=CategorySerializer(categories,many=True).data
            context['categories']=categories_s
        else:
            context['categories']=''

        products=ProductRepo(user=user).list(category_id=parent_id)
        if len(products)>0:
            products_s=ProductSerializer(products,many=True).data
            context['products']=products_s
        else:
            context['products']=''
        parent=category_repo.get(category_id=parent_id)
        if parent is not None:
            parent_s=CategorySerializer(parent).data
            context['parent']=parent_s
        else:
            context['parent']=''
        can_add_category=EmployeeRepo(user=user).me() is not None and len(products)==0
        can_add_product=(EmployeeRepo(user=user).me() is not None or SupplierRepo(user=user).me() is not None) and len(categories)==0
        context['can_add_category']='1' if can_add_category else '0'
        context['can_add_product']='1' if can_add_product else '0'



        can_edit_category=EmployeeRepo(user=user).me() is not None
        can_edit_product=EmployeeRepo(user=user).me() is not None 
        context['can_edit_category']='1' if can_edit_category else '0'
        context['can_edit_product']='1' if can_edit_product else '0'
        if parent is not None :
            context['breadcrumb']=parent.get_breadcrumb()
        return JsonResponse(context)
    def add_shop(self,request):
        user=request.user
        if request.method=='POST':
            add_shop_form=AddShopForm(request.POST)
            if add_shop_form.is_valid():
                # input('add_shop_form.is_valid')
                price=add_shop_form.cleaned_data['price']
                supplier_id=add_shop_form.cleaned_data['supplier_id']
                product_id=add_shop_form.cleaned_data['product_id']
                unit_name=add_shop_form.cleaned_data['unit_name']
                available=add_shop_form.cleaned_data['available']
                shop=ShopRepo(user=request.user).add(product_id=product_id,price=price,supplier_id=supplier_id,unit_name=unit_name,available=available)
                if shop is not None:
                    shops=ShopRepo(user=user).list(product_id=product_id)
                    shop_s=ShopSerializer(shops,many=True).data
                    return JsonResponse({'shops':shop_s})                    
                return JsonResponse({'result':'2'})                    
            return JsonResponse({'result':'3'})
        return JsonResponse({'result':'4'})


class CategoryDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
  

    def get_object(self, category_id):
        try:
            return CategoryRepo(user=user).get(category_id=category_id)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_id, format=None):
        category = CategoryRepo(user=user).get(category_id=category_id)
        context = {'request': request}
        serializer = CategorySerializer(category, context=context)
        data = serializer.data
        if category.parent is not None:
            data['parent'] = CategorySerializer(
                category.parent, context=context).data
        products = ProductRepo(user=user).list(category_id=category.id)
        data['products'] = ProductSerializer(
            products, many=True, context=context).data
        return JsonResponse(data, safe=False)

    # def put(self, request, category_id, format=None):
    #     category = self.get_object(category_id=category_id)
    #     serializer = CategorySerializer(category, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, category_id, format=None):
    #     category = self.get_object(category_id=category_id)
    #     CategoryRepo(user=user).de
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class CartApi(APIView):

    def add_to_cart(self,request):
        user=request.user
        profile=ProfileRepo(user=user).me
        if request.method=='POST':
            add_to_cart_form=AddToCartForm(request.POST)
            if add_to_cart_form.is_valid():
                customer_id=add_to_cart_form.cleaned_data['customer_id']                
                customer= CustomerRepo(user=user).get(customer_id=customer_id)
                if customer is None:
                    profile_name=profile.name if profile is not None else ''
                    return JsonResponse({'profile_name':profile_name,'error_message':'حساب مشتری نادرست'})
                shop_id=add_to_cart_form.cleaned_data['shop_id']
                quantity=add_to_cart_form.cleaned_data['quantity']
                if quantity is None:
                    quantity=1
                cart_line=CartRepo(user=request.user).add_to_cart(shop_id=shop_id,quantity=quantity,customer_id=customer_id)
                if cart_line is not None:
                    return JsonResponse({'result':'1'})
                    
                return JsonResponse({'result':'2'})
                    
            return JsonResponse({'result':'3'})
        return JsonResponse({'result':'4'})
        



    MY_ORDERS='MY_ORDERS'
    DETAIL='DETAIL'
    MY_CART='MY_CART'
    REMOVE_FROM_CART='REMOVE_FROM_CART'
    ADD_TO_CART='ADD_TO_CART'
    SUBMIT_CART='SUBMIT_CART'

    def post(self, request, format=None):
        request.user=auth_user(request)
        user=request.user
        if user is None:
            return JsonResponse({'message': 'auth problem'}) 
        action=str(request.headers.get('action'))
        if action==self.MY_CART:
            return self.my_cart(request)
        if action==self.REMOVE_FROM_CART:
            return self.remove_from_cart(request)
        if action==self.ADD_TO_CART:
            return self.add_to_cart(request)
        if action==self.SUBMIT_CART:
            return self.submit_cart(request)
        return JsonResponse({'message': 'no action'})
    def my_cart(self,request):
        user=request.user
        cart=CartRepo().get_user_cart_for_api(user)
        context = {'request': request}
        cart_s=CartLineSerializer(cart['lines'],many=True,context=context).data
        orders_s=OrderSerializer(cart['orders'],many=True,context=context).data
        return JsonResponse({'cartLines':cart_s,'orders':orders_s,'total':int(cart['total']),'lines_total':int(cart['lines_total'])})
    
    def submit_cart(self,request):
        description=str(request.data['description'])
        address=str(request.data['address'])
        orders=CartRepo().submit(request.user,address,description)
        context = {'request': request}
        orders_s=OrderSerializer(orders,many=True,context=context).data
        return JsonResponse({'orders':orders_s})

    def remove_from_cart(self,request):
        id=int(request.data['id'])
        done=CartRepo().remove_from_cart(request.user,id)
        if not done:
            return JsonResponse({'message':str(done)})
        #return self.my_cart(request)
        cart=CartRepo().get_user_cart_for_api(request.user)
        context = {'request': request}
        cart_s=CartLineSerializer(cart,many=True,context=context).data
        return JsonResponse({'cartLines':cart_s,'message':str(done)})

class SyncApi(APIView):
    def post(self,request):
        user=request.user
        context = {'request': request}
        if not request.user.is_authenticated:
            request.user=auth_user(request)

        categories = CategoryRepo(user=user).list_all()
        suppliers=SupplierRepo().list()
        shippers=ShipperRepo().list()
        token = str(Token.objects.get(user=request.user))
        # .values('first_name','last_name','image','mobile','email')
        profile=ProfileRepo(user=request.user).get_by_user()
        addresses=ProfileRepo(user=request.user).get_addresses(profile.user)
        productRepo=ProductRepo(user=user)
       
        profile_s = ProfileSerializer(profile, context=context).data
        categories_s = CategorySerializer(categories,many=True, context=context).data
        beams_s=BeamNotificationSerializer(ProfileRepo(user=request.user).my_beams(profile),many=True,context=context).data
        suppliers_s = SupplierSerializer(suppliers,many=True, context=context).data
        shippers_s = ShipperSerializer(shippers,many=True, context=context).data   
        addresses_s=DeliveryAddressSerializer(addresses,many=True,context=context).data  
        shopRegions_s = ShopRegionSerializer(ShopRegionRepo().list(),many=True, context=context).data 
        fav_products_s=ProductBriefSerialize(ProfileRepo(user=request.user).my_favorites(profile),many=True,context=context).data     
        channels_s=ChannelSerializer(ProfileRepo(user=request.user).my_channels(profile),many=True,context=context).data
        return JsonResponse(
            {
                'channels':channels_s,
                'profile':profile_s,
                'token':token,
                'beams':beams_s,
                'products':fav_products_s,
                'addresses':addresses_s,
                'categories':categories_s,
                'shippers':shippers_s,
                'suppliers':suppliers_s,
                'shopRegions':shopRegions_s
            }
        )           


    def get(self, request, format=None):
        user=request.user
        categories = CategoryRepo(user=user).list_all()
        suppliers=SupplierRepo().list()
        shippers=ShipperRepo().list()

        context = {'request': request}
        categories_s = CategorySerializer(categories,many=True, context=context).data
        suppliers_s = SupplierSerializer(suppliers,many=True, context=context).data
        shippers_s = ShipperSerializer(shippers,many=True, context=context).data        
        shopRegions_s = ShopRegionSerializer(ShopRegionRepo().list(),many=True, context=context).data        
        return JsonResponse({'categories':categories_s,'shippers':shippers_s,'suppliers':suppliers_s,'shopRegions':shopRegions_s}, safe=False)

class SearchApi(APIView):
    def post(self,request):
        request.user=auth_user(request)
        search_text=str(request.data['name'])
        context = {'request': request}
        data=ProductRepo(user=user).search(search_text)
        products=ProductSerializer(data['products'],many=True,context=context).data
        suppliers=SupplierSerializer(data['suppliers'],many=True,context=context).data
        categories=CategorySerializer(data['categories'],many=True,context=context).data
        return JsonResponse({'products':products,'categories':categories,'suppliers':suppliers})




urlpatterns = [
    path('delete_comment/',Basic_api().delete_comment,name='delete_comment'),
    path('add_comment/',Basic_api().add_comment,name='add_comment'),
    path('cart/add/',CartApi().add_to_cart,name='api_add_to_cart'),
    path('shop/add/',ShopApi().add_shop,name='api_add_shop'),
    path('shop/<int:parent_id>/',ShopApi().get_shop,name='api_get_shop'),
    path('category/add/',ShopApi().add_category,name='api_add_category'),
    path('product/add/',ShopApi().add_product,name='api_add_product'),
    path('product_comment/add/',ProductApi().add_comment,name='api_add_product_comment'),
    path('product_comment/del/',ProductApi().del_comment,name='api_del_product_comment'),

    # must be rewritten
    path('categories/', CategoryList.as_view()),
    path('categories/<int:category_id>/', CategoryDetail.as_view()),
    path('products/', ProductApi().list_all),
    path('product/<int:product_id>/', ProductApi().detail),
    path('products/<int:category_id>/', ProductApi().list),
    
    
    path('order/', OrderApi.as_view()),
    path('sync/', SyncApi.as_view()),
    path('cart/',CartApi.as_view()),
    path('search/',SearchApi.as_view()),
    
]
