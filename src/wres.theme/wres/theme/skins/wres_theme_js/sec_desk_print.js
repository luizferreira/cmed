function secDeskPrint(){
    
    // copia o tbody da .visits_table visivel (pode ser Hoje ou Amanhã)
    tbody_copy = $(".visits_table:visible").children("tbody").clone();

    // print_table = $("#print-table");
    print_table = $("table.cmedPrint");
    print_table.children("tbody").remove(); // limpa qualquer tbody já existente
    print_table.append(tbody_copy); // insere a cópia na tabela que será impressa

    // Esconde/Mostra titulo dependendo se será impresso Hoje ou Amanhã
    if($(".selected")[1].id == "fieldsetlegend-tomorrow"){
        $("#today-title").addClass("visualNoPrint");
        $("#tomorrow-title").removeClass("visualNoPrint");
    }
    else {
        $("#tomorrow-title").addClass("visualNoPrint");
        $("#today-title").removeClass("visualNoPrint");
    }

    print();
}