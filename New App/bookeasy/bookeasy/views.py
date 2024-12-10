# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from .models import Movie
from .forms import MovieForm
from .forms import AuthorsForm
from .forms import BookForm
from .models import Authors
from .models import Cart
from .models import userProfile
from .forms import userProfileForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Order
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils.timezone import localdate




#--Books-Section--
def base(request):
    book = Book.objects.all()
    return render(request, 'base.html', {'book': book})
# Check if user is staff
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('base')
    else:
        form = BookForm()
    return render(request,'add_book.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_book(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('base')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})

@login_required
@user_passes_test(is_admin)
def delete_book(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    book.delete()
    return redirect('base')

#--homepage--
def homepage(request):
    return render(request, 'homepage.html')

#--logout--
def logout_user(request):
    logout(request)
    return redirect('base')

#--profile--
def profile_user(request):
    return ('profile')


#--login-ajax-form--
@csrf_exempt
def login_ajax(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "message": "Invalid credentials"})
    return JsonResponse({"success": False, "message": "Invalid request"})

@csrf_exempt

#--register-ajax-form
def register_ajax(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return JsonResponse({"success": False, "message": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message": "Username already taken"})

        user = User.objects.create_user(username=username, email=email, password=password1)
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "message": "Invalid request"},locals())


#--Movie-Section--
@login_required
@user_passes_test(is_admin)

#--Add-Movie--
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('base')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})


def books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})    


def movies(request):
    movies = Movie.objects.all()
    return render(request, 'movie.html', {'movies': movies})

#--Edit-Movie--
@login_required
@user_passes_test(is_admin)
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('base')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})

#--Delete-Movie--
@login_required
@user_passes_test(is_admin)
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie,movie_id=movie_id)
    movie.delete()
    return redirect('base')

#--Author-Deatils--
def author_detail(request, author_id):
    author = get_object_or_404(Authors, author_id=author_id)
    books = Book.objects.filter(author_uuid=author)
    return render(request, 'author_detail.html', {'author': author, 'books': books})

#--Add-Author--
@login_required
@user_passes_test(is_admin)
def add_author(request):
    if request.method == 'POST':
        form = AuthorsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('authors_list')  
    else:
        form = AuthorsForm()
    return render(request, 'add_author.html', {'form': form})

#--Display-Auhtor-List--
@login_required
@user_passes_test(is_admin)
def authors_list(request):
    authors = Authors.objects.all()
    return render(request, 'authors_list.html', {'authors': authors})

#--Edit-Author-Deatils--
@login_required
@user_passes_test(is_admin)
def edit_author(request, author_id):
    author = get_object_or_404(Authors, author_id=author_id)
    if request.method == 'POST':
        form = AuthorsForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect('authors_list')  
    else:
        form = AuthorsForm(instance=author)
    return render(request, 'edit_author.html', {'form': form})


#--Books-Deatils--
def book_details(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)
    author = book.author_uuid  
    return render(request, 'book_details.html', {'book': book, 'author': author})


"""def search_authors(request):
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q'
    authors = Authors.objects.filter(author_name__icontains=query) if query else Authors.objects.all()  # Filter by 'author_name'
    return render(request, 'search_results.html', {'authors': authors, 'query': query})"""

def search_authors(request):
    query = request.GET.get('q', '')  
    
    if query:
        # Try to get the author by name
        author = get_object_or_404(Authors, author_name__icontains=query)  
        return redirect('author_detail', author_id=author.author_id)  

    return redirect('home')


# ----Cart Section ----

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Book, Cart

def add_to_cart(request, book_id):
    # Get the book object
    book = get_object_or_404(Book, book_id=book_id)
    user = request.user  # Get the logged-in user

    # Get or create a cart item for the user and the book
    cart_item, created = Cart.objects.get_or_create(
        user_id=user,
        cart_book_id=book
    )

    # Get the quantity from the request (default to 1 if not provided)
    quantity = int(request.POST.get('quantity', 1))

    if not created:  # If the cart item already exists
        if cart_item.quantity + quantity <= book.books_available:  # Check stock availability
            cart_item.quantity += quantity  # Increment the quantity
            cart_item.save()
            messages.success(request, f"{book.book_name} quantity updated to {cart_item.quantity} in your cart.")
        else:
            messages.error(request, f"Not enough stock available. Only {book.books_available} items left.")
    else:  # If the cart item is newly created
        if book.books_available >= quantity:  # Ensure stock is available
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"{book.book_name} added to your cart with quantity {quantity}.")
        else:
            messages.error(request, f"Only {book.books_available} items of {book.book_name} are in stock.")

    # Update the available books count
    book.books_available = max(book.books_available - cart_item.quantity, 0)
    book.save()

    return redirect('cart_view')  # Redirect to the cart view  

