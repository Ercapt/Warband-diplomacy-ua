# Українська локалізація Diplomacy для Mount & Blade: Warband

Переклад моду **Diplomacy 4.3+ for Steam** українською.

Автор перекладу: https://steamcommunity.com/id/gouseks/

## Встановлення

1. Зробіть резервну копію папки `languages` вашого моду Diplomacy.
2. Скопіюйте вміст `languages/en/` з цього репозиторію до:
   `.../MountBlade Warband/Modules/Diplomacy/languages/en/`
3. Файл `info_pages.txt` перегенеровується з `source/module_info_pages.py`
   скриптом `tools/fix_info.py` (потрібен Python 3.11+):
   `python tools/fix_info.py`
4. Кнопка «Посібник» (замість «Ідея гри») — це рядок `ui_info_pages`
   у системному файлі `languages/en/ui.csv` основної гри, не моду.

## Стиль

- Шляхта, гільдмайстер, старости — на **Ви**.
- Бандити, лутівщики, дезертири — на **ти**.
- Селяни — проста мова, точкові архаїзми (либонь, мосьпане), без перебору.
- Міста/замографи — рід за контекстом, без «він/вона» там, де движок не дає роду.

## Ліцензія

CC BY-SA 4.0 (див. файл LICENSE).
