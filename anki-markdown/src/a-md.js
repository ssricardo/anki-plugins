let mdNotice = '<div class="amd_edit_notice" title="This addon tries to prevent Anki from formatting as HTML">Markdown ON</div>';

function pasteAmdContent(inputValue) {
    let focused = $(':focus');
    if (! focused || focused == 'undefined') {
        return;
    }

    let selection = undefined
    try {
        selection = window.getSelection()
    } catch (e) {
        console.warn(e)
    }

    if (focused.is('input') || focused.is('textarea')) {
        if (!selection) {
            let ta = focused.get()[0]
            selection = ta.value.substring(ta.selectionStart, ta.selectionEnd);
        }

        let newVal = (selection && selection != '') ? focused.val().replace(selection, inputValue) : focused.val() + inputValue;
        focused.val(newVal);
    } else {
        let newVal = (selection && selection != '') ? focused.text().replace(selection, inputValue) : focused.text() + inputValue;
        focused.text(newVal);
    }
}

function showMarkDownNotice() {
    return; // FIXME: getting JS error

    let shownNotice = $('.amd_edit_notice').length;
    if (!shownNotice) {
        $('#fields').prepend(mdNotice);
    }    
}

function getFieldId(originalField, ankiOrd) {
    let id = originalField.attr('id');

    if (!id) {
        id = `f_${ankiOrd}`
    }
    return id;
}

function getFieldVal(originalField) {
    let nativeField = originalField.get()[0]
    let text = nativeField.fieldHTML
    return {nativeField, text};
}

function convertToTextArea(originalField, parent) {
    let attrs = { };

    let name = originalField.attr('name');
    let ankiOrd = originalField.attr('ord');

    let id = getFieldId(originalField, ankiOrd);
    let {nativeField, text} = getFieldVal(originalField);

    let newTa = $("<textarea />", attrs)
        .attr('id', 'mirror--' + id)
        .attr('name', 'mirror--' + (name) ? name : id)
        .attr('data-origin', id)
        .attr('ord', ankiOrd)
        .val(text)
        .attr('class', 'clearfix field')
        .on('input', function(evt) {
            if (evt.which === 27) {
                currentField.blur();
                return;
            }
            nativeField.fieldHTML = ( $(this).val() );
            dispatchInput(originalField[0]);
        } )
        .focus(function() {
            currentField = originalField[0];
            pycmd("focus:" + ankiOrd);
            // enableButtons();        // aparently removed on newer versions

            $.each($("#topbutsright > button"), function() {
                let field = $(this).removeAttr('disabled')
            });
        })
        .blur(function() {
            var event = new Event('blur', {
                bubbles: true,
                cancelable: true,
            });

            originalField[0].dispatchEvent(event);
        });
    parent.append(newTa)
}

function dispatchInput(originalField) {
    var event = new Event('input', {
        bubbles: true,
        cancelable: true,
    });

    originalField.dispatchEvent(event);
}

function handleNoteAsMD() {
    if (isAmdActive()) {
        updateFieldsValues();
        return;
    }
    $('.field').wrap('<span class="amd amd-active"></span>');
    $('.field').wrap('<span class="original-field"></span>');

    $.each($(".field"), function() {
        let field = $(this)
        let amdRoot = field.parent().parent()
        convertToTextArea(field, amdRoot);
    });
}

function updateFieldsValues() {
    $.each($(".field"), function () {
        let field = $(this)
        let ord = field.attr('ord');
        let id = getFieldId(field, ord)
        let {nativeField, text} = getFieldVal(field)
        $(`#mirror--${id}`).val(text)
    });
}

function isAmdActive() {
    return ($('.amd-active').length);
}

function removeMdDecoration() {
    $('.amd').
        css('border-left', 'none');
}

// ----------------------------- Editor Previewer---------------

let previewInitialized = false;

let showMarkdown = null;
let hideMarkdown = null;

function setPreviewUp() {
    $(`<table id="prev_layout">
        <tr id="fd_w_prev">
            <td id="col_field"></td>
            <td id="prev_toggler" onclick="togglePreview()">            
            </td>
            <td id="preview" class="ui-resizable">
                <i>Markdown preview</i>
            </td>
        </tr>
    </div>`).insertAfter('#topbutsOuter');
    let originalFields = $('#fields').detach();
    $('#col_field').prepend(originalFields);    
    previewInitialized = true;
    showMarkdown = 'S<br/>h<br/>o<br/>w<br/><br/>M<br/>a<br/>r<br/>k<br/>d<br/>o<br/>w<br/>n<br/>';
    hideMarkdown = 'H<br/>i<br/>d<br/>e<br/><br/>M<br/>a<br/>r<br/>k<br/>d<br/>o<br/>w<br/>n<br/><br/>';
    $('#prev_toggler').html(hideMarkdown);
}

function setFieldPreview(name, value) {
    if (! previewInitialized) {
        return;
    }
    let element = $('#pvalue' + name);
    if (! element.length) {
        $('#preview').append(`
            <div id="pfd` + name + `">
                <h4>` + name + `</h4>
                <p id="pvalue`+ name + `"></p>
            </div>
        `);
        element = $('#pvalue' + name);
    }
    element.html(value);
}

function cleanPreview() {
    $('#preview').empty();
}

function togglePreview() {
    let prevDiv = $('#preview');
    if (prevDiv.css('display') == 'none') {
        prevDiv.css('display', '');
        $('#prev_toggler').html(hideMarkdown);
    } else {
        prevDiv.css('display', 'none');
        $('#prev_toggler').html(showMarkdown);
    }
}
