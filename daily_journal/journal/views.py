from django.shortcuts import get_object_or_404, render, redirect
from datetime import date, timedelta

from .models import Entry, DataTracker, DataOption, DataResponse

def index(request):
    trackers = DataTracker.objects.all()
    return render(
        request,
        'journal/index.html',
        {'trackers': trackers}
    )

def access_entry(request, year, month, day):
    entry = Entry.objects.filter(
        pub_date__year=year, 
        pub_date__month=month, 
        pub_date__day=day
    ).first()
    entry_date = date(year, month, day)
    trackers = DataTracker.objects.all()
    option_responses = {}

    #Set tracker id to response option id
    if(entry):
        for response in entry.dataresponse_set.all():
            option_responses[response.data_tracker.id] = response.data_option.id

    return render(
        request, 
        'journal/access_entry.html',  
        {
            'entry': entry,
            'entry_date': entry_date,
            'trackers': trackers,
            'option_responses': option_responses
        }
    )

def set_entry(request, year, month, day):
    message = ""
    entry = Entry.objects.filter(
        pub_date__year=year, 
        pub_date__month=month, 
        pub_date__day=day
    ).first()

    # Create or update entry
    if entry:
        entry.content = request.POST['content']
    else:
        entry = Entry(
            content = request.POST['content'], 
            pub_date = date(year, month, day)
        )
    try:
        entry.save()
        message = "Saved entry for "+ str(entry.pub_date)
    except:
        message = "Unable to save entry for "+ str(entry.pub_date)

    # Save new or update tracker responses
    for tracker in DataTracker.objects.all():
        tracker_id = 'tracker' + str(tracker.id)

        if tracker_id in request.POST:
            option = get_object_or_404(DataOption, pk=request.POST[tracker_id])
            response, _ = DataResponse.objects.get_or_create(entry=entry, data_tracker=tracker)
            response.data_option = option
            try:
                response.save()
            except:
                message += "\n response for " + tracker.name + " was unable to save"

    return redirect( 
        'journal/index.html',
        {'message': message}
    )

def entries(request, year):
    dates = {}
    start_date = date(year, 1, 1)
    end_date = date(year+1, 1, 1)
    delta = timedelta(days=1)

    # Create dictionary of every date within a year
    # incase there are missing entries
    while start_date < end_date:
        dates[start_date] = None
        start_date += delta
    
    # Add entries for every date available
    entries = Entry.objects.filter(
        pub_date__year = year
    )
    for entry in entries:
        dates[entry.pub_date] = entry

    return render(
        request,
        'journal/get_entries.html',
        {
            'dates': dates,
            'col_size': 7,
            'tracker': None
        }
    )
