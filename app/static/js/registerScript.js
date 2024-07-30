<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Select all interest items
        var interestItems = document.querySelectorAll('.interest-item');

        // Function to update the visual style based on the checkbox state
        var updateStyle = function(checkbox, label, item) {
            if (checkbox.checked) {
                label.style.backgroundColor = '#007bff';
                label.style.color = '#fff';
                item.style.borderColor = '#007bff';
            } else {
                label.style.backgroundColor = '';
                label.style.color = '';
                item.style.borderColor = '#ccc';
            }
        };

        // Add click event listener to each item
        interestItems.forEach(function(item) {
            var checkbox = item.querySelector('input[type="checkbox"]');
            var label = item.querySelector('.interest-label');

            // Initialize the style based on the initial checkbox state
            updateStyle(checkbox, label, item);

            // Toggle the checkbox and update the style on click
            item.addEventListener('click', function() {
                checkbox.checked = !checkbox.checked;
                updateStyle(checkbox, label, item);
            });
        });
    });
</script>
