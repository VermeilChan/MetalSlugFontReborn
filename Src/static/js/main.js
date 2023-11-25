$(document).ready(function () {
    $('#font').change((function() {
        if ($('#font').val() == "1" || $('#font').val() == "2") {
            $('#color').html(
                `<option value=Blue>Blue</option>
                <option  value=Orange-1>Orange 1</option>
                <option  value=Orange-2>Orange 2</option>`
            )
        }
        else if ($('#font').val() == "3" || $('#font').val() == "4") {
            $('#color').html(
                `<option value=Blue> Blue</option>
                <option value=Orange-1> Orange 1</option>`
            )
        }
        else if ($('#font').val() == "5") {
            $('#color').html(
                `<option value=Orange-1 >Orange 1</option>`
            )
        }
        else {
            return null;
        }
    }))
})
