$(document).ready(function () {
    function refresh_positions(data) {
        var data = JSON.parse(data);
        for(var peer in data) {
           var peerid = peer_id(peer);
            console.log(peerid);
            $element = $("#" + peerid);
            console.log($element.length);
            if($element.length > 0) {
               console.log("#" + peerid + " exists. Moving.");
            } else {
                console.log("#" + peerid + " does not exist.");
               $("body").append('<div id="'+peerid+'">'+peer+'</div>');
               $("#"+ peerid).css('position', 'absolute');
               $("#"+ peerid).css('top',300); 
               $("#"+ peerid).css('left', 300);
               $element = $("#" + peerid);
            }
               $element.css('top', data[peer]['y']);
               $element.css('left', data[peer]['x']); 
        }
    }

    function peer_id(peer) {
        return peer.replace(/[\.:]/g,'');
    }

    var sock = null;
    var wsuri = "ws://192.168.1.128:9000";

    window.onload = function() {
        sock = new WebSocket(wsuri);

        sock.onopen = function() {
            console.log("connected to " + wsuri);
        }

        sock.onclose = function(e) {
            console.log("connection closed (" + e.code + ")");
        }

        sock.onmessage = function(e) {
            console.log("message received: " + e.data);
            refresh_positions(e.data);
        }
    };

    function send() {
        var msg = document.getElementById('message').value;
        sock.send(msg);
    };
});

