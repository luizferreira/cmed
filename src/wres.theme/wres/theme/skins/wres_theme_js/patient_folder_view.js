//define the table search object, which can implement both functions and properties
window.tableSearch = {};

//initialize the search, setup the current object
tableSearch.init = function() {
    //define the properties I want on the tableSearch object
    this.Rows = document.getElementById('data').getElementsByTagName('tr');
    this.RowsLength = tableSearch.Rows.length;
    this.RowsText = [];

    //loop through the table and add the data to the table search object
    for (var i = 0; i < tableSearch.RowsLength; i++) {
        this.RowsText[i] = (tableSearch.Rows[i].innerText) ? tableSearch.Rows[i].innerText.toUpperCase() : tableSearch.Rows[i].textContent.toUpperCase();
        }
    }

//onlys shows the relevant rows as determined by the search string
    tableSearch.runSearch = function() {
        //get the search term
        this.Term = document.getElementById('textBoxSearch').value.toUpperCase();
        
        //loop through the rows and hide rows that do not match the search query
        for (var i = 0, row; row = this.Rows[i], rowText = this.RowsText[i]; i++) {
            row.style.display = ((rowText.indexOf(this.Term) != -1) || this.Term === '') ? '' : 'none';
        }
    }

 //handles the enter key being pressed
        tableSearch.search = function(e) {
            //checks if the user pressed the enter key, and if they did then run the search
            var keycode;
            if (window.event) { keycode = window.event.keyCode; }
            else if (e) { keycode = e.which; }
            else { return false; }
            if (keycode == 13) {
                tableSearch.runSearch();
            }
            else { return false; }
        }

        $(document).ready(function(){
        tableSearch.init();
        });

    