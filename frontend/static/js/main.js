document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips everywhere using Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handling event form submission with basic validation
    const eventForm = document.querySelector('#event-form');
    if (eventForm) {
        eventForm.addEventListener('submit', function(event) {
            // Example validation: ensure the event name is entered
            let eventName = document.querySelector('#event-name').value;
            if (!eventName) {
                alert('Please enter an event name.');
                event.preventDefault(); // Prevent form submission
            }
        });
    }

    // Confirm dialog for deleting items
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this?')) {
                event.preventDefault(); // Prevent the delete action
            }
        });
    });
});
