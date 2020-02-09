
function GetGamePhase() {
    $.ajax({
        type: "POST",
        url: "/get_game_phase",
        success: function(result) {
            if(result == '1'){
                document.location.replace("/start");
            }
        }
    });
}

function GetGamePoints() {
    $.ajax({
        type: "POST",
        url: "/get_game_points",
        success: function(result) {
            document.getElementById("score").children[0].innerHTML=result;
        }
    });
}

function PostGameEnd() {
    $.ajax({
        type: "POST",
        url: "/end_music"
    });
}