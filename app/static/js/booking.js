async function search_flight(queryString) {
    console.log(start.value, arrival_airport.value, departure_airport.value)
    await fetch('/api/flight?' + queryString, {
        method: 'get',
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res){
        return res.json()
    }).then(function (data) {
        if (data.status == 200) {
            let flights = JSON.parse(data.flights)
            console.log(flights)
            let flight_html = ''

            flights.forEach(function (f) {
                console.log(f, f.stop_airports.length)

                departure_time = new Date(f.departure_time)

                let arrivial_time = addTimeStrings(f.departure_time, f.time_flight)
                flight_html += `
                    <div class="py-10">
                      <div class="max-w-full p-5  bg-white flex flex-col rounded overflow-hidden shadow-lg">
                        <div class="flex flex-row items-baseline flex-nowrap p-2">
                          <svg viewBox="0 0 64 64" data-testid="tripDetails-bound-plane-icon" pointer-events="all" aria-hidden="true" class="mt-2 mr-1" role="presentation" style="fill: rgb(102, 102, 102); height: 0.9rem; width: 0.9rem;">
                            <path d="M43.389 38.269L29.222 61.34a1.152 1.152 0 01-1.064.615H20.99a1.219 1.219 0 01-1.007-.5 1.324 1.324 0 01-.2-1.149L26.2 38.27H11.7l-3.947 6.919a1.209 1.209 0 01-1.092.644H1.285a1.234 1.234 0 01-.895-.392l-.057-.056a1.427 1.427 0 01-.308-1.036L1.789 32 .025 19.656a1.182 1.182 0 01.281-1.009 1.356 1.356 0 01.951-.448l5.4-.027a1.227 1.227 0 01.9.391.85.85 0 01.2.252L11.7 25.73h14.5L19.792 3.7a1.324 1.324 0 01.2-1.149A1.219 1.219 0 0121 2.045h7.168a1.152 1.152 0 011.064.615l14.162 23.071h8.959a17.287 17.287 0 017.839 1.791Q63.777 29.315 64 32q-.224 2.685-3.807 4.478a17.282 17.282 0 01-7.84 1.793h-9.016z"></path>
                          </svg>
                          <h1 class="ml-2 uppercase font-bold text-gray-500">departure</h1>
                          <p class="ml-2 font-normal text-gray-500">${f.departure_time.split(' ')[0]}</p>
                        </div> 
                        <div class="mt-2 flex sm:flex-row mx-6 sm:justify-between flex-wrap ">
                          <div class="flex flex-row place-items-center p-2">
                            <img alt="Qatar Airways" class="w-10 h-10" src="https://i.pinimg.com/originals/7a/ec/17/7aec17946661a88378269d0b642b61f3.png" style="opacity: 1; transform-origin: 0% 50% 0px; transform: none;" />
                            <div class="flex flex-col ml-2">
                              <p class="text-[16px] text-gray-500 font-bold">Vietnam Airline</p>
                              <p class="text-[14px] text-gray-500">${f.id}</p> 
                            </div>
                          </div>
        
                          <div class="flex flex-col p-2">
                            <p class="font-bold">${f.departure_time.split(' ')[1].slice(0,5)}</p>
                            <p class="text-gray-500">
                                <span class="font-bold">${abbreviateWords(f.departure_airport.name)}</span> ${f.departure_airport.name}</p>
                            <p class="text-gray-500">${f.departure_airport.location}</p>
                          </div>
                          <div class="flex items-center">
                            <p class="text-gray-500"><span class="font-bold">${f.stop_airports.length > 0 ? `${f.stop_airports.length} điểm dừng` : `bay thẳng`}</span></p>
                          </div> 
                          <div class="flex flex-col flex-wrap p-2">
                            <p class="font-bold">${arrivial_time.getHours()}:${arrivial_time.getMinutes()}</p>
                            <p class="text-gray-500"><span class="font-bold">${abbreviateWords(f.arrival_airport.name)}</span> ${f.arrival_airport.name}</p>
                            <p class="text-gray-500">${f.arrival_airport.location}</p>
                          </div>
                        </div>
                        <div class="mt-4 flex flex-row flex-wrap md:flex-nowrap justify-end items-center"> 
                          <div class="md:border-l-2 mx-6 md:border-dotted items-center flex flex-row py-4 mr-6 flex-wrap">
                            <div class="text-[22px] text-orange-500 mx-2 flex flex-col"> 
                              <p class="font-bold">${f.economy_price.toLocaleString('it-IT', {style : 'currency', currency : 'VND'})}</p>
                            </div>
                            <button onclick="book_flight('${f.id}', '${abbreviateWords(f.departure_airport.name)}', '${f.departure_airport.location}', '${abbreviateWords(f.arrival_airport.name)}', '${f.arrival_airport.location}', '${f.departure_time.split(' ')[1].slice(0,5)}', '${arrivial_time.getHours()}:${arrivial_time.getMinutes()}')" class="w-32 h-11 rounded flex border-solid border font-bold text-white bg-blue-600 mx-2 justify-center place-items-center items-center">
                                <div class="">Đặt vé</div>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                `
            })
            document.querySelector('#flight_container').innerHTML = flight_html
        }

    })
}


function book_flight(flight_id, departure_airport_name, departure_airport_location, arrival_airport_name, arrival_airport_location, departure_time, arrivial_time) {
    fetch('/flight', {
        method: 'post',
        body: JSON.stringify({
            'flight_id': flight_id,
            'departure_airport_name': departure_airport_name,
            'departure_airport_location': departure_airport_location,
            'arrival_airport_name': arrival_airport_name,
            'arrival_airport_location': arrival_airport_location,
            'departure_time': departure_time,
            'arrival_time': arrivial_time
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }
    ).then(function (res) {
        return res.json()
    }).then(function (data) {
        console.log(data.status)
        if (data.status == '200')
            window.location.replace(data.route)
    })
}

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


