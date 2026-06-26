Скрипт `scripts/render_pdf_to_png.py` конвертирует PDF-файлы в PNG-изображения (по одному файлу на страницу). Используется библиотека [PyMuPDF](https://pymupdf.readthedocs.io/) — внешние зависимости вроде Poppler не нужны.

## Установка зависимостей

Выполнить один раз из корня проекта:

```powershell
cd C:\Users\Маша\maga\ann_avar_ocr_finetuning
pip install -r requirements.txt
```

## Подготовка входных файлов

Положить PDF-файлы в папку `train_pdfs/`:

```
train_pdfs/
  my_document.pdf
  another.pdf
```

## Запуск

### С параметрами по умолчанию

Вход: `train_pdfs`, выход: `train_pdfs/img`, разрешение 200 DPI:

```powershell
python scripts/render_pdf_to_png.py
```

### С явными параметрами

```powershell
python scripts/render_pdf_to_png.py --input train_pdfs --output train_pdfs/img --dpi 200
```

## Результат

Для каждой страницы PDF создаётся отдельный PNG-файл:

```
train_pdfs/img/
  my_document_page_001.png
  my_document_page_002.png
  another_page_001.png
```

Шаблон имени: `{имя_pdf}_page_{номер}.png`, где номер — трёхзначный (001, 002, …).

## Добавление новых PDF

Положить новые `.pdf` в `train_pdfs/` и снова запустить скрипт.