import pusher
import json
from .forms import *
from django.http import HttpResponse,JsonResponse,Http404
from django.shortcuts import render,redirect,reverse
from django.views import View
from app.excel import ReportWorkBook,ReportSheet
from app.settings import *
from app.views import getContext as app_getContext
from .repo import *
from .serializers import *
from app.serializers import CommentSerializer
from app.forms import UploadProfileImageForm,EditProfileForm,ChangeProfileForm
import datetime
if PUSHER_IS_ENABLE:
    from leopusher.models import PusherChannelNameEnum

TEMPLATE_ROOT='market/'
def getContext(request):
    
    user=request.user
    context=app_getContext(request)
    # context['current_profile']=ProfileRepo(user=user).get_by_user(user=user)
    # context['current_shipper']=ShipperRepo(user=user).get_by_user(user=user)
    # context['current_supplier']=SupplierRepo(user=user).get_by_user(user=user)
    # context['current_customer']=CustomerRepo(user=user).get_by_user(user=user)
    # context['current_employee']=EmployeeRepo(user=user).get_by_user(user=user)

    
    active_shipper=ShipperRepo(user=user).me
    active_supplier=SupplierRepo(user=user).me
    active_customer=CustomerRepo(user=user).me
    active_employee=EmployeeRepo(user=user).me
    
 

    context['master_categories']=CategoryRepo(user=user).list_master()
    context['active_shipper']=active_shipper
    context['active_supplier']=active_supplier
    context['active_customer']=active_customer
    context['active_employee']=active_employee





    if active_customer is not None:
        # my_channels=active_customer.channels.all()
        # my_channels_s=MyChannelSerializer(my_channels,many=True).data
        # context['my_channels_s']=json.dumps(my_channels_s)
        cart=CartRepo(user=user).get_by_customer(customer_id=active_customer.pk)
        context['cart']=cart 
        my_list=active_customer.favorites.all()
        context['my_list']=my_list       
    elif active_supplier is not None:
        # my_channels=active_supplier.channels.all()
        # my_channels_s=MyChannelSerializer(my_channels,many=True).data
        # context['my_channels_s']=json.dumps(my_channels_s)
        pass
    elif active_shipper is not None:
        # my_channels=active_shipper.channels.all()
        # my_channels_s=MyChannelSerializer(my_channels,many=True).data
        # context['my_channels_s']=json.dumps(my_channels_s)
        pass
    elif active_employee is not None:
        # my_channels=active_employee.channels.all()
        # my_channels_s=MyChannelSerializer(my_channels,many=True).data
        # context['my_channels_s']=json.dumps(my_channels_s)
        pass
    else:
        pass
    my_channels_s=[]
    context['my_channels_s']=json.dumps(my_channels_s)
    
    context['search_form']=SearchForm()
    parent_categories=CategoryRepo(user=user).list_master()
    context['parent_categories']=parent_categories
    return context


class ManagerView(View):
    def manager(self,request):
        context=getContext(request=request)
        context['send_pusher_beam_form']=pusher_forms.SendPusherBeamForm()
        context['send_pusher_channel_form']=pusher_forms.SendPusherChannelForm()
        context['channel_names']=PusherChannelNameEnum.values
        return render(request,TEMPLATE_ROOT+'manager.html',context)
  

