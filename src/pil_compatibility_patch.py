# -*- coding: utf-8 -*-
"""
PIL兼容性补丁
自动添加到所有使用PIL的脚本中
"""

# PIL兼容性补丁 - 解决ANTIALIAS被弃用的问题
try:
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.Resampling.LANCZOS
    if not hasattr(Image, 'BICUBIC'):
        Image.BICUBIC = Image.Resampling.BICUBIC
    if not hasattr(Image, 'BILINEAR'):
        Image.BILINEAR = Image.Resampling.BILINEAR
    if not hasattr(Image, 'NEAREST'):
        Image.NEAREST = Image.Resampling.NEAREST
except ImportError:
    pass 