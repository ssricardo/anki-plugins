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
            document.execCommand("insertHTML", false, "\\n\\n");
        }
        return false;
    }
}

function handleNoteAsMD() {
    $('.field').wrap('<pre class=\"amd\"></pre>');
    $('.field').keypress(handleMdKey);
}