from django.urls import path
from .views import *


urlpatterns = [
    path('user_offers/', UserOffersView.as_view()),
    path('add_offer/', AddOfferView.as_view()),
    path('edit_offer/<int:offer_id>/', EditOfferView.as_view()),
    path('offer_details/<int:offer_id>/', DetailsOfferView.as_view()),
    ]