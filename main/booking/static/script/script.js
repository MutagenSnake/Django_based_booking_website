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
                dayFrom = bookingData[i]['day_from']
                dayTo = bookingData[i]['day_to']
                const paragraph = document.createElement("tr");
                paragraph.innerHTML = `<tr><th scope="row">Time From: ${dayFrom} Time To: ${dayTo}</th></tr>`;
                document.getElementById("tableBodyForInsertion").appendChild(paragraph);}
        }}

getData()
listDates()

// Script for calendar

// function returning list of booked days
function getApplianceDays (allBookings) {
    workingDayStringList = [];
    for (let i = 0; i < allBookings.length; i++) {
//        console.log(bookings[i]['appliance'])
        if (allBookings[i]['appliance'] == applianceID) {
            console.log(allBookings[i])
            // Get dates in date format
            let dateIsoStart= allBookings[i]['day_from'];
            let dateIsoEnd= allBookings[i]['day_to'];
            const dateStart = new Date(dateIsoStart);
            const dateEnd = new Date(dateIsoEnd);
            // Get days within
            let difference = dateEnd.getTime() - dateStart.getTime();
            let totalDays = Math.ceil(difference / (1000 * 3600 * 24));
            let dateList = [];
            for (let i = 0; i < totalDays+1; i++) {
                let workingDate = new Date(dateIsoStart);
                workingDate.setDate(workingDate.getDate() + i);
                dateList.push(workingDate);
                }

            for (let i = 0; i < dateList.length; i++) {
                const day = dateList[i].getDate();
                const month = dateList[i].getMonth();
                const year = dateList[i].getFullYear();

//                console.log(`${month+1}/${day}/${year}`)
                workingDayStringList.push(`${month+1}/${day}/${year}`)
            }}
        }
        return workingDayStringList
}



let nav = 0;
let clicked = null;
let events = localStorage.getItem('events') ? JSON.parse(localStorage.getItem('events')) : [];

const calendar = document.getElementById('calendar');
const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

async function load() {
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

    const bookingData = await getData()

    const workingDayStringList = getApplianceDays(bookingData);

    for(let i = 1; i <= paddingDays + daysInMonth; i++) {
        const daySquare = document.createElement('div');
        daySquare.classList.add('day');

        const dayString = `${month+1}/${i - paddingDays}/${year}`;

        if (i > paddingDays) {
            daySquare.innerText = i - paddingDays;

            if (workingDayStringList.includes(dayString)) {
                daySquare.innerHTML = `${i - paddingDays}<br>Booked`
                daySquare.style.boxShadow = "0px 0px 3px red";
            }

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
