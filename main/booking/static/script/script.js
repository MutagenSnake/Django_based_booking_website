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

