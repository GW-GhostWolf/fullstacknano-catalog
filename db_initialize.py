#!/usr/bin/env python3
# Insert initial data into catalog database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_configuration import Base, User, Category, Item

engine = create_engine("postgres://catalog:newcatalogpassword@localhost/catalog")
Base.metadata.bind = engine
dbSession = sessionmaker(bind=engine)
session = dbSession()

# Default users because postgresql fails foreign key checks otherwise
session.add(User(name="Creator", email="mk.michael.phone@gmail.com"))
session.add(User(name="Michael", email="michael.poc@att.net"))
session.commit()

# Equipment for Bouldering
newCategory = Category(name="Bouldering", user_id=1)
session.add(newCategory)
newItem = Item(name="Crash Pad",
               description="landing area. don't want to hit the ground.",
               category=newCategory,
               user_id=1)
session.add(newItem)
newItem = Item(name="Climbing Shoes",
               description="aggressive climbing shoes are best for "
                           "bouldering. down turned toe.",
               category=newCategory,
               user_id=1)
session.add(newItem)
newItem = Item(name="Chalk Pot",
               description="leave the chalk on the ground. "
                           "routes aren't that long.",
               category=newCategory,
               user_id=2)
session.add(newItem)
session.commit()

# Equipment for Sport Climbing
newCategory = Category(name="Sport Climbing", user_id=1)
session.add(newCategory)
newItem = Item(name="Rope",
               description="safety first. don't want to hit the ground.",
               category=newCategory,
               user_id=1)
session.add(newItem)
newItem = Item(name="Draws",
               description="safety first. quick draws to attach to bolts.",
               category=newCategory,
               user_id=1)
session.add(newItem)
newItem = Item(name="Harness",
               description="safety first. attach to that rope somehow.",
               category=newCategory,
               user_id=1)
session.add(newItem)
newItem = Item(name="Climbing Shoes",
               description="moderate shoes work well for sport climbing. "
                           "routes can be long, so comfort matters",
               category=newCategory,
               user_id=2)
session.add(newItem)
newItem = Item(name="Chalk Bag",
               description="must attach to harness.",
               category=newCategory,
               user_id=2)
session.add(newItem)
session.commit()

# Equipment for Camping
newCategory = Category(name="Camping", user_id=1)
session.add(newCategory)
newItem = Item(name="Tent",
               description="unless you like bugs and rain.",
               category=newCategory,
               user_id=1)
session.add(newItem)
newItem = Item(name="Sleeping Bag",
               description="got to keep warm.",
               category=newCategory,
               user_id=2)
session.add(newItem)
session.commit()

# output results to see where we are
cats = session.query(Category).all()
for cat in cats:
    print(cat.id, cat.name)

items = session.query(Item).all()
for item in items:
    print(item.category.name, item.name, item.description)
