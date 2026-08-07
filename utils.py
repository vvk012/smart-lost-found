import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app


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
