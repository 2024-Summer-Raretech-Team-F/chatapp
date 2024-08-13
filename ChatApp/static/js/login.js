document.addEventListener('DOMContentLoaded', (event) => {
  try {
    setTimeout(() => {
      const formOverlay = document.querySelector('.form-overlay');
      if (formOverlay) {
        formOverlay.classList.remove('hidden');
        requestAnimationFrame(() => {
          formOverlay.style.opacity = 1; // フェードイン効果を開始
          formOverlay.style.transform = 'translateY(0)'; // 浮かび上がる効果を開始
        });
      } else {
        console.error('formOverlay not found');
      }
    }, 2000); // 2秒後にフォームを表示

    // アニメーション終了時に再度繰り返さないようにする
    const honhiLElement = document.querySelector('#honhiL');
    if (honhiLElement) {
      honhiLElement.addEventListener('animationend', function() {
        this.style.animation = 'none';
      });
    } else {
      console.error('#honhiL not found');
    }

    const leftElement = document.querySelector('.left');
    if (leftElement) {
      leftElement.addEventListener('animationend', function() {
        this.style.animation = 'none';
      });
    } else {
      console.error('.left not found');
    }
  } catch (error) {
    console.error('Error during DOMContentLoaded:', error);
  }
});
