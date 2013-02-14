function novaData(n) {
        this.length = n
        return this
    }
    NMes = new novaData(12)
    NMes[1] = "Janeiro"
    NMes[2] = "Fevereiro"
    NMes[3] = "Março"
    NMes[4] = "Abril"
    NMes[5] = "Maio"
    NMes[6] = "Junho"
    NMes[7] = "Julho"
    NMes[8] = "Agosto"
    NMes[9] = "Setembro"
    NMes[10] = "Outubro"
    NMes[11] = "Novembro"
    NMes[12] = "Dezembro"
    DDias = new novaData(7)
    DDias[1] = "Domingo"
    DDias[2] = "Segunda-Feira"
    DDias[3] = "Terça-Feira"
    DDias[4] = "Quarta-Feira"
    DDias[5] = "Quinta-Feira"
    DDias[6] = "Sexta-Feira"
    DDias[7] = "Sábado"
    
    function NData(cDate) {
		var Dia = DDias[cDate.getDay() + 1]
        var Mes = NMes[cDate.getMonth() + 1]
        msie4 = ((navigator.appName == "Microsoft Internet Explorer")
            && (parseInt(navigator.appVersion) >= 4 ));
        if (msie4) {
            var ano = cDate.getYear()
        }
        else {
             var ano = cDate.getYear() +1900
        }
        return Dia + ", " + cDate.getDate() + " de " + Mes + " " +  " de " + ano
    }     
    function stringToDate(){
        try{
        var doc_date = document.getElementById("doc_date").innerHTML;
        var dateArray = doc_date.split("/");
        var date = new Date(dateArray[2],dateArray[1]-1,dateArray[0]);
            return date;    
        }
        catch(err){
          d1 = new Date()
		  return d1;
        }
    }
     $(document).ready(function(){
		var doc_date = stringToDate();

		$(".date").each(function(index,value){
          $(this).html(NData(doc_date));  
        });

        $(".tomorrow-string").each(function(index,value){
          doc_date = new Date(doc_date.getTime() +  24 * 60 * 60 * 1000)
          $(this).html(NData(doc_date));  
        });
    });
                            
