# ann_avar_ocr_finetuning

Извлечение текста из сканов **аварских газет**: сегментация вёрстки, OCR и fine-tuning модели распознавания.

Основной рабочий путь — классическая сегментация (connected components) + **PaddleOCR c моделью `cyrillic_PP-OCRv5_mobile_rec`**.  
**PP-StructureV3** оставлен как exploratory baseline: на газетной вёрстке он работает хуже, чем классический пайплайн.

## Pipeline

```
PDF → render_pdf_to_png.py → PNG pages
PNG → classical layout (connected components) → crops + metadata.json
crops → OCR (cyrillic_PP-OCRv5_mobile_rec) → ocr_results.json
manual_corrections.md → fine-tune v5 (Colab) → inference model on Drive
fine-tuned model → OCR на новых страницах
```

## Notebooks (Google Colab)

Запускаю в Google Colab, потому что там у меня есть GPU. 

Ссылка на рабочую папку в Google Drive: https://drive.google.com/drive/folders/1Te8AWfT7UjYIMIiTGYAujxnYJI1CgPzl?usp=sharing

Порядок запуска тетрадок:

| Шаг | Notebook | Назначение |
|-----|----------|------------|
| 1 | [classical_layout_segmentation.ipynb](notebooks/classical_layout_segmentation.ipynb) | Обработка pdf-файла (файлов). Бинаризация, connected components, сохранение crops |
| 2 | [baseline_ocr_on_classical_crops.ipynb](notebooks/baseline_ocr_on_classical_crops.ipynb) | Распознавание "чистой" моделью. OCR crops, экспорт `manual_corrections.md` |
| 3 | [ocr_rec_finetune_colab.ipynb](notebooks/ocr_rec_finetune_colab.ipynb) | Дообучение (пока тестовое). CER/WER → smoke-test fine-tuning → export inference |\
| — | [pp_structure_v3_explore.ipynb](notebooks/pp_structure_v3_explore.ipynb) | УСТАРЕВШАЯ тетрадка. Хотела дообучать эту модель, но она слишком плохо сегментирует (PP-StructureV3) |

## Структура

ann_avar_ocr_finetuning/
├── notebooks/          # основной пайплайн (тетрадки для запуска в Colab)
├── scripts/            # локальные утилиты (PDF → PNG, словарь, черновик разметки)
├── docs/               # гайды (по рендеру и параметрам кропа, для себя)
├── data/               # было нужно для PPOCRLabel-разметки (изначальный путь, от которого пришлось отказаться)
├── configs/            # yaml для обучения
├── train_pdfs/         # отрендеренные страницы для обучения
├── tlarta_all_pdfs/    # полный корпус (gitignored, потому что слишком большой)


## Ссылки

- [PaddleOCR PP-StructureV3](https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/pipeline_usage/PP-StructureV3.html)
- [Text recognition (PP-OCRv5)](https://www.paddleocr.ai/main/en/version3.x/module_usage/text_recognition.html)
