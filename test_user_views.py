"""User view tests."""

import os
from unittest import TestCase

from models import db, User, BookmarkedPark, CollectedPark, Park
from bs4 import BeautifulSoup
os.environ['DATABASE_URL'] = 'postgresql:///park_collector_test'

from app import app, CURR_USER_KEY

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    
  def setUp(self):
    """Create test client, and sample data."""

    db.drop_all()
    db.create_all()

    User.query.delete()
    BookmarkedPark.query.delete()
    CollectedPark.query.delete()
    Park.query.delete()

    self.client = app.test_client()

    self.u1 = User.signup(username='u1',password='test1',email='u1@test.com',first='user',last='one')
    self.u1.id=11111
    self.u2 = User.signup(username='u2',password='test2',email='u2@test.com',first='user',last='two')
    self.u2.id=22222
    
    db.session.add_all([self.u1,self.u2])
    db.session.commit()

  def tearDown(self):
    res = super().tearDown()
    db.session.rollback()
    return res
  
  def test_show_user_profile(self):
    """Test show edit user profile with user in session."""
    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.u1.id

      res = c.get('/users/profile')

      self.assertEqual(res.status_code, 200)
      self.assertIn('Edit Your Profile', str(res.data))
      self.assertIn('u1', str(res.data))
      self.assertNotIn('u2', str(res.data))
  
  def test_invalid_show_profile(self):
    """Test invalid user profile access w/o user in session."""
    with self.client as c:
      res = c.get('/users/profile', follow_redirects=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('Access unauthorized.', str(res.data))

  def test_invalid_user_delete(self):
    """Test invalid user deletion w/o user in session."""
    with self.client as c:
      res = c.post('/users/delete', follow_redirects=True)

      self.assertEqual(res.status_code, 200)
      self.assertIn('Access unauthorized', str(res.data))
      self.assertIn('Where to next', str(res.data))
  
  def setup_bookmarked(self):
    b1 = BookmarkedPark(park_code='abcd', park_name='park abcd', user_id= self.u1.id)
    b2 = BookmarkedPark(park_code='efdg', park_name='park efdg', user_id= self.u1.id)
    db.session.add_all([b1,b2])
    db.session.commit()

  def test_show_bookmarked(self):
    """Test show user bookmarked parks and button text for collected park."""
    self.setup_bookmarked()
    self.setup_collected()

    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.u1.id
    
    res = c.get(f'/users/{self.u1.id}/bookmarked')
    soup = BeautifulSoup(str(res.data), 'html.parser')
    found = soup.find_all('tr', {'class': 'bookmarked-park'})
    
    self.assertEqual(res.status_code, 200)
    self.assertEqual(len(found), 2)
    self.assertIn('abcd', found[0].text)
    self.assertIn('efdg', found[1].text)
    #test 'collect' column button text 
    self.assertIn('Collected!', str(res.data))

  def test_unauthorized_show_bookmarked(self):
    """Test unauthorized access of another user's bookmarked parks."""
    self.setup_bookmarked()

    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.u2.id
      
      res = c.get(f'/users/{self.u1.id}/bookmarked', follow_redirects=True)
      soup = BeautifulSoup(str(res.data), 'html.parser')
      found = soup.find_all('div', {'class': 'collection-card'})
      
      self.assertEqual(res.status_code, 200)
      self.assertIn('Access unauthorized', str(res.data))
      self.assertEqual(len(found), 0)

  def test_add_bookmark(self):
    """Test bookmarking park for specific user."""
    PARK_DATA_TEST = {
    "parkCode": "star",
    "parkName": "park star"
  }
    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.u1.id

      res = c.post('/api/bookmark', json=PARK_DATA_TEST)
      self.assertEqual(res.status_code, 200)
     
      collected = BookmarkedPark.query.filter(BookmarkedPark.park_code=='star').all()
      self.assertEqual(len(collected), 1)
      self.assertEqual(collected[0].user_id, self.u1.id)
  
  def test_invalid_add_bookmark(self):
    """Test bookmarking park via GET request and w/o user in session."""
    with self.client as c:
      res = c.get('/api/bookmark', follow_redirects=True)
      self.assertIn('Invalid request', str(res.data))

  def test_delete_bookmark(self):
    """Test deleting a collected park."""
    self.setup_bookmarked()

    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.u1.id

      url = '/api/bookmark/abcd'

      res = c.delete(url)
      self.assertEqual(res.status_code, 200)

      b = BookmarkedPark.query.all()
      self.assertEqual(len(b), 1)
      self.assertIn('efdg', b[0].park_code)

  def setup_collected(self):
    c1 = CollectedPark(park_code='abcd', park_name='park abcd', user_id= self.u1.id)
    c2 = CollectedPark(park_code='mnop', park_name='park mnop', user_id= self.u1.id)
    db.session.add_all([c1,c2])
    db.session.commit()

  def test_show_collected(self):
    """Test show user collected parks."""
    self.setup_collected()

    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.u1.id
      
      res = c.get(f'/users/{self.u1.id}/collected')
      soup = BeautifulSoup(str(res.data), 'html.parser')
      found = soup.find_all('div', {'class': 'collection-card'})

      self.assertEqual(res.status_code, 200)
      self.assertEqual(len(found), 2)
        
  def test_unauthorized_show_collected(self):
    """Test unauthorized access of another user's collected parks."""
    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.u2.id
      
      res = c.get(f'/users/{self.u1.id}/collected', follow_redirects=True)
      soup = BeautifulSoup(str(res.data), 'html.parser')
      found = soup.find_all('div', {'class': 'collection-card'})
      
      self.assertEqual(res.status_code, 200)
      self.assertIn('Access unauthorized', str(res.data))
      self.assertEqual(len(found), 0)

  def test_add_collect(self):
    """Test bookmarking park for specific user."""
    PARK_DATA_TEST = {
    "parkCode": "hijk",
    "parkName": "park hijk"
  }
    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.u1.id

      res = c.post('/api/collect', json=PARK_DATA_TEST)
      self.assertEqual(res.status_code, 200)

      collected = CollectedPark.query.filter(CollectedPark.park_code=='hijk').all()
      self.assertEqual(len(collected), 1)
      self.assertEqual(collected[0].user_id, self.u1.id)

  def test_invalid_add_collect(self):
    """Test collecting park via GET request and w/o user in sesssion."""
    with self.client as c:
      res = c.get('/api/collect', follow_redirects=True)
      self.assertIn('Invalid request', str(res.data))

  def test_delete_collected(self):
    """Test deleting a collected park."""
    self.setup_collected()

    with self.client as c:
      with c.session_transaction() as sess:
        sess[CURR_USER_KEY] = self.u1.id

      url = '/api/collect/abcd'

      res = c.delete(url)
      self.assertEqual(res.status_code, 200)

      c = CollectedPark.query.all()
      self.assertEqual(len(c), 1)
      self.assertIn('mnop', c[0].park_code)


