from models import User, db, Post, Tag, PostTag
from app import app


# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
joe_smith = User(first_name='Joe', 
                    last_name='Smith', 
                    image_url = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png')

jane_smooth = User(first_name='Jane', 
                    last_name='Smooth', 
                    image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWomPds9w5emH_C6RY8xF7KRCJe6I5zwVsuw&usqp=CAU')

bob_korn = User(first_name='Bob', 
                    last_name='Korn', 
                    image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR77iOanUEwD6cR1bth7E0y0jnAJCnDH6Zp1Q&usqp=CAU')

p1 = Post(title = 'First Post!',
          content = 'Oh, hai',
          user_id = 1)

p2 = Post(title = 'Yet Another Post!',
          content = 'Oh, hi',
          user_id = 1)

p3 = Post(title = 'Flask is Awesome',
          content = 'flask is so cool!',
          user_id = 1)

tag1 = Tag(name='fun')

post_tag1= PostTag(post_id = 1,
                   tag_id = 1)
# Add new objects to session, so they'll persist
db.session.add(joe_smith)
db.session.add(jane_smooth)
db.session.add(bob_korn)
db.session.add(p1)
db.session.add(p2)
db.session.add(p3)
db.session.add(tag1)
# Commit--otherwise, this never gets saved!
db.session.commit()

db.session.add(post_tag1)
db.session.commit()