from django.urls import path
from . import views

app_name = 'journal'
urlpatterns = [
    # ex: /journal/
    path('', views.index, name='index'),
    # ex: /journal/change/1/
    path('change/<int:entry_id>/', views.change_entry, name='change_entry'),
    # ex: /journal/add/
    path('add/<int:year>/<int:month>/<int:day>', views.add_entry, name='add_entry'),
    # ex: /journal/get/{year}/{month}
    path('get/<int:year>', views.get_entries, name='get_entries'),
]