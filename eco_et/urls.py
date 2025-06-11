from django.contrib import admin
from django.urls import path

from main import views
from main.views import *
from django.urls import re_path as url
from django.views.static import serve
from eco_et import settings

handler = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_handler, name='index_handler'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_handler, name='cart_handler'),
    path('cart/update/', update_cart, name='update_cart'),
    path('cart/remove/', remove_from_cart, name='remove_from_cart'),
    path('that_meet/<int:category_id>/<int:blog_id>', that_meet_handler),

    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }
        )
]
