
             function aparecer_pastas() {
      var x = document.getElementById("ver_arquivos");
    if (x.style.display === "none")
    {
        x.style.display = "block";
}
else
{
        x.style.display = "none";

}



    }


       function aparecer_senhas() {
      var x = document.getElementById("ver_senhas");

    if (x.style.display === "none")
    {
        x.style.display = "block";
}
else
{
        x.style.display = "none";

}



    }

    window.onload = initPage;

function initPage(){
  var y = document.getElementById("ver_arquivos");
y.style.display = "none";
}
