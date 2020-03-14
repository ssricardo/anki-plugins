let mdNotice = '<div class="amd_edit_notice" title="This addon tries to prevent Anki from formatting as HTML">Markdown ON</div>';
let amdActive = false;

function pasteAmdContent(inputValue) {
    let focused = $(':focus');
    if (! focused || focused == 'undefined') {
        return;
    }
    let selection = window.getSelection()
    if (focused.is('input') || focused.is('textarea')) {
        let newVal = (selection && selection != '') ? focused.val().replace(selection, inputValue) : focused.val() + inputValue;
        focused.val(newVal);
    } else {
        let newVal = (selection && selection != '') ? focused.text().replace(selection, inputValue) : focused.text() + inputValue;
        focused.text(newVal);
    }
}

function showMarkDownNotice() {
    let shownNotice = $('.amd_edit_notice').length;
    if (! shownNotice) {
        $('#fields').prepend(mdNotice);
    }    
}

function convertToTextArea(originalField) {
    var attrs = { };

    var name = originalField.attr('name');
    var id = originalField.attr('id');
    var text = originalField.text();

    $("<textarea />", attrs)
        .attr('id', 'mirror--' + id)
        .attr('name', 'mirror--' + (name) ? name : id)
        .attr('data-origin', id)
        .val(text)
        .attr('class', 'field clearfix')
        .on('input', function(evt) {
            if (evt.which === 27) {
                currentField.blur();
                return;
            }
            originalField.text( $(this).val() );

            dispatchInput(originalField[0]);
        } )
        .focus(function() {
            currentField = originalField[0];
            pycmd("focus:" + currentFieldOrdinal());
            enableButtons();
        })
        .blur(function() {
            var event = new Event('blur', {
                bubbles: true,
                cancelable: true,
            });

            originalField[0].dispatchEvent(event);
        })
        .insertAfter('#' + id);

    originalField.css('display', 'none');
}

function dispatchInput(originalField) {
    var event = new Event('input', {
        bubbles: true,
        cancelable: true,
    });

    originalField.dispatchEvent(event);
}

function handleNoteAsMD() {
    if (amdActive) {
        console.log('amd is already active');
        return;
    }
    $('.field').wrap('<span class=\"amd\"></span>');

    $.each($(".field"), function() {
        convertToTextArea($(this));
    });
    amdActive = true;
}

function disableAmd() {
    amdActive = false;
}

$(function() {
  if (wrapInternal) {
    var originalWrapInternal = wrapInternal;
    wrapInternal = function (front, back, plainText) {
        if (! amdActive) {
            return originalWrapInternal(front, back, plainText);
        }

        if (! currentField) {
            return;
        }

        let currentMirror = $('#mirror--' + currentField.id);
        if (! currentMirror) {
            console.warn('Anki Markdown seems not correctly sync. No mirror for : ' + currentField.id);
            return originalWrapInternal(front, back, plainText);
        }

        let cFocus = currentMirror[0];

        if (cFocus.selectionStart || cFocus.selectionStart == '0') {
//            cFocus.value = cFocus.value.substring(0, cFocus.selectionStart) + front +
//                cFocus.value.substring(cFocus.selectionStart, cFocus.selectionEnd) + back +
//                cFocus.value.substring(cFocus.selectionEnd);

            let newTxt = front +
                cFocus.value.substring(cFocus.selectionStart, cFocus.selectionEnd) + back;

            document.execCommand('insertText', false, newTxt);
        } else {
            document.execCommand('insertText', false, front + back);
        }
    }
  }
});

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
