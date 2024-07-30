<script>
// JavaScript to handle the expand/collapse functionality and selection visual update
document.addEventListener('DOMContentLoaded', function() {
    var offerings = document.querySelectorAll('.course-offering');

    offerings.forEach(function(offering) {
        var checkbox = offering.querySelector('input[type="checkbox"]');
        var label = offering.querySelector('.offering-label');

        // Toggle the checkbox and update the style on click
        label.addEventListener('click', function() {
            checkbox.checked = !checkbox.checked;
            if (checkbox.checked) {
                label.style.backgroundColor = '#007bff';
                label.style.color = '#fff';
            } else {
                label.style.backgroundColor = '#f1f1f1';
                label.style.color = '#000';
            }
        });
    });
});
</script>