var divElement    = document.getElementById('viz1687885788898');
var vizElement    = divElement.getElementsByTagName('object')[0];
var scriptElement = document.createElement('script');

vizElement.style.width = '900px';
vizElement.style.height='1127px';
scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
vizElement.parentNode.insertBefore(scriptElement, vizElement);