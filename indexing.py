# # import os
# # import json
# # from PyPDF2 import PdfReader
# # import easyocr
# # import re
# #
# #
# # class PDFIndexer:
# #     def __init__(self, file_path, ocr_languages=None):
# #         self.file_path = file_path
# #         self.fields_and_labels = {}
# #         self.ocr_languages = ocr_languages if ocr_languages else ['en', 'sk', 'de']  # Підтримка мов
# #
# #     def extract_text(self):
# #         """
# #         Витягує текст із PDF. Якщо текст не читається, використовує OCR.
# #         """
# #         try:
# #             reader = PdfReader(self.file_path)
# #             text_data = []
# #             for page in reader.pages:
# #                 text = page.extract_text()
# #                 if text:  # Якщо текст є
# #                     text_data.append(text)
# #                 else:  # Якщо текст не читається, використовуємо OCR
# #                     text_data.append(self.perform_ocr_on_page(page))
# #             return "\n".join(text_data)
# #         except Exception as e:
# #             raise Exception(f"Error reading PDF: {e}")
# #
# #     def perform_ocr_on_page(self, page_image):
# #         """
# #         Використовує OCR для зчитування тексту із зображення сторінки.
# #         """
# #         try:
# #             reader = easyocr.Reader(self.ocr_languages)
# #             ocr_result = reader.readtext(page_image)
# #             return "\n".join([item[1] for item in ocr_result])
# #         except Exception as e:
# #             return f"Error performing OCR: {e}"
# #
# #     def find_fields_and_labels(self, text):
# #         """
# #         Автоматично знаходить всі можливі пари "лейбл — значення" у тексті.
# #         """
# #         lines = text.splitlines()
# #         results = {}
# #
# #         for line in lines:
# #             # Шукаємо можливі пари через двокрапку, тире або подібні символи
# #             match = re.match(r"(.+?)[:\-–]\s*(.+)", line)
# #             if match:
# #                 label = match.group(1).strip()
# #                 value = match.group(2).strip()
# #                 results[label] = value
# #
# #         self.fields_and_labels.update(results)
# #         return results
# #
# #     def save_to_json(self, output_path):
# #         """
# #         Зберігає результати у JSON файл.
# #         """
# #         with open(output_path, 'w', encoding='utf-8') as f:
# #             json.dump(self.fields_and_labels, f, ensure_ascii=False, indent=4)
# #
# #     def process(self, output_path):
# #         """
# #         Основний процес індексації PDF.
# #         """
# #         text = self.extract_text()
# #         self.find_fields_and_labels(text)
# #         self.save_to_json(output_path)
# #
# #
# # if __name__ == "__main__":
# #     # Шлях до PDF
# #     # pdf_file = "example.pdf"
# #     pdf_file = "./uploads/123.pdf"
# #
# #     # Шлях для збереження JSON
# #     output_json = "indexed_fields.json"
# #
# #     # Ініціалізація індексатора
# #     indexer = PDFIndexer(pdf_file, ocr_languages=['en', 'sk', 'de', 'uk'])
# #
# #     # Запуск індексації
# #     try:
# #         indexer.process(output_json)
# #         print(f"Індексація завершена. Результати збережено в файл: {output_json}")
# #     except Exception as e:
# #         print(f"Помилка при обробці PDF: {e}")
# #
#
# import os
# import json
# from PyPDF2 import PdfReader
# import easyocr
# import re
#
#
# class PDFIndexer:
#     def __init__(self, file_path, ocr_languages=None):
#         self.file_path = file_path
#         self.fields_and_labels = {}
#         self.ocr_languages = ocr_languages if ocr_languages else ['en', 'sk', 'de', 'uk']
#
#     def extract_text(self):
#         """Витягує текст із PDF. Якщо текст не читається, використовує OCR."""
#         try:
#             reader = PdfReader(self.file_path)
#             text_data = []
#             for page in reader.pages:
#                 text = page.extract_text()
#                 if text:  # Якщо текст є
#                     text_data.append(text)
#                 else:  # Якщо текст не читається, використовуємо OCR
#                     text_data.append(self.perform_ocr_on_page(page))
#             return "\n".join(text_data)
#         except Exception as e:
#             raise Exception(f"Error reading PDF: {e}")
#
#     def perform_ocr_on_page(self, page_image):
#         """OCR для зображень."""
#         try:
#             reader = easyocr.Reader(self.ocr_languages)
#             ocr_result = reader.readtext(page_image)
#             return "\n".join([item[1] for item in ocr_result])
#         except Exception as e:
#             return f"Error performing OCR: {e}"
#
#     def find_fields_and_labels(self, text):
#         """
#         Знаходить всі можливі пари "лейбл — значення" у тексті.
#         """
#         lines = text.splitlines()
#         results = {}
#         buffer_label = None
#
#         for line in lines:
#             # Шукаємо поля з двокрапкою, крапками або підкресленнями
#             match = re.match(r"(.+?)[\s:]*([.]+|[_]+)?\s*(.+)?", line)
#             if match:
#                 label = match.group(1).strip()
#                 separator = match.group(2)
#                 value = match.group(3).strip() if match.group(3) else None
#
#                 if separator or value:  # Якщо є розділювач або значення
#                     results[label] = value if value else "не заповнено"
#                 else:
#                     # Якщо лише "Поле", але без значення, зберігаємо в буфер
#                     buffer_label = label
#             elif buffer_label:
#                 # Якщо значення на наступному рядку
#                 results[buffer_label] = line.strip() if line.strip() else "не заповнено"
#                 buffer_label = None
#
#         self.fields_and_labels.update(results)
#         return results
#
#     def find_signatures(self, text):
#         """
#         Шукає підписи, використовуючи ключові слова та порожні рядки із підкресленням.
#         """
#         signature_patterns = [
#             r"(Signature|Підпис|Unterschrift|Podpis):?\s*(.+)?",  # Пошук підписів за ключовими словами
#             r".*[\s_]{5,}.*"  # Лінії або підкреслення
#         ]
#         signatures = []
#
#         for pattern in signature_patterns:
#             matches = re.findall(pattern, text, re.IGNORECASE)
#             for match in matches:
#                 if isinstance(match, tuple):
#                     signatures.append(" ".join(match).strip())
#                 else:
#                     signatures.append(match.strip())
#
#         return {"Signatures": signatures}
#
#     def save_to_json(self, output_path):
#         """Зберігає результати у JSON файл."""
#         with open(output_path, 'w', encoding='utf-8') as f:
#             json.dump(self.fields_and_labels, f, ensure_ascii=False, indent=4)
#
#     def process(self, output_path):
#         """
#         Основний процес індексації PDF.
#         """
#         text = self.extract_text()
#         self.find_fields_and_labels(text)
#         signatures = self.find_signatures(text)
#         self.fields_and_labels.update(signatures)
#         self.save_to_json(output_path)
#
#
# if __name__ == "__main__":
#     # Шлях до PDF
#     pdf_file = "./uploads/123.pdf"
#
#     # Шлях для збереження JSON
#     output_json = "indexed_fields.json"
#
#     # Ініціалізація індексатора
#     indexer = PDFIndexer(pdf_file, ocr_languages=['en', 'sk', 'de', 'uk'])
#
#     # Запуск індексації
#     try:
#         indexer.process(output_json)
#         print(f"Індексація завершена. Результати збережено в файл: {output_json}")
#     except Exception as e:
#         print(f"Помилка при обробці PDF: {e}")