class ShopView(View):
    def list_vue(self,request,*args,**kwargs):
        if 'parent_id' in kwargs:
            parent_id= kwargs.get("parent_id")
        else:
            parent_id=0
        context=getContext(request=request)
        user=request.user
        category_repo=CategoryRepo(user=user)

        
        categories=category_repo.list(parent_id=parent_id)
        if len(categories)>0:
            categories_s=CategorySerializer(categories,many=True).data
            context['categories']=json.dumps(categories_s)
        else:
            context['categories']='[]'

        products=ProductRepo(user=user).list(category_id=parent_id)
        if len(products)>0:
            products_s=ProductSerializer(products,many=True).data
            context['products']=json.dumps(products_s)
        else:
            context['products']='[]'
        parent=category_repo.get(category_id=parent_id)
        if parent is not None:
            parent_s=CategorySerializer(parent).data
            context['parent']=json.dumps(parent_s)
        else:
            context['parent']='{}'

        can_add_category=EmployeeRepo(user=user).me is not None
        can_add_product=EmployeeRepo(user=user).me is not None or SupplierRepo(user=user).me is not None
        can_edit_category=EmployeeRepo(user=user).me is not None
        can_edit_product=EmployeeRepo(user=user).me is not None 
        context['can_add_category']='1' if can_add_category else '0'
        context['can_add_product']='1' if can_add_product else '0'
        context['can_edit_category']='1' if can_edit_category else '0'
        context['can_edit_product']='1' if can_edit_product else '0'
        if can_add_category:
            add_category_form=AddCategoryForm()
            context['add_category_form']=add_category_form
        if can_add_product and not parent_id==0:
            add_product_form=AddProductForm()
            context['add_product_form']=add_product_form
        return render(request=request,template_name=TEMPLATE_ROOT+'list_vue.html',context=context)
    
    
    def list(self,request,*args,**kwargs):
        user=request.user
        if 'parent_id' in kwargs:
            parent_id= kwargs.get("parent_id")
        else:
            parent_id=0
        context=getContext(request=request)
        category_repo=CategoryRepo(user=user)
        product_repo=ProductRepo(user=user)
        categories=category_repo.list(parent_id=parent_id)
        if parent_id==0:            
            products=product_repo.list_for_home()
        else:            
            products=product_repo.list(category_id=parent_id)

        # categories.top_products_length=len(categories.top_products())
        # categories.top_products()=categories.top_products()[:5]
        # for category in categories:
        #     # products=product_repo.top_products(category.id)
        #     # category.top_products=products[:5]
        #     products=
        #     category.count=len(products)
        context['categories']=categories
        # products=product_repo.list_all()
        context['products']=products
        brands=BrandRepo(user=user).list()
        context['brands']=brands
        parent=category_repo.get(category_id=parent_id)
        # print(len(parent.sub_products()))
        # print(parent.sub_products())
        context['parent']=parent
        if parent is not None : context['breadcrumb']=parent.get_breadcrumb()

        can_add_category=(len(products)==0) and (user.has_perm('market.add_category'))
        can_add_product=(len(categories)==0) and (user.has_perm('market.add_product'))
        can_edit_category=SupplierRepo(user=user).me is not None
        can_edit_product=SupplierRepo(user=user).me is not None 

        context['can_add_category']=can_add_category
        context['can_add_product']=can_add_product
        context['can_edit_category']=can_edit_category
        context['can_edit_product']=can_edit_product
        if can_add_category:
            add_category_form=AddCategoryForm()
            context['add_category_form']=add_category_form
        if can_add_product and not parent_id==0:
            add_product_form=AddProductForm()
            context['add_product_form']=add_product_form
            unit_names=ProductUnitRepo(user=user).list()
            context['unit_names']=unit_names
        # return render(request=request,template_name=TEMPLATE_ROOT+'list.html',context=context)
    
        return render(request=request,template_name='one-tech/shop.html',context=context)
    def my_list(self,request,*args,**kwargs):
        user=request.user
        if 'parent_id' in kwargs:
            parent_id= kwargs.get("parent_id")
        else:
            parent_id=0
        context=getContext(request=request)
        category_repo=CategoryRepo(user=user)
        product_repo=ProductRepo(user=user)
        categories=category_repo.list(parent_id=parent_id)
        if parent_id==0:            
            products=product_repo.my_list()
        else:            
            products=product_repo.my_list()

        # categories.top_products_length=len(categories.top_products())
        # categories.top_products()=categories.top_products()[:5]
        # for category in categories:
        #     # products=product_repo.top_products(category.id)
        #     # category.top_products=products[:5]
        #     products=
        #     category.count=len(products)
        context['categories']=categories
        # products=product_repo.list_all()
        context['products']=products
        brands=BrandRepo(user=user).list()
        context['brands']=brands
        parent=category_repo.get(category_id=parent_id)
        # print(len(parent.sub_products()))
        # print(parent.sub_products())
        context['parent']=parent
        if parent is not None : context['breadcrumb']=parent.get_breadcrumb()

        can_add_category=(len(products)==0) and (user.has_perm('market.add_category'))
        can_add_product=(len(categories)==0) and (user.has_perm('market.add_product'))
        can_edit_category=SupplierRepo(user=user).me is not None
        can_edit_product=SupplierRepo(user=user).me is not None 

        context['can_add_category']=can_add_category
        context['can_add_product']=can_add_product
        context['can_edit_category']=can_edit_category
        context['can_edit_product']=can_edit_product
        if can_add_category:
            add_category_form=AddCategoryForm()
            context['add_category_form']=add_category_form
        if can_add_product and not parent_id==0:
            add_product_form=AddProductForm()
            context['add_product_form']=add_product_form
        unit_names=ProductUnitRepo(user=user).list()
        context['unit_names']=unit_names
        # return render(request=request,template_name=TEMPLATE_ROOT+'list.html',context=context)
    
        return render(request=request,template_name='one-tech/shop.html',context=context)
    
    
    def remove_shop(self,request):
        user=request.user
        if request.method=='POST':
            remove_shop_form=RemoveShopForm(request.POST)
            if remove_shop_form.is_valid():
                shop_id=remove_shop_form.cleaned_data['shop_id']
                supplier_id=ShopRepo(user=user).get(shop_id=shop_id).supplier.id
                ShopRepo(user=request.user).remove(shop_id=shop_id)
                if supplier_id is not None:
                    return redirect(reverse('market:supplier',kwargs={'supplier_id':supplier_id}))
    
    
    def add_shop(self,request):
        if request.method=='POST':
            add_shop_form=AddShopForm(request.POST)
            if add_shop_form.is_valid():
                price=add_shop_form.cleaned_data['price']
                supplier_id=add_shop_form.cleaned_data['supplier_id']
                product_id=add_shop_form.cleaned_data['product_id']
                unit_name=add_shop_form.cleaned_data['unit_name']
                available=add_shop_form.cleaned_data['available']
                shop=ShopRepo(user=request.user).add(product_id=product_id,price=price,supplier_id=supplier_id,unit_name=unit_name,available=available)
                if shop is not None:
                    return redirect(shop.product.get_absolute_ur())
    def add_category(self,request):
        if request.method=='POST':
            add_category_form=AddCategoryForm(request.POST)
            if add_category_form.is_valid():
                parent_id=add_category_form.cleaned_data['parent_id']
                name=add_category_form.cleaned_data['name']
                category=CategoryRepo(user=request.user).add(name=name,parent_id=parent_id)
                if parent_id is None:
                    parent_id=0
                return redirect(reverse('market:list',kwargs={'parent_id':parent_id}))
    def add_product(self,request):
        if request.method=='POST':
            add_product_form=AddProductForm(request.POST)
            if add_product_form.is_valid():
                unit_name= add_product_form.cleaned_data['unit_name']
                category_id= add_product_form.cleaned_data['category_id']
                name=add_product_form.cleaned_data['name']
                product=ProductRepo(user=request.user).add(name=name,unit_name=unit_name,category_id=category_id)
                return redirect(reverse('market:list',kwargs={'parent_id':category_id}))
    def brand(self,request,brand_id,*args, **kwargs):
        user=request.user
        
        context=getContext(request=request)
        
        product_repo=ProductRepo(user=user)
        products=product_repo.list_by_brand(brand_id=brand_id)

        context['products']=products
        brands=BrandRepo(user=user).list()
        context['brands']=brands
        brand=BrandRepo(user=user).brand(brand_id=brand_id)
        
        context['parent']=brand
        return render(request=request,template_name='one-tech/shop.html',context=context)
    

