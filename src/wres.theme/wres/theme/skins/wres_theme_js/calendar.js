/* menu functions */
function multidoctorGoTo(form_id) {
  eval(targ + ".location='" + selObj.options[selObj.selectedIndex].value + "'");
  if(restore) selObj.selectedIndex = 0;
}

/* Set date based on "jump_to_date". */
function setJumpDate(monthId, dayId, yearId, jumpDateId, form) {
    var month = document.getElementById(monthId);
    var day = document.getElementById(dayId);
    var year = document.getElementById(yearId);
    var jumpDate = document.createElement("input");
    
    // set jumpDate properties
    jumpDate.type = "hidden";
    jumpDate.id = jumpDateId;
    jumpDate.name = jumpDateId;
    jumpDate.value = year.value + "/" + month.value + "/" + day.value;
    
    // append jumpDate to form
    form.appendChild(jumpDate);
    
    // submit form
    form.submit();
}

/* Content menu functions */
function calendarGoTo(targ, selObj, restore) {
  eval(targ + ".location='" + selObj.options[selObj.selectedIndex].value + "'");
  if(restore) selObj.selectedIndex = 0;
}


/* calendar functions */

var PREFIX = "cal";
var BGCOLOR_DEFAULT = new Array(new Array("event", "#DEE7EC"), new Array("noevent", "#F7F9FA"), new Array("outOfMonth", "#FFFFFF"));
var BGCOLOR_HIGHLIGHTED = "#FFE7C4";
var MAX_ID = 0;



/**
 * Functions called from pt. Calls highlightEventRange() and showCalPopup() or clearEventRange() and hideCalPopup().
 */
function mouseOverEvent(start, end, eventID) {
    if (evntOpen != null){
      hideCalPopup(evntOpen);
      evntOpen=null
    }
    highlightEventRange(start, end);
    showCalPopup(eventID);
    evntOpen = eventID;
}
var evntID;
var evntOpen=null;
function mouseOutEvent(start, end, eventID) {
    clearEventRange(start, end);
    evntID = eventID;
    setTimeout("javascript: hideCalPopup(evntID);", 5000 ) // after 5 seconds
}



/**
 * Functions used for highlighting the time-range of an event in the current (month, week, week2, day) calendarview.
 */
function setMax(maxID) {
    MAX_ID = maxID;
}
function highlightEventRange(start, end) {
    for(i = start; i <= end; i++) {
        if ((MAX_ID > 0) && (i > MAX_ID)) {
            i = end;
        }
        else {
            
               if(getElem("id", PREFIX + i, null)!=null)
                  getElem("id", PREFIX + i, null).style.backgroundColor = BGCOLOR_HIGHLIGHTED;
        }
    }
}
function clearEventRange(start, end) {
    for(i = start; i <= end; i++) {
        if ((MAX_ID > 0) && (i > MAX_ID)) {
            i = end;
        }
        else {
            elem = getElem("id", PREFIX + i, null);
            elemClass = getAttr("id", PREFIX + i, null, "class");
            bgcolor = "";
            for(j = 0; j < BGCOLOR_DEFAULT.lenght; j++) {
                if (BGCOLOR_DEFAULT[j][0] == elemClass) {
                    bgcolor = BGCOLOR_DEFAULT[j][1];
                    j = BGCOLOR_DEFAULT.length;
                }
            }
            
            if(getElem("id", PREFIX + i, null)!=null)
                  getElem("id", PREFIX + i, null).style.backgroundColor = bgcolor;
        }
    }
}

/**
 * function used to show/hide popup "window" (div-tag)
 */
function showCalPopup(tagID) {
    getElem("id", tagID, null).style.visibility = "visible";
}
function hideCalPopup(tagID) {    
    getElem("id", tagID, null).style.visibility = "hidden";
}

function onChangeDateHandler(field, year, month, day, hour, minute, ampm){
    var fyear   = document.getElementById(year);
    var fmonth  = document.getElementById(month);
    var fday    = document.getElementById(day);
    if(isValidDay(fyear, fmonth, fday)){
        alert("Entrou no validador");
        update_date_field(field, year, month, day, hour, minute, ampm);
        return true;
    }
    else{
        var last_day = getMonthLength(fmonth.value, fyear.value);
        fday.value = last_day.toString();
        update_date_field(field, year, month, day, hour, minute, ampm);
        return false;
    }
}

function onChangeDayHandler(field, year, month, day, hour, minute, ampm){
    var fday    = document.getElementById(day);
    var cache_day_value = fday.value;
    var ok = onChangeDateHandler(field, year, month, day, hour, minute, ampm);
    if(!ok){
       alert("this month doesn't have day " + cache_day_value);
    }
}

function getMonthLength(month, year){
    var month_length = {'01': 31,
        '02': 28,
        '03': 31,
        '04': 30,
        '05': 31,
        '06': 30,
        '07': 31,
        '08': 31,
        '09': 30,
        '10': 31,
        '11': 30,
        '12': 31
    };
    if(isBissext(year)){
        month_length['02'] = 29;
    }
    return month_length[month];
}

function isValidDay(year, month, day){
    return day.value <= getMonthLength(month.value, year.value);
}

function isBissext(year){
    return (year%4==0);
}
