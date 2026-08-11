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

# Who claimed this item as theirs, their proof/verification note, and when.
claimed_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
claim_message = db.Column(db.Text, nullable=True)
claimed_at = db.Column(db.DateTime, nullable=True)

claimant = db.relationship("User", foreign_keys=[claimed_by_id])


def __repr__(self):
    return f"<FoundItem {self.item_name}>"


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
class Claim(db.Model):
    """A student's claim that a found item belongs to them. The finder
    (the student who reported the found item) reviews the claim's proof
    details and contact info, then reaches out and marks the item
    Returned once ownership is confirmed."""
    __tablename__ = "claims"

    id = db.Column(db.Integer, primary_key=True)
    found_item_id = db.Column(db.Integer, db.ForeignKey("found_items.id"), nullable=False)
    claimant_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    proof_description = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    found_item = db.relationship("FoundItem", backref="claims")
    claimant = db.relationship("User", backref="claims")

    def __repr__(self):
        return f"<Claim on FoundItem {self.found_item_id} by User {self.claimant_id}>"