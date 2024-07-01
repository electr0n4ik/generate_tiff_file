import os
import math

from PIL import Image

def get_collect_images(folder):
    """
    Получает изображения из заданной папки.

    Args:
    - folder (str): Путь к папке, из которой нужно собрать изображения.

    Returns:
    - list: Список объектов изображений (PIL.Image.Image).
    """

    images = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.split('.')[-1] in ['jpg', 'png', 'jpeg']:
                image_path = os.path.join(root, file)
                images.append(Image.open(image_path))
    return images

def save_as_tiff(images, output_path):
    """
    Сохраняет список изображений в формате TIFF.

    Args:
    - images (list): Список объектов изображений (PIL.Image.Image).
    - output_path (str): Путь для сохранения файла TIFF.
    """

    if images:
        images[0].save(output_path, save_all=True, append_images=images[1:])

def create_collage(images, cols, rows, 
                   thumb_width, thumb_height, 
                   padding):
    """
    Создает коллаж изображений с заданными параметрами.

    Args:
    - images (list): Список объектов изображений (PIL.Image.Image).
    - cols (int): Количество столбцов в коллаже.
    - rows (int): Количество строк в коллаже.
    - thumb_width (int): Ширина миниатюры.
    - thumb_height (int): Высота миниатюры.
    - padding (int): Внутренний интервал между миниатюрами.

    Returns:
    - PIL.Image.Image: Объект изображения с созданным коллажем.
    """
    
    collage_width = cols * thumb_width + (cols - 1) * padding
    collage_height = rows * thumb_height + (rows - 1) * padding
    collage_image = Image.new('RGB', (collage_width, collage_height), 'white')
    
    for i, img in enumerate(images):
        img.thumbnail((thumb_width, thumb_height))
        x = (i % cols) * (thumb_width + padding)
        y = (i // cols) * (thumb_height + padding)
        collage_image.paste(img, (x, y))
    
    return collage_image

def get_cols_rows(count_images):
    """
    Получает оптимальное количество столбцов и строк для коллажа 
    из заданного количества изображений.

    Args:
    - count_images (int): Количество изображений.

    Returns:
    - tuple: Кортеж из двух целых чисел (cols, rows), 
    где cols - количество столбцов, rows - количество строк.
    """

    if count_images == 0:
        return 0, 0

    cols = int(math.sqrt(count_images) + 1)
    rows = int(count_images / cols)
    while cols > 0:
        if cols * rows == count_images:
            return cols, rows
        elif cols * rows > count_images:
            rows -= 1
            continue
        elif cols * rows < count_images:
            cols += 1

    return 1, count_images

def get_count_images(folder):
    """
    Получает количество изображений в заданной папке.

    Args:
    - folder (str): Путь к папке, в которой нужно подсчитать изображения.

    Returns:
    - int: Количество изображений (файлов с расширениями jpg, jpeg, png).
    """

    count = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.split('.')[-1] in ['jpg', 'jpeg', 'png']:
                count += 1
    return count

def add_border(collage_image, padding=10):
    """
    Добавляет белую рамку.

    Args:
    - collage_image (PIL.Image.Image): Изображение для рамки.
    - padding (int): Ширина рамки.

    Returns:
    - PIL.Image.Image: Изображение с добавленной рамкой.
    """

    width, height = collage_image.size
    border_image = Image.new('RGB', (width + 2 * padding, height + 2 * padding), 'white')
    border_image.paste(collage_image, (padding, padding))
    return border_image
