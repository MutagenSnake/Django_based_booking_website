let url = 'http://127.0.0.1:8000/bookingapi'

var bookData = [];
const applianceID = document.getElementById("applianceID").innerText;

const htmlElement = ''

async function getData() {
    try {
        const rawData = await fetch(url)
        const data = await rawData.json()
        return data
    } catch (err) {
        console.log('Error in fetching data')
    }
}

async function listDates() {
    const bookingData = await getData()
        for (let i = 0; i < bookingData.length; i++) {
            if (bookingData[i]['appliance'] == applianceID) {
                const paragraph = document.createElement("tr");
                paragraph.innerHTML = `<tr><th scope="row">Time From: ${bookingData[i]['day_from']} Time To: ${bookingData[i]['day_to']}</th></tr>`;
                document.getElementById("tableBodyForInsertion").appendChild(paragraph);}
        }}

getData()
listDates()

// Script for calendar

bookings = [
    {
        "id": 7,
        "appliance": 1,
        "day_from": "2022-11-01T21:16:00Z",
        "day_to": "2022-11-15T21:16:00Z",
        "user": 1
    },
    {
        "id": 8,
        "appliance": 1,
        "day_from": "2022-11-04T21:16:00Z",
        "day_to": "2022-11-21T21:16:00Z",
        "user": 1
    },
    {
        "id": 9,
        "appliance": 2,
        "day_from": "2022-12-01T21:16:00Z",
        "day_to": "2022-12-10T21:16:00Z",
        "user": 1
    },
    {
        "id": 10,
        "appliance": 2,
        "day_from": "2022-11-02T21:17:00Z",
        "day_to": "2022-11-19T21:17:00Z",
        "user": 1
    }
]
// get booking data
console.log(bookings)

for (let i = 0; i < bookings.length; i++) {
    // Get dates in date format
    let dateIsoStart= bookings[i]['day_from'];
    let dateIsoEnd= bookings[i]['day_to'];
    const dateStart = new Date(dateIsoStart);
    const dateEnd = new Date(dateIsoEnd);
    // Get days within
    let difference = dateEnd.getTime() - dateStart.getTime();
    let totalDays = Math.ceil(difference / (1000 * 3600 * 24));
    let dateList = [];
    for (let i = 0; i < totalDays; i++) {
        let workingDate = dateStart;
        workingDate.setDate(workingDate.getDate() + i);
        console.log(workingDate)
        dateList.push(workingDate);
        }
    console.log(dateList)
}



let nav = 0;
let clicked = null;
let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];

const calendar = document.getElementById('calendar');
const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

function load() {
    const dt = new Date();

    if (nav !== 0) {
        dt.setMonth(new Date().getMonth() + nav);
    }

    const day = dt.getDate();
    const month = dt.getMonth();
    const year = dt.getFullYear();

    const firstDayOfMonth = new Date(year, month, 1);
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const dateString = firstDayOfMonth.toLocaleDateString('en-us', {
        weekday: 'long',
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
    });

    const paddingDays = weekdays.indexOf(dateString.split(', ')[0]);
    document.getElementById('monthDisplay').innerText = `${dt.toLocaleDateString('en-us', {month: 'long'})} ${year}`;

    calendar.innerHTML = '';

    for(let i = 1; i <= paddingDays + daysInMonth; i++) {
        const daySquare = document.createElement('div');
        daySquare.classList.add('day');

        const dayString = `${month+1}/${i - paddingDays}/${year}`;

        if (i > paddingDays) {
            daySquare.innerText = i - paddingDays;
            daySquare.addEventListener('click', () => console.log(`${month+1}/${i - paddingDays}/${year}`));
        }
        else {
            daySquare.classList.add('padding');
        }

        calendar.appendChild(daySquare);
    }

}

function initButtons() {
    document.getElementById('nextButton').addEventListener('click', () => {
    nav++;
    load();
    });
    document.getElementById('backButton').addEventListener('click', () => {
    nav--;
    load();
    });

};

initButtons();
load();


