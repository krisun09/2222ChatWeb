function addFriendWindowAlert(){
    var message = "You have successfully sent the request";
    alert(message);
}

function setLocalStorage(key, value) {
    localStorage.setItem(key, value);
}

function getLocalStorage(key) {
    var value = localStorage.getItem(key)
    return value
}

function setCookie(key, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = key + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(key) {
    var keyEQ = key + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(keyEQ) == 0)
        // If the cookie is found (c.indexOf(name) == 0), return the value of the cookie (c.substring(name.length, c.length).
        document.getElementById(getCookie('name')).innerHTML = c.substring(keyEQ.length,c.length);
        return c.substring(keyEQ.length,c.length);
    }
    // If the cookie is not found, return "".
    return "not found";
}

function setSessionStorage(key, value) {
    sessionStorage.setItem(key, value);
    alert('username successfully stored')
}

function getSessionStorage(key) {
    var value = sessionStorage.getItem(key)
    return value
}