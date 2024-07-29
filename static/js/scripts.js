
function saveDataToCookie(data) {
    const d = new Date();
    d.setTime(d.getTime() + (365*24*60*60*1000)); // Cookie 有效期 1 年
    let expires = "expires=" + d.toUTCString();
    document.cookie = "userData=" + JSON.stringify(data) + ";" + expires + ";path=/";
}

function getDataFromCookie() {
    const name = "userData=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return JSON.parse(c.substring(name.length, c.length));
        }
    }
    return null;
}

function saveFormData() {
    const formData = {};
    document.querySelectorAll('input[type=radio]:checked').forEach(function(input) {
        formData[input.name] = input.value;
    });
    saveDataToCookie(formData);
}

function loadFormData() {
    const savedData = getDataFromCookie();
    if (savedData) {
        for (const name in savedData) {
            const selector = `input[name="${name}"][value="${savedData[name]}"]`;
            const input = document.querySelector(selector);
            if (input) {
                input.checked = true;
            }
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    loadFormData();
    document.querySelectorAll('input[type=radio]').forEach(function(input) {
        input.addEventListener('change', saveFormData);
    });
});

