from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample user."""
        User.query.delete() #delete all users

        user = User(first_name="TestFirstUser", last_name="TestLastUser", image_url='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')


        db.session.add(user)
        db.session.commit()
        # create a new user

        self.user_id = user.id
        self.user = user

    
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirstUser', html)

    def test_show_add_user(self):
        with app.test_client() as client:
            resp = client.get(f"/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> Create a User </h1>', html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name": "TestFirstUser2", "last_name": "TestLastUser2", "image_url": 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png'}
            resp = client.post("/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestFirstUser2 TestLastUser2 Details</h1>", html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestFirstUser TestLastUser Details</h1>', html)

    def test_show_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> Edit a User </h1>', html)


class PostTestCase(TestCase):

    def setUp(self):
        """Add sample post."""
        Post.query.delete() #delete all posts  
        User.query.delete() #delete all users 

        user = User(first_name="TestFirstUser", last_name="TestLastUser", image_url='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')

        db.session.add(user)
        db.session.commit()

        post = Post(title="TestTitle", content = "Test Content", user_id = 1 )

        db.session.add(post)
        db.session.commit()
        # create a new post

        self.post_id = post.id
        self.post = post
        self.user_id = user.id
        self.user = user
        
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_show_new_post(self):
        with app.test_client() as client:
            resp = client.get("/1/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> Add Post for TestFirstUserTestLastUser </h1>', html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "TestTitle2", "content": "TestContent2", "user_id": f"{self.user_id}"}
            resp = client.post(f"{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestFirstUser TestLastUser Details</h1>", html)

    def test_show_user_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestTitle</h1>', html)

    def test_show_edit_post_page(self):
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1> Edit Post </h1>', html)