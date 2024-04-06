// document.addEventListener("DOMContentLoaded", function() {
//     // Get reference to the "View Data" button
//     const viewDataBtn = document.getElementById('view-data-btn');

//     // Add click event listener to the button
//     viewDataBtn.addEventListener('click', function() {
//         // Check if the button should fetch user data
//         const fetchUserData = viewDataBtn.dataset.fetchUserData === 'true';
//         if (fetchUserData) {
//             // Send AJAX request to Django view to fetch user data
//             fetch(window.location.href + '?fetch_user_data=true')
//                 .then(response => response.json())
//                 .then(data => {
//                     // Display fetched data in the fetched-data-container div
//                     const fetchedDataContainer = document.getElementById('fetched-data-container');
//                     fetchedDataContainer.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
//                 })
//                 .catch(error => console.error('Error fetching user data:', error));
//         }
//     });
// });




<script>
  const dataContainer = document.getElementById('dataContainer');

  fetch('/api/students')
    .then(response => response.json())
    .then(data => displayStudentData(data))
    .catch(error => console.error(error));

  function displayStudentData(data) {
    // Clear previous data
    dataContainer.innerHTML = '';

    // Filter data for the signed-in user
    const currentUserData = data.filter(student => student.user === '{{ request.user.username }}');

    // Create table headers
    const tableHeaders = Object.keys(currentUserData[0]);
    const headerRow = document.createElement('tr');
    tableHeaders.forEach(header => {
      const th = document.createElement('th');
      th.textContent = header;
      headerRow.appendChild(th);
    });
    dataContainer.appendChild(headerRow);

    // Create table rows
    currentUserData.forEach(student => {
      const row = document.createElement('tr');
      tableHeaders.forEach(header => {
        const cell = document.createElement('td');
        cell.textContent = student[header];
        row.appendChild(cell);
      });
      dataContainer.appendChild(row);
    });
  }
</script>