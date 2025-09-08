from app import app, db
from models import Category

defaults = ["Category"]

with app.app_context():
    for name in defaults:
        if not Category.query.filter_by(name=name).first():
            db.session.add(Category(name=name))
    db.session.commit()

print("Default categories added!")
