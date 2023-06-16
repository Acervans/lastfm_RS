var rad;
var searchInputs;
var prevForm, prevInput;

const tags = new Set(Array.from(document.querySelectorAll("#tags_list option")).
    map((tag) => tag.value));

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
    const tagsInput  = document.querySelector("#id_cosine-tags"),
          dummyInput = document.querySelector("#tags-placeholder"),
          tagsSpans  = document.querySelectorAll("#tags span");

    var tagsValues = Object.values(tagsSpans).map((span) => span.innerText || span.textContent);

    if (tags.has(dummyInput.value))
        tagsValues.push(dummyInput.value);

    tagsInput.value = tagsValues;
}

function swap(node1, node2) {
    const afterNode2 = node2.nextElementSibling;
    const parent     = node2.parentNode;

    node1.replaceWith(node2);
    parent.insertBefore(node1, afterNode2);
}

function swapInputs(visibleInput) {
    if (visibleInput.id !== prevInput.id) {
        visibleInput.type = 'text';
        prevInput.type = 'hidden';
        swap(prevInput, visibleInput);
        prevInput = visibleInput;
    }
}

function init_forms() {
    rad = document.getElementsByClassName('form-group')[0]['model'];
    prevForm = rad[0];

    Array.from(rad).forEach((r, i) => {
        if (r.checked) {
            prevForm = rad[i];
            show(document.getElementById(rad[i].value));
        }
        rad[i].addEventListener('change', function () {
            if (this !== prevForm) {
                hide(document.getElementById(prevForm.value));
                show(document.getElementById(this.value));
                prevForm = this;
            }
        });
    });
}

function init_search() {
    const searchDiv = document.querySelector("#search");
    searchInputs = searchDiv.querySelectorAll("input[type=text], input[type=hidden]");
    prevInput = searchInputs[0];

    searchDiv.querySelectorAll("input[type=radio]").forEach((searchBy, i) => {
        if (searchBy.checked)
            swapInputs(searchInputs[i]);
        searchBy.addEventListener('change', () => {
            if (!prevInput.value)
                prevInput.removeAttribute('value');
            swapInputs(searchInputs[i]);
        });
    });
}

jQuery($ => {
    // Tags separated by comma
    $("#tags-placeholder").on({
        focusout() {
            const inputTags = this.value.replace(/,\s*$/g, '');
            this.value = '';

            if (inputTags.length > 0) {
                inputTags.split(/\s*,\s*/g).forEach((txt) => {
                    if (txt && tags.has(txt))
                        $("<span/>", { text: txt.toLowerCase(), insertBefore: this });
                });
            }
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

init_forms();
init_search();