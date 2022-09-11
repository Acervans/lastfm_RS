var isToggled = true;

/* Toggle sidebar */
function toggleNav() {
    let nav = document.getElementById("sidebar"),
        content = document.getElementsByClassName("col-sm-10")[0],
        btn = document.getElementsByClassName("sidebar-btn")[0],
        navW = nav.scrollWidth;
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

/* Get height with padding and margin */
function getAbsoluteHeight(elem) {
    let styles = window.getComputedStyle(elem),
        margin = Math.abs(parseFloat(styles['marginTop'])) + Math.abs(parseFloat(styles['marginBottom']));

    return Math.ceil(elem.offsetHeight + margin);
}

/* Set content height using window and prior elements' heights */
function setContentHeight() {
    let logoH = getAbsoluteHeight(document.getElementById('logo')),
        hrH = getAbsoluteHeight(document.getElementById('content-separator')),
        winH = window.innerHeight;

    document.getElementById('main').style.maxHeight = (winH - hrH - logoH - 2).toString() + 'px';
}

window.onload = setContentHeight;
window.addEventListener('resize', setContentHeight);