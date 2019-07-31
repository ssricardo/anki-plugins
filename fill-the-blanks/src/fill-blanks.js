let ifEnabled = true;
let shouldIgnoreCase = false;

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

    cleanUpView(field);

    if (current == '' ) {
        field.data('lastValue', '');
        return;
    }

    if (shouldIgnoreCase) {
        current = current.toLowerCase();
        reference = reference.toLowerCase();
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

function cleanUpView(field) {
    field.removeClass('st-ok');
    field.removeClass('st-incomplete');
    field.removeClass('st-error');
}

function disableInstantFb() {
    ifEnabled = false;
}

function ignoreCaseOnFeedback() {
    shouldIgnoreCase = true;
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