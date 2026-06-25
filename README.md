# ann_avar_ocr_finetuning

# Avar Newspaper OCR

A research project for extracting text from scanned Avar-language newspapers using document layout analysis and OCR fine-tuning.

The pipeline is based on PaddleOCR PP-StructureV3. It first detects structural regions on newspaper pages, such as text blocks, headings, images, and tables, then applies OCR to extract text from the detected regions. To improve recognition quality for the Avar language, the OCR recognition model is fine-tuned on manually annotated newspaper fragments.

## Goals

- Detect layout regions in scanned newspaper pages.
- Extract text from Avar-language newspaper scans.
- Prepare a manually annotated OCR dataset.
- Fine-tune an OCR recognition model for Avar text.
- Evaluate OCR quality before and after fine-tuning.

----


# OCR для аварских газет

Учебный проект по извлечению текста из сканов газет на аварском языке с использованием анализа структуры документа и дообучения OCR-модели.

В проекте используется PaddleOCR PP-StructureV3 для выделения областей газетной страницы: текстовых блоков, заголовков, изображений и таблиц. После этого к найденным областям применяется OCR. Для повышения качества распознавания аварского текста OCR-модель дообучается на вручную размеченных фрагментах газет.

## Цели проекта

- Выделять структурные области на страницах газет.
- Извлекать текст из сканов аварских газет.
- Подготовить вручную размеченный OCR-датасет.
- Дообучить модель распознавания текста на аварском языке.
- Сравнить качество OCR до и после дообучения.
