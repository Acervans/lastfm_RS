function show(element) {
    if (element) {
        element.style.overflow = 'auto'
        element.style.height   = 'auto';
        element.style.opacity  = '1';
    }
}

function hide(element) {
    if (element) {
        element.style.overflow = 'hidden';
        element.style.height   = '0';
        element.style.opacity  = '0';
    }
}

function replaceTags() {
    const tags_input  = document.querySelector("#id_cosine-tags"),
          dummy_input = document.querySelector("#tags-placeholder"),
          tags_spans  = document.querySelectorAll("#tags span");

    var tags_values = Object.values(tags_spans).map((span) => span.innerText || span.textContent);

    if (tags.has(dummy_input.value))
        tags_values.push(dummy_input.value);

    tags_input.value = tags_values;
}

const tags = new Set(Array.from(document.querySelectorAll('#tags_list option')).
    map((tag) => tag.value));

var rad = document.getElementsByClassName('form-group')[0]['model'];
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

jQuery($ => {
    // Tags separated by comma
    $("#tags-placeholder").on({
        focusout() {
            var txt = this.value.replace(/(^,)|(,$)/g, '');
            if (txt && tags.has(txt)) {
                $("<span/>", { text: txt.toLowerCase(), insertBefore: this });
            }
            this.value = "";
        },
        keyup(ev) {
            if (/(,|Enter)/.test(ev.key))
                $(this).focusout();
        }
    });

    $("#tags").on("click", "span", function () {
        $(this).remove();
    });
});