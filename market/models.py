from django.db import models
from accounts.models import CustomUser

# Create your models here.


class Owner(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    farming_name=models.CharField(max_length=100)
    location=models.CharField(max_length=200)
    class Meta:
        verbose_name="Owner"
        verbose_name_plural="Owners"
    def __str__(self):
        return self.user.first_name + " " + self.farming_name
    


class Product(models.Model):
    owner=models.ForeignKey(Owner,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.PositiveIntegerField()
    product_image=models.ImageField(upload_to='product_images')
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at=models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        verbose_name="Product",
        verbose_name_plural="Products"
    def __str__(self):
        return self.product_name



class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    session_key=models.CharField(max_length=40,null=True,blank=True)
    products = models.ManyToManyField(Product, through='CartItem')
    class Meta:
        verbose_name="Cart"
        verbose_name_plural="Carts"

    def __str__(self):
        if self.user:
          return f"Cart of {self.user.username}"
        return f"Cart of session {self.session_key}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    class Meta:
        verbose_name="CartItem"
        verbose_name_plural="CartItems"
    def __str__(self):
        if self.cart.user:
          return f"{self.quantity} of {self.product.product_name} in {self.cart.user.username}'s cart"    
        return f"{self.quantity} of {self.product.product_name} in session {self.cart.session_key}"
        




class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="Order"
        verbose_name_plural="Orders"

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"
    



class ProductMessage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta:
        verbose_name="ProductMessage"
        verbose_name_plural="ProductMessages"

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username} about {self.product.product_name}"


class ProductComments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name="ProductComment"
        verbose_name_plural="ProductComments"

    def __str__(self):
        return f"Comment by {self.user.username} on {self.product.product_name}"
    





class Consultant(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    location=models.CharField(max_length=200)
    class Meta:
        verbose_name="Consultant"
        verbose_name_plural="Consultants"
    def __str__(self):
        return self.user.first_name     


class ConsultantPost(models.Model):
    consultant=models.ForeignKey(Consultant,on_delete=models.CASCADE)
    post_title=models.CharField(max_length=100)
    post_description=models.TextField()
    post_image=models.ImageField(upload_to='post_images')
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name="ConsultantPost"
        verbose_name_plural="ConsultantPosts"
    def __str__(self):
        return self.post_title



class RequestTobeOwer(models.Model):
    STATUS_CHOICES=[
        ("pending","pending"),
        ("approved","approved"),
        ("rejected","rejected")
    ]
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    farming_name=models.CharField(max_length=100)
    location=models.CharField(max_length=200)
    license=models.FileField(upload_to='license_files')
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default="pending")
    class Meta:
        verbose_name="Request to be Owner"
        verbose_name_plural="Requests to be Owners"
    def __str__(self):
        return f"Request to be owner of {self.farming_name} by {self.user.username}"





class Payment(models.Model):

    Status_Choice=[
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Failed','Failed')
    ]
    order=models.OneToOneField(Order,on_delete=models.CASCADE, related_name='payment',null=True,blank=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(max_length=10,choices=Status_Choice,default='Pending')
    payment_date=models.DateTimeField(auto_now_add=True)
    transaction_id=models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name="Payment"
        verbose_name_plural="Payments"
    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} on {self.payment_date}"
    