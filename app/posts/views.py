import os
import secrets
from PIL import Image
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.posts.forms import CreatePostForm, UpdatePostForm, CreateCategoryForm, UpdateCategoryForm, CreateTagForm, \
    UpdateTagForm
from app.posts.models import Posts, Categories, Tags, post_tags
from app import db
from config import APP_ROOT_PATH
from . import posts_bp
from app.posts.posts_config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, MAX_IMAGE_SIZE


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def resize_and_save_image(file, destination_folder, target_size):
    img = Image.open(file)
    img.thumbnail(target_size)

    random_string = secrets.token_hex(10)
    original_filename, file_extension = os.path.splitext(secure_filename(file.filename))
    new_filename = f"{random_string}{file_extension}"
    image_path = os.path.join(destination_folder, new_filename)

    try:
        img.save(image_path)
        return image_path
    except Exception as e:
        flash(f"Error saving image: {e}", category="flash-error")
        return None


@posts_bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        type = form.type.data
        image_file = form.image_file.data
        category_id = form.category.data
        enabled = form.enabled.data

        if image_file and allowed_file(image_file.filename):
            image_path = resize_and_save_image(image_file, UPLOAD_FOLDER, MAX_IMAGE_SIZE)
            image_path = os.path.basename(image_path)
        else:
            image_path = None

        new_post = Posts(title=title, text=text, type=type, image_file=image_path,
                         user_id=current_user.id, category_id=category_id, enabled=enabled)

        db.session.add(new_post)
        db.session.commit()

        selected_tags = form.tag.data
        for tag_id in selected_tags:
            tag = Tags.query.get(tag_id)
            if tag:
                new_post.tags.append(tag)

        db.session.commit()

        flash('Post added successfully!', 'flash-success')
        return redirect(url_for('posts.view_posts'))
    return render_template('create_post.html', form=form)


@posts_bp.route('/view_posts', methods=['GET'])
@login_required
def view_posts():
    page = request.args.get('page', 1, type=int)
    posts = Posts.query.order_by('id', 'created').paginate(page=page, per_page=5)
    image_path = url_for('static', filename='posts_images/')
    return render_template('posts_list.html', posts=posts, image_path=image_path)


@posts_bp.route("/view_post/<int:id>", methods=['GET', 'POST'])
@login_required
def view_post(id):
    post = Posts.query.get_or_404(id)
    image_path = url_for('static', filename='posts_images/')
    created_at = post.created
    category = (Categories.query.get_or_404(post.category_id)).name
    return render_template('view_post.html', post=post, image_path=image_path, created_at=created_at, category=category)


@posts_bp.route('/update_post/<int:id>', methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Posts.query.get_or_404(id)
    if post.user_id != current_user.id:
        flash('You are not authorized to update this post!', 'flash-error')
        return redirect(url_for('posts.view_posts'))

    current_post_image = post.image_file

    form = UpdatePostForm(
        title=post.title,
        text=post.text,
        type=post.type
    )
    if form.validate_on_submit():
        old_image_path = post.image_file
        old_file_name = os.path.basename(old_image_path)
        app_static_folder = os.path.join(APP_ROOT_PATH, 'static')
        full_old_image_path = os.path.join(app_static_folder, 'posts_images', old_file_name)
        new_image_file = form.image_file.data
        if new_image_file:
            image_path = resize_and_save_image(new_image_file, UPLOAD_FOLDER, MAX_IMAGE_SIZE)
            if image_path:
                post.image_file = os.path.basename(image_path)
                if full_old_image_path and os.path.isfile(
                        full_old_image_path) and current_post_image != 'postdefault.jpg':
                    os.remove(full_old_image_path)

        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        post.category_id = form.category.data

        db.session.commit()
        flash('Post updated successfully!', 'flash-success')
        return redirect(url_for('posts.view_post', id=post.id))

    return render_template('update_post.html', form=form, post=post)


@posts_bp.route('/delete_post/<int:id>')
@login_required
def delete_post(id):
    post = Posts.query.get_or_404(id)
    if post.user_id != current_user.id:
        flash('You are not authorized to delete this post!', 'flash-error')
        return redirect(url_for('posts.view_posts'))

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'flash-success')
    return redirect(url_for('posts.view_posts'))


@posts_bp.route('/create_category', methods=['GET', 'POST'])
@login_required
def create_category():
    form = CreateCategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        new_category = Categories(name=name)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully!', 'flash-success')
        return redirect(url_for('posts.view_categories'))
    return render_template('create_category.html', form=form)


@posts_bp.route('/view_categories', methods=['GET'])
def view_categories():
    categories_with_forms = [{"id": c.id, "form": UpdateCategoryForm(name=c.name)} for c in Categories.query.all()]
    form = CreateCategoryForm()
    return render_template('categories_list.html', categories=categories_with_forms, form=form)


@posts_bp.route('/update_category/<int:id>', methods=['GET', 'POST'])
@login_required
def update_category(id):
    category = Categories.query.get_or_404(id)

    form = UpdateCategoryForm(
        name=category.name
    )
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated successfully!', 'flash-success')

    return redirect(url_for('posts.view_categories'))


@posts_bp.route('/delete_category/<int:id>')
@login_required
def delete_category(id):
    category = Categories.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'flash-success')
    return redirect(url_for('posts.view_categories'))


@posts_bp.route('/create_tag', methods=['GET', 'POST'])
@login_required
def create_tag():
    form = CreateTagForm()
    if form.validate_on_submit():
        name = form.name.data
        new_tag = Tags(name=name)
        db.session.add(new_tag)
        db.session.commit()
        flash('Tag was added successfully!', 'flash-success')
        return redirect(url_for('posts.view_tags'))
    return render_template('create_tag.html', form=form)


@posts_bp.route('/view_tags', methods=['GET'])
def view_tags():
    page = request.args.get('page', 1, type=int)
    tags = Tags.query.paginate(page=page, per_page=5)
    return render_template('tags_list.html', tags=tags)


@posts_bp.route("/view_tag/<int:id>", methods=['GET', 'POST'])
def view_tag(id):
    tag = Tags.query.get_or_404(id)
    posts = Posts.query.join(post_tags).filter(post_tags.c.tag_id == id).all()
    return render_template('view_tag.html', tag=tag, posts=posts)


@posts_bp.route('/update_tag/<int:id>', methods=['GET', 'POST'])
@login_required
def update_tag(id):
    tag = Tags.query.get_or_404(id)

    form = UpdateTagForm(
        name=tag.name
    )
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.commit()
        flash('Tag was updated successfully!', 'flash-success')
        return redirect(url_for('posts.view_tag', id=tag.id))

    return render_template('update_tag.html', form=form, tag=tag)


@posts_bp.route("/delete_tag/<int:id>")
@login_required
def delete_tag(id):
    tag = Tags.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag was successfully deleted", "flash-success")
    return redirect(url_for("posts.view_tags"))
