

function checkFieldValue(reference, field) {
    if (window.event.keyCode === 13) {
        pycmd("ans");
        return;
    }    

    let current = field.val().trim();
    // console.log('Cur: ' + current + '; starts? ' + reference.startsWith(current));
    let previous = field.data('lastValue');

    if (current == previous) {
        return;
    }

    field.removeClass('st-ok');
    field.removeClass('st-incomplete');
    field.removeClass('st-error');

    if (current == '' ) {
        field.data('lastValue', '');
        return;
    }

    if (current == reference) {
        field.addClass('st-ok');
    } else {
        if (reference.startsWith(current)) {            
            field.addClass('st-incomplete');
        } else {
            field.addClass('st-error');
        }
    }
    field.data('lastValue', current);
}