function initDragula() {
    var items = [... document.querySelectorAll('.tk-container')];
    dragula(items, {
        direction: 'horizontal',
        revertOnSpill: true,
        ignoreInputTextSelection: false
    });

    console.log('Nach dragula init');
}

function restoreOriginal() {
    document.querySelectorAll('.tkOriginalVal').forEach(element => {
        console.log('element')
        let ref = element.id.replace('originalVal-', '');
        let ulContainer = document.getElementById('tkContainer-' + ref);
        if (ulContainer != undefined) {
            ulContainer.style.display = 'none';
        }
        let textnode = document.createTextNode(element.value);
        element.parentElement.appendChild(textnode);
    })
    
}