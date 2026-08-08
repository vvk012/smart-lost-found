import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from flask_mail import Message
from extensions import mail


def save_item_image(file_storage):
    """Saves an uploaded image securely and returns the stored filename,
    or None if no file was provided.

    Security measures:
    - secure_filename() strips path separators / dangerous characters.
    - A random UUID prefix prevents filename collisions and guessing.
    - Only extensions in ALLOWED_EXTENSIONS are ever accepted (also
      enforced client-side by FileAllowed() in the form).
    """
    if not file_storage or file_storage.filename == "":
        return None

    filename = secure_filename(file_storage.filename)
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in current_app.config["ALLOWED_EXTENSIONS"]:
        return None

    unique_name = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
    file_storage.save(save_path)
    return unique_name


def send_report_confirmation(to_email, recipient_name, item_name, item_type):
    """Sends a confirmation email after a lost/found report is submitted.

    Wrapped in try/except by the caller — a failed email should never
    break the report-submission flow (e.g. if SMTP creds aren't set up
    yet, or the campus wifi blocks outgoing SMTP).
    """
    verb = "lost" if item_type == "lost" else "found"
    subject = f"Report Received: {item_name} ({verb})"
    body = (
        f"Hi {recipient_name},\n\n"
        f"Your {verb} item report for \"{item_name}\" has been received "
        f"on the Campus Lost & Found Portal.\n\n"
        f"You can view and manage all your reports anytime from the "
        f"'My Reports' section of your dashboard.\n\n"
        f"— Campus Lost & Found Portal, ITS Engineering College"
    )
    msg = Message(subject=subject, recipients=[to_email], body=body)
    mail.send(msg)