class DownloadView(View):
    def get(self,request,*args,**kwargs):
        if 'supplier_id' in kwargs:
            supplier_id= kwargs.get("supplier_id") 
            return DownloadView().get_list_supplier(request=request,supplier_id=supplier_id)
    def get_list_xlsx(self,request):
        user=request.user
        products_s=ProductSerializer(ProductRepo(user=user).list_all(),many=True,context={'request':request}).data
        categories_s=CategorySerializer(CategoryRepo(user=user).list_all(),many=True,context={'request':request}).data
       
        report_work_book=ReportWorkBook(file_name='cart')
        report_work_book.sheets.append(ReportSheet(data=products_s,table_headers=None,title='محصولات'))
        report_work_book.sheets.append(ReportSheet(data=categories_s,table_headers=None,title='دسته ها'))
        response=report_work_book.to_excel()    
        return response
    def get_list_supplier(self,request,supplier_id):
        user=request.user
        supplier=SupplierRepo(user=user).get(supplier_id=supplier_id)
        # products_s=ProductSerializer(ProductRepo(user=user).list_all(),many=True,context={'request':request}).data
        categories_s=CategorySerializer(CategoryRepo(user=user).list_all(),many=True,context={'request':request}).data
        # employees_s=EmployeeSerializer(supplier.employees.all(),many=True,context={'request':request}).data
        # shops_s=ShopSerializer(ShopRepo(user=user).get_by_supplier(supplier_id=supplier_id),many=True,context={'request':request}).data
        
   
        products_s=ProductRepo(user=user).list_all().values('id','name','image','thumbnail')

        # categories_s=CategoryRepo(user=user).list_all().values('product_id')
        employees_s=supplier.employees.all().values('personeli_code','name')
        shops_s=ShopRepo(user=user).get_by_supplier(supplier_id=supplier_id).values('product_id','price','unit_name')
        
        report_work_book=ReportWorkBook()
        report_work_book.sheets.append(ReportSheet(data=products_s,table_headers=None,title='محصولات'))
        report_work_book.sheets.append(ReportSheet(data=categories_s,table_headers=None,title='دسته ها'))
        if len(shops_s)>0:report_work_book.sheets.append(ReportSheet(data=shops_s,table_headers=None,title='عرضه ها'))
        if len(employees_s)>0:report_work_book.sheets.append(ReportSheet(data=employees_s,table_headers=None,title='کارکنان'))
        response=report_work_book.to_excel()    
        return response
    def get_order(self,request,order_id):
        user=request.user
        order=OrderRepo(user=user).get(order_id=order_id)
        # products_s=ProductSerializer(ProductRepo(user=user).list_all(),many=True,context={'request':request}).data
        lines_s=[]
        total=0
        for i,line in enumerate(order.lines,1):
            total+=line.price*line.quantity
            line_s={
                'ردیف':i,
                'کالا':line.product.name,
                'تعداد':line.quantity,
                'واحد':line.unit_name,
                'قیمت':line.price,
                'جمع':line.price*line.quantity,
            }
            lines_s.append(line_s)
        line_s={
            'ردیف':'',
            'کالا':'',
            'تعداد':'',
            'واحد':'',
            'قیمت':'',
            'جمع':total,
        }
        lines_s.append(line_s)
        line_s={
            'ردیف':'',
            'کالا':'',
            'تعداد':'',
            'واحد':'',
            'قیمت':'هزینه ارسال',
            'جمع':order.ship_fee,
        }
        lines_s.append(line_s)
        line_s={
            'ردیف':'',
            'کالا':'',
            'تعداد':'',
            'واحد':'',
            'قیمت':'جمع کل',
            'جمع':total+order.ship_fee,
        }
        lines_s.append(line_s)
        report_work_book=ReportWorkBook()
        report_work_book.sheets.append(ReportSheet(data=lines_s,table_headers=None,title='سفارش شماره '+str(order_id)))
        response=report_work_book.to_excel()    
        return response
    def get_product_label(self,request,product_id,shop_id=None):
        user=request.user
        product=ProductRepo(user=user).get(product_id=product_id)


