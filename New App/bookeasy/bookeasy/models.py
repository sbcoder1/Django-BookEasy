from django.db import models
from django.contrib.auth.models import User
import uuid

class Movie(models.Model):
    movie_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    director = models.CharField(max_length=255)
    maleactor = models.CharField(max_length=255)
    femaleactor = models.CharField(max_length=255)
    music = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    movieimage = models.ImageField(upload_to='movies/%Y/%m/%d/')

    def __str__(self):
        return self.name


class Authors(models.Model):
    author_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_name = models.CharField(max_length=355)
    bio = models.TextField(max_length=800)
    authorimage = models.ImageField(upload_to='authors/')
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.author_name


class Book(models.Model):
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart_it = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    book_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    publish_date = models.DateField(blank=True, null=True)
    publisher_name = models.CharField(max_length=255)
    total_pages = models.IntegerField()
    books_available = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    isbn = models.CharField(max_length=13, unique=True)
    book_image = models.ImageField(upload_to='book_images/')

    author_uuid = models.ForeignKey(
        Authors,
        related_name='books',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.book_name
    
#cart
class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    cart_book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cart_items')
    book_name = models.CharField(max_length=255, blank=True, editable=False)
    book_image = models.ImageField(upload_to='cart_book_images/', blank=True, null=True, editable=False)
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2, blank=True, editable=False)
    books_available = models.PositiveIntegerField(default=0, editable=False)
    quantity = models.PositiveIntegerField(default=1)
    added_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Populate fields from the related Book model
        if self.cart_book_id:
            self.book_name = self.cart_book_id.book_name
            self.book_image = self.cart_book_id.book_image
            self.price_at_addition = self.cart_book_id.price
            self.books_available = self.cart_book_id.books_available
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.price_at_addition * self.quantity

    def __str__(self):
        return f"{self.book_name} - {self.quantity} pcs"

    
#userProfile  
class userProfile(models.Model):
    # Link to the auth_user table
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    fname = models.CharField(max_length=150, editable=False)
    lname = models.CharField(max_length=150, editable=False)
    email = models.EmailField(max_length=254, editable=False)

    # Additional fields
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    hobbie = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    states = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    house_no = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Populate fname, lname, and email from the User table
        if self.username:
            self.fname = self.username.first_name
            self.lname = self.username.last_name
            self.email = self.username.email
        super(userProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"Profile of {self.username.username}"



#Order Table
class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_no = models.CharField(max_length=15, unique=True, blank=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product_name = models.TextField(editable=False)
    product_image = models.ImageField(upload_to='order_product_images/', null=True, blank=True, editable=False)
    product_quantity = models.PositiveIntegerField(default=1, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Shipped', 'Shipped'),
            ('Delivered', 'Delivered'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )

    def save(self, *args, **kwargs):
    # Generate order_no in the format BEBM0000001
        if not self.order_no:
            # Query the last order by the `order_id` field
            last_order = Order.objects.order_by('order_time').last()
            if last_order and last_order.order_no:
                # Extract the numeric part of the order_no and increment it
                last_number = int(last_order.order_no[4:])  # Remove the 'BEBM' prefix
                self.order_no = f"BEBM{str(last_number + 1).zfill(7)}"
            else:
                # Initialize the first order number
                self.order_no = "BEBM0000001"
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_no} by {self.user.username}"