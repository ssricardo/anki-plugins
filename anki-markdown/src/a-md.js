let mdNotice = '<div class="amd_edit_notice" title="This addon tries to prevent Anki from formatting as HTML">Markdown ON</div>';

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

function handleMdKey(evt) {
    if (evt.keyCode === 13 && ! evt.shiftKey) {

        if (currentField) {
            document.execCommand("insertHTML", false, "\n\n");
        }
        return false;
    }
}

function handleNoteAsMD() {
    $('.field').wrap('<pre class=\"amd\"></pre>');
    $('.field').keypress(handleMdKey);
}

// ----------------------------- Editor Previewer---------------

let previewInitialized = false;
let previewerStyle = `<style type="text/css">
#prev_layout {
    border: 0;
    width: 100%;
}
#preview {
}
#prev_toggler {        
    background-color: #777;
    width: 20px;
    text-align: center;
    line-height: 1.1;
    cursor: pointer;
    color: #FFF;
    vertical-align: middle;
    padding-top: 40px;
}
#fd_w_prev {
    vertical-align: top;
}
#col_field {
}

#preview {
    width: 40%;
    padding-left: 10px;
    overflow: auto;
}

#prev_layout .field {
    overflow: auto;
}
</style>`;

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
    $(previewerStyle).appendTo('body');
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