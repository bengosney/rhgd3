document.querySelectorAll('.messages .close_button').forEach((elem) => {
    elem.addEventListener('click', (e) => {
        const href = elem.getAttribute('href');

        fetch(href);
        elem.parentElement.remove();
        e.preventDefault();
    });
});
