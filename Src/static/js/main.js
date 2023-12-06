$(document).ready(function () {
    const $font = $('#font');
    const $color = $('#color');

    $font.change(function () {
        updateColorOptions($font.val());
    });

    function updateColorOptions(fontValue) {
        let colorOptions = '';

        switch (fontValue) {
            case '1':
            case '2':
                colorOptions = `
                    <option value="Blue">Blue</option>
                    <option value="Orange-1">Orange 1</option>
                    <option value="Orange-2">Orange 2</option>`;
                break;

            case '3':
            case '4':
                colorOptions = `
                    <option value="Blue">Blue</option>
                    <option value="Orange-1">Orange 1</option>`;
                break;

            case '5':
                colorOptions = `<option value="Orange-1">Orange 1</option>`;
                break;

            default:
                return;
        }

        $color.html(colorOptions);
    }
});

$(document).ready(function() {
    if (navigator.userAgent.indexOf("Firefox") != -1) {
    $("*").css({
        "scrollbar-color": "#1f1f1f #353535",
        "scrollbar-width": "12px"
    });
    }
});
