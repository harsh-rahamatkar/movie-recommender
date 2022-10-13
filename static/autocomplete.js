for (i = 0; i < films.length; i++) {
    films[i] = String(films[i])
}

suggestion_list = new Array()

document.querySelector("#autoCompleteInput").addEventListener('input', function (element) {
    element = element.target
    element.value = element.value.toUpperCase()
    inputvalue = element.value

    if (inputvalue == "") {
        $('.movie-button').attr('disabled', true);
    }
    else {
        $('.movie-button').attr('disabled', false);
    }

    suggestion_list = new Array()
    for (i = 0; i < films.length; i++) {
        if (films[i].includes(inputvalue)) {
            suggestion_list.push(films[i])
            if (suggestion_list.length > 2) {
                break
            }
        }
    }

    for(i = 0; i < 3; i++) {
        if (suggestion_list[i] == undefined) suggestion_list[i]=""
    }

    $(".suggest-dropdown").attr("style", "display: block; width: fit-content; margin: auto;")
    document.querySelector("#suggest0").innerHTML = suggestion_list[0]
    document.querySelector("#suggest1").innerHTML = suggestion_list[1]
    document.querySelector("#suggest2").innerHTML = suggestion_list[2]
})


document.querySelectorAll('.suggest-item').forEach(e => e.addEventListener('click', function(element) {
    element = element.target
    document.querySelector("#autoCompleteInput").value = element.innerHTML
    $(".suggest-dropdown").attr("style", "display: none; width: fit-content; margin: auto;")
}))