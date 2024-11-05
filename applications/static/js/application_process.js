function showStep(step) {
    document.querySelectorAll('.step').forEach(stepDiv => stepDiv.style.display = 'none');
    document.getElementById(`step-${step}`).style.display = 'block';
    document.getElementById('progress-bar').value = step;
}

function nextStep(currentStep) {
    showStep(currentStep + 1);
}

function previousStep(currentStep) {
    showStep(currentStep - 1);
}
