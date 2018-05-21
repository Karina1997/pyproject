$(document).ready(

    $(document).on('click', 'button.ajaxlike', function(e) {
    var data = $(this).data();
    console.log(data);
    var likesSpan = $('#likes-' + data.postid);
    $.ajax({url: data.url, method:'post'}).done(function(data, status, response) {
        alert(data);
        $(likesSpan).html(data)});
    return false;
}))

$(document).ready(
    function func () {

        function csrfSafeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", $('meta[name=csrf]').attr("content"));
                }
            }
        });

    }
)
