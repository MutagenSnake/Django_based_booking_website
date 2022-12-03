//var dataSet = {{data|safe}};
//    var dataSetLength = dataSet.length;
//    const bookingElement = document.getElementById("bookingList");
//    var bookings = [];
//    for (var i = 0; i < dataSetLength; i++) {
//        bookingHtml = `<li>${dataSet[i]}</li>`;
//        bookings.push(bookingHtml);
//        }
//    bookingElement.innerHTML = bookings;

let url = 'http://127.0.0.1:8000/bookingapi'

let bookData = []

fetch(url)
  .then((response) => response.json())
  .then((data) => bookData.push(data));

console.log(bookData)