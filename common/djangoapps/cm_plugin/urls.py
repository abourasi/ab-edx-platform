from django.urls import path
from .views import set_cookie

urlpatterns = [
    path('cm/set_cookie/', set_cookie, name='set_cookie'),
]