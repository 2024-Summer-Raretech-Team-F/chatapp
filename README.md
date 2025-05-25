# 📖 Chimy 〜 小学校向け連絡帳チャットアプリ 〜
## DEMO


## Member
### Leader
- [**take917**](https://github.com/take917)

### Frontend
- [**Fugashi3**](https://github.com/Fugashi-umashi)
- [**NARU06120322**](https://github.com/NARU06120322)

### Backend
- [**Fuji**](https://github.com/anton-fuji)

### Infra
- [**HHTAKU**](https://github.com/HHTAKU)

# 🌱 Skill Stack
| Frontend                                                                                                                                           | Backend                                                                                                                                                         | Infra                                                                                                                           |
|----------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| <img src="https://img.shields.io/badge/HTML-E34F26?logo=html5&logoColor=white" alt="HTML" height="30" /> <br/> <img src="https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=white" alt="CSS" height="30" /> <br/> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black" alt="JavaScript" height="30" /> | <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python" height="30" /> <br/> <img src="https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white" alt="Flask" height="30" /> <br/> <img src="https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white" alt="MySQL" height="30" /> | <img src="https://img.shields.io/badge/AWS-232F3E?logo=amazonaws&logoColor=white" alt="AWS" height="30" /> <br/> <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker" height="30" /> |
# 🛠️ Setup
**起動方法**
```
docker compose up
```

### ディレクトリ構成
```
.
├── ChatApp              # ディレクトリ
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── static          # 静的ファイル用ディレクトリ
│   ├── templates       # Template(HTML)用ディレクトリ
│   └── util
|         └──DB.py
├── Docker
│   ├── Flask
│   │   └── Dockerfile # Flask(Python)用Dockerファイル
│   └── MySQL
│       ├── Dockerfile  # MySQL用Dockerファイル
│       ├── init.sql    # MySQL初期設定ファイル
│       └── my.cnf
├── docker-compose.yml   # Docker-composeファイル
└── requirements.txt     # 使用モジュール記述ファイル
```
