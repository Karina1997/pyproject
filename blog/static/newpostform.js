$(document).ready(function () {

    function closeDialog() {
        $('.modal').modal('unshow')
    }
    function openDialog() {
        $('.modal').modal('show')
    }
    $(document).on('click', '.newpost', function (event) {
        openDialog();
        $.get(this.href, function (data) {
            $('#dialogBody').html(data);
        })
        event.preventDefault();
    })
})

$(document).on('submit', '[data-formtype="ajaxForm"]', function () {
    $.post(this.action, $(this).serialize(), function (data) {
        if (data == "OK") document.location.reload();
        else $('#dialogBody').html(data);
    });
    event.preventDefault();
})