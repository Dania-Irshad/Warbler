"""User message tests."""

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


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD1"
        )
        
        db.session.add(user)
        db.session.commit()

        self.user1 = user

        self.client = app.test_client()

    def tearDown(self):
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()
        db.session.rollback()

    def test_message_model(self):
        """Does basic model work?"""

        message = Message(
            text="first message"
        )

        db.session.add(message)
        db.session.commit()

        self.user.likes.append(message)
        db.session.commit()
        self.assertEqual(len(self.user.messages), 1)

