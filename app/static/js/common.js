
function abbreviateWords(inputString) {
    let arr = inputString.split(' ')
    let str = ''

    arr.forEach(function (f) {
        str += f.slice(0,1)
    })

    return str.toUpperCase()
}


function addTimeStrings(dateString, timeString) {
    // Chuyển đổi chuỗi ngày và giờ thành đối tượng Date
    var date = new Date(dateString);
    var dateMillis = date.getTime();

    //JavaScript doesn't have a "time period" object, so I'm assuming you get it as a string

    var parts = timeString.split(/:/);
    var timePeriodMillis = (parseInt(parts[0], 10) * 60 * 60 * 1000) +
                           (parseInt(parts[1], 10) * 60 * 1000) +
                           (parseInt(parts[2], 10) * 1000);

    var newDate = new Date();
    newDate.setTime(dateMillis + timePeriodMillis);

    return newDate;
}