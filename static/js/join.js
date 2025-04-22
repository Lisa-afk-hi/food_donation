document.addEventListener('DOMContentLoaded', function() {
    const purposeSelect = document.getElementById('purpose');
    const donationTypeDiv = document.getElementById('donation-type');
    const assistanceNeedsDiv = document.getElementById('assistance-needs');
    
    function toggleFields() {
        const purpose = purposeSelect.value;
        
        // Hide all conditional fields first
        donationTypeDiv.style.display = 'none';
        assistanceNeedsDiv.style.display = 'none';
        
        // Show relevant fields based on selection
        if (purpose === 'donate') {
            donationTypeDiv.style.display = 'block';
        } else if (purpose === 'assistance') {
            assistanceNeedsDiv.style.display = 'block';
        }
    }
    
    // Initial toggle
    toggleFields();
    
    // Add event listener for changes
    purposeSelect.addEventListener('change', toggleFields);
});