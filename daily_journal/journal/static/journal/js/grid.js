function setGrid(id, year, trackerId) {
    $('#'+id+'-grid-prev').click(function() {
        getEntries(id, Number($('#'+id+' .grid-year').html()) - 1)
    })
    $('#'+id+'-grid-next').click(function() {
        getEntries(id, Number($('#'+id+'-grid-year').html()) + 1)
    })

    getEntries(id, year)
}

function calculateGridWidth(id) {
    let rows = $('#'+id+' .grid-outer')
    let rowWidth = Number($(rows[0]).css('width').replace('px',''))
    return (rows.length * rowWidth) + "px"
}

function getEntries(id, year, trackerId)
{    
    $('#'+id+'-grid-content').load("/journal/entries/".concat(year), function() {
        $('#'+id+'-grid-content').tooltip({show: null});
        $('#'+id+'-grid-year').html(year) 
        $('#'+id+'-grid-content').css("maxWidth", calculateGridWidth(id));
    });
}