class ProductView(View): 
    def add_product_comment(self,request):
        if request.method=='POST':
            add_product_comment_form=AddProductCommentForm(request.POST)
            if add_product_comment_form.is_valid():
                product_id=add_product_comment_form.cleaned_data['product_id']
                comment=add_product_comment_form.cleaned_data['comment']
                product_comment=ProductRepo(user=request.user).add_comment(product_id=product_id,comment=comment)
                if product_comment is not None:
                    return redirect(reverse('market:product',kwargs={'product_id':product_id}))
        return redirect(reverse('market:product',kwargs={'product_id':product_id}))

    def get_list_xlsx(self,request):
        user=request.user
        products_s=ProductSerializer(ProductRepo(user=user).list_all(),many=True,context={'request':request}).data
        categories_s=CategorySerializer(CategoryRepo(user=user).list_all(),many=True,context={'request':request}).data
       
        report_work_book=ReportWorkBook(file_name='cart')
        report_work_book.sheets.append(ReportSheet(data=products_s,table_headers=None,title='محصولات'))
        report_work_book.sheets.append(ReportSheet(data=categories_s,table_headers=None,title='دسته ها'))
        response=report_work_book.to_excel()    
        return response
    def list(self,request,category_id):
        context=getContext(request)        
        # if request.user.is_authenticated:
        #     context['new_definition_form']=NewDefinitionForm()
        context['products']=ProductRepo(user=user).list(category_id=category_id)     
        return render(request,TEMPLATE_ROOT+'products.html',context=context)
 
    def product(self,request,product_id):
        user=request.user
        context=getContext(request)
        brands=BrandRepo(user=user).list()
        context['brands']=brands        
        # if request.user.is_authenticated:
        #     context['new_definition_form']=NewDefinitionForm()
        shops=ShopRepo(user=request.user).list(product_id=product_id)
        context['shops']=shops
        context['shops_s']='[]'
        active_customer=CustomerRepo(user=user).me
        active_supplier=SupplierRepo(user=user).me
        if active_customer is not None:            
            add_to_cart_form=AddToCartForm()
            if len(shops)>0:
                context['add_to_cart_form']=add_to_cart_form
            shop_s=ShopSerializer(shops,many=True).data
            context['shops_s']=json.dumps(shop_s)
        if active_supplier is not None:
            context['add_shop_form']=AddShopForm()  
            # context['add_shop_form']=True       
            shop_s=ShopSerializer(shops,many=True).data
            context['shops_s']=json.dumps(shop_s)
        unit_names=ProductUnitRepo(user=user).list_for_product(product_id)
        unit_names_s=ProductUnitSerializer(unit_names,many=True).data
        context['unit_names_s']=json.dumps(unit_names_s)
        product=ProductRepo(user=request.user).get(product_id)
        context['product']=product
        context['metadatas']=product.metadatas.all()
        product_relateds=ProductRepo(user=user).related(product_id=product_id)
        context['product_relateds']=product_relateds
        context['product_s']=json.dumps(ProductSerializer(product).data)
        product_repo=ProductRepo(user=user)
        product_comments=product_repo.comments(product_id=product_id)
        product_comments_s=ProductCommentSerializer(product_comments,many=True).data
        context['product_comments_s']=json.dumps(product_comments_s)
        context['comments_s']=json.dumps(CommentSerializer(product.comments.all(),many=True).data)
        context['product_comments']=product_comments
        if user is not None and user.is_authenticated:
            context['add_product_comment_form']=AddProductCommentForm()
            context['add_product_like_form']=AddProductLikeForm()
            context['is_liked']=product_repo.is_my_favorite(product_id=product_id)
        context['breadcrumb']=product.category.get_breadcrumb()
        #return render(request,TEMPLATE_ROOT+'product.html',context=context)
        return render(request=request,template_name='one-tech/product.html',context=context)
    
    def add_to_cart(self,request):
        user=request.user
        if request.method=='POST':
            add_to_cart_form=AddToCartForm(request.POST)
            if add_to_cart_form.is_valid():
                shop_id=add_to_cart_form.cleaned_data['shop_id']
                quantity=add_to_cart_form.cleaned_data['quantity']
                if quantity is None:
                    quantity=1
                cart_line=CartRepo(user=request.user).add_to_cart(shop_id=shop_id,quantity=quantity)
                return redirect(cart_line.shop.product.get_absolute_url())
    def add_like(self,request):
        if request.method=='POST':
            add_product_like_form=AddProductLikeForm(request.POST)
            if add_product_like_form.is_valid():
                product_id=add_product_like_form.cleaned_data['product_id']
                is_liked=ProductRepo(user=request.user).add_like(product_id=product_id)
                return JsonResponse({'is_liked':is_liked})


