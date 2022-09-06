from django.urls import path, include
from rest_framework import routers

from .views import SignUpAPI, SignInAPI, MainUser
from knox import views as knox_views

# router = routers.DefaultRouter()
# router.register('auth/register', SignUpAPI, 'register')
# router.register('auth/login', SignInAPI, 'login')
# router.register('auth/user', MainUser, 'user')

urlpatterns = [
    path('', include('knox.urls')),
    path('register', SignUpAPI.as_view()),
    path('login', SignInAPI.as_view()),
    path('user', MainUser.as_view()),
    path('logout', knox_views.LogoutView.as_view(), name="knox-logout"),
]


# urlpatterns = router.urls