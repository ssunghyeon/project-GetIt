function num2str(count) {
    if (count > 10000) {
        return parseInt(count / 1000) + "k"
    }
    if (count > 500) {
        return parseInt(count / 100) / 10 + "k"
    }
    if (count == 0) {
        return ""
    }
    return count
}

function listing(username) {
    if (username == undefined) {
        username = ""
    }
    $('#cards-box').empty();
    $('#recentboard').addClass('is-active');
    $('#hotboard').removeClass('is-active');
    $('#mylist').addClass('is-active');
    $('#script').removeClass('is-active');
    $.ajax({
        type: "GET",
        url: `/listing?username_give=${username}`,
        data: {},
        success: function (response) {
            if (response['result'] == "success") {
                let cards = response['cards']
                for (let i = 0; i < cards.length; i++) {
                    let card = cards[i]
                    let file = card['file']
                    let temp_html = `<div class="card" id="${card['_id']}">
                                                <div class="card-image" onclick="location.href='/detail/${card['username']}/${card['_id']}'">
                                                    <figure class="image is-4by3">
                                                        <img src="../static/titleimg/${file}"
                                                             alt="Placeholder image">
                                                    </figure>
                                                </div>
                                                <div class="card-content">
                                                    <div class="content" style="margin-bottom: 15px; font-family: 'Poor Story', cursive;">
                                                        <a>${card['tag']}</a>                                                       
                                                    </div>
                                                    <div class="media" style="margin-bottom: 15px;">
                                                        <div class="media-left">
                                                            <a class="image is-48x48" href="/user/${card['username']}">
                                                                <img class="is-rounded" src="/static/${card['profile_pic_real']}" alt="Placeholder image">
                                                            </a>
                                                        </div>
                                                        <div class="media-content">
                                                            <p class="title is-4">${card['profile_name']}</p>
                                                            <p class="subtitle is-6">@${card['username']}</p>
                                                        </div>
                                                    </div>
                                                    <div class="content" style="font-size: 12px; display: flex; align-items: center; justify-content: space-between;">
                                                        <div class="date">
                                                            <p>${card['time']}</p>                                                                                                         
                                                        </div>
                                                        <div class="heart">
                                                            <i class="fa fa-heart" aria-hidden="true"></i>   
                                                            <span class="like_num">${num2str(card["count_heart"])}</span>                                                       
                                                        </div>
                                                    </div>
                                                </div>
                                     </div>`

                    $('#cards-box').append(temp_html)
                }
            }

        }
    })
}

function hotsting(username) {
    $('#cards-box').empty();
    $('#hotboard').addClass('is-active');
    $('#recentboard').removeClass('is-active');
    $.ajax({
        type: "GET",
        url: `/hotsting?username_give=${username}`,
        data: {},
        success: function (response) {
            if (response['result'] == "success") {
                let hotcards = response['hotcards']
                for (let i = 0; i < hotcards.length; i++) {
                    let card = hotcards[i]
                    let file = card['file']
                    let temp_html = `<div class="card" id="${card['_id']}">
                                                <div class="card-image" onclick="location.href='/detail/${card['username']}/${card['_id']}'">
                                                    <figure class="image is-4by3">
                                                        <img src="../static/titleimg/${file}"
                                                             alt="Placeholder image">
                                                    </figure>
                                                </div>
                                                <div class="card-content">
                                                    <div class="content" style="margin-bottom: 15px; font-family: 'Poor Story', cursive;">
                                                        <a>${card['tag']}</a>                                                       
                                                    </div>
                                                    <div class="media" style="margin-bottom: 15px;">
                                                        <div class="media-left">
                                                            <a class="image is-48x48" href="/user/${card['username']}">
                                                                <img class="is-rounded" src="/static/${card['profile_pic_real']}" alt="Placeholder image">
                                                            </a>
                                                        </div>
                                                        <div class="media-content">
                                                            <p class="title is-4">${card['profile_name']}</p>
                                                            <p class="subtitle is-6">@${card['username']}</p>
                                                        </div>
                                                    </div>
                                                    <div class="content" style="font-size: 12px; display: flex; align-items: center; justify-content: space-between;">
                                                        <div class="date">
                                                            <p>${card['time']}</p>                                                                                                         
                                                        </div>
                                                        <div class="heart">
                                                            <i class="fa fa-heart" aria-hidden="true"></i>   
                                                            <span class="like_num">${num2str(card["count_heart"])}</span>                                                       
                                                        </div>
                                                    </div>
                                                </div>
                                     </div>`

                    $('#cards-box').append(temp_html)
                }
            }

        }
    })
}

