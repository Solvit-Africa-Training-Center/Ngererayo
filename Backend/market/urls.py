
from django.urls import path,include
from rest_framework import routers
from .placeorder import PlaceOrderView
from .RequestedFarmer import RequestTobeOwnerView
from .messaging_views import (ProductMessageView,
                              SendProductCommentsView,
                    SendProductMessageView,
                    GetProductCommentsView,
                    GetSendMessage,
                    
                    GetReplyMessage,
                    GetProductCommentsReplyView,
                    ReplyProductComments,
                    ReplayMessage)


from .views import (ProductView,
                    OwnerView,
                    OwnerProductsView,
                    ProductListView,
                    ProductDetailView,
                    OwnerDeleteProduct,
                    ProductView,
                    OwnerEditProductView,CartView, AddToCartView)



router=routers.DefaultRouter()
router.register("products",ProductView,basename="products")
router.register("owners",OwnerView,basename="owners")





urlpatterns=[
    path("",include(router.urls)),
    path("latest-products/",ProductView.as_view({'get':'list'}), name="latest-products"),
    path("all-products/",ProductListView.as_view()),
    path("product/<int:product_id>/",ProductDetailView.as_view()),
    path("Requested-owner/",RequestTobeOwnerView.as_view(), name ="request-owner"),
    path("owner/<int:owner_id>/products/",OwnerProductsView.as_view()),
path('owner-product/<int:product_id>/edit/', OwnerEditProductView.as_view(), name='owner-edit-product'),
path("owner-product/<int:product_id>/delete/", OwnerDeleteProduct.as_view(), name='owner-delete-product'),
path('cart/', CartView.as_view(), name='cart'),
path('cart_add/', AddToCartView.as_view(), name='cart_add'),

path("place-order/",PlaceOrderView.as_view(), name="place-order"),
path("product-message/<int:product_id>/",ProductMessageView.as_view(),name="product-messages"),
path("product/<int:product_id>/messages/", ProductMessageView.as_view(), name="product-messages"),
path("messages/<int:product_id>/send/", SendProductMessageView.as_view(), name="send-message"),
path("messages/<int:product_id>/", GetSendMessage.as_view(), name="get-send-message"),
path("messages/replies/<int:message_id>/", GetReplyMessage.as_view(), name="get-reply-message"),
path("messages/<int:message_id>/reply/", ReplayMessage.as_view(), name="reply-message"),
path("comments/<int:product_id>/send/", SendProductCommentsView.as_view(), name="send-comment"),
path("comments/<int:comment_id>/reply/", ReplyProductComments.as_view(), name="reply-comment"),
path("comments/<int:product_id>/", GetProductCommentsView.as_view(), name="get-comments"),
path("comments/replies/<int:comment_id>/", GetProductCommentsReplyView.as_view(), name="get-comment-replies"),


]


