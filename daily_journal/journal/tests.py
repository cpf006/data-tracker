import sys
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from .models import Entry, DataTracker, DataOption, DataResponse

class SetEntriesViewTests(TestCase):
    def test_proper_creation(self):
        """
        Test to ensure set entry properly sets content of entry
        """
        c = Client()
        response = c.post(
            reverse(
                'journal:set_entry', 
                kwargs={
                    'year':2020,
                    'month':1,
                    'day':1,
                }
            ),
            {'content': 'test'}
        )

        entry = Entry.objects.first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(entry.content, 'test')
        
    
class SetTrackerViewTests(TestCase):
    def test_proper_creation(self):
        """
        Test to ensure set_tracker properly saves tracker
        with its options and option colors. Also updates 
        exisitng options if present.
        """
        c = Client()
        tracker = DataTracker(name='test', color='none')
        tracker.save()
        optionOne = DataOption(name='One', color='red', data_tracker=tracker)
        optionOne.save()
        response = c.post(
            reverse('journal:set_tracker'),
            {
                'name': 'test',
                'color': 'color',
                'option_name1': 'One',
                'option_color1': 'green',
                'option_name2': 'Two',
                'option_color2': 'red',
            }
        )
        tracker = DataTracker.objects.first()
        optionTwo = DataOption.objects.get(name='Two')
        optionOne.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(tracker.name, 'test')
        self.assertEqual(tracker.color, 'color')
        self.assertEqual(optionOne.color, 'green')
        self.assertEqual(optionTwo.color, 'red')
