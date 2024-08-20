// JavaScriptでリロード機能を追加
document.getElementById('reload-btn').addEventListener('click', function() {
    location.reload();
});

document.getElementById('backButton').addEventListener('click', function() {
    // 直前のページに戻る
    history.back();
});

//document.addEventListener('DOMContentLoaded', function() {
    // Flaskから渡された未読メッセージ数
    //var unreadTeacherMessages = parseInt(document.getElementById('unread-teacher').textContent);
    //var unreadGroupMessages = parseInt(document.getElementById('unread-group').textContent);

    //if (unreadTeacherMessages > 0) {
    //    document.getElementById('unread-teacher').style.display = 'inline-block';
    //} else {
   //     document.getElementById('unread-teacher').style.display = 'none';
    //}

    //if (unreadGroupMessages > 0) {
   //     document.getElementById('unread-group').style.display = 'inline-block';
   // } else {
    //    document.getElementById('unread-group').style.display = 'none';
   // }
//}); 
