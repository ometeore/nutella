function show(){
    document.getElementById("section_substitute").style.display = "block";
    document.getElementById("remove").style.display = "none";
    document.getElementById("remove2").style.display = "none";
}

function validate_aliment(aliment_search){

  $.ajax({
    url:'/aliment/validation',
    data: {
      'element_search': aliment_search
    },
    dataType: 'json',
    success: function (data) {
      if(data.is_taken) {
        console.log('ok il y a encore des aliments qui match');
        //document.getElementById("element_search").style.border = "2px solid #00FF00"; 
        array = document.getElementsByClassName("element_search");
        for(x = 0; x < array.length; x++){
          array[x].style.border = "2px solid #00FF00";
        }
      }
      else{
        console.log("Nous n'avons rien trouvé correspondant a la recherche " + aliment_search);
        //document.getElementById("element_search").style.border = "2px solid #FF0000"; 
        array = document.getElementsByClassName("element_search");
        for(x = 0; x < array.length; x++){
          array[x].style.border = "2px solid #FF0000";
        }
      }
    }
  })

}
