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