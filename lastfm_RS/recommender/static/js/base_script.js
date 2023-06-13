var isToggled = true;

/* Toggle sidebar */
function toggleNav() {
    let nav = document.querySelector("#sidebar"),
        content = document.querySelector(".col-sm-10"),
        btn = document.querySelector(".sidebar-btn"),
        row = document.querySelector("#sidebar-btn-row"),
        navW = nav.clientWidth;

    if (isToggled) {
        btn.style.transform = "rotate(180deg)";
        nav.style.marginLeft = `-${navW + 2}px`;
        content.style.flexBasis = "100%";
        row.style.maxHeight = "100vh";
        isToggled = false;
    }
    else if (!isToggled) {
        btn.style.transform = "";
        nav.style.marginLeft = 0;
        content.style.flexBasis = "88%";
        row.style.maxHeight = 0;
        isToggled = true;
    }
}

/* Copies an element's content */
function copyEvent(id) {
    var copyText = document.getElementById(id);
    selectText(copyText);

    // Copy the text inside the element
    if (navigator.clipboard)
        navigator.clipboard.writeText(copyText.textContent);
}

/* Select an element's content */
function selectText(node) {
    if (document.body.createTextRange) {
        const range = document.body.createTextRange();
        range.moveToElementText(node);
        range.select();
    } else if (window.getSelection) {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(node);
        selection.removeAllRanges();
        selection.addRange(range);
    } else {
        console.warn("Could not select text in node: Unsupported browser.");
    }
}

/* Get height with padding and margin */
function getAbsoluteHeight(elem) {
    let styles = window.getComputedStyle(elem),
        margin = parseFloat(styles['marginTop']) + parseFloat(styles['marginBottom']);

    return Math.ceil(elem.offsetHeight + margin);
}

/* Set content height using window and prior elements' heights */
function setContentHeight() {
    let logoH = getAbsoluteHeight(document.getElementById('logo')),
        hrH   = getAbsoluteHeight(document.getElementById('content-separator')),
        sbH   = getAbsoluteHeight(document.getElementById('sidebar-btn-row')),
        winH  = window.innerHeight;

    document.getElementById('main').style.maxHeight = (winH - hrH - sbH - logoH - 2).toString() + 'px';
}

function openLoader(txt=undefined) {
    const loader = document.querySelector("#loading-modal");    
    if (txt) {
        const button = loader.querySelector("button");
        const span   = loader.querySelector("span");

        button.textContent = '';
        button.appendChild(span);
        button.append(` ${txt}`);
    }
    loader.style.opacity = 1;
}

function hideLoader() {
    document.querySelector("#loading-modal").style.opacity = 0;
}

function scrollToBottom() {
    const main = document.querySelector("#main");
    main.scrollTo({
        top: main.scrollHeight,
        left: 0,
        behavior: 'smooth',
    });
}

document.querySelector("#sidebar").addEventListener('webkitTransitionEnd', setContentHeight);

window.addEventListener('load'  , setContentHeight);
window.addEventListener('resize', setContentHeight);