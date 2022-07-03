$(window).on("load", function () {
    $('#preLoader').attr("hidden", true);
    $('#main').attr("hidden", false);

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    $(".alert").delay(4000).slideUp(200, function () {
        $(this).alert('close');
    });
});