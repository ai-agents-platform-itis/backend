import json
import logging
import os
import re
import string
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


HEADER_PATTERN = re.compile(r"^(#+)\s(.+)")
PUNCTUATION_PATTERN = re.compile(f"[{re.escape(string.punctuation)}]")
WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Нормализация текста: удаление знаков препинания и специальных символов."""
    if not isinstance(text, str):
        raise ValueError("Входной текст должен быть строкой")

    # Удаление знаков препинания
    text = PUNCTUATION_PATTERN.sub(" ", text)
    # Удаление переносов строк и лишних пробелов
    text = WHITESPACE_PATTERN.sub(" ", text)
    # Приведение к нижнему регистру
    return text.lower().strip()


def parse_markdown(content: str) -> Dict[str, Any]:
    """Парсинг markdown контента и создание структурированных данных."""
    # if not os.path.exists(md_path):
    #     raise FileNotFoundError(f"Файл {md_path} не найден")

    # try:
    #     with open(md_path, "r", encoding="utf-8") as file:
    #         content = file.read()
    # except Exception as e:
    #     logger.error(f"Ошибка при чтении файла {md_path}: {e}")
    #     raise

    sections: List[str] = []
    section_titles: List[str] = []
    current_section: str | None = None
    current_content: List[str] = []

    for line in content.splitlines():
        section_match = HEADER_PATTERN.match(line)

        if section_match:
            if current_section:
                sections.append("\n".join(current_content).strip())
                section_titles.append(current_section)
                current_content = []
            current_section = section_match.group(2)
            current_content.append(current_section)
        else:
            current_content.append(line)

    if current_section:
        sections.append("\n".join(current_content).strip())
        section_titles.append(current_section)

    # Нормализация текста для векторной базы данных
    normalized_sections = [normalize_text(section) for section in sections]
    full_text = " ".join(normalized_sections)

    # Создаем структуру метаданных
    metadata = {
        "section_count": len(section_titles),
    }

    # Добавляем заголовки как отдельные поля
    for i, title in enumerate(section_titles):
        metadata[f"section_{i + 1}"] = title

    return {"text": full_text, "metadata": metadata}


def process_all_markdown(input_folder: str, output_folder: str) -> None:
    """Обработка всех markdown файлов в директории."""
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Входная директория {input_folder} не найдена")

    try:
        os.makedirs(output_folder, exist_ok=True)
    except Exception as e:
        logger.error(f"Ошибка при создании выходной директории: {e}")
        raise

    for root, _, files in os.walk(input_folder):
        for file_name in files:
            if file_name.endswith(".md"):
                try:
                    md_path = os.path.join(root, file_name)
                    output_path = os.path.join(
                        output_folder, file_name.replace(".md", ".json")
                    )
                    with open(md_path, "r", encoding="utf-8") as file:
                        content = file.read()
                    parsed_data = parse_markdown(content)

                    with open(output_path, "w", encoding="utf-8") as file:
                        json.dump(parsed_data, file, ensure_ascii=False, indent=4)
                    logger.info(f"Результат сохранен в {output_path}")
                except Exception as e:
                    logger.error(f"Ошибка при обработке файла {file_name}: {e}")


if __name__ == "__main__":
    process_all_markdown(input_folder="input_md", output_folder="parsed_output_md")
