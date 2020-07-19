from django.urls import path
from . import views

app_name = 'journal'
urlpatterns = [
    # ex: /journal/
    path('', views.index, name='index'),
    # ex: /journal/entry/set/2020/1/1
    path('entry/set/<int:year>/<int:month>/<int:day>', views.set_entry, name='set_entry'),
    # ex: /journal/entry/2020/1/1
    path('entry/<int:year>/<int:month>/<int:day>', views.access_entry, name='access_entry'),
    # ex: /journal/get/{year}
    path('get/<int:year>', views.get_entries, name='get_entries'),
]