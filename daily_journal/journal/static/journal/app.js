
function setGrid(id, year) {
    jQuery('#'+id+' .grid-prev')[0].click(function() {
        "click", getEntries(id, Number(jQuery('#'+id+' .grid-year')[0].innerHTML) + 1)
    })
    jQuery('#'+id+' .grid-next')[0].click(function() {
        "click", getEntries(id, Number(jQuery('#'+id+' .grid-year')[0].innerHTML) - 1)
    })

    getEntries(id, year)
}

function getEntries(id, year)
{    
    jQuery('#'+id+' .grid-content').load("/journal/entries/".concat(year), function() { jQuery('#'+id+' .grid-year')[0].innerHTML = year });
    jQuery('#'+id+' .grid-content').tooltip({show: null});
}
