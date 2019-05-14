let canvas = document.querySelector('#canvas');
let context = canvas.getContext("2d");

let u =  document.getElementById("u").value;
host = "ws://localhost:8888/show/update/?u="+u;
websocket = new WebSocket(host);
websocket.onopen = function(evt){}; // 建立连接
websocket.onmessage = function(evt){};

websocket.onmessage = function(evt){    // 获取服务器返回的信息
            if(evt.data){
            alert("识别的数字是："+ evt.data);
            }
        }
websocket.onerror = function(evt){};

let clientWidth = document.documentElement.clientWidth;
let clientHeight = document.documentElement.clientHeight;

back.onclick = function(){
    history.back(-1);
}

send.onclick = function(){
    var img  = document.getElementById("img");
    context.drawImage(img,0,0,clientWidth,clientHeight,0,0,28,28);
    var image_src = canvas.toDataURL("image/png");
	websocket.send(image_src);
}


