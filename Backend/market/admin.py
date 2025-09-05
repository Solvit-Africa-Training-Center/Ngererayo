from django.contrib import admin


from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import (
    Product,Cart,CartItem,Order,Owner,ProductComments,ProductMessage
    ,Consultant,ConsultantPost,RequestTobeOwer
    ,Payment
)

# Register your models here.



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'owner', 'price', 'quantity','description','product_image']
    list_filter = ['owner', 'price']
    search_fields = ['product_name', 'description']
    list_per_page = 10




@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'farming_name', 'location']
    search_fields = ['user__username', 'farming_name']
    list_per_page = 10
    



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__username']
    list_per_page = 10



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    search_fields = ['cart__user__username', 'product__name']
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'cart', 'created_at', 'address']
    # search_fields = ('user__username', 'product__name', 'address')
    list_per_page = 10



@admin.register(ProductMessage)
class ProductMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'product', 'message', 'created_at']
    search_fields = ['sender__username', 'receiver__username', 'product__name', 'message']
    list_per_page = 10



@admin.register(ProductComments)
class ProductCommentsAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'comment', 'created_at']
    search_fields = ['product__name', 'user__username', 'comment']
    list_per_page = 10



@admin.register(Consultant)
class ConsultantAdmin(admin.ModelAdmin):
    list_display=["user","location"]
    search_fields=["location"]

    




@admin.register(ConsultantPost)
class ConsultantPostAdmin(admin.ModelAdmin):
    list_display=["post_title","created_at"]




@admin.register(RequestTobeOwer)
class    RequestTobeOwerAdmin(admin.ModelAdmin):
        list_display=["user","farming_name","location"]
        search_fields=["user__username","farming_name","location"]
        list_per_page=10
        actions =["approve_request","reject_request"]

        def send_seller_email(self, user, approved=True):
            subject ="Seller Request Approved" if approved else "Seller Request Rejected"
            context={
                'subject':subject,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'approved':approved,
            
            }

            html_content=render_to_string('emails/seller_request.html',context)
            text_content=strip_tags(html_content)

            email=EmailMultiAlternatives(
                subject,
                text_content,
                "Ngererayo Market <gihozoismail@gmail.com> ",
                  [user.email]
            )
            email.attach_alternative(html_content,"text/html")
            email.send()
        def  approve_request(self, request,queryset):
            for req in queryset:

                Owner.objects.create(
                    user=req.user,
                    farming_name=req.farming_name,
                    location=req.location,
                )
                req.user.role="farmer"
                req.user.save()

                self.send_seller_email(req.user,approved=True)
                req.delete()


            self.message_user(request, "Request approved successfully")
        approve_request.short_description="approved selected request"


        def reject_request(self, request,queryset):
            for req in queryset:
                self.send_seller_email(req.user,approved=False)
                req.delete()
                self.message_user(request, "Request rejected successfully")
        reject_request.short_description="rejected selected request"                    
                






    
    
