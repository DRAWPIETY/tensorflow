let canvas = document.querySelector('#canvas');
let context = canvas.getContext("2d");

let clientWidth = document.documentElement.clientWidth;
let clientHeight = document.documentElement.clientHeight;
canvas.width = clientWidth;
canvas.height = clientHeight;
context.strokeStyle = 'red';//一定不能用黑色，不然得到的np.arry里全是0
context.lineWidth = 50;//笔触粗细
let previousPoint;
canvas.addEventListener('touchend', function(){
  previousPoint = null
})

if(/Android|webOS|iPhone|iPod|BlackBerry/i.test(navigator.userAgent)) {//在移动端
	canvas.addEventListener('touchmove', function(e){
		e.preventDefault();
		let {pageX,pageY}= e.touches[0];
		if(previousPoint){
		  context.beginPath();
		  context.moveTo(previousPoint.pageX, previousPoint.pageY); // 移动到上一个点
		  context.lineTo(pageX,pageY); // 画线到这一个点
		  context.stroke()
		}
		previousPoint = { pageX, pageY };
	})
}else{	//在PC端
	canvas.onmousedown = function(ev) {
		var ev = ev || event;
		context.beginPath();
		context.moveTo(ev.clientX - canvas.offsetLeft, ev.clientY - canvas.offsetTop);
		document.onmousemove = function(ev) {
			var ev = ev || event;
			context.lineTo(ev.clientX - canvas.offsetLeft, ev.clientY - canvas.offsetTop);
			context.stroke();
		}
		document.onmouseup = function(ev) {
			document.onmousemove = document.onmouseup = null;
			context.closePath();
		}
	}
}

function canvas2image(canvas) {
	var image = new Image();
	image.src = canvas.toDataURL("image/png");
	return image;
}


clear.onclick = function(){
	context.clearRect(0, 0, canvas.width, canvas.height);
}


save.onclick = function(){
	var img=canvas2image(canvas);
	document.getElementById("image_src").value=img.src;
}
