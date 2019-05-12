let ifEnabled = true;

function checkFieldValue(reference, field) {
    if (window.event.keyCode === 13) {
        pycmd("ans");
        return;
    }

    if (! ifEnabled) {
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

function disableInstantFb() {
    ifEnabled = false;
}

function focusOnFirst() {
    setTimeout(() => {
        try {
            $('#typeans0').focus();
        } catch (error) {
            console.warn(error);
        }        
    }, 300);   
}