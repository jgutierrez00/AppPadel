$(function() {
  $('#flash').delay(500).fadeIn('normal', function() {
     $(this).delay(2500).fadeOut();
  });
});

document.getElementById('btndisplay1').addEventListener('click', function(){
  document.getElementById('btndisplay1').style.display = 'none';
  document.getElementById('btndisplay2').style.display = 'none';
  document.getElementById('divttable1').style.display = 'block';
  document.getElementById('btnbacktt').style.display = 'block';
})
  
document.getElementById('btndisplay2').addEventListener('click', function(){
  document.getElementById('btndisplay1').style.display = 'none';
  document.getElementById('btndisplay2').style.display = 'none';
  document.getElementById('divttable2').style.display = 'block';
  document.getElementById('btnbacktt').style.display = 'block';
})

document.getElementById('btnbacktt').addEventListener('click', function(){
  document.getElementById('btnbacktt').style.display = 'none';
  document.getElementById('divttable1').style.display = 'none'
  document.getElementById('divttable2').style.display = 'none'
  document.getElementById('btndisplay1').style.display = 'inline-block';
  document.getElementById('btndisplay2').style.display = 'inline-block';
})