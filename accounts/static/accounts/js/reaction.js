
const hearts =
    document.querySelectorAll(".like-icon");

const csrf = document.querySelector("input[name=csrfmiddlewaretoken]").value;

hearts.forEach((heart) => {

    heart.addEventListener(
        "click",

        async function() {

            const blogId =
                this.dataset.blogId;

            const response =
                await fetch(
                    `/blog/react/${blogId}/`,
                    {
                        method: "POST",

                        headers: {
                            "X-CSRFToken": csrf
                        }
                    }
                );

            const data =
                await response.json();

            if(data.liked){

                this.classList.remove(
                    "bi-heart"
                );

                this.classList.add(
                    "bi-heart-fill","text-danger"
                );

            } else {

                this.classList.remove(
                    "bi-heart-fill"
                );

                this.classList.add(
                    "bi-heart"
                );

            }

        }
    );

});

