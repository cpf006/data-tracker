function setGrid(id, year, trackerId) {
    $('#'+id+'-grid-prev').click(function() {
        getEntries(id, Number($('#'+id+' .grid-year').html()) - 1, trackerId)
    })
    $('#'+id+'-grid-next').click(function() {
        getEntries(id, Number($('#'+id+'-grid-year').html()) + 1, trackerId)
    })

    getEntries(id, year, trackerId)
}

function calculateGridWidth(id) {
    let rows = $('#'+id+' .grid-outer')
    let rowWidth = Number($(rows[0]).css('width').replace('px',''))
    return (rows.length * rowWidth) + "px"
}

function getEntries(id, year, trackerId=null) { 
    let data = year+(trackerId ? '?tracker_id='+trackerId : '');
    $('#'+id+'-grid-content').load(
        "/journal/entries/"+data,
        function() {
            $('#'+id+'-grid-content').tooltip({show: null});
            $('#'+id+'-grid-year').html(year) 
            $('#'+id+'-grid-content').css("maxWidth", calculateGridWidth(id));
        }
    );
}
