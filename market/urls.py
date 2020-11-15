from django.urls import path,include
from .views import *
app_name='market'
urlpatterns=[  
    
    path('api/', include('market.api')),
    path('',ShopView().list,name='home'),
    path('my_list/',IndexView().my_list,name='my_list'),
    path('suppliers/',SupplierView().list,name='suppliers'),
    path('submit_cart/',CartView().submit_cart,name='submit_cart'),
    path('orders/<int:customer_id>/',OrderView().orders,name='orders'),
    path('orders_/<int:supplier_id>/',OrderView().orders,name='orders_supplier'),
    path('orders_/<int:supplier_id>/<start_date>/<end_date>/',OrderView().orders,name='orders_supplier_by_date'),
    path('orders__/<int:shipper_id>/',OrderView().orders,name='orders_shipper'),
    path('cart/<int:customer_id>/',CartView.as_view(),name='cart'),
    path('order/<int:order_id>/',OrderView().order,name='order'),
    path('do_pack_order/',OrderView().do_pack_order,name='do_pack_order'),
    path('do_deliver_order/',OrderView().do_deliver_order,name='do_deliver_order'),
    path('do_ship_order/',OrderView().do_ship_order,name='do_ship_order'),
    path('add_category/',ShopView().add_category,name='add_category'), 
    path('add_product/',ShopView().add_product,name='add_product'), 
    path('add_shop/',ShopView().add_shop,name='add_shop'), 
    path('add_product_comment/',ProductView().add_product_comment,name='add_product_comment'), 
    path('remove_shop/',ShopView().remove_shop,name='remove_shop'), 
    path('add_to_cart/',ProductView().add_to_cart,name='add_to_cart'),    
    path('remove_from_cart/',CartView().remove_from_cart,name='remove_from_cart'), 
    path('tables/',TableView().list,name='tables'),    
    path('xlsx/',ProductView().get_list_xlsx,name='xlsx'),
    path('brand/<int:brand_id>/',ShopView().brand,name='brand'),
    path('products/<int:category_id>/',ProductView().list,name='products'),
    path('product/<int:product_id>/',ProductView().product,name='product'),
    path('list/<int:parent_id>/',IndexView.as_view(),name='list'),
    path('list_vue/<int:parent_id>/',ShopView().list_vue,name='list_vue'),
    path('supplier/<int:supplier_id>/',SupplierView().supplier,name='supplier'),
    path('ware_house/<int:ware_house_id>/',WareHouseViews().ware_house,name='ware_house'),
    path('download/<int:supplier_id>/',DownloadView.as_view(),name='download'),
    path('download/order/<int:order_id>/',DownloadView().get_order,name='download_order'),
    # path('w/d/<name>/',views.WordView().word_name,name='word_name'),
    # path('new_definition/',views.WordView().new_definition,name='new_definition'),
    # path('new_word/',views.WordView().new_word,name='new_word'),
    path('add_like/',ProductView().add_like,name='add_like'),
    # path('add_dislike/',views.WordView().add_dislike,name='add_dislike'),
    path('search/',IndexView().search,name='search'),

    path('manager/',ManagerView().manager,name='manager'),
    


    
]