document.addEventListener('DOMContentLoaded', function () {
    const stages = ['stage1', 'stage2', 'stage3'];
    let currentStage = 0;

    function showStage(stageIndex) {
        stages.forEach((stage, index) => {
            document.getElementById(stage).style.display = index === stageIndex ? 'block' : 'none';
        });
        updateProgressBar(stageIndex);
    }

    function updateProgressBar(stageIndex) {
        const progressPercent = ((stageIndex + 1) / stages.length) * 100;
        const progressBar = document.querySelector('.progress-bar');
        progressBar.style.width = progressPercent + '%';
        progressBar.textContent = `Step ${stageIndex + 1} of ${stages.length}`;
    }

    document.getElementById('next-button').addEventListener('click', () => {
        if (currentStage < stages.length - 1) currentStage++;
        showStage(currentStage);
    });

    document.getElementById('prev-button').addEventListener('click', () => {
        if (currentStage > 0) currentStage--;
        showStage(currentStage);
    });

    showStage(currentStage); // Initial display
});
