var isToggled = true;

/* Toggle sidebar */
function toggleNav() {
    let nav = document.getElementById("sidebar"),
        content = document.getElementsByClassName("col-sm-10")[0],
        btn = document.getElementsByClassName("sidebar-btn")[0],
        navW = nav.clientWidth;
    if (isToggled) {
        btn.style.transform = "rotate(180deg)";
        nav.style.marginLeft = `-${navW + 2}px`;
        content.style.flexBasis = "100%";
        isToggled = false;
    }
    else if (!isToggled) {
        btn.style.transform = "";
        nav.style.marginLeft = 0;
        content.style.flexBasis = "88%";
        isToggled = true;
    }

}

/* Copies an element's content */
function copyEvent(id) {
    var copyText = document.getElementById(id);
    selectText(copyText);

    // Copy the text inside the element
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
        hrH = getAbsoluteHeight(document.getElementById('content-separator')),
        sbH = getAbsoluteHeight(document.getElementById('sidebar-btn-row')),
        winH = window.innerHeight;

    document.getElementById('main').style.maxHeight = (winH - hrH - sbH - logoH - 2).toString() + 'px';
}

window.onload = setContentHeight;
window.addEventListener('resize', setContentHeight);