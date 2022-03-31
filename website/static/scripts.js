let cookies = decodeURIComponent(document.cookie)

function getCookie(cName) {
  const name = cName + "=";
  const cDecoded = decodeURIComponent(cookies);
  const cArr = cDecoded.split('; ');
  let res;
  cArr.forEach(val => {
    if (val.indexOf(name) === 0) res = val.substring(name.length);
  })
  return res;
}

function checkDay(){
  var textC = transform(getCookie("dia"));
  var realC = new Date().getDay();
  if(textC < realC){
    return -1;
  }else if(textC == realC){
    return 0;
  }
  return 1;
}

function checkHour(hour, min){
  var realH = new Date().getHours();
  if(hour < realH){
    return false;
  }else if(hour == realH){
    if(min < new Date().getMinutes()){
      return false;
    }else{
      return true;
    }
  }
  return hour < realH;
}

function filterText(text){
  let hour = text.substring(0,2);
  let min = text.substring(3,5);
  var array = new Array(hour, min);
  return array;
}

function changeBooks(checkHours){
  const arrayPA = document.getElementById("listPA").getElementsByTagName("button");
  const arrayPB = document.getElementById("listPB").getElementsByTagName("button")
  if(!checkHours){
    Object.values(arrayPA).forEach(function(elem){
      elem.outerHTML = "<li class=\"list-group-item list-group-item-action disabled\">Hora no disponible</li>"
    })
    Object.values(arrayPB).forEach(function(elem){
      elem.outerHTML = "<li class=\"list-group-item list-group-item-action disabled\">Hora no disponible</li>"
    })
  }else{
    Object.values(arrayPA).forEach(function(elem){
      let time = filterText(elem.innerHTML);
      if(!checkHour(time[0], time[1])){
        elem.outerHTML = "<li class=\"list-group-item list-group-item-action disabled\">Hora no disponible</li>"
      }
    }) 
    Object.values(arrayPB).forEach(function(elem){
      let time = filterText(elem.innerHTML);
      if(!checkHour(time[0], time[1])){
        elem.outerHTML = "<li class=\"list-group-item list-group-item-action disabled\">Hora no disponible</li>"
      }
    })
  }
}


function removePossibleBooks(){
  if(checkDay() == -1){
    changeBooks(false);  
  }else if(checkDay() == 0){
    changeBooks(true); 
  }
  return new Promise(resolve =>{
    setTimeout(() => {
      resolve("Resolved");
    }, 5000);
  });
}

async function asyncCall(){
  console.log("Calling");
  const result = await removePossibleBooks();
  console.log(result);
}

function transform(day){
  var res = 0;
  switch(day){
    case "Lunes":
      res = 1;
      break;
    case "Martes":
      res = 2;
      break;
    case "Miercoles":
      res = 3;
      break;
    case "Jueves":
      res = 4;
      break;
    case "Viernes":
      res = 5;
      break;
    case "Sabado":
      res = 6;
      break;
    default:
      res = -1;
      break;
  }
  return res;
}

$(function () {
  $('#flash').delay(500).fadeIn('normal', function () {
    $(this).delay(2500).fadeOut();
  });
  if(window.location.href == "http://localhost:5000/horarios"){
    asyncCall();  
  }
});


$(document).ready(function(){
  var r1 = getCookie("reserva1");
  var r2 = getCookie("reserva2");
  r1 = r1.substring(1, r1.length-1)
  r2 = r2.substring(1, r2.length-1)
  if(r1 != ""){
    document.getElementById("reserva1").innerHTML = "<li class=\"list-group-item\" id=\"reserva1\">" + r1 +"</li>";
  }else{
    document.getElementById("reserva1").innerHTML = "<li class=\"list-group-item\" id=\"reserva1\">Sin reserva</li>";
  }
  if(r2 != ""){
    document.getElementById("reserva2").innerHTML = "<li class=\"list-group-item\" id=\"reserva1\">" + r2 +"</li>";
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
