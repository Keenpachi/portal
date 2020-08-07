from django.urls import path
from .views import*

urlpatterns = [
    path('', HomeView.as_view()),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('delete_account/', DeleteView.as_view() )
]