import os
import json
from PyPDF2 import PdfReader
import easyocr
import re


class PDFIndexer:
    def __init__(self, file_path, ocr_languages=None):
        self.file_path = file_path
        self.fields_and_labels = {}
        self.signatures = []
        self.ocr_languages = self.validate_ocr_languages(ocr_languages or ['en', 'sk', 'de', 'uk'])
        self.ocr_reader = easyocr.Reader(self.ocr_languages, gpu=False)

    @staticmethod
    def validate_ocr_languages(ocr_languages):
        """
        Перевіряє список мов для OCR, щоб уникнути помилок із кириличними мовами.
        """
        supported_languages = [
            'en', 'uk', 'sk', 'de', 'ru', 'be', 'bg', 'mn', 'cs', 'pl', 'es', 'fr', 'it', 'nl', 'sv', 'fi', 'pt', 'da'
        ]
        cyrillic_langs = {'uk', 'ru', 'be', 'bg', 'mn'}
        validated_languages = []

        for lang in ocr_languages:
            if lang not in supported_languages:
                raise ValueError(f"Language '{lang}' is not supported by EasyOCR.")
            validated_languages.append(lang)

        # Додати англійську для сумісності з кириличними мовами
        if any(lang in cyrillic_langs for lang in validated_languages) and 'en' not in validated_languages:
            validated_languages.append('en')

        return validated_languages

    def extract_text(self):
        """
        Витягує текст із PDF. Використовує OCR для сторінок, що не містять тексту.
        """
        try:
            reader = PdfReader(self.file_path)
            extracted_text = []
            for page_index, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_text.append(text)
                else:
                    print(f"Performing OCR on page {page_index + 1}")
                    ocr_text = self.perform_ocr_on_page(page)
                    extracted_text.append(ocr_text)
            return "\n".join(extracted_text)
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {e}")

    def perform_ocr_on_page(self, page_image):
        """
        Використовує OCR для зчитування тексту зі сторінки.
        """
        try:
            ocr_result = self.ocr_reader.readtext(page_image)
            return "\n".join([item[1] for item in ocr_result])
        except Exception as e:
            return f"Error performing OCR: {e}"

    def find_fields_and_labels(self, text):
        """
        Знаходить усі можливі поля та їх значення у тексті.
        """
        lines = text.splitlines()
        results = {}
        buffer_label = None

        for line in lines:
            line = line.strip()
            if not line:
                continue  # Пропустити порожні рядки

            # Пошук формату: Label: Value
            match = re.match(r"(.+?)([:\-–.]|[_]+)\s*(.*)", line)
            if match:
                label = match.group(1).strip()
                value = match.group(3).strip() if match.group(3) else "не заповнено"
                results[label] = value
                buffer_label = None
            elif buffer_label:
                # Значення на наступному рядку
                results[buffer_label] = line
                buffer_label = None
            else:
                # Збереження як можливий лейбл
                buffer_label = line

        self.fields_and_labels.update(results)
        return results

    def find_signatures(self, text):
        """
        Шукає підписи у тексті, включаючи ключові слова та порожні рядки з підкресленням.
        """
        lines = text.splitlines()
        signatures = []

        for i, line in enumerate(lines):
            # Пошук ключових слів для підписів
            if re.search(r"(Signature|Підпис|Unterschrift|Podpis)", line, re.IGNORECASE):
                context = lines[i - 1].strip() if i > 0 else ""
                signatures.append(f"{context} {line.strip()}")
            elif re.match(r"[_]{5,}", line):
                signatures.append(line.strip())

        self.signatures.extend(signatures)
        return {"Signatures": signatures}

    def index_pdf(self):
        """
        Основний процес індексації PDF.
        """
        text = self.extract_text()
        self.find_fields_and_labels(text)
        self.find_signatures(text)

    def save_results(self, output_path):
        """
        Зберігає індексовані результати у JSON файл.
        """
        result = self.fields_and_labels
        result["Signatures"] = self.signatures
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"Results saved to {output_path}")

    def process(self, output_path):
        """
        Виконує повний процес індексації та збереження результатів.
        """
        try:
            self.index_pdf()
            self.save_results(output_path)
        except Exception as e:
            print(f"Error processing PDF: {e}")


if __name__ == "__main__":
    # Шлях до PDF
    pdf_file = "./uploads/123.pdf"

    # Шлях для збереження результатів
    output_json = "indexed_fields.json"

    # Ініціалізація індексатора
    indexer = PDFIndexer(pdf_file, ocr_languages=['en', 'sk', 'de', 'uk'])

    # Запуск індексації
    try:
        indexer.process(output_json)
    except Exception as e:
        print(f"An error occurred: {e}")
