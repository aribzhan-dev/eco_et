from django.contrib import admin
from django.urls import path
from main.views import *
from django.urls import re_path as url
from django.views.static import serve
from eco_et import settings

handler = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_handler),
    path('cart', cart_handler),
    path('details/<int:blog_id>', details_handler),
    path('that_meet', that_meet_handler),

    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }
        )
]
