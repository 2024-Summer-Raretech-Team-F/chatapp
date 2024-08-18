document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const formOverlay = document.querySelector('.form-overlay');
        if (formOverlay) {
            formOverlay.style.opacity = 1; // フェードインを開始
        } else {
            console.error('formOverlay not found');
        }
    }, 2000); // 2秒後にフォームを表示
});