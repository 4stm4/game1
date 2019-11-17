
function Sound(source, volume, loop)
{
    this.source = source;
    this.volume = volume;
    this.loop = loop;
    var son;
    this.son = son;
    this.finish = false;
    this.stop = function()
    {
        document.body.removeChild(this.son);
    }
    this.start = function()
    {
        if (this.finish) return false;
        this.son = document.createElement("embed");
        this.son.setAttribute("src", this.source);
        this.son.setAttribute("hidden", "true");
        this.son.setAttribute("volume", this.volume);
        this.son.setAttribute("autostart", "true");
        this.son.setAttribute("loop", this.loop);
        document.body.appendChild(this.son);
    }
    this.remove=function()
    {
        document.body.removeChild(this.son);
        this.finish = true;
    }
    this.init = function(volume, loop)
    {
        this.finish = false;
        this.volume = volume;
        this.loop = loop;
    }
}

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
            document.getElementById("sum").children[0].innerHTML=result;
        }
    });
}