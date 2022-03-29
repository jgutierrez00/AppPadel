let cookies = decodeURIComponent(document.cookie)

$(function () {
  $('#flash').delay(500).fadeIn('normal', function () {
    $(this).delay(2500).fadeOut();
  });
});

$(document).ready(function(){
  console.log(cookies);
  var r1 = getCookie("reserva1");
  var r2 = getCookie("reserva2");
  if(r1 != ""){
    document.getElementById("reserva1").innerHTML = "<li class=\"list-group-item\" id=\"reserva1\">" + getCookie("reserva1") +"</li>";
  }else{
    document.getElementById("reserva1").innerHTML = "<li class=\"list-group-item\" id=\"reserva1\">Sin reserva</li>";
  }
  if(r2 != ""){
    document.getElementById("reserva2").innerHTML = "<li class=\"list-group-item\" id=\"reserva1\">" + getCookie("reserva2") +"</li>";
  }else{
    document.getElementById("reserva2").innerHTML = "<li class=\"list-group-item\" id=\"reserva1\">Sin reserva</li>";
  }
});

document.getElementById('btndisplay1').addEventListener('click', function () {
  document.getElementById('btndisplay1').style.display = 'none';
  document.getElementById('btndisplay2').style.display = 'none';
  document.getElementById('divttable1').style.display = 'block';
  document.getElementById('btnbacktt').style.display = 'block';
})

document.getElementById('btndisplay2').addEventListener('click', function () {
  document.getElementById('btndisplay1').style.display = 'none';
  document.getElementById('btndisplay2').style.display = 'none';
  document.getElementById('divttable2').style.display = 'block';
  document.getElementById('btnbacktt').style.display = 'block';
})

document.getElementById('btnbacktt').addEventListener('click', function () {
  document.getElementById('btnbacktt').style.display = 'none';
  document.getElementById('divttable1').style.display = 'none'
  document.getElementById('divttable2').style.display = 'none'
  document.getElementById('btndisplay1').style.display = 'inline-block';
  document.getElementById('btndisplay2').style.display = 'inline-block';
})

function getCookie(cName) {
  const name = cName + "=";
  const cDecoded = decodeURIComponent(cookies);
  const cArr = cDecoded.split('; ');
  let res;
  cArr.forEach(val => {
    if (val.indexOf(name) === 0) res = val.substring(name.length);
  })
  return res.substring(1, res.length-1);
}