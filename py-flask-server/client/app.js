function getBathValue(){
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for(var i in uiBathrooms){
        if(uiBathrooms[i].checked){
            return parseInt(i)+1;
        }
    }
    return -1;
}

function getBedValue(){
    var uiBed = document.getElementsByName("uiBed");
    for(var i in uiBed){
        if(uiBed[i].checked){
            return parseInt(i)+1;
        }
    }

    return -1;
}


function onClickedEstimatePrice(){
    console.log("Estimate price button clicked");
    var sqft = document.getElementById("uiSqft");
    var bed = getBedValue();
    var bath = getBathValue();
    var location = document.getElementById("uiLocations");
    var estPrice = document.getElementById("uiEstimatedPrice");

    console.log(parseFloat(sqft.value) + " : " + bed + " : " + bath + " : " + location.value);

    var url = "http://127.0.0.1:5000/predict_home_price";

    $.post(url, {
        TotalSqft: parseFloat(sqft.value),
        Bedroom: bed,
        Bathroom: bath,
        Location: location.value
    }, function(data, status){
        console.log(data.estimated_price);
        estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " $</h2>";
        console.log(status);
    });
}

function onPageLoad(){
    console.log("Document loaded");
    var url = "http://127.0.0.1:5000/get_location_names";
    $.get(url, function(data, status){
        console.log("Retrieved get_location_names function request");
        if(data){
            var locations = data.locations;
            var uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            for(var i in locations){
                var opt = new Option(locations[i]);
                $('#uiLocations').append(opt);
            }
        }
    });

}



window.onload = onPageLoad;