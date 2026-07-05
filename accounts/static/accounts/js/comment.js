console.log("comments.js loaded");
const form = document.getElementById("comment-form");
console.log(form);
form.addEventListener("submit", async function(e){

    e.preventDefault();

    const commentInput =
        document.getElementById("comment-input");

    const commentText =
        commentInput.value;

    const csrf =
        document.querySelector(
            "[name=csrfmiddlewaretoken]"
        ).value;

    const response = await fetch("", {

        method: "POST",

        headers: {
            "X-CSRFToken": csrf
        },

        body: new URLSearchParams({
            comment: commentText
        })

    });

    const data = await response.json();

    const commentsContainer =
        document.getElementById("comments-container");

    commentsContainer.insertAdjacentHTML(
        "afterbegin",

        `
        <div class="comment border rounded p-3 mb-2">
    <div>
        <strong>${data.username}</strong>
        <small class="text-muted ms-2">
            ${data.created_at}
        </small>
    </div>

    <div class="mt-1">
        ${data.content}
    </div>
</div>
        `
    );

    commentInput.value = "";

});