class CartView(View):
    
    def submit_cart(self,request):
        user=request.user
        if request.method=='POST':
            submit_cart_form=SubmitCartForm(request.POST)
            if submit_cart_form.is_valid():
                customer_id=submit_cart_form.cleaned_data['customer_id']
                # input(customer_id)
                supplier_id=submit_cart_form.cleaned_data['supplier_id']
                address=submit_cart_form.cleaned_data['address']
                description=submit_cart_form.cleaned_data['description']
                no_ship=submit_cart_form.cleaned_data['no_ship']
                orders=CartRepo(user=user).submit(customer_id=customer_id,address=address,description=description,no_ship=no_ship,supplier_id=supplier_id)  
                if orders is not None and len(orders)>0:
                    context=getContext(request)
                    context['page_confirm']={'orders':orders}
                    return redirect(reverse('market:cart',kwargs={'customer_id':customer_id}))


    def remove_from_cart(self,request):
        if request.method=='POST':
            remove_from_cart_form=RemoveFromCartForm(request.POST)
            if remove_from_cart_form.is_valid():
                shop_id=remove_from_cart_form.cleaned_data['shop_id']
                done=CartRepo(user=request.user).remove_from_cart(shop_id=shop_id)
                if done:
                    return self.get(request)
    
        
    def get(self,request,customer_id=0):
        user=request.user
        if customer_id==0:
            customer=CustomerRepo(user=user).me
            if customer is not None:
                customer_id=customer.pk
            else:
                redirect(reverse('market:home'))
        context=getContext(request)
        cart=CartRepo(user=user).get_by_customer(customer_id=customer_id)
        context['cart']=cart
        cart_orders=CartRepo(user=user).get_cart_orders(customer_id=customer_id)
        remove_from_cart_form=RemoveFromCartForm()
        context['remove_from_cart_form']=remove_from_cart_form
        if cart_orders is None or len(cart_orders)==0:
            pass
        else:
            context['cart_orders']=cart_orders
        
        context['selected_customer']=CustomerRepo(user=user).get(customer_id=customer_id)
        return render(request,'one-tech/cart.html',context)


