from django.urls import path
from . import views

app_name = 'journal'
urlpatterns = [
    # ex: /journal/
    path('', views.index, name='index'),
    # ex: /journal/2020
    path('<int:year>', views.index, name='index'),
    # ex: /journal/set_tracker
    path('set_tracker/', views.set_tracker, name='set_tracker'),
    # ex: /journal/delete_tracker/1
    path('delete_tracker/<int:pk>', views.delete_tracker, name='delete_tracker'),
    # ex: /journal/set_entry/2020/1/1
    path(
        'set_entry/<int:year>/<int:month>/<int:day>',
        views.set_entry,
        name='set_entry'
    ),
    # ex: /journal/entry/2020/1/1
    path(
        'entry/<int:year>/<int:month>/<int:day>',
        views.access_entry,
        name='access_entry'
    ),
    # ex: /journal/entries/2020
    path('entries/<int:year>', views.entries, name='entries'),
]
