document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-button').forEach(button => {
        button.onclick = function () {
            const postId = this.dataset.postId;
            const action = this.dataset.action;
            fetch(`/api/likes/${postId}/${action}/`, {
                method: action === 'add_like' ? 'POST' : 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.detail) {
                    alert(data.detail);
                }
            });
        }
    });
});
