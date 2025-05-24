from flask import Blueprint, request
from flask_login import login_required, current_user
from models.models import db, Post
from .response import custom_response
from datetime import datetime
from http import HTTPStatus as status

post = Blueprint('post', __name__)

#--------  Create Blog Post ----------
@post.route('/create', methods=['POST'])
@login_required
def create_post():
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return custom_response("fail", message="Title and content are required", status_code=status.BAD_REQUEST)

    new_post = Post(title=title, content=content, author=current_user)
    db.session.add(new_post)
    db.session.commit()

    return custom_response("success", data={"postId": new_post.id}, message="Post created successfully", status_code=status.CREATED)


#-------- Get all blog posts (public view with pagination, filter and limit)----
@post.route('/all', methods=['POST'])
def get_all_posts():
    data = request.json or {}
    page = int(data.get('page', 1))
    limit = int(data.get('limit', 10))
    author_filter = data.get('author')
    title_filter = data.get('title')

    query = Post.query

    if author_filter:
        query = query.join(Post.author).filter(Post.author.has(username=author_filter))

    if title_filter:
        query = query.filter(Post.title.ilike(f"%{title_filter}%"))

    paginated = query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=limit, error_out=False)
    posts = paginated.items

    post_list = [
        {
            'id': p.id,
            'title': p.title,
            'content': p.content,
            'author': p.author.username,
            'timestamp': p.timestamp.strftime('%Y-%m-%d %H:%M')
        }
        for p in posts
    ]
    return custom_response("success", data={
        "posts": post_list,
        "page": page,
        "limit": limit,
        "total": paginated.total
    })

#----- Get post through post id ------
@post.route('/get-post', methods=['POST'])
def get_post():
    data = request.json
    post_id = data.get('postId')
    post = Post.query.get_or_404(post_id)
    post_data = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username,
        'timestamp': post.timestamp.strftime('%Y-%m-%d %H:%M')
    }
    return custom_response("success", data=post_data)

# Update a post (author can only update post via session login.)
@post.route('/update', methods=['PUT'])
@login_required
def update_post():
    data = request.json
    post_id = data.get('postId')
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return custom_response("fail", message="Unauthorized", status_code=status.FORBIDDEN)

    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()

    return custom_response("success", message="Post updated successfully")

# Delete a post (author can only delete post via session login.)
@post.route('/delete', methods=['DELETE'])
@login_required
def delete_post():
    data = request.json
    post_id = data.get('postId')
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        return custom_response("fail", message="Unauthorized", status_code=status.FORBIDDEN)

    db.session.delete(post)
    db.session.commit()
    return custom_response("success", message="Post deleted successfully")
