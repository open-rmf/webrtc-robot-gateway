var pc = null;
let sendChannel;

function sendCmdRotateLeft() {
  console.log("Left");
  sendChannel.send("A");
}

function sendCmdRotateRight() {
  console.log("Right");
  sendChannel.send("D");
}

function sendCmdForward() {
  console.log("Forward");
  sendChannel.send("W");
}

function sendCmdReverse() {
  console.log("Reverse");
  sendChannel.send("S");
}

function sendCmdStop() {
  console.log("Stop");
  sendChannel.send("X");
}

function negotiate() {
    pc.addTransceiver('video', {direction: 'recvonly'});
    pc.addTransceiver('audio', {direction: 'recvonly'});
    return pc.createOffer().then(function(offer) {
        return pc.setLocalDescription(offer);
    }).then(function() {
        // wait for ICE gathering to complete
        return new Promise(function(resolve) {
            if (pc.iceGatheringState === 'complete') {
                resolve();
            } else {
                function checkState() {
                    if (pc.iceGatheringState === 'complete') {
                        pc.removeEventListener('icegatheringstatechange', checkState);
                        resolve();
                    }
                }
                pc.addEventListener('icegatheringstatechange', checkState);
            }
        });
    }).then(function() {
        var offer = pc.localDescription;
        return fetch('/offer', {
            body: JSON.stringify({
                sdp: offer.sdp,
                type: offer.type,
            }),
            headers: {
                'Content-Type': 'application/json'
            },
            method: 'POST'
        });
    }).then(function(response) {
        return response.json();
    }).then(function(answer) {
        return pc.setRemoteDescription(answer);
    }).catch(function(e) {
        alert(e);
    });
}

function start() {
    var config = {
        sdpSemantics: 'unified-plan'
    };

    config.iceServers = [{urls: ['stun:stun.l.google.com:19302']}];

    pc = new RTCPeerConnection(config);

    // Connect DataChannel
    sendChannel = pc.createDataChannel('sendChannel');
    sendChannel.onopen = function() { 
        document.getElementById('teleop').style.display = 'inline-block';
        console.log("sendChannel for teleop is open"); 
    }
    sendChannel.onclose = function() { 
        document.getElementById('teleop').style.display = 'none';
        console.log("sendChannel for teleop is closed"); 
    }

    // connect audio / video
    pc.addEventListener('track', function(evt) {
        if (evt.track.kind == 'video') {
            document.getElementById('video').srcObject = evt.streams[0];
        } else {
            document.getElementById('audio').srcObject = evt.streams[0];
        }

    });

    document.getElementById('start').style.display = 'none';
    negotiate();
    document.getElementById('stop').style.display = 'inline-block';
}

function stop() {
    document.getElementById('start').style.display = 'inline-block';
    document.getElementById('stop').style.display = 'none';

    // close peer connection
    setTimeout(function() {
        pc.close();
    }, 500);
}
