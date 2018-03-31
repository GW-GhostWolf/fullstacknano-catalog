#!/usr/bin/env python3
# Insert initial data into catalog database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_configuration import Base, Category, Item

engine = create_engine("sqlite:///categlog.db")
Base.metadata.bind = engine
dbSession = sessionmaker(bind=engine)
session = dbSession()

# Equipment for Bouldering
newCategory = Category(name="Bouldering")
session.add(newCategory)
newItem = Item(name="Crash Pad",
               description="landing area. don't want to hit the ground.",
               category=newCategory)
session.add(newItem)
newItem = Item(name="Climbing Shoes",
               description="aggressive climbing shoes are best for "
                           "bouldering. down turned toe.",
               category=newCategory)
session.add(newItem)
newItem = Item(name="Chalk Pot",
               description="leave the chalk on the ground. "
                           "routes aren't that long.",
               category=newCategory)
session.add(newItem)
session.commit()

# Equipment for Sport Climbing
newCategory = Category(name="Sport Climbing")
session.add(newCategory)
newItem = Item(name="Rope",
               description="safety first. don't want to hit the ground.",
               category=newCategory)
session.add(newItem)
newItem = Item(name="Draws",
               description="safety first. quick draws to attach to bolts.",
               category=newCategory)
session.add(newItem)
newItem = Item(name="Harness",
               description="safety first. attach to that rope somehow.",
               category=newCategory)
session.add(newItem)
newItem = Item(name="Climbing Shoes",
               description="moderate shoes work well for sport climbing. "
                           "routes can be long, so comfort matters",
               category=newCategory)
session.add(newItem)
newItem = Item(name="Chalk Bag",
               description="must attach to harness.",
               category=newCategory)
session.add(newItem)
session.commit()

# Equipment for Camping
newCategory = Category(name="Camping")
session.add(newCategory)
newItem = Item(name="Tent",
               description="unless you like bugs and rain.",
               category=newCategory)
session.add(newItem)
newItem = Item(name="Sleeping Bag",
               description="got to keep warm.",
               category=newCategory)
session.add(newItem)
session.commit()

# output results to see where we are
cats = session.query(Category).all()
for cat in cats:
    print(cat.id, cat.name)

items = session.query(Item).all()
for item in items:
    print(item.category.name, item.name, item.description)