class TableView(View): 
    def list(self,request):
        user=request.user
        context=getContext(request)        
        # if request.user.is_authenticated:
        #     context['new_definition_form']=NewDefinitionForm()
        products=ProductRepo(user=request.user).list_all()
        categories=CategoryRepo(user=request.user).list_all()
        suppliers=SupplierRepo(user=user).list()
        customers=CustomerRepo(user=user).list()
        context['products']=products
        context['categories']=categories
        context['suppliers']=suppliers
        context['customers']=customers
        return render(request,TEMPLATE_ROOT+'tables.html',context=context)


class IndexView(View):
    def my_list(self,request,*args, **kwargs):
        user=request.user

        context=getContext(request=request)
        product_repo=ProductRepo(user=user)
        context['products']=product_repo.my_list()
        
        category_repo=CategoryRepo(user=user)
        categories=category_repo.list_master()
        context['categories']=categories
        return render(request,'one-tech/shop.html',context)

    
    def search(self,request):        
        context=getContext(request)
        if request.method=='POST':
            search_form=SearchForm(request.POST)   
            if search_form.is_valid():
                search_for=search_form.cleaned_data['search_for']
                search_result=ProductRepo(user=request.user).search(search_for=search_for)
                products=search_result['products']
                catgories=search_result['categories']
                if len(products)>0 or len(catgories)>0:
                    context['products']=products
                    context['categories']=catgories
                else:
                    context['empty_search']=True              
                    return render(request,'one-tech/search.html',context=context)
                    # if request.user.is_authenticated:
                    #     context['new_word_form']=NewWordForm()
                context['search_for']=search_for
                return render(request,'one-tech/shop.html',context=context)            
            return render(request,TEMPLATE_ROOT+'search.html',context=context)                
        return render(request,TEMPLATE_ROOT+'search.html',context=context)
                
    def index(self,request,*args,**kwargs):

        
        user=request.user
        if not user or user is None or not user.is_authenticated :
            return redirect(reverse('authentication:login'))
        if user is None or not user.is_authenticated:
            return redirect(reverse('authentication:login'))
        profile=ProfileRepo(user=user).me
        transaction_list_amount=[]
        transaction_list_rest=[]
        transaction_list_labels=[]
        MAX_COUNT=8
        high_amount=0
        high_rest=0
        low_rest=0
        low_amount=0
        transactions=ProfileTransactionRepo(user=user).list(profile.id)[:MAX_COUNT]
        MAX_COUNT=len(transactions)
        for i,transaction in enumerate(transactions):
            until_date=transaction.date_added
            amount=transaction.get_balanced_amount(profile.id)/1000
            if i % 3==0:
                transaction_list_labels.append(str(MAX_COUNT-i))
            else:
                transaction_list_labels.append(str(MAX_COUNT-i))
            rest=ProfileTransactionRepo(user=user).rest(until_date=until_date)/1000
            rest=int(rest)
            amount=int(amount)
            # amount=amount if amount>0 else 0-amount
            # amount=amount if amount>0 else 0-amount
            if amount>high_amount:
                high_amount=amount
            if amount<low_amount:
                low_amount=amount            
            if rest>high_rest:
                high_rest=rest
            if rest<low_rest:
                low_rest=rest
            transaction_list_rest.append(rest)
            transaction_list_amount.append(amount)
        context=getContext(request)
        context['high_amount']=high_amount*1.1
        context['high_rest']=high_rest*1.1
        context['low_rest']=low_rest*1.1
        context['low_amount']=low_amount*1.1
        context['transaction_list_labels']=json.dumps(transaction_list_labels)
        context['transaction_list_rest']=json.dumps(transaction_list_rest)
        context['transaction_list_amount']=json.dumps(transaction_list_amount)
        context['total']=ProfileTransactionRepo(user=request.user).rest()
        return render(request,TEMPLATE_ROOT+'index.html',context)          

    def get(self,request,*args,**kwargs):
        if 'parent_id' in kwargs:
            parent_id= kwargs.get("parent_id")
            return ShopView().list(request=request,parent_id=parent_id)
        return ShopView().list(request=request,parent_id=0)
    

