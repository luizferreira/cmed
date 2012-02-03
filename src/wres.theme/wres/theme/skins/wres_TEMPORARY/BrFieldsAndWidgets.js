function autoTab(field, index){
    var form = field.form;
    var fieldName = field.name;
    var iLen = String(fieldName).length;
    var fieldFamily = form[fieldName];
    var fieldFamilySize = fieldFamily.length;
    nextIndex = index + 1;
    if (nextIndex >= fieldFamilySize){
        nextIndex = 0;
    }
    if ((field.value.length==field.getAttribute("maxlength")) && nextIndex){
        form[fieldName][nextIndex].focus();
    }
    updateField  (form, fieldFamily, String(fieldName).substring(1, iLen));
}

function updatePhone(field){
    var form = field.form;
    var fieldName = field.name;
    var iLen = String(fieldName).length;
    var fieldFamily = form[fieldName];
    var fieldFamilySize = fieldFamily.length;
    updateField  (form, fieldFamily, String(fieldName).substring(1, iLen));

}

function updateTime(field){
    var form = field.form;
    var fieldName = field.name;
    var iLen = String(fieldName).length;
    var fieldFamily = form[fieldName];
    var fieldFamilySize = fieldFamily.length;
    updateField  (form, fieldFamily, String(fieldName).substring(1, iLen));
}

function updateField(form, fieldFamily, fieldName){
    var tmp_value = '';
    for (i=0;i<fieldFamily.length;i++){
        if (fieldFamily[i].type =='text'){
            tmp_value += fieldFamily[i].value;
        }else{
            tmp_value += fieldFamily[i].options[fieldFamily[i].selectedIndex].value;
            if (tmp_value == '--')
            {
                tmp_value = ''
            }
        }
    }
    form[fieldName].value = tmp_value;
}