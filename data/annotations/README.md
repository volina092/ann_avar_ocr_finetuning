# OCR annotation dataset (PaddleOCR recognition format)

Размеченные страницы газет для fine-tuning модели распознавания.

## Структура

```
data/annotations/
  0_tlyarata_8_-na_pechat/
    page_001/
      Label.txt          # путь_к_crop<TAB>текст
      crop_img/
        line_0001.jpg
        line_0002.jpg
    page_002/
      ...
  char_dict_avar.txt     # опционально, копия из data/char_dict_avar.txt
```

## Формат Label.txt

Одна строка = одна строка текста (crop):

```
crop_img/line_0001.jpg	Иргадулаб, щибаб лъагIалида...
crop_img/line_0002.jpg	Щибаб лъагIалидаса цIикIунеб...
```

- Разделитель: таб (`\t`)
- Кодировка: UTF-8
- Строки с `#` в начале — комментарии (игнорируются при обучении)

## Как добавить разметку

1. Отрендерьте PDF: `python scripts/render_pdf_to_png.py`
2. (Опционально) Черновик из текстового слоя PDF:
   `python scripts/extract_pdf_text_layer.py --pdf train_pdfs/0_tlyarata_8_-na_pechat.pdf --png train_pdfs/img/0_tlyarata_8_-na_pechat_page_001.png`
3. Проверьте и исправьте в **PPOCRLabel** (см. `docs/annotation_guide.md`)
4. Загрузите папку `data/annotations/` на Google Drive для Colab

## Train / val split

Делите **по страницам**, не по отдельным строкам. Скрипт split встроен в `notebooks/ocr_rec_finetune_colab.ipynb`.
