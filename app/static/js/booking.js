function bookFlight() {
    fetch('/api/schedule', {
        method: 'get',
        body: JSON.stringify({
            "departure_airport": departure_airport,
            "arrival_airport": arrival_airport,
            "start": start,
            "end": end,
            "roundTrip": roundTrip
        })
    })
}


function add_flight() {
    fetch('/api/schedule', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'departure_time': departure_time,
            'time_flight': time_flight,
            'route': route_flight,
            'aircraft': aircraft,
            'economy_seats': economy_seats,
            'business_seats': business_seats
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }
    )
        .then(function (res) {
            return res.json()
        })
        .then(function (data) {
            console.log(data)
        })

}