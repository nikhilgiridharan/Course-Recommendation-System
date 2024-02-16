function openPopup() {
    document.getElementById("popupWindow").style.display = "block";
}

function closePopup() {
    document.getElementById("popupWindow").style.display = "none";
}

document.addEventListener('DOMContentLoaded', function() {
    // Select the dropdown element
    var selectElement = document.getElementById('sortOptions');

    // Add change event listener
    selectElement.addEventListener('change', function() {
        var selectedValue = this.value; // Get the selected option value
        if (selectedValue) {
            // Update the URL with the selected value as a parameter
            window.location.href = updateURLParameter(window.location.href, 'sort', selectedValue);
        }
    });
});

function updateURLParameter(url, param, paramVal) {
    var tempArray = url.split("?");
    var baseUrl = tempArray[0];
    return baseUrl + "?" +  param + "=" + paramVal;
}
