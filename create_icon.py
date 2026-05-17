#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
生成 video-parser 的 ICO 图标文件
"""
import subprocess
import sys

def install_pillow():
    """安装 Pillow 库"""
    print("正在安装 Pillow...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    print("Pillow 安装成功！")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    install_pillow()
    from PIL import Image, ImageDraw, ImageFont

def create_icon():
    """创建 ICO 图标"""
    # 创建不同尺寸的图标（ICO 可以包含多个尺寸）
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    images = []
    
    for size in sizes:
        # 创建透明背景的图片
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        width, height = size
        
        # 绘制渐变背景（蓝色系）
        for y in range(height):
            # 从上到下的渐变色
            r = int(30 + (y / height) * 20)
            g = int(90 + (y / height) * 40)
            b = int(180 + (y / height) * 50)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
        # 绘制播放按钮图标（三角形）
        if width >= 32:
            # 计算三角形的位置和大小
            triangle_size = width // 3
            center_x = width // 2
            center_y = height // 2
            
            # 三角形的三个点
            points = [
                (center_x - triangle_size // 2, center_y - triangle_size // 2),
                (center_x - triangle_size // 2, center_y + triangle_size // 2),
                (center_x + triangle_size // 2, center_y),
            ]
            
            # 绘制白色播放按钮
            draw.polygon(points, fill=(255, 255, 255, 255))
            
            # 添加边框效果
            border_points = [
                (center_x - triangle_size // 2 - 2, center_y - triangle_size // 2 - 2),
                (center_x - triangle_size // 2 - 2, center_y + triangle_size // 2 + 2),
                (center_x + triangle_size // 2 + 2, center_y),
            ]
            draw.polygon(border_points, fill=(255, 255, 255, 100))
        
        # 对于小尺寸，简化设计
        elif width == 16:
            center_x = width // 2
            center_y = height // 2
            triangle_size = 5
            points = [
                (center_x - 2, center_y - 2),
                (center_x - 2, center_y + 2),
                (center_x + 3, center_y),
            ]
            draw.polygon(points, fill=(255, 255, 255, 255))
        
        images.append(img)
    
    # 保存为 ICO 文件
    output_path = 'logo.ico'
    images[0].save(
        output_path,
        format='ICO',
        sizes=[img.size for img in images],
        append_images=images[1:]
    )
    
    print(f"✓ ICO 图标已生成: {output_path}")
    print(f"  包含尺寸: {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")
    return output_path

if __name__ == '__main__':
    try:
        create_icon()
        print("\n完成！现在可以使用这个 logo.ico 进行打包了。")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
