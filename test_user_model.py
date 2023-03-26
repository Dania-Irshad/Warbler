"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1"
        )

        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD2"
        )
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.user1 = user1
        self.user2 = user2

        self.client = app.test_client()

    def tearDown(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.session.rollback()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def test_repr(self):
        self.assertEqual(self.user.__repr__(), f"<User #{self.id}: {self.username}, {self.email}>")

    def test_is_following(self):
        self.user1.following.append(self.user2)
        db.session.commit()

        self.assertEqual(self.user1.is_following(self.user2), True)
        self.assertEqual(self.user2.is_following(self.user1), False)
    

    def test_is_followed_by(self):
        self.user1.following.append(self.user2)
        db.session.commit()

        self.assertEqual(self.user2.is_followed_by(self.user1), True)
        self.assertEqual(self.user1.is_followed_by(self.user2), False)

    def test_user_authenticate(self):
        u = User.authenticate(self.user1.username, "HASHED_PASSWORD1")
        self.assertIsNone(u)
        self.assertEqual(User.authenticate("wrongusername", "HASHED_PASSWORD1"), False)
        self.assertEqual(User.authenticate(self.user1.username, "wrongpassword"), False)