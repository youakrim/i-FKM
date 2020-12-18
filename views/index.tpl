<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Fuzzy k-means !</title>
    <link rel="stylesheet" type="text/css" href="/style/style.css">
  </head>
  <body>
    <form action="#" id='tform' onsubmit='getMask()'>
      <select id="algo">
        <option value="fuzzy_k_means">Fuzzy k means</option>
        <option value="k_means">K-means</option>
      </select>
      <label>Nombre de clusters <input id="nb_clusters" type="range" min='2' max='10' step="1" onchange="updateTextInput(this.value);" /> <span id="textInput">2</span></label>
      <label>Valeur de m<input id="m" type="range" value='1.1' min='1.5' max='2' step="0.1" onchange="updateMInput(this.value);"/><span id="mInput">1.5</span></label>
      <label>Epsilon<input id="e" type="range" value='0.5' min='0' max='1' step="0.1" onchange="updateEInput(this.value);"/><span id="eInput">0.5</span></label>
      <label>Alpha coupe <input type="checkbox" id="alpha_cut"/>  </label>
      <label>Alpha<input id="a" type="range" value='0.5' min='0' max='1' step="0.1" onchange="updateAInput(this.value);"/><span id="aInput">0.5</span></label>

      <input type="submit" value="Actualiser"/>

    </form>
    <div class="ajax-spinner-bars">
      <div class="bar-1"></div>
      <div class="bar-2"></div>
      <div class="bar-3"></div>
      <div class="bar-4"></div>
      <div class="bar-5"></div>
      <div class="bar-6"></div>
      <div class="bar-7"></div>
      <div class="bar-8"></div>
      <div class="bar-9"></div>
      <div class="bar-10"></div>
      <div class="bar-11"></div>
      <div class="bar-12"></div>
      <div class="bar-13"></div>
      <div class="bar-14"></div>
      <div class="bar-15"></div>
      <div class="bar-16"></div>
    </div>
    <img id='img' src='img/small_land.jpg'/>
    <script>
    function loadingIU(){
      document.getElementsByClassName('ajax-spinner-bars')[0].style.display = 'block';

    }
    function loadingCompleted(){
      document.getElementsByClassName('ajax-spinner-bars')[0].style.display = 'none';
    }
    function updateTextInput(val) {
          document.getElementById('textInput').innerHTML=val;
        }
    function updateMInput(val) {
          document.getElementById('mInput').innerHTML=val;
        }
    function updateEInput(val) {
          document.getElementById('eInput').innerHTML=val;
        }
    function updateAInput(val) {
          document.getElementById('aInput').innerHTML=val;
        }
    //document.getElementById("tform").submit = function(){getMask();};
    function displayMask(mask_src){
      var mask = document.getElementById('img');
      mask.src = mask_src;
    }
    function getMask(){
      var m = document.getElementById('m').value;
      var e = document.getElementById('e').value;
      var nb_clusters = document.getElementById('nb_clusters').value;
      var alpha_cut = document.getElementById('alpha_cut').checked.toString();
      var a = document.getElementById('a').value;
      var algo = document.getElementById('algo').value;
      loadingIU();
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/compute_k_means');
      xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
      xhr.addEventListener('readystatechange', function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
          //loadingCompleted();
          loadingCompleted();
          displayMask(xhr.responseText);
        }
      });
      xhr.send('algo='+algo+'&m='+m+'&e='+e+'&nb_clusters='+nb_clusters+'&alpha_cut='+alpha_cut+'&a='+a);
    }

    </script>

  </body>
</html>
