import "./ShowComment.css"
import { useSelector } from "react-redux";
import React, { useState, useEffect, useRef } from "react";
import CommentThreeDots from "../CommentThreeDots"



function ShowComment({ post, postComments }) {





    const sessionUser = useSelector(state => state.session.user);
    const allLikes = useSelector(state => state.likes.allLikes)
    // console.log("######", allLikes)
    // console.log(post.post_id)
    const myLikes = allLikes[post.post_id]
    const likedUsers = []
    if (myLikes.length) {

        for (let item of myLikes) {
            likedUsers.push(item.user_first_name + " " + item.user_last_name)
        }
        // console.log("&&&&", likedUsers)
    }




    const [showCommnet, setShowComment] = useState(true);
    const ulRef = useRef();

    const openComment = () => {
        if (showCommnet) return;
        setShowComment(true)
    }

    useEffect(() => {
        if (!showCommnet) return;

        const closeComment = (e) => {
            if (e.target.className === "comment-button") return;
            if (!ulRef.current) return
            if (!ulRef.current.contains(e.target)) {
                setShowComment(false);
            }
        };

        document.querySelector(".home-post-container")?.addEventListener("click", closeComment);

        return () => document.querySelector(".home-post-container")?.removeEventListener("click", closeComment);
    }, [showCommnet]);

    const ulClassName = "comment-dropdown" + (showCommnet ? "" : " hidden")
    // const closeComment = () => setShowComment(false)


    return (

        <>

            {postComments.length > 0 && (

                <div className="comment-like-count-line">

                    <div className="like-count-div">
                        {likedUsers.length ? (
                            `liked by ${likedUsers[likedUsers.length - 1]} and ${likedUsers.length - 1} others`
                        ) : (
                            <></>
                        )}

                    </div>
                    <button
                        className="show-comment-button"
                        onClick={openComment}
                    >{postComments.length} comments</button>

                </div>
            )}



            <ul
                className={ulClassName}
                ref={ulRef}
            >
                {
                    postComments.map(comment => {
                        // console.log(comment)

                        return (
                            <div className="comment-container">

                                <div className="comment-user-photo">

                                    <img className="comment-profile-photo" src={comment.comment_user_profile_photo} alt=""></img>


                                </div>
                                <div className="single-comment">
                                    <div className="name-plus-three-dots">
                                        <div className="comment-user-name-title">
                                            <div className="comment-user-name" key={comment.comment_user_first_name}>{comment.comment_user_first_name} {comment.comment_user_last_name}</div>
                                            <div className="comment-user-title">placeholder for user title</div>
                                        </div>
                                        {sessionUser && comment.comment_user_id == sessionUser.id && (
                                            <CommentThreeDots post={post} comment={comment} />
                                        )}


                                    </div>
                                    <div className="comment-content" key={comment.comment_content}>{comment.comment_content}</div>


                                </div>

                            </div>
                        )

                    })
                }
            </ul>


        </>

    )
}

export default ShowComment