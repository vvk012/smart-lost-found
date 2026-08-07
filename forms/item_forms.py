from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Optional

CATEGORY_CHOICES = [
    ("ID Card", "ID Card"), ("Wallet", "Wallet"), ("Charger", "Charger"),
    ("Earphones", "Earphones"), ("Laptop", "Laptop"), ("Keys", "Keys"),
    ("Books", "Books"), ("Calculator", "Calculator"),
    ("Water Bottle", "Water Bottle"), ("Other", "Other"),
]

STATUS_CHOICES = [("Pending", "Pending"), ("Claimed", "Claimed"), ("Returned", "Returned")]

PHONE_VALIDATOR = Regexp(r"^\d{10}$", message="Enter a valid 10-digit phone number")


class LostItemForm(FlaskForm):
    item_name = StringField("Item Name", validators=[DataRequired(), Length(max=100)])
    category = SelectField("Category", choices=CATEGORY_CHOICES, validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=1000)])
    location_lost = StringField("Location Lost", validators=[DataRequired(), Length(max=150)])
    date_lost = DateField("Date Lost", validators=[DataRequired()])
    student_name = StringField("Your Name", validators=[DataRequired(), Length(max=100)])
    contact_number = StringField("Contact Number", validators=[DataRequired(), PHONE_VALIDATOR])
    image = FileField("Upload Image (optional)", validators=[
        Optional(), FileAllowed(["jpg", "jpeg", "png", "gif", "webp"], "Images only!")
    ])
    submit = SubmitField("Report Lost Item")


class FoundItemForm(FlaskForm):
    item_name = StringField("Item Name", validators=[DataRequired(), Length(max=100)])
    category = SelectField("Category", choices=CATEGORY_CHOICES, validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired(), Length(max=1000)])
    location_found = StringField("Location Found", validators=[DataRequired(), Length(max=150)])
    date_found = DateField("Date Found", validators=[DataRequired()])
    finder_name = StringField("Your Name", validators=[DataRequired(), Length(max=100)])
    contact_number = StringField("Contact Number", validators=[DataRequired(), PHONE_VALIDATOR])
    image = FileField("Upload Image (optional)", validators=[
        Optional(), FileAllowed(["jpg", "jpeg", "png", "gif", "webp"], "Images only!")
    ])
    submit = SubmitField("Report Found Item")


class SearchForm(FlaskForm):
    class Meta:
        csrf = False  # search is a GET form, CSRF protection isn't needed

    keyword = StringField("Item Name", validators=[Optional(), Length(max=100)], default="")
    category = SelectField("Category", choices=[("", "All Categories")] + CATEGORY_CHOICES, validators=[Optional()], default="")
    location = StringField("Location", validators=[Optional(), Length(max=150)], default="")
    status = SelectField("Status", choices=[("", "All Statuses")] + STATUS_CHOICES, validators=[Optional()], default="")
    item_type = SelectField("Type", choices=[("", "Lost & Found"), ("lost", "Lost Only"), ("found", "Found Only")], validators=[Optional()], default="")
    submit = SubmitField("Search")
