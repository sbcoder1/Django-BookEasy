# urls.py
from django.urls import path
from django.contrib import admin
from .views import login_ajax, register_ajax, base, homepage, logout_user, profile_user, add_book, edit_book, delete_book,add_movie,books,movies,edit_movie,delete_movie,author_detail,add_author, edit_author,authors_list,search_authors
from .views import book_details,add_to_cart,remove_from_cart,update_cart,cart_view,update_profile,myprofile,order_details,checkout,order_history,dispatch_order,download_receipt
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', base, name='base'),
    path('admin/', admin.site.urls),
    path('login_ajax/', login_ajax, name='login_ajax'),
    path('register_ajax/', register_ajax, name='register_ajax'),
    path('homepage/', homepage, name='homepage'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile_user, name='profile'),
    
    path('books/',books,name='books'),
    path('add-book/', add_book, name='add_book'),
    path('edit_book/<uuid:book_id>/',edit_book, name='edit_book'),
    path('delete_book/<uuid:book_id>/', delete_book, name='delete_book'),
    path('search/', search_authors, name='search_authors'),
    
    path('movies/',movies,name='movies'),
    path('add-movie/',add_movie,name='add_movie'),
    path('edit_movie/<int:movie_id>/', edit_movie, name='edit_movie'),
    path('delete_movie/<int:movie_id>/', delete_movie, name='delete_movie'),
    
    path('authors/<uuid:author_id>/',author_detail, name='author_detail'),
    path('authors/add/', add_author, name='add_author'),
    path('authors/', authors_list, name='authors_list'),
    path('authors/edit/<uuid:author_id>/', edit_author, name='edit_author'),
    path('book_details/<uuid:book_id>/', book_details, name='book_details'),
    
    path('add-to-cart/<uuid:book_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart/<uuid:cart_item_id>/<str:action>/', update_cart, name='update_cart'),
    path('remove-from-cart/<uuid:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart_view'),
    
    path('update-profile/',update_profile, name='updateprofile'),
    path('my-profile/',myprofile,name='myprofile'),
    
    path('checkout/', checkout, name='checkout'),
    path('order_details/<uuid:order_id>/',order_details, name='order_details'),
    path('order-history/', order_history, name='order_history'),
    path('dispatch_order/<uuid:order_id>/', dispatch_order, name='dispatch_order'),
    path('download_receipt/', download_receipt, name='download_receipt'),
    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)