from flask import Flask, render_template_string
import os
import time
import psutil  # Библиотека ядра для сбора метрик оперативной памяти

app = Flask(__name__)

# Фиксация времени старта контейнера для расчета Uptime
START_TIME = time.time()
# Глобальный счетчик обработанных запросов
REQUEST_COUNT = 0

@app.before_request
def increment_counter():
    global REQUEST_COUNT
    REQUEST_COUNT += 1

@app.route('/')
def hello_world():
    uptime = round(time.time() - START_TIME, 2)
    html_template = """<!DOCTYPE html>
    <html>
    <head>
        <title>КР</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f0f4f8; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.06); text-align: center; max-width: 550px; }
            h1 { color: #2c3e50; }
            .info-box { background: #e3faf2; color: #20c997; padding: 15px; border-radius: 6px; font-family: monospace; font-size: 16px; margin: 20px 0; font-weight: bold; }
            .btn { display: inline-block; background: #4dabf7; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold; transition: 0.2s; }
            .btn:hover { background: #339af0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Flask Web Server [Вариант №18]</h1>
            <p>Приложение успешно развернуто через конвейер GitHub Actions на базе Self-Hosted раннера в WSL2 по стратегии GitHub Flow.</p>
            <div class="info-box">Сервер непрерывно работает (Uptime): {{ uptime }} сек.</div>
            <a href="/diagnostics" class="btn">Запустить диагностику ОЗУ</a>
        </div>
    </body>
    </html>"""
    return render_template_string(html_template, uptime=uptime)

@app.route('/diagnostics')
def diagnostics():
    # Сбор низкоуровневых системных метрик ОЗУ процесса и хоста WSL2
    process = psutil.Process(os.getpid())
    rss_memory = round(process.memory_info().rss / (1024 * 1024), 2)  # RSS в МБ
    vms_memory = round(process.memory_info().vms / (1024 * 1024), 2)  # Виртуальная в МБ
    system_ram = psutil.virtual_memory()
    
    html_template = """<!DOCTYPE html>
    <html>
    <head>
        <title>Панель диагностики ОЗУ - Контур CD</title>
        <style>
            body { background: #0f172a; color: #38bdf8; font-family: 'Courier New', monospace; padding: 30px; }
            .panel { border: 2px solid #38bdf8; padding: 25px; border-radius: 8px; max-width: 650px; background: #1e293b; box-shadow: 0 0 25px rgba(56,189,248,0.2); }
            .title { font-size: 18px; font-weight: bold; margin-bottom: 20px; border-bottom: 1px dashed #38bdf8; padding-bottom: 10px; text-transform: uppercase; }
            .row { margin: 10px 0; font-size: 15px; }
            .highlight { color: #f8fafc; font-weight: bold; }
            .back { display: inline-block; margin-top: 20px; color: #fb7185; text-decoration: none; border-bottom: 1px solid; }
        </style>
    </head>
    <body>
        <div class="panel">
            <div class="title">=== Мониторинг утилизации ресурсов ОЗУ ===</div>
            <div class="row">Занято физической памяти (RSS): <span class="highlight">{{ rss }} МБ</span></div>
            <div class="row">Виртуальный объем процесса (VMS): <span class="highlight">{{ vms }} МБ</span></div>
            <div class="row">Общая доступная память системы: <span class="highlight">{{ total_ram }} ГБ</span></div>
            <div class="row">Процент загрузки ОЗУ хоста WSL2: <span class="highlight">{{ ram_percent }}%</span></div>
            <div class="row">Всего транзакций обработано сервером: <span class="highlight">{{ count }}</span></div>
            <a href="/" class="back">&lt;&lt; Вернуться на главную страницу</a>
        </div>
    </body>
    </html>"""
    return render_template_string(html_template, 
                                  rss=rss_memory, 
                                  vms=vms_memory, 
                                  total_ram=round(system_ram.total / (1024**3), 2), 
                                  ram_percent=system_ram.percent, 
                                  count=REQUEST_COUNT)

if __name__ == '__main__':
    # Запуск Flask-сервера строго на порту 8888 в соответствии с требованиями КР
    app.run(host='0.0.0.0', port=8888)