def update_cart(request, cart_item_id, action):
    cart_item = get_object_or_404(Cart, cart_id=cart_item_id)
    book = cart_item.cart_book_id  # Get the book associated with the cart item
    available_stock = book.books_available  # The available stock of the book

    if action == 'increase':
        # Ensure we do not exceed the available stock
        if cart_item.quantity < available_stock:
            cart_item.quantity += 1  # Increase quantity by 1
            book.books_available -= 1  # Decrease the available stock by 1
            cart_item.save()
            book.save()
            messages.success(request, f"Added 1 more {book.book_name} to your cart.")
        else:
            messages.error(request, f"Not enough stock available. Only {available_stock} left.")
    
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # Decrease quantity by 1
            book.books_available += 1  # Increase the available stock by 1
            cart_item.save()
            book.save()
            messages.success(request, f"Removed 1 {book.book_name} from your cart.")
        else:
            messages.error(request, "You cannot reduce quantity below 1.")

    return redirect('cart_view')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, cart_id=cart_item_id)
    book = cart_item.cart_book_id  # Get the book associated with the cart item
    # Return the stock to available books if the cart item is removed
    book.books_available += cart_item.quantity
    cart_item.delete()  # Remove the item from the cart

    # Save the book to reflect the updated available stock
    book.save()
    
    return redirect('cart_view')


def cart_view(request):
    cart_items = Cart.objects.filter(user_id=request.user)

    total_price = sum(item.total_price for item in cart_items)

    total_quantity = sum(item.quantity for item in cart_items)

    return render(request, 'addtocart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity, 
    })
    

#--Profile-Section--
@login_required
def update_profile(request):
    profile, created = userProfile.objects.get_or_create(username=request.user)
    
    if request.method == 'POST':
        form = userProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('books')  
    else:
        form = userProfileForm(instance=profile)

    return render(request, 'updateprofile.html', {'form': form})



def myprofile(request):
    return render(request,'myprofile.html')


#------Order View Section------

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user_id=request.user)
    if not cart_items:
        return redirect('cart') 

    # Create an order
    order = Order.objects.create(
        user=request.user,
        product_name=", ".join([item.book_name for item in cart_items]),
        product_image=cart_items.first().book_image,  
        product_quantity=sum(item.quantity for item in cart_items),
        total_amount=sum(item.total_price for item in cart_items),
    )

    cart_items.delete()
    
    return redirect('order_details', order_id=order.order_id)

def order_details(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'order_details.html', {'order': order})


def order_history(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            # Superusers can view all orders
            orders = Order.objects.all().order_by('-order_time')
        else:
            # Regular users only see their orders
            orders = request.user.orders.all().order_by('-order_time')
        return render(request, 'order_history.html', {'orders': orders})
    else:
        return redirect('login')


@login_required
def dispatch_order(request, order_id):
    if not request.user.is_superuser:
        return redirect('order_history')  
    
    order = get_object_or_404(Order, order_id=order_id)
    
    if order.status in ['Delivered', 'Cancelled']:
        return redirect('order_history')  
    
    order.status = 'Processing'  
    order.save()
    return redirect('order_history')

#--Download Recipet--
def download_receipt(request):
    orders = Order.objects.filter(user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_history_{localdate()}.pdf"'

    # Create a PDF object
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Title
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(100, height - 100, f"Your Order History  : {request.user.username}")

    # Order table header
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, height - 150, "Order No")
    pdf.drawString(200, height - 150, "Product Name")
    pdf.drawString(350, height - 150, "Quantity")
    pdf.drawString(450, height - 150, "Total Amount")
    pdf.drawString(550, height - 150, "Status")

    # List orders
    y_position = height - 180
    for order in orders:
        pdf.setFont("Helvetica", 10)
        pdf.drawString(100, y_position, str(order.order_no))
        pdf.drawString(200, y_position, order.product_name)
        pdf.drawString(350, y_position, str(order.product_quantity))
        pdf.drawString(450, y_position, f"₹ {order.total_amount}")
        pdf.drawString(550, y_position, order.status)
        y_position -= 20

    pdf.showPage()
    pdf.save()

    return response




