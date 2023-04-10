"""Park view tests."""

import os
from unittest import TestCase

from models import db, User, BookmarkedPark, CollectedPark, Park
from bs4 import BeautifulSoup
os.environ['DATABASE_URL'] = 'postgresql:///park_collector_test'

from app import app, CURR_USER_KEY

app.config['WTF_CSRF_ENABLED'] = False

class ParkViewTestCase(TestCase):
    
  def setUp(self):
    """Create test client, and sample data."""

    db.drop_all()
    db.create_all()

    User.query.delete()
    BookmarkedPark.query.delete()
    CollectedPark.query.delete()
    Park.query.delete()

    self.client = app.test_client()

    #NPS topic ID for 'arctic'
    self.topic_id = '77B7EFDF-1A74-409C-8BA2-324EC919DB0E'

    p1 = Park(park_code='lavo', park_name='Lassen Volcanic National Park', park_state='CA')
    db.session.add(p1)
    db.session.commit()

    self.park_name = p1.park_name
    self.park_code = p1.park_code

  def tearDown(self):
    res = super().tearDown()
    db.session.rollback()
    return res
  
  def test_get_park_by_topic(self):
    """Test show national parks by topic."""
    with self.client as c:
      res = c.get(f'/parks/topic/{self.topic_id}')
      
      self.assertEqual(res.status_code, 200)
      self.assertIn('Arctic', str(res.data))
      self.assertIn('Alagnak Wild River', str(res.data))
  
  def test_query_park(self):
    """Test query with complete park name from form."""
    with self.client as c:
      res = c.get('/park', data= {'q': self.park_name}, follow_redirects=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn(f'<h1>{self.park_name}</h1>', str(res.data))
  
  def test_invalid_query_park(self):
    """Test query with incomplete park name from form."""
    with self.client as c:
      res = c.get('/park', data= {'q': 'las'}, follow_redirects=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('Please select a valid park', str(res.data))
    
  def test_get_park_by_code(self):
    """Test display of retrieving a park by park code."""
    with self.client as c:
      res = c.get(f'/park/{self.park_code}')

      self.assertEqual(res.status_code, 200)
      self.assertEqual(res.status_code, 200)
      self.assertIn(f'<h1>{self.park_name}</h1>', str(res.data))