class WareHouseViews(View):
    def ware_house(self,request,ware_house_id,*args,**kwargs):
        user=request.user
        context=getContext(request=request)

        ware_house=WareHouseRepo(user=user).get(ware_house_id=ware_house_id)
        if ware_house is None:
            raise Http404
        context['ware_house']=ware_house
        return render(request,TEMPLATE_ROOT+'ware-house.html',context)


class SupplierView(View):
    def supplier(self,request,supplier_id,*args,**kwargs):
        user=request.user

        if supplier_id is not None:
            context=getContext(request)





            transaction_list_amount=[]
            transaction_list_labels=[]
            MAX_COUNT=8
            high_amount=0
            low_amount=0
            orders=OrderRepo(user=user).list_for_supplier(supplier_id=supplier_id)[:MAX_COUNT]
            MAX_COUNT=len(orders)
            for i,order in enumerate(orders):
                total=order.total()/1000
                if i % 3==0:
                    transaction_list_labels.append(str(MAX_COUNT-i))
                else:
                    transaction_list_labels.append(str(MAX_COUNT-i))                
                total=int(total)
                # amount=amount if amount>0 else 0-amount
                # amount=amount if amount>0 else 0-amount
                if total>high_amount:
                    high_amount=total
                if total<low_amount:
                    low_amount=total     
                transaction_list_amount.append(total)
            context=getContext(request)
            context['high_amount']=high_amount*1.1            
            context['low_amount']=low_amount*1.1
            context['transaction_list_labels']=json.dumps(transaction_list_labels)
            context['transaction_list_amount']=json.dumps(transaction_list_amount)
            
            supplier=SupplierRepo(user=user).get(supplier_id=supplier_id)
            if supplier is None:
                raise Http404

            context['supplier']=supplier
            products=ProductRepo(user=request.user).list_by_supplier(supplier_id=supplier_id)
            context['products']=products
            shops=ShopRepo(user=user).get_by_supplier(supplier_id=supplier_id)
            context['shops']=shops
            context['remove_shop_form']=RemoveShopForm()
            return render(request,TEMPLATE_ROOT+'supplier.html',context)
    def list(self,request):
        user=request.user
        
        context=getContext(request=request)
        suppliers=SupplierRepo(user=user).list()
        context['suppliers']=suppliers
        return render(request,TEMPLATE_ROOT+'tables.html',context)


