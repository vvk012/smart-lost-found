from datetime import datetime
from extensions import db

CATEGORIES = ["ID Card", "Wallet", "Charger", "Earphones", "Laptop",
              "Keys", "Books", "Calculator", "Water Bottle", "Other"]


class LostItem(db.Model):
    __tablename__ = "lost_items"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location_lost = db.Column(db.String(150), nullable=False)
    date_lost = db.Column(db.Date, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    # Pending -> still missing | Claimed -> matched with a found report | Returned -> resolved
    status = db.Column(db.String(20), nullable=False, default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<LostItem {self.item_name}>"


class FoundItem(db.Model):
    __tablename__ = "found_items"

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location_found = db.Column(db.String(150), nullable=False)
    date_found = db.Column(db.Date, nullable=False)
    finder_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    # Pending -> awaiting claim | Claimed -> owner identified | Returned -> resolved
    status = db.Column(db.String(20), nullable=False, default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<FoundItem {self.item_name}>"
