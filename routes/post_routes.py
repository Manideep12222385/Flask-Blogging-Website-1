from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from controllers.post_controller import (
    list_posts, get_post, create_post, update_post, delete_post, list_drafts
)
from utils.roles import role_required
from forms.post_forms import PostForm
from models.user import RoleEnum

from forms.comment_form import CommentForm
from models.comment import Comment
from models.reaction import Reaction
from models.post import Post
from extensions import db

from sqlalchemy import or_     

post_bp = Blueprint('posts', __name__, url_prefix='/posts')

@post_bp.route('/')
@login_required
def show_posts():
    page = request.args.get('page', 1, type=int)
    pagination = list_posts(published=True, page=page)
    return render_template('posts.html', posts=pagination.items, pagination=pagination, title="Published Posts")

@post_bp.route('/drafts')
@login_required
@role_required('admin', 'publisher')
def drafts():
    page = request.args.get('page', 1, type=int)
    pagination = list_drafts(page=page)
    return render_template('posts.html', posts=pagination.items, pagination=pagination, title="Draft Posts")

@post_bp.route('/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = get_post(post_id)
    form = CommentForm()

    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(body=form.body.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash("💬 Comment added!", "success")
        return redirect(url_for('posts.post_detail', post_id=post.id))

    return render_template('post_detail.html', post=post, form=form)


@post_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'publisher')
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        create_post(form, current_user)
        flash('✅ Post created successfully!', 'success')
        return redirect(url_for('posts.show_posts'))

    return render_template('post_form.html', form=form, post=None)

@post_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'publisher')
def edit_post(post_id):
    post = get_post(post_id)

    if current_user.role == RoleEnum.PUBLISHER and post.author_id != current_user.id:
        flash("❌ You can only edit your own posts.", "danger")
        return redirect(url_for('posts.show_posts'))

    form = PostForm(obj=post)

    if form.validate_on_submit():
        update_post(post_id, form)
        flash("✅ Post updated successfully!", "success")
        return redirect(url_for('posts.post_detail', post_id=post_id))

    return render_template('post_form.html', form=form, post=post)

@post_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
@role_required('admin', 'publisher')
def delete_post_route(post_id):
    post = get_post(post_id)

    if current_user.role == RoleEnum.PUBLISHER and post.author_id != current_user.id:
        flash("❌ You can only delete your own posts.", "danger")
        return redirect(url_for('posts.show_posts'))

    delete_post(post_id)
    flash("🗑️ Post deleted successfully!", "info")
    return redirect(url_for('posts.show_posts'))

@post_bp.route('/mine')
@login_required
@role_required('admin', 'publisher')
def my_posts():
    page = request.args.get('page', 1, type=int)
    pagination = list_posts(published=True, page=page)
    my_posts = [post for post in pagination.items if post.author_id == current_user.id]
    return render_template('posts.html', posts=my_posts, title="My Posts")

@post_bp.route('/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = get_post(post_id)
    reaction = next((r for r in post.reactions if r.user_id == current_user.id), None)

    if reaction:
        db.session.delete(reaction)
        db.session.commit()
        flash("💔 Unliked the post.", "info")
    else:
        new_reaction = Reaction(user_id=current_user.id, post_id=post_id)
        db.session.add(new_reaction)
        db.session.commit()
        flash("❤️ Liked the post.", "success")

    return redirect(url_for('posts.post_detail', post_id=post_id))

@post_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    posts = []

    if query:
        posts = Post.query.filter(
            Post.is_published == True,
            or_(
                Post.title.ilike(f'%{query}%'),
                Post.body.ilike(f'%{query}%')
            )
        ).order_by(Post.created_at.desc()).all()
    
    return render_template('posts.html', posts=posts, title=f"Search Results for '{query}'")