class OrderView(View):
    def orders(self,request,customer_id=None,supplier_id=None,shipper_id=None,start_date=None,end_date=None):
        user=request.user
        context=getContext(request=request)
        profile=ProfileRepo(user=user).me
        if customer_id is not None:
            if customer_id==0:
                customer_id=profile.id
            customer=CustomerRepo(user=user).get(customer_id=customer_id) 
            context['title_orders']='خرید شده توسط '+customer.profile.name()
            
            context['name']=customer.profile.name()
            orders=OrderRepo(user=user).list_for_customer(customer_id=customer_id)
        elif supplier_id is not None:
            if supplier_id==0:
                supplier_id=profile.id
            supplier=SupplierRepo(user=user).get(supplier_id=supplier_id)
            orders=OrderRepo(user=user).list_for_supplier(supplier_id=supplier_id)
            context['supplier']=supplier
            context['name']=supplier.title
            context['title_orders']='فروخته شده توسط '+supplier.name()
        
        elif shipper_id is not None:
            if shipper_id==0:
                shipper_id=profile.id
            shipper=ShipperRepo(user=user).get(shipper_id=shipper_id)
            orders=OrderRepo(user=user).list_for_shipper(shipper_id=shipper_id)
            context['title_orders']='آماده ارسال برای  '+shipper.name
        
        
        if start_date is not None:
            start_date=start_date.replace('_', '/')
            context['start_date']=start_date
            start_date=PersianCalendar().to_gregorian(start_date,start=True)
            orders=orders.filter(order_date__gte=start_date)
        else:
            start_date=str(PersianCalendar().now())[0:10].replace('-', '/')
            context['start_date']=start_date

        if end_date is not None:
            end_date=end_date.replace('_', '/')
            context['end_date']=end_date
            end_date=PersianCalendar().to_gregorian(end_date,end=True)            
            orders=orders.filter(order_date__lte=end_date)
            
        else:
            end_date=str(PersianCalendar().now())[0:10].replace('-', '/')
            context['end_date']=end_date

        context['orders']=orders

        return render(request,TEMPLATE_ROOT+'orders.html',context)

    def do_deliver_order(self,request):
        if request.method=='POST':
            do_deliver_form=DoDeliverForm(request.POST)
            if do_deliver_form.is_valid():
                order_id=do_deliver_form.cleaned_data['order_id']
                description=do_deliver_form.cleaned_data['description']
                order=OrderRepo(user=request.user).do_deliver(order_id=order_id,description=description)
                
                if order is not None:
                    return redirect(order.get_absolute_url())
        return redirect(reverse('market:orders',kwargs={'profile_id':0}))
    def do_pack_order(self,request):
        if request.method=='POST':
            do_pack_form=DoPackForm(request.POST)
            if do_pack_form.is_valid():
                order_id=do_pack_form.cleaned_data['order_id']
                count_of_packs=do_pack_form.cleaned_data['count_of_packs']
                description=do_pack_form.cleaned_data['description']
                if count_of_packs is None:
                    count_of_packs=1
                order=OrderRepo(user=request.user).do_pack(order_id=order_id,count_of_packs=count_of_packs,description=description)
                if order is not None:
                    return redirect(order.get_absolute_url())
        return redirect(reverse('market:orders_supplier',kwargs={'supplier_id':0}))
    
    
    def do_ship_order(self,request):
        if request.method=='POST':
            do_ship_form=DoShipForm(request.POST)
            if do_ship_form.is_valid():
                order_id=do_ship_form.cleaned_data['order_id']
                description=do_ship_form.cleaned_data['description']
                order=OrderRepo(user=request.user).do_ship(order_id=order_id,description=description)
                
                if order is not None:
                    return redirect(order.get_absolute_url())
        return redirect(reverse('market:orders_shipper',kwargs={'shipper_id':0}))
    
    def order(self,request,order_id):
        user=request.user
        profile=ProfileRepo(user=user).me
        order=OrderRepo(user=user).get(order_id=order_id)
        if order is None:
            raise Http404
        context=getContext(request=request)
        context['order']=order
        active_customer=CustomerRepo(user=user).me
        active_supplier=SupplierRepo(user=user).me
        active_shipper=ShipperRepo(user=user).me
        # input(active_supplier)
        # input(order.supplier)
        # do pack form
        if active_supplier is not None and order.supplier==active_supplier and order.status==OrderStatusEnum.ACCEPTED:
            do_pack_form=DoPackForm()
            context['do_pack_form']=do_pack_form
        
         # do ship form
        
        
        if active_shipper is not None and order.status==OrderStatusEnum.PACKED:
            do_ship_form=DoShipForm()
            context['do_ship_form']=do_ship_form
        # do deiver form
        customer=CustomerRepo(user=user).me
        if customer is not None and (order.status==OrderStatusEnum.SHIPPED or (order.status==OrderStatusEnum.PACKED and order.no_ship==True)) and order.customer==customer:
            do_deliver_form=DoDeliverForm()
            context['do_deliver_form']=do_deliver_form

        return render(request,TEMPLATE_ROOT+'order.html',context)


    def get(self,request,profile_id=0,*args, **kwargs):
        user=request.user
        if profile_id==0:
            profile=ProfileRepo(user=user).get_by_user()
            profile_id=profile.id
        else:
            profile=ProfileRepo(user=user).get(profile_id=profile_id)
        context=getContext(request=request)
        transaction_repo=ProfileTransactionRepo(user=user)
        transactions=transaction_repo.list_by_profile(profile_id=profile_id)
        context['transactions']=transactions
        context['transaction_title']=profile.name
        context['rest_all']=transaction_repo.get_rest(profile_id=profile_id)
        return render(request,TEMPLATE_ROOT+'transactions.html',context)