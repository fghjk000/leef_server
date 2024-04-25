from django.urls import path

from leef.views import UserCreateAPIView, UserDetailAPIView, SignupAPIView, LogoutAPIView, LoginAPIView

urlpatterns = [
    path('', UserCreateAPIView.as_view()),
    path('<int:user_id>', UserDetailAPIView.as_view()),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('login/', LoginAPIView.as_view(), name='login')
]
