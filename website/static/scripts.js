$(function() {
  $('#flash').delay(500).fadeIn('normal', function() {
     $(this).delay(2500).fadeOut();
  });
});

document.getElementById('divbtn1').addEventListener('click', function(){
  document.getElementById('divbtn1').style.display = 'none';
  document.getElementById('divbtn2').style.display = 'none';
  document.getElementById('divttable1').style.display = 'block';
  document.getElementById('btnbacktt').style.display = 'block';
})
  
document.getElementById('divbtn2').addEventListener('click', function(){
  document.getElementById('divbtn1').style.display = 'none';
  document.getElementById('divbtn2').style.display = 'none';
  document.getElementById('divttable2').style.display = 'block';
  document.getElementById('btnbacktt').style.display = 'block';
})

document.getElementById('btnbacktt').addEventListener('click', function(){
  document.getElementById('btnbacktt').style.display = 'none';
  document.getElementById('divttable1').style.display = 'none'
  document.getElementById('divttable2').style.display = 'none'
  document.getElementById('divbtn1').style.display = 'inline-block';
  document.getElementById('divbtn2').style.display = 'inline-block';
})