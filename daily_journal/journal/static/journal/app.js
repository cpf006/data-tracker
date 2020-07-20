
function setGrid(id, year) {
    jQuery('#'+id+' .grid-prev')[0].click(function() {
        "click", getEntries(id, Number(jQuery('#'+id+' .grid-year')[0].innerHTML) + 1)
    })
    jQuery('#'+id+' .grid-next')[0].click(function() {
        "click", getEntries(id, Number(jQuery('#'+id+' .grid-year')[0].innerHTML) - 1)
    })

    getEntries(id, year)
}

function calculateGridWidth(id) {
    let rows = jQuery('#'+id+' .grid-outer')
    let rowWidth = Number(jQuery(rows[0]).css('width').replace('px',''))
    return (rows.length * rowWidth) + "px"
}

function getEntries(id, year)
{    
    jQuery('#'+id+' .grid-content').load("/journal/entries/".concat(year), function() {
        jQuery('#'+id+' .grid-content').tooltip({show: null});
        jQuery('#'+id+' .grid-year')[0].innerHTML = year 
        jQuery('#'+id+' .grid-content').css("maxWidth", calculateGridWidth(id));
    });
}


