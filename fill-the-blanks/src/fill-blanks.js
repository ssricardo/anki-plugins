let ifEnabled = true;
let shouldIgnoreCase = false;
let shouldIgnoreAccents = false;
var typedWords = [];

function checkFieldValue(reference, fieldIndex) {
    if (window.event.keyCode === 13) {
        pycmd("ans");
        return;
    }
    let field = $('#typeans' + fieldIndex);

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

    if (shouldIgnoreAccents) {
        current = current.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
        reference = reference.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
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
    updateTypedValue(fieldIndex);
}

function cleanUpView(field) {
    field.removeClass('st-ok');
    field.removeClass('st-incomplete');
    field.removeClass('st-error');
}

// ------------- Verification ---------------
function cleanUpTypedWords() {
    typedWords = [];
}

function prepareTypedWords(numFields) {
    for (let i = 0; i < numFields; i++) {
        typedWords.push("");
    }
}

function updateTypedValue(position) {
    let content = $("#typeans" + position).val().trim();
    typedWords[position] = content;
}

// --------------- Options ------------------

function disableInstantFb() {
    ifEnabled = false;
}

function ignoreCaseOnFeedback() {
    shouldIgnoreCase = true;
}

function ignoreAccentsOnFeedback() {
    shouldIgnoreAccents = true;
}

// ------------------------------------

function focusOnFirst() {
    setTimeout(() => {
        try {
            $('#typeans0').focus();
        } catch (error) {
            console.warn(error);
        }        
    }, 300);   
}