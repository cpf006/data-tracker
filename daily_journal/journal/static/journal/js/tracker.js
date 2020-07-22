function createTracker() {
    refreshModal();
    $('#tracker-modal-label').html("New Tracker");
    $('#tracker-modal').modal('show');
}

function deleteTrackerOption(event) {
    $(event.target).parent().parent().remove();
}

function refreshModal() {
    let option = $('.tracker-modal-option').first().clone();
    $('.tracker-modal-option').remove();
    $('#tracker-modal-options').append(option);
    $("#tracker-modal-form")[0].reset();
    addTrackerOption();
}

function addTrackerOption() {
    let option = $('.tracker-modal-option').first().clone();
    let next = $('.tracker-modal-option').length;
    option.find('.option_name').first().attr('name', 'option_name'+next);
    option.find('.option_color').first().attr('name', 'option_color'+next);
    $('#tracker-modal-options').append(option);
    option.show();
}

function saveTracker() {
    var valid = true;
    $('#tracker-modal-form input:visible').each(function( index ) {
        if( ! $(this).val() && $(this).is(":visible")){
            $(this).addClass('border border-danger');
            valid = false;
        }
    });

    if(valid) {
        $.post(
            "/journal/set_tracker/",
            $("#tracker-modal-form").serialize(),
            function() {
                location.reload();
            }
        );
    } else {
        alert('Please fill out all fields.');
    }
}
