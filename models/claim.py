from datetime import datetime
from extensions import db


class Claim(db.Model):
    __tablename__ = "claims"

    id = db.Column(db.Integer, primary_key=True)

    # The found item being claimed
    found_item_id = db.Column(
        db.Integer,
        db.ForeignKey("found_items.id"),
        nullable=False
    )

    # Student making the claim
    claimant_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # Secure verification answers
    identifying_detail = db.Column(db.Text, nullable=False)
    item_contents = db.Column(db.Text, nullable=False)
    special_mark = db.Column(db.Text, nullable=True)

    # Pending -> Approved / Rejected
    status = db.Column(
        db.String(20),
        nullable=False,
        default="Pending"
    )

    rejection_reason = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    reviewed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    found_item = db.relationship(
        "FoundItem",
        backref=db.backref(
            "claims",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    claimant = db.relationship(
        "User",
        backref=db.backref(
            "claims",
            lazy=True
        )
    )

    def __repr__(self):
        return f"<Claim {self.id} - {self.status}>"