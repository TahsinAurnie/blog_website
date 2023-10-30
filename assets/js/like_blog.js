const likeIcon = document.getElementById('like-icon')
const likeCount = document.getElementById('like-count')

likeIcon.onclick = () => {
    console.log('clicked')
    const blogId = likeIcon.getAttribute('data-blog');
    // call view by the blog-id
    const url = `/like_blog/${parseInt(blogId)}/`;
    fetch(url, {
        method: 'GET',
        headers: {
            "Content-type": 'application/json'
        }
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        console.log(data)
        if(data.liked){
            likeIcon.classList.remove('empty-heart')
        }
        else{
            likeIcon.classList.add('empty-heart')
        }
        likeCount.innerHTML = data.like_count;
    })
    .catch(error => {
        console.log(error)
    })
}
