from flask import Blueprint, jsonify,request,session
from flask_login import login_required,current_user
from app.models import db
from app.models import User
from app.models import Post
from app.forms import PostForm

post_routes=Blueprint("posts",__name__)

def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages

#get all posts
@post_routes.route("/")
def posts():
    all_posts = Post.query.order_by(Post.created_at.desc()).all()
    # print(all_posts[0].to_dict())
    all_users=User.query.all()
    # print(all_users.to_dict())

    for post in all_posts:
        # print(post.id)
        post.user_first_name=None
        post.user_last_name=None
        post.user_profile_photo=None
        post.user_title=None
        for user in all_users:
            if post.user_id ==user.id:
                post.user_first_name=user.first_name
                post.user_last_name=user.last_name
                post.user_profile_photo=user.profile_photo
                post.user_title=user.title

 
    
    data = {
        "posts":[{
            "post_id":post.id,
            "post_user_id":post.user_id,
            "post_user_first_name":post.user_first_name,
            "post_user_last_name":post.user_last_name,
            "post_content":post.post_content,
            "post_photo":post.post_photo,
            "created_at":post.created_at,
            "updated_at":post.updated_at,
            "profile_photo":post.user_profile_photo,
            "title":post.user_title
        } for post in all_posts]
    }

    return data

# get a post
@post_routes.route("/<int:postId>")
def post_by_id(postId):
  post = Post.query.get(postId)
  data={"post":[{
    "post_id":post.id,
    "post_content":post.post_content
  }]}

  return data

#create a post
@post_routes.route('/', methods=["POST"])
@login_required
def create_post():

  form = PostForm()
  form["csrf_token"].data = request.cookies["csrf_token"]

  if form.validate_on_submit():
    # post_photo = None
    # if "post_photo" in request.get_json():
    #     post_photo = request.get_json()["post_photo"]
    post = Post(
      user_id = int(current_user.id),
      post_content = request.get_json()["post_content"],
      post_photo = request.get_json().get("post_photo"),
      
    )


    db.session.add(post)
    db.session.commit()
    return post.to_dict()
  else:
    return {'errors': validation_errors_to_error_messages(form.errors)}, 400

  # if form.errors:
  #   return form.errors


#edit a post
@post_routes.route('/<int:postId>', methods=["PUT"])
@login_required
def edit_post_by_post_id(postId):
  post = Post.query.get(postId)
#   print("post at edit BE route--->",post.to_dict())
#   print("current user id ---->",current_user.id)
  if not post:
    return {"errors": ["post couldn't be found"]}, 404

  form = PostForm()
  form["csrf_token"].data = request.cookies["csrf_token"]

  if form.validate_on_submit():

    post.id=int(postId)
    post.user_id = int(current_user.id)
    post.post_content = request.get_json()["post_content"]
    post.post_photo = request.get_json()["post_photo"]
  

    db.session.commit()
    return post.to_dict()


  else:
     return {'errors': validation_errors_to_error_messages(form.errors)}, 400


#delete a post
@post_routes.route("/<int:postId>",methods=["DELETE"])
@login_required
def delete_post(postId):
    post=Post.query.get(postId)
    # print("!!!!!",post)
    if not post:
        return {"errors":["Post could not be found"]},404

    db.session.delete(post)
    db.session.commit()
    return {"message":["Post successfully deleted"]},200