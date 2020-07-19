from django.shortcuts import get_object_or_404, render, redirect
from datetime import date

from .models import Entry

def index(request):
    latest = Entry.objects.order_by('-pub_date')[:5]
    return render(
        request,
        'journal/index.html',
        {'latest': latest}
    )

def change_entry(request, entry_id):
    entry = get_object_or_404(Entry.objects.get(pk=entry_id))
    return render(
        request, 
        'journal/change_entry.html', 
        {'entry': entry}
    )

def add_entry(request, year, month, day):
    entry = Entry.objects.filter(
        pub_date__year=year, 
        pub_date__month=month, 
        pub_date__day=day
    ).first()

    if entry:
        redirect('change_entry', entry_id=entry.id)
    else:
        return render(
            request, 
            'journal/add_entry.html', 
        )

def get_entries(request, year):
    entries = Entry.objects.filter(
        pub_date__year=year
    )
    return render(
        request, 
        'journal/get_entries.html', 
        {
            'entries': entries,
            'start_date': date(year, 1, 1)
        }
    )
