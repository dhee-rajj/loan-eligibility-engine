from django.urls import path
from .views import upload_csv

urlpatterns = [
    path('', upload_csv, name='upload_csv'),
]


 id |   source   |        bank_name        |             product_name
| min_credit_score | min_income_monthly |     scraped_at 