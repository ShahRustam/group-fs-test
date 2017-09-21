/**
 * Created by Rustam on 20.10.2016.
 */
$('.form-control').on('focus', function () {
    var $this = $(this),
        formGroupBlock = $this.closest('.form-group');

    var label = $("label[for='" + $(this).attr('id') + "']").find('.error-message');
    $this.removeClass('input--error');
    label.remove();
});

$("input[type='checkbox']").on('click', function () {
    var $this = $(this);

    var label = $("label[for='" + $(this).attr('id') + "']").find('.error-message');
    $this.removeClass('input--error');
    label.remove();
});

$('body').keypress(function (e) {
    var key = e.which;
    if (key == 13) {
        var button = $(".onEnterSubmit");
        if (button.length) {
            button[0].onclick();
        }
    }
});
function GoTo(section) {
    window.scrollTo(0, $("#" + section).offset().top - 50);
}
