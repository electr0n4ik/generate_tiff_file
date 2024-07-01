from src.helpers import *

def main(folders):
    """
    Создание коллажей изображений для каждой папки в заданном списке.

    Args:
    - folders (list): Список папок, из которых будут собираться изображения.

    Проходит по каждой папке, собирает изображения, 
    создает коллаж и сохраняет его в формате TIFF.
    """

    images = []
    for folder in folders:
        folder = 'src/' + folder
        
        if not get_count_images(folder):
            continue

        images.extend(get_collect_images(folder))
        num_images = get_count_images(folder)
        cols, rows = get_cols_rows(get_count_images(folder))
        total_width = sum(img.width for img in images)
        total_height = sum(img.height for img in images)
        avg_width = total_width // (num_images)
        avg_height = total_height // (num_images)

        collage = create_collage(images,
                                 cols=cols,
                                 rows=rows,
                                 thumb_width=avg_width,
                                 thumb_height=avg_height,
                                 padding=(avg_height // 5) // 2)
        
        collage_with_border = add_border(collage, padding=avg_height // 5)
        save_as_tiff([collage_with_border], f'{folder}.tiff')
        images = []

if __name__ == "__main__":
    main(os.listdir('src'))
