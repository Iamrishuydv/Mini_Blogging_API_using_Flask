from flask import Blueprint, request
from models.models import db, Post, Comment
from .response import custom_response
from datetime import datetime
from http import HTTPStatus as status

comment = Blueprint('comment', __name__)

#------- Add comment on post by public --------
@comment.route('/add', methods=['POST'])
def add_comment():
    data = request.json
    post_id = data.get('postId')
    name = data.get('name')
    content = data.get('content')

    if not post_id or not name or not content:
        return custom_response("fail", message="postId, name, and content are required", status_code=status.BAD_REQUEST)

    post = Post.query.get(post_id)
    if not post:
        return custom_response("fail", message="Post not found", status_code=status.NOT_FOUND)

    new_comment = Comment(name=name, content=content, post=post)
    db.session.add(new_comment)
    db.session.commit()

    return custom_response("success", message="Comment added successfully", status_code=status.CREATED)

#--------- Get all comments for a post with pagination and limit (public view) ------
@comment.route('/list', methods=['POST'])
def get_comments():
    data = request.json or {}
    post_id = data.get('postId')
    page = int(data.get('page', 1))
    limit = int(data.get('limit', 10))

    post = Post.query.get(post_id)
    if not post:
        return custom_response("fail", message="Post not found", status_code=status.NOT_FOUND)

    query = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.desc())
    paginated = query.paginate(page=page, per_page=limit, error_out=False)
    comments = paginated.items

    comment_list = [
        {
            'id': c.id,
            'name': c.name,
            'content': c.content,
            'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M')
        }
        for c in comments
    ]

    return custom_response("success", data={
        "comments": comment_list,
        "page": page,
        "limit": limit,
        "total": paginated.total
    })
