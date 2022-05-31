document.addEventListener("DOMContentLoaded", function(event) {

    var dropdowns = document.getElementsByClassName("dropdown");
    function dropdownToggleEventHandler(dropdown){
        return function(e){
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

    function isEmpty(obj){
        return Object.keys(obj).length === 0;
    }
    url = location.toString()
    function getUrl(params){
        if (isEmpty(params)){
            return url.split('?')[0]
        }

        entries = Object.entries(params)
        params_str = '?'

        for (i = 0; i < entries.length; i++) {
            param = entries[i][0] + "=" + entries[i][1];
            params_str += param
            if(i != entries.length - 1)
                params_str += "&"
        }

        return url.split('?')[0] + params_str
    }
    function toggleFilterParam(value, param_name){
        if ((isEmpty(params)) || (! (param_name in params))){
            params[param_name] = value
        }
        else{
            if (! (params[param_name].includes(value))){
                params[param_name] = params[param_name] + ',' + value
            }
            else{
                if (! (params[param_name].includes(','))){
                    delete params[param_name]
                }
                else{
                    items = params[param_name].split(',')
                    items.splice(items.indexOf(value), 1)
                    params[param_name] = items.join(',')
                }
            }
        }
    }
    function toggleRadioParam(value, param_name){
        if ((isEmpty(params)) || (! (param_name in params))){
            params[param_name] = value
        }
        else{
            if (params[param_name] === value){
                delete params[param_name]
            }
            else{
                params[param_name] = value
            }
        }
    }

    var params = window.location.search.replace('?','').split('&').reduce(function(p,e){
                var a = e.split('=');
                p[ decodeURIComponent(a[0])] = decodeURIComponent(a[1]);
                if (a != "") {return p;}
            }, {});
    if(! params) params = {}

    checkboxes_genre = document.getElementsByClassName('dropdown__body__it genre')
    checkboxes_country = document.getElementsByClassName('dropdown__body__it country')
    radio_buttons_year = document.getElementsByClassName('dropdown__body__it year')
    radio_buttons_rate = document.getElementsByClassName('dropdown__body__it rate')
    radio_buttons_sort = document.getElementsByClassName('dropdown__body__it sort')

    if (! isEmpty(params)){
        if ('genres' in params){
            var genres = params['genres'].split(',')
            for (var i = 0; i < checkboxes_genre.length; i++){
                if(genres.indexOf(checkboxes_genre[i].id.split('-')[1]) != -1)
                    checkboxes_genre[i].classList.add('checked');
            }
        }
        if ('countries' in params){
            var countries = params['countries'].split(',')
            for (var i = 0; i < checkboxes_country.length; i++){
                if(countries.indexOf(checkboxes_country[i].id.split('-')[1]) != -1)
                    checkboxes_country[i].classList.add('checked');
            }
        }
        if ('subscription' in params){
            if (params['subscription'] === 'true'){
                document.getElementById('filter__subscription').classList.add('checked')
            }
            if (params['subscription'] === 'false'){
                document.getElementById('filter__free').classList.add('checked')
            }
        }
        if ('year' in params){
            document.getElementById(`year_${params['year']}`).classList.add('checked')
        }
        if ('rate' in params){
            document.getElementById(`rate_${params['rate']}`).classList.add('checked')
        }
        if ('sort' in params){
            document.getElementById(`sort_${params['sort']}`).classList.add('checked')
        }
    }

    // genre
    function checkboxesGenreEventHandler(checkbox_genre){
        return function(){
            var genre = checkbox_genre.id.split('-')[1];

            toggleFilterParam(genre, 'genres')

            location.assign(getUrl(params))
        }
    }
    for (var i = 0; i < checkboxes_genre.length; i++) {
        checkboxes_genre[i].addEventListener('click', checkboxesGenreEventHandler(checkboxes_genre[i]))
    }
    // country
    function checkboxesCountryEventHandler(checkbox_country){
        return function(){
            var country = checkbox_country.id.split('-')[1];

            toggleFilterParam(country, 'countries')

            location.assign(getUrl(params))
        }
    }
    for (var i = 0; i < checkboxes_country.length; i++) {
        checkboxes_country[i].addEventListener('click', checkboxesCountryEventHandler(checkboxes_country[i]))
    }
    // year
    function radioButtonsYearEventHandler(radio_button_year){
        return function(){
            var year = radio_button_year.id.split('_')[1];

            if (year != 'all-years'){
                toggleRadioParam(year, 'year')

                location.assign(getUrl(params))
            }
            else if ('year' in params){
                delete params['year']

                location.assign(getUrl(params))
            }
        }
    }
    for (var i = 0; i < radio_buttons_year.length; i++) {
        radio_buttons_year[i].addEventListener('click', radioButtonsYearEventHandler(radio_buttons_year[i]))
    }
    if ((isEmpty(params)) || (! ('year' in params))){
        document.getElementById('year_all-years').classList.add('checked')
    }
    // rate
    function radioButtonsRateEventHandler(radio_button_rate){
        return function(){
            var rate = radio_button_rate.id.split('_')[1];

            if (rate != 'all-rates'){
                toggleRadioParam(rate, 'rate')

                location.assign(getUrl(params))
            }
            else if ('rate' in params){
                delete params['rate']

                location.assign(getUrl(params))
            }

        }
    }
    for (var i = 0; i < radio_buttons_rate.length; i++) {
        radio_buttons_rate[i].addEventListener('click', radioButtonsRateEventHandler(radio_buttons_rate[i]))
    }
    if ((isEmpty(params)) || (! ('rate' in params))){
        document.getElementById('rate_all-rates').classList.add('checked')
    }
    // sort
    function radioButtonsSortEventHandler(radio_button_sort){
        return function(){
            var sort = radio_button_sort.id.split('_')[1];

            if (sort != params['sort']){
                toggleRadioParam(sort, 'sort')

                location.assign(getUrl(params))
            }
        }
    }
    for (var i = 0; i < radio_buttons_sort.length; i++) {
        radio_buttons_sort[i].addEventListener('click', radioButtonsSortEventHandler(radio_buttons_sort[i]))
    }
    if ((isEmpty(params)) || (! ('sort' in params))){
        document.getElementById('sort_popular').classList.add('checked')
    }


    document.getElementById('filter__free').onclick = function(){
        if ('subscription' in params){
            if (params['subscription'] === 'false'){
                delete params['subscription']
            }
            else{
                params['subscription'] = false
            }
        }
        else{
            params['subscription'] = false
        }

        location.assign(getUrl(params))
    }
    document.getElementById('filter__subscription').onclick = function(){
        if ('subscription' in params){
            if (params['subscription'] === 'true'){
                delete params['subscription']
            }
            else{
                params['subscription'] = true
            }
        }
        else{
            params['subscription'] = true
        }

        location.assign(getUrl(params))
    }

    btn_reset_filters = document.querySelector('.btn-reset-filters')
    if (! isEmpty(params)){
        btn_reset_filters.classList.add('active')

        btn_reset_filters.onclick = function () {
            location.assign(url.split('?')[0])
        }
    }
    else{
        btn_reset_filters.classList.add('disabled')
    }

});