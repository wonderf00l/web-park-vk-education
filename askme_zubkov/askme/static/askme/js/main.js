function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(".btn.btn-primary.arrow.question.like").on("click", function (ev) {
    fetch("/question/react/", {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: 'question_id=' + $(this).data('id') + '&' + 'reaction=1',
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status == 'ok') {
            console.log(data.user_rating, data.total_rating);
            $(`#${$(this).data('id')}`).text(data.total_rating.toString());

            if (data.user_rating != 0) {
                $(this).attr("disabled", true);
            }
            else {
                $(`.btn.btn-primary.arrow.question.dislike.${$(this).data('id')}`).attr("disabled", false);
            }
        }
        else {
            console.log("error while setting like");
        }
    })
});

$(".btn.btn-primary.arrow.question.dislike").on("click", function (ev) {
    fetch("/question/react/", {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: 'question_id=' + $(this).data('id') + '&' + 'reaction=-1',
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status == 'ok') {
            console.log(data.user_rating, data.total_rating);
            $(`#${$(this).data('id')}`).text(data.total_rating.toString());
            
            if (data.user_rating != 0) {
                $(this).attr("disabled", true);
            }
            else {
                $(`.btn.btn-primary.arrow.question.like.${$(this).data('id')}`).attr("disabled", false);
            }
            
        }
        else {
            console.log("error while setting like");
        }
    })
});

$(".btn.btn-primary.arrow.answer.like").on("click", function (ev) {
    fetch("/answer/react/", {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: 'answer_id=' + $(this).data('id') + '&' + 'reaction=1',
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status == 'ok') {
            console.log(data.user_rating, data.total_rating);
            $(`#${$(this).data('id')}`).text(data.total_rating.toString());

            if (data.user_rating != 0) {
                $(this).attr("disabled", true);
            }
            else {
                $(`.btn.btn-primary.arrow.answer.dislike.${$(this).data('id')}`).attr("disabled", false);
            }
        }
        else {
            console.log("error while setting like");
        }
    })
});

$(".btn.btn-primary.arrow.answer.dislike").on("click", function (ev) {
    fetch("/answer/react/", {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": 'application/x-www-form-urlencoded;charset=UTF-8'
        },
        body: 'answer_id=' + $(this).data('id') + '&' + 'reaction=-1',
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status == 'ok') {
            console.log(data.user_rating, data.total_rating);
            $(`#${$(this).data('id')}`).text(data.total_rating.toString());
            
            if (data.user_rating != 0) {
                $(this).attr("disabled", true);
            }
            else {
                $(`.btn.btn-primary.arrow.answer.like.${$(this).data('id')}`).attr("disabled", false);
            }
            
        }
        else {
            console.log("error while setting like");
        }
    })
});
