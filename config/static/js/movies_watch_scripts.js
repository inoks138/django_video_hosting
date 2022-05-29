document.addEventListener("DOMContentLoaded", function(event) {

    var dropdowns = document.getElementsByClassName("dropdown");
    function dropdownToggleEventHandler(dropdown){
        return function(){
            dropdown.classList.toggle("dropdown__show");
        }
    }
    function dropdownCloseEventHandler(dropdown){
        document.addEventListener('click', function(e){
            const withinBoundaries = e.composedPath().includes(dropdown);

            if ( ! withinBoundaries ) {
                dropdown.classList.remove('dropdown__show');
            }
        })
    }
    for (var i = 0; i < dropdowns.length; i++) {
        var dropdown = dropdowns[i]
        var dropdown_head = dropdown.firstElementChild

        dropdown_head.onclick = dropdownToggleEventHandler(dropdown)
        dropdownCloseEventHandler(dropdown)
    }
});