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