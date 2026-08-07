from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user

from extensions import db
from models import LostItem, FoundItem
from forms import LostItemForm, FoundItemForm, SearchForm
from utils import save_item_image

items_bp = Blueprint("items", __name__)


@items_bp.route("/report/lost", methods=["GET", "POST"])
@login_required
def report_lost():
    form = LostItemForm()
    if form.validate_on_submit():
        image_filename = save_item_image(form.image.data)
        item = LostItem(
            item_name=form.item_name.data.strip(),
            category=form.category.data,
            description=form.description.data.strip(),
            location_lost=form.location_lost.data.strip(),
            date_lost=form.date_lost.data,
            student_name=form.student_name.data.strip(),
            contact_number=form.contact_number.data.strip(),
            image_filename=image_filename,
            user_id=current_user.id,
        )
        db.session.add(item)
        db.session.commit()
        flash("Lost item reported successfully. We hope you find it soon!", "success")
        return redirect(url_for("items.item_details", item_type="lost", item_id=item.id))

    return render_template("items/report_lost.html", form=form)


@items_bp.route("/report/found", methods=["GET", "POST"])
@login_required
def report_found():
    form = FoundItemForm()
    if form.validate_on_submit():
        image_filename = save_item_image(form.image.data)
        item = FoundItem(
            item_name=form.item_name.data.strip(),
            category=form.category.data,
            description=form.description.data.strip(),
            location_found=form.location_found.data.strip(),
            date_found=form.date_found.data,
            finder_name=form.finder_name.data.strip(),
            contact_number=form.contact_number.data.strip(),
            image_filename=image_filename,
            user_id=current_user.id,
        )
        db.session.add(item)
        db.session.commit()
        flash("Found item reported successfully. Thank you for helping the campus!", "success")
        return redirect(url_for("items.item_details", item_type="found", item_id=item.id))

    return render_template("items/report_found.html", form=form)


@items_bp.route("/search")
def search():
    form = SearchForm(request.args, meta={"csrf": False})
    lost_results, found_results = [], []

    if request.args:
        keyword = (form.keyword.data or "").strip()
        category = form.category.data
        location = (form.location.data or "").strip()
        status = form.status.data
        item_type = form.item_type.data

        if item_type in ("", "lost"):
            q = LostItem.query
            if keyword:
                q = q.filter(LostItem.item_name.ilike(f"%{keyword}%"))
            if category:
                q = q.filter(LostItem.category == category)
            if location:
                q = q.filter(LostItem.location_lost.ilike(f"%{location}%"))
            if status:
                q = q.filter(LostItem.status == status)
            lost_results = q.order_by(LostItem.created_at.desc()).all()

        if item_type in ("", "found"):
            q = FoundItem.query
            if keyword:
                q = q.filter(FoundItem.item_name.ilike(f"%{keyword}%"))
            if category:
                q = q.filter(FoundItem.category == category)
            if location:
                q = q.filter(FoundItem.location_found.ilike(f"%{location}%"))
            if status:
                q = q.filter(FoundItem.status == status)
            found_results = q.order_by(FoundItem.created_at.desc()).all()

    return render_template("items/search.html", form=form,
                            lost_results=lost_results, found_results=found_results,
                            searched=bool(request.args))


@items_bp.route("/item/<item_type>/<int:item_id>")
def item_details(item_type, item_id):
    if item_type == "lost":
        item = LostItem.query.get_or_404(item_id)
    elif item_type == "found":
        item = FoundItem.query.get_or_404(item_id)
    else:
        abort(404)
    return render_template("items/item_details.html", item=item, item_type=item_type)
