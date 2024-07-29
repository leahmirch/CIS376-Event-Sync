document.addEventListener('DOMContentLoaded', function() {
    // Function to update the event list dynamically without reloading the page
    function updateEventList() {
        fetch('/api/events')
            .then(response => response.json())
            .then(events => {
                const eventsList = document.querySelector('#events-list');
                eventsList.innerHTML = ''; // Clear existing events
                events.forEach(event => {
                    let eventElement = document.createElement('tr');
                    eventElement.innerHTML = `
                        <td>${event.name}</td>
                        <td>${new Date(event.date).toLocaleString()}</td>
                        <td>${event.location}</td>
                        <td>
                            <a href="/event/${event.id}" class="btn btn-info">View</a>
                            <a href="/event/${event.id}/edit" class="btn btn-secondary">Edit</a>
                            <button class="btn btn-danger btn-delete" data-id="${event.id}">Delete</button>
                        </td>
                    `;
                    eventsList.appendChild(eventElement);
                });
                attachDeleteEventListeners(); // Re-attach listeners to new delete buttons
            })
            .catch(error => console.error('Error loading events:', error));
    }

    // Attach event listeners to delete buttons
    function attachDeleteEventListeners() {
        const deleteButtons = document.querySelectorAll('.btn-delete');
        deleteButtons.forEach(button => {
            button.addEventListener('click', function(event) {
                const eventId = this.getAttribute('data-id');
                if (confirm('Are you sure you want to delete this event?')) {
                    fetch(`/api/events/${eventId}`, { method: 'DELETE' })
                        .then(response => {
                            if (response.ok) {
                                updateEventList(); // Refresh the list after deletion
                            } else {
                                alert('Failed to delete event.');
                            }
                        })
                        .catch(error => console.error('Error deleting event:', error));
                }
            });
        });
    }

    // Initial call to update the event list on page load
    updateEventList();
});
