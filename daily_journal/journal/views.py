from django.shortcuts import get_object_or_404, render, redirect
from datetime import date, timedelta

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

def entries(request, year):
    dates = {}
    start_date = date(year, 1, 1)
    end_date = date(year+1, 1, 1)
    delta = timedelta(days=1)
    while start_date < end_date:
        dates[start_date] = 'Test'
        start_date += delta
    
    entries = list(Entry.objects.filter(
        pub_date__year = year
    ).values())

    for entry in entries:
        dates[entry['pub_date']] = entry

    return render(
        request,
        'journal/get_entries.html',
        {
            'dates': dates
        }
    )
