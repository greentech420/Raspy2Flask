$(function(){
	$("#mycheck1").on('click',function(){
		$.ajax({
			type:'POST',
			url:'/gpio',
			data:JSON.stringify({
				"pin":17,
				"state":document.getElementById("mycheck1").checked ? 1:0
			}),
			dataType:'json',
			contentType:'application/json'
		}).done(function(data){
			//window.alert(data);
			console.log(data.msg);
			document.getElementById('message').textContent = data.msg;
		}).fail(function(){
			window.alert("データが受信できませんでした");
		})
	});
});

$(function(){
	$("#mycheck2").on('click',function(){
		$.ajax({
			type:'POST',
			url:'/gpio',
			data:JSON.stringify({
				"pin":22,
				"state":document.getElementById("mycheck2").checked ? 1:0
			}),
			dataType:'json',
			contentType:'application/json'
		}).done(function(data){
			//window.alert(data);
			console.log(data.msg);
			document.getElementById('message').textContent = data.msg;
		}).fail(function(){
			window.alert("データが受信できませんでした");
		})
	});
});

$(function(){
	$("#mycheck3").on('click',function(){
		$.ajax({
			type:'POST',
			url:'/gpio',
			data:JSON.stringify({
				"pin":22
				"state":document.getElementById("mycheck3").checked ? 1:0
			}),
			dataType:'json',
			contentType:'application/json'
		}).done(function(data){
			//window.alert(data);
			console.log(data.msg);
			document.getElementById('message').textContent = data.msg;
		}).fail(function(){
			window.alert("データが受信できませんでした");
		})
	});
});