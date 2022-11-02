from django.urls import path
from stories.views import *

app_name = 'stories'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index, name = 'index'), # Tên mô tả ở name là viết liền ko dấu, ko có khoảng trắng
    path('category/<int:pk>/', category, name = 'category'),
    path('contact/', contact, name = 'contact'),
    path('contact-2/', contact_2, name = 'contact_2'),
    path('story/<int:pk>/', story, name = 'story'),
    path('search/', search, name = 'search'),
]
