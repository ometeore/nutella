function show(){
    document.getElementById("section_substitute").style.display = "block";
    document.getElementById("remove").style.display = "none";
    document.getElementById("remove2").style.display = "none";
}

function submit_form(){
  document.getElementById("form_cat_select").submit();
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
        array = document.getElementsByClassName("element_search");
        for(x = 0; x < array.length; x++){
          array[x].style.border = "2px solid #00FF00";
        }
      }
      else{
        console.log("Nous n'avons rien trouvé correspondant a la recherche " + aliment_search);
        array = document.getElementsByClassName("element_search");
        for(x = 0; x < array.length; x++){
          array[x].style.border = "2px solid #FF0000";
        }
      }
    }
  })
}

function select_categorie(categorie_search){

  $.ajax({
    url:'/espace_admin/selection',
    data: {
      'select_categorie': categorie_search
    },
    dataType: 'json',
    success: function (data) {
      if(data.name_list.length != 0) {
        document.getElementById('select_cat_input').style.border = "2px solid #00FF00";
        array = document.getElementsByClassName("magic_tr");
        for(x = 0; x < array.length; x++){
          array[x].style.display = "none";
        }
        for(i = 0; i < data.name_list.length; i++){
          elm = document.getElementById(data.name_list[i]);
          elm.style.display="revert";
        }
      }
      else{
        document.getElementById('select_cat_input').style.border = "2px solid #FF0000";
      }
    }
  })
}
