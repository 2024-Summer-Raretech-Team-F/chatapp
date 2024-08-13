document.addEventListener('DOMContentLoaded', () => {
    const notices = [
        { date: '2025-05-01', title: '連休開始' },
        { date: '2024-08-11', title: '山の日' },
        { date: '2025-05-09', title: '授業終了' }
    ];

//アカウントサンプル//

    const accounts = [
        {
            id: 1,
            name: "アカウント1",
            chats: [
                { name: "ユーザーA", message: "承知いたしました。", time: "10:00 AM" },
                { name: "ユーザーB", message: "学校案内について", time: "10:05 AM" }
            ]
        },
        {
            id: 2,
            name: "アカウント2",
            chats: [
                { name: "ユーザーC", message: "授業参観について", time: "11:00 AM" },
                { name: "ユーザーD", message: "本日の授業に関しまして", time: "11:15 AM" }
            ]
        },
        {
            id: 3,
            name: "アカウント3",
            chats: [
                { name: "ユーザーE", message: "アレルギーについて", time: "12:00 PM" },
                { name: "ユーザーF", message: "宿題について", time: "12:30 PM" }
            ]
        }
    ];
    

// チャットリストを生成する関数
function populateChatList(chatListElement, chats) {
    chats.forEach(chat => {
        const chatItem = document.createElement('div');
        chatItem.className = 'chat-item';
        chatItem.innerHTML = `
            <i class="fa-regular fa-circle-user fa-sm"></i>
            <div>
                <span class="chat-name">${chat.name}</span>
                 <div class="chat-content">
                    <span class="chat-message">${chat.message}</span> <span class="chat-time">${chat.time}</span>
                </div>
            </div>
        `;
        chatItem.addEventListener('click', () => {
            window.location.href = 'chat.html';
        });
        chatListElement.appendChild(chatItem);
    });
}

    //お知らせクリック遷移//
    const noticeBtn = document.getElementById('notice-btn');
    noticeBtn.addEventListener('click', () => {
        window.location.href = 'notices.html';
    });

    //カレンダー乗っける//
    const calendarElement = document.getElementById('calendar');
    generateCalendar(calendarElement, notices);

    //チャット一覧のせる//
    const chatListContainer = document.getElementById('chat-list');

/*===================================================*/
//チャット関係//
    accounts.forEach(account => {
        // アカウントのコンテナを作成
        const accountDiv = document.createElement('div');
        accountDiv.classList.add('account');
        accountDiv.setAttribute('data-account-id', account.id);

        // アカウント名を追加
        const accountName = document.createElement('div');
        accountName.classList.add('account-name');
        accountName.textContent = account.name;
        accountDiv.appendChild(accountName);

        // チャットリストを作成して追加
        populateChatList(accountDiv, account.chats);

        // アカウントコンテナをメインのチャットリストに追加
        chatListContainer.appendChild(accountDiv);
    });

});


/*===================================================*/

//カレンダー生成意味わからん…//

let currentYear = 2024;
let currentMonth = 7; // 0が1月、4が5月

const notices = [
    { date: '2024-08-11', title: '山の日' },
    { date: '2025-05-09', title: 'ミーティング' }
];

function generateCalendar(calendarElement, notices) {
    calendarElement.innerHTML = ''; // 既存のカレンダーをクリア

    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay(); // 月初めの曜日を取得

    const table = document.createElement('table');
    const headerRow = table.insertRow();

    ['日', '月', '火', '水', '木', '金', '土'].forEach(day => {
        const cell = headerRow.insertCell();
        cell.textContent = day;
    });

    let row = table.insertRow();

    // 月初めの曜日に基づいて空のセルを追加
    for (let i = 0; i < firstDayOfMonth; i++) {
        row.insertCell();
    }

    for (let i = 1; i <= daysInMonth; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const dayOfWeek = date.getDay();

        if (dayOfWeek === 0 && i !== 1) {
            row = table.insertRow();
        }

        const cell = row.insertCell();
        cell.textContent = i;
        cell.dataset.date = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        
        // 土曜日と日曜日の色を設定する
        if (dayOfWeek === 6) {
            cell.classList.add('saturday');
        } else if (dayOfWeek === 0) {
            cell.classList.add('sunday');
        }

        cell.addEventListener('click', () => {
            const selectedDateNotice = notices.find(notice => notice.date === cell.dataset.date);
            document.getElementById('selected-date-notice').textContent = selectedDateNotice ? selectedDateNotice.title : 'その日にお知らせはありません。';
        });
    }

    calendarElement.appendChild(table);

    // 現在の年月を表示
    const monthNames = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"];
    document.getElementById('calendar-month').textContent = `${currentYear}年 ${monthNames[currentMonth]}`;
}

function changeMonth(offset) {
    currentMonth += offset;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    } else if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    generateCalendar(document.getElementById('calendar'), notices);
}

document.getElementById('prev-month').addEventListener('click', () => changeMonth(-1)); 
document.getElementById('next-month').addEventListener('click', () => changeMonth(1)); 

// 初期化
document.addEventListener('DOMContentLoaded', () => { // DOMが完全にロードされた後に初期化?

    generateCalendar(document.getElementById('calendar'), notices);
});








