var nextPositionMap = new Map();

function initTokenizer() {
    let items = [... document.querySelectorAll('.tk-container')];
    dragula(items, {
        direction: 'horizontal',
        revertOnSpill: true,
        ignoreInputTextSelection: false
    }).on('drop', function (el) {
        console.log(el);
        console.log(el.parent);
        console.log(el.parentElement);
        resetMarkerCurrent(el.parentElement);
    });

    items.forEach(container => {
        nextPositionMap.set(container.id, 0);
        container.querySelectorAll('li').forEach(e => {
            e.addEventListener("click", e => setNextItem(e, container));
        });
        resetMarkerCurrent(container);
    });
}

function setNextItem(elem, parent) {
    let nextPosition = nextPositionMap.get(parent.id);
    let curIndex = Array.from(parent.children).indexOf(elem.target);

    if (nextPosition < curIndex) {
        parent.children[nextPosition].before(elem.target);
    } else {
        parent.children[nextPosition].after(elem.target);
    }

    if (nextPosition < parent.childElementCount - 1) {
        nextPosition++;
        nextPositionMap.set(parent.id, nextPosition)
    }
    resetMarkerCurrent(parent);
}

function resetMarkerCurrent(parent) {
    let nextPosition = nextPositionMap.get(parent.id);
    $(parent.children).removeClass('current-pos');
    $(parent.children[nextPosition]).addClass('current-pos');
}

// ----------------------- Handling result ---------------------

function getResult() {
    let containers = [... document.querySelectorAll('.tk-container')];
    return containers.map(cn => [... cn.querySelectorAll('li')].map(e => e.innerText).join(" "))
}

function setFeedback(results) {    
    document.querySelectorAll(".tk-feedback").forEach(elem => {
        if (results.length > 0) {
            elem.style.display = 'block';
            elem.innerText = '(' + results[0] + ')';
            results.splice(0, 1)
        }
    });
}

// Used only on test
function restoreOriginal() {
    document.querySelectorAll('.tkOriginalVal').forEach(element => {
        let ref = element.id.replace('originalVal-', '');
        let ulContainer = document.getElementById('tkContainer-' + ref);
        if (ulContainer != undefined) {
            ulContainer.style.display = 'none';
        }
        let textnode = document.createTextNode(element.value);
        element.parentElement.appendChild(textnode);
    })
    
}
