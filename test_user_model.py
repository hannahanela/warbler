"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
#from flask_bcrypt import ValueError

from models import db, User, Message, Follows, HASHED_PASSWORD_LENGTH

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

TEST_IMAGE_URL = "https://picsum.photos/id/237/200/300"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        db.session.rollback()
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()


    def tearDown(self):
        db.session.rollback()


    def test_user_model(self):
        u1 = User.query.get_or_404(self.u1_id)

        # User should have no messages & no followers
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)


    def test_repr_method(self):
        """Test repr method returns correct string for user.

        """
        u1 = User.query.get_or_404(self.u1_id)

        self.assertEqual(u1.__repr__(), f'<User #{u1.id}: u1, u1@email.com>')


    def test_is_following(self):
        """Test if is_following user method returns true when user1 is following
        user 2

        """
        u1 = User.query.get_or_404(self.u1_id)
        followed_user = User.query.get_or_404(self.u2_id)
        u1.following.append(followed_user)
        db.session.commit()

        is_following_result = u1.is_following(followed_user)

        self.assertTrue(is_following_result)


    def test_is_not_following(self):
        """Test if is_following user method returns false when user 1 is not 
        following user2

        """
        u1 = User.query.get_or_404(self.u1_id)
        not_followed_user = User.query.get_or_404(self.u2_id)

        is_following_result = u1.is_following(not_followed_user)

        self.assertFalse(is_following_result)


    def test_is_followed_by(self):
        """Test if is_followed_by user method returns true when user1 is 
        followed by user2

        """
        u1 = User.query.get_or_404(self.u1_id)
        following_user = User.query.get_or_404(self.u2_id)
        following_user.following.append(u1)
        db.session.commit()

        is_followed_by_result = u1.is_followed_by(following_user)

        self.assertTrue(is_followed_by_result)


    def test_is_not_followed_by(self):
        """Test if is_followed_by user method returns false when user1 is not
        followed by user2

        """
        u1 = User.query.get_or_404(self.u1_id)
        following_user = User.query.get_or_404(self.u2_id)

        is_followed_by_result = u1.is_followed_by(following_user)

        self.assertFalse(is_followed_by_result)

    def test_user_signup_successful(self):
        """Test if signup user method successfully:
            - hashes password
            - adds to database
            - returns instance of user.
        
        """
        test_user = User.signup(
            "u_test",
            "u_test@email.com",
            "test_password",
            TEST_IMAGE_URL,
            )

        # Test hashed password length is HASHED_PASSWORD_LENGTH.
        hashed_password = test_user.password
        self.assertEqual(len(hashed_password), HASHED_PASSWORD_LENGTH)

        # Test successfully added to db.
        test_user_in_db = User.query.filter_by(username='u_test').one_or_none()
        self.assertIsNotNone(test_user_in_db)

        # Test is instance of User.
        self.assertIsInstance(test_user, User)
        

    def test_user_signup_failure(self):
        """Test is user signup fails:
            - Cannot add user without a username
            - Cannot add user with same username
            - Cannot add user without a password
            - TODO:Cannot add user without an email
            
            """

        def attempt_no_username():
            User.signup(
                None,
                "u_test@email.com",
                "test_password",
                TEST_IMAGE_URL,
                ) 
            return 'attempt_no_username failed'           

        self.assertRaises(IntegrityError, attempt_no_username)
        db.session.rollback()

        def attempt_duplicate_username():
            User.signup(
                "u1",
                "u_test@email.com",
                "test_password",
                TEST_IMAGE_URL,
                ) 
            return 'create_duplicate_username failed'           

        self.assertRaises(IntegrityError, attempt_duplicate_username)
        db.session.rollback()
        
        def attempt_no_password():
            User.signup(
                "u_test",
                "u_test@email.com",
                None,
                TEST_IMAGE_URL,
                ) 
            return 'attempt_no_password failed'           

        self.assertRaises(ValueError, attempt_no_password)
        db.session.rollback()



       

        