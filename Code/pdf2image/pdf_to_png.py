from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import os

def crop_white_borders(image):
    """
    裁剪图片的空白边界，只保留有内容的部分
    """
    # 转换为numpy数组
    image_array = np.array(image)
    
    # 判断是否为全白像素
    is_white = np.all(image_array == 255, axis=2)
    
    # 获取非空白区域的边界
    rows = np.any(~is_white, axis=1)
    cols = np.any(~is_white, axis=0)
    
    if not np.any(rows) or not np.any(cols):
        return image  # 如果整个图片都是空白，返回原图
    
    # 获取边界的最小和最大索引
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    # 增加一些边距（可选）
    padding = 50  # 可以调整这个值
    rmin = max(0, rmin - padding)
    rmax = min(image_array.shape[0], rmax + padding)
    cmin = max(0, cmin - padding)
    cmax = min(image_array.shape[1], cmax + padding)
    
    # 裁剪图片
    return image.crop((cmin, rmin, cmax, rmax))

def convert_pdf_to_images(pdf_path, output_format='jpg', dpi=300):
    """
    转换PDF为图片，并自动裁剪空白区域
    """
    # 设置poppler路径
    poppler_path = '/opt/homebrew/bin'  # M1/M2 Mac
    # poppler_path = '/usr/local/bin'   # Intel Mac
    
    # 转换PDF为图片
    images = convert_from_path(
        pdf_path,
        dpi=dpi,
        thread_count=os.cpu_count(),
        poppler_path=poppler_path
    )
    
    # 创建输出目录
    output_dir = 'output_images'
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理每一页
    for i, image in enumerate(images):
        # 裁剪空白边界
        cropped_image = crop_white_borders(image)
        
        # 构建输出文件路径
        base_filename = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = os.path.join(
            output_dir, 
            f'{base_filename}_page_{i+1}.{output_format}'
        )
        
        # 保存图片
        if output_format.lower() == 'png':
            cropped_image.save(output_path, 'PNG', optimize=False)
        else:
            cropped_image.save(
                output_path, 
                'JPEG', 
                quality=95, 
                optimize=False,
                progressive=True
            )

# Example usage
pdf_path = 'example.pdf'
convert_pdf_to_images(pdf_path, output_format='png', dpi=300)