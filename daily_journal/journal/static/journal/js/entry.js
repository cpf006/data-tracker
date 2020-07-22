function saveEntry(year, month, day) {
    $.post(
        "/journal/set_entry/"+year+"/"+month+"/"+day,
        $("#entry-form").serialize(),
        function() {
            window.location.href = "/journal/"+year;
        }
    );

    return false;
}