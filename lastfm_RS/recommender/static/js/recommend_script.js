function show(element) {
    if (element) {
        element.style.overflow = 'auto'
        element.style.height = 'auto';
        element.style.opacity = '1';
    }
}

function hide(element) {
    if (element) {
        element.style.overflow = 'hidden';
        element.style.height = '0';
        element.style.opacity = '0';
    }
}

var rad = document.getElementsByClassName('form-group')[0]['recommend-model'];
var prev = rad[0];

for (var i = 0; i < rad.length; i++) {
    if (rad[i].checked) {
        prev = rad[i];
        show(document.getElementById(rad[i].value));
    }
    rad[i].addEventListener('change', function () {
        if (this !== prev) {
            hide(document.getElementById(prev.value));
            show(document.getElementById(this.value));
            prev = this;
        }
    });
}