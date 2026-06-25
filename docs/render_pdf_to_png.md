# Рендеринг PDF → PNG

Скрипт `scripts/render_pdf_to_png.py` конвертирует PDF-файлы в PNG-изображения (по одному файлу на страницу). Используется библиотека [PyMuPDF](https://pymupdf.readthedocs.io/) — внешние зависимости вроде Poppler не нужны.

## Установка зависимостей

Выполните один раз из корня проекта:

```powershell
cd C:\Users\Маша\maga\ann_avar_ocr_finetuning
pip install -r requirements.txt
```

## Подготовка входных файлов

Положите PDF-файлы в папку `train_pdfs/`:

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

## Параметры

| Параметр   | По умолчанию     | Описание              |
|------------|------------------|-----------------------|
| `--input`  | `train_pdfs`     | Папка с PDF-файлами   |
| `--output` | `train_pdfs/img` | Папка для PNG         |
| `--dpi`    | `200`            | Разрешение рендеринга |

Для OCR обычно достаточно 200–300 DPI.

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

Положите новые `.pdf` в `train_pdfs/` и снова запустите скрипт. Он обработает все PDF в папке; файлы с совпадающими именами будут перезаписаны.
