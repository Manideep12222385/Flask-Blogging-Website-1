from flask import flash
from models.post import Post
from extensions import db
from utils.file_upload import save_file

def list_posts(published=True, page=1, per_page=5):
    return Post.query.filter_by(is_published=published) \
              .order_by(Post.created_at.desc()) \
              .paginate(page=page, per_page=per_page)

def get_post(post_id):
    return Post.query.get_or_404(post_id)


def create_post(form, user):
    if not form.title.data or not form.body.data:
        flash('All fields are required.', 'error')
        return None

    media_url = None
    if form.media.data:
        media_url = save_file(form.media.data)

    post = Post(
        title=form.title.data,
        body=form.body.data,
        is_published=form.is_published.data,
        author=user,
        media_url=media_url
    )
    db.session.add(post)
    db.session.commit()
    flash('Post created successfully!', 'success')
    return post

def update_post(post_id, form):
    post = get_post(post_id)
    if not form.title.data or not form.body.data:
        flash('All fields are required.', 'error')
        return None

    post.title = form.title.data
    post.body = form.body.data
    post.is_published = form.is_published.data
    db.session.commit()
    flash('✅ Post updated successfully!', 'success')
    return post

def delete_post(post_id):
    post = get_post(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('🗑️ Post deleted successfully!', 'info')

def list_drafts(page=1, per_page=5):
    return list_posts(published=False, page=page, per_page=per_page)
