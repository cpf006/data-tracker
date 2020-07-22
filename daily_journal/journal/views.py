from django.shortcuts import get_object_or_404, render
from django.core import serializers
from django.http.response import JsonResponse
from datetime import date, timedelta
import re

from .models import Entry, DataTracker, DataOption, DataResponse


def index(request, year=None):
    """
    Loads entry year view along with year views for all trackers.
    """
    trackers = DataTracker.objects.all()
    return render(
        request,
        'journal/index.html',
        {
            'trackers': trackers,
            'year': year
        }
    )


def access_entry(request, year, month, day):
    """
    Loads an entry if it exists, else loads empty entry form.
    """
    entry = Entry.objects.filter(
        pub_date__year=year,
        pub_date__month=month,
        pub_date__day=day
    ).first()
    entry_date = date(year, month, day)
    trackers = DataTracker.objects.all()
    option_responses = {}

    # Set tracker id to response option id
    if(entry):
        for response in entry.dataresponse_set.all():
            option_responses[
                response.data_tracker.id
            ] = response.data_option.id

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
    """
    Sets an entries content if it already exists or creates a new one.
    Sets all new data responses as well as updates any
    esisting ones for this entry.
    """
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
            content=request.POST['content'],
            pub_date=date(year, month, day)
        )
    entry.save()

    # Save new or update tracker responses
    for tracker in DataTracker.objects.all():
        tracker_id = 'tracker' + str(tracker.id)

        if tracker_id in request.POST:
            option = get_object_or_404(DataOption, pk=request.POST[tracker_id])
            response, _ = DataResponse.objects.get_or_create(
                entry=entry,
                data_tracker=tracker
            )
            response.data_option = option
            response.save()

    return JsonResponse(serializers.serialize('python', [entry, ]), safe=False)


def delete_tracker(request, pk):
    """
    Deletes tracker.
    """
    get_object_or_404(DataTracker, pk=pk).delete()
    return JsonResponse({'message': 'Tracker Deleted'})


def set_tracker(request):
    """
    Sets a trackers color if it already exists or creates a new one.
    Creates new data options or updates existing ones.
    """
    tracker = DataTracker.objects.filter(name=request.POST['name']).first()

    # Create or update tracker
    if tracker:
        tracker.color = request.POST['color']
    else:
        tracker = DataTracker(
            name=request.POST['name'],
            color=request.POST['color']
        )
    tracker.save()

    # Save new or update options
    for field in request.POST:
        if 'option_name' in field:
            option_id = re.sub('option_name', '', field)
            name = request.POST[field]
            color = request.POST['option_color'+option_id]
            option = DataOption.objects.filter(
                name=name,
                data_tracker=tracker
            ).first()
            if option:
                option.color = color
            else:
                option = DataOption(
                    name=name,
                    color=color,
                    data_tracker=tracker
                )
            option.save()

    return JsonResponse(
        serializers.serialize('python', [tracker, ]),
        safe=False
    )


def entries(request, year):
    """
    Loads entries for a specified year.
    If a tracker id is present the color assigned to the response option
    selected will appear instead of the entry default.
    """
    entry_color = 'rgba(144, 198, 149, 1)'
    tracker = None
    dates = {}
    start_date = date(year, 1, 1)
    end_date = date(year+1, 1, 1)
    delta = timedelta(days=1)

    # Create dictionary of every date within a year
    # incase there are missing entries
    while start_date < end_date:
        dates[start_date] = None
        start_date += delta
    # Get tracker if set
    if 'tracker_id' in request.GET:
        tracker = get_object_or_404(DataTracker, pk=request.GET['tracker_id'])

    # Add entries color
    entries = Entry.objects.filter(pub_date__year=year)
    for entry in entries:
        color = entry_color
        if tracker:
            color = None
            response = DataResponse.objects.filter(
                entry=entry,
                data_tracker=tracker
            ).first()
            if response:
                color = response.data_option.color
        dates[entry.pub_date] = color

    return render(
        request,
        'journal/get_entries.html',
        {
            'dates': dates,
            'col_size': 7,
            'tracker': None
        }
    )
