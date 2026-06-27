# 2D платформер написанный на Python, PyGame
[Лицензия: MIT](LICENSE)

Читайте это на других языках: [English/Английский](README.md)

Читайте всю документацию: [Документация](Documentation.ru.md)

Это образовательный репозиторий. Посмотрите репозиторий активной разработки: [Репозиторий](https://github.com/SIBDuck/JumpOverlord-play/)

- **Один играбельный уровень** (скоро будет добавлено больше)
- **Два языка** - Английский и Русский

## Механики
- **Coyote time (койот тайм)** - возможность прыгнуть после падения с платформы
- **Jump buffer (буфер прыжка)** - запоминание нажатия на прыжок перед приземлением
- **Меню паузы**
- **Меню смерти**
- **Меню победы**
- **Режим отладки** - показ хитбоксов (в настройках)

## Управление
- A/D - передвижение
- SPACE - прыжок
- ESC - пауза
- F1 - переключение полноэкранного режима

## Геймплей - скриншоты и гифки

![Screenshot 1](images/screenshot1.png)
![Screenshot 2](images/screenshot2.png)
![Screenshot 3](images/screenshot3.png)
![Screenshot 4](images/screenshot4.png)
![Screenshot 5](images/screenshot5.png)
![Screenshot 6](images/screenshot6.png)
![Gameplay GIF](images/game.gif)

## Установка
1. Скачайте файл `SIBGames.zip`
2. Распакуйте его
3. Откройте `SIBGames/pythonProject/`
4. Запустите `Main.exe` (Python и сторонние библиотеки устанавливать не нужно)

## Системные требования 
- **ОС:** Windows 10/11
- **Процессор:** 1.5 ГГц
- **ОЗУ:** 512 МБ
- **Видеокарта:** Любая (DirectX 9 совместима)
- **Место на диске:** 189 МБ

## 📁 Структура Проекта
### JumpOverlord
```
SIBGames
│
├── pythonProject/                    # Корневая папка с игрой
│   ├── Main.py                       # Главный файл игры (точка входа)
│   ├── Main.spec                     # Конфигурация PyInstaller (сборка .exe)
│   ├── objects.json                  # Объекты игры
│   │
│   ├── images/                       # Изображения (текстуры, кнопки, флаги, фон)
│   ├── levels/                       # ASCII-уровни (.txt)
│   ├── fonts/                        # Шрифты (OpenSans)
│   ├── pleft/                        # Спрайты игрока (движение влево)
│   └── pright/                       # Спрайты игрока (движение вправо)
│
├── Documentation_screens/            # Скриншоты кода (5 приложений)
│   ├── Appendix_1/
│   ├── Appendix_2/
│   ├── Appendix_3/
│   ├── Appendix_4/
│   └── Appendix_5/
│
├── screenshots_gifs/                 # Скриншоты и гифки для README
│
├── .gitignore                        # Игнорируемые файлы (build/, dist/, .idea/ и т.д.)
│
├── README.md                         # Описание проекта (Английский)
├── README.ru.md                      # Описание проекта (Русский)
│
├── DOCUMENTATION.md                  # Полная документация (Английский)
├── DOCUMENTATION.ru.md               # Полная документация (Русский)
│
├── LICENSE                           # Лицензия MIT
```
## 🙏 Спасибо
- Python, Pygame
- Google Fonts (Open Sans)
- Flaticon, Iconfinder
- Различным бесплатным источникам (Pinterest, и др.)

## Лицензия
**MIT** — бесплатно использовать, модифицировать, распространять.  
Создано как учебный материал для начинающих.
