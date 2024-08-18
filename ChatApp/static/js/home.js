// JavaScriptでリロード機能を追加
document.getElementById('reload-btn').addEventListener('click', function() {
    location.reload();
});

document.getElementById('backButton').addEventListener('click', function() {
    // 直前のページに戻る
    history.back();
});