function starsting(username) {
    $('#cards-box').empty();
    $('#script').addClass('is-active');
    $('#mylist').removeClass('is-active');
    $.ajax({
        type: "GET",
        url: `/starsting?username_give=${username}`,
        data: {},
        success: function (response) {
            if (response['result'] == "success") {
                let cards = response['cards']
                for (let i = 0; i < cards.length; i++) {
                    let card = cards[i]
                    let file = card['file']
                    let temp_html = `<div class="card" id="${card['_id']}">
                                                <div class="card-image" onclick="location.href='/detail/${card['username']}/${card['_id']}'">
                                                    <figure class="image is-4by3">
                                                        <img src="../static/titleimg/${file}"
                                                             alt="Placeholder image">
                                                    </figure>
                                                </div>
                                                <div class="card-content">
                                                    <div class="content" style="margin-bottom: 15px; font-family: 'Poor Story', cursive;">
                                                        <a>${card['tag']}</a>                                                       
                                                    </div>
                                                    <div class="media" style="margin-bottom: 15px;">
                                                        <div class="media-left">
                                                            <a class="image is-48x48" href="/user/${card['username']}">
                                                                <img class="is-rounded" src="/static/${card['profile_pic_real']}" alt="Placeholder image">
                                                            </a>
                                                        </div>
                                                        <div class="media-content">
                                                            <p class="title is-4">${card['profile_name']}</p>
                                                            <p class="subtitle is-6">@${card['username']}</p>
                                                        </div>
                                                    </div>
                                                    <div class="content" style="font-size: 12px; display: flex; align-items: center; justify-content: space-between;">
                                                        <div class="date">
                                                            <p>${card['time']}</p>                                                                                                         
                                                        </div>
                                                        <div class="heart">
                                                            <i class="fa fa-heart" aria-hidden="true"></i>   
                                                            <span class="like_num">${num2str(card["count_heart"])}</span>                                                       
                                                        </div>
                                                    </div>
                                                </div>
                                     </div>`

                    $('#cards-box').append(temp_html)
                }
            }

        }
    })
}

function searchsting() {
    $('#cards-box').empty();
    $('#search-modal').removeClass('is-active');
    $('#recentboard').addClass('is-active');
    $('#hotboard').removeClass('is-active');
    let searchtext = $('#input-searchtext').val();
    $.ajax({
        type: "POST",
        url: '/searchsting',
        data: {
            searchtext_give : searchtext
        },
        success: function (response) {
            if (response['result'] == "success") {
                let cards = response['cards']
                for (let i = 0; i < cards.length; i++) {
                    let card = cards[i]
                    let file = card['file']
                    let temp_html = `<div class="card" id="${card['_id']}">
                                                <div class="card-image" onclick="location.href='/detail/${card['username']}/${card['_id']}'">
                                                    <figure class="image is-4by3">
                                                        <img src="../static/titleimg/${file}"
                                                             alt="Placeholder image">
                                                    </figure>
                                                </div>
                                                <div class="card-content">
                                                    <div class="content" style="margin-bottom: 15px; font-family: 'Poor Story', cursive;">
                                                        <a>${card['tag']}</a>                                                       
                                                    </div>
                                                    <div class="media" style="margin-bottom: 15px;">
                                                        <div class="media-left">
                                                            <a class="image is-48x48" href="/user/${card['username']}">
                                                                <img class="is-rounded" src="/static/${card['profile_pic_real']}" alt="Placeholder image">
                                                            </a>
                                                        </div>
                                                        <div class="media-content">
                                                            <p class="title is-4">${card['profile_name']}</p>
                                                            <p class="subtitle is-6">@${card['username']}</p>
                                                        </div>
                                                    </div>
                                                    <div class="content" style="font-size: 12px; display: flex; align-items: center; justify-content: space-between;">
                                                        <div class="date">
                                                            <p>${card['time']}</p>                                                                                                         
                                                        </div>
                                                        <div class="heart">
                                                            <i class="fa fa-heart" aria-hidden="true"></i>   
                                                            <span class="like_num">${num2str(card["count_heart"])}</span>                                                       
                                                        </div>
                                                    </div>
                                                </div>
                                     </div>`

                    $('#cards-box').append(temp_html)
                }
            }

        }
    })
}