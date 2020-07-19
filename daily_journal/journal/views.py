from django.shortcuts import get_object_or_404, render, redirect
from datetime import date

from .models import Entry, DataTracker, DataOption, DataResponse

def index(request):
    latest = Entry.objects.order_by('-pub_date')[:5]
    return render(
        request,
        'journal/index.html',
        {'latest': latest}
    )

def access_entry(request, year, month, day):
    entry = Entry.objects.filter(
        pub_date__year=year, 
        pub_date__month=month, 
        pub_date__day=day
    ).first()
    entry_date = date(year, month, day)
    trackers = DataTracker.objects.all()

    return render(
        request, 
        'journal/access_entry.html',  
        {
            'entry': entry,
            'entry_date': entry_date,
            'trackers': trackers
        }
    )

def set_entry(request, year, month, day):
    entry = Entry.objects.filter(
        pub_date__year=year, 
        pub_date__month=month, 
        pub_date__day=day
    ).first()

    #Create or update entry
    if entry:
        entry.content = request.POST['content']
    else:
        entry = Entry(
            content = request.POST['content'], 
            pub_date = date(year, month, day)
        )
    entry.save()

    #Save new or update tracker responses
    for tracker in DataTracker.objects.all():
        tracker_id = 'tracker' + str(tracker.id)

        if tracker_id in request.POST:
            response = DataResponse.objects.get(entry=entry, data_tracker=tracker)
            option = get_object_or_404(DataOption, pk=request.POST[tracker_id])
            if response:
                response.data_option = option
            else:
                response = DataResponse(
                    entry = entry,
                    data_option = option,
                    data_tracker = tracker 
                )
            response.save()

    return render(
        request,
        'journal/index.html',
        {'message': "Entry for %s saved." % str(entry.pub_date)}
    )

def get_entries(request, year):
    entries = Entry.objects.filter(
        pub_date__year = year
    )
    return render(
        request, 
        'journal/get_entries.html', 
        {
            'entries': entries,
            'start_date': date(year, 1, 1)
        }
    )
