#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PIL兼容性修复脚本
解决Pillow新版本中ANTIALIAS被弃用的问题
"""

import sys
import os

def fix_pil_compatibility():
    """修复PIL兼容性问题"""
    print("正在修复PIL兼容性问题...")
    
    try:
        # 尝试导入PIL
        from PIL import Image
        
        # 检查是否需要修复
        if not hasattr(Image, 'ANTIALIAS'):
            print("检测到Pillow新版本，添加ANTIALIAS兼容性支持...")
            Image.ANTIALIAS = Image.Resampling.LANCZOS
            print("✓ ANTIALIAS兼容性已修复")
        else:
            print("✓ PIL兼容性正常")
        
        # 检查其他可能需要的兼容性修复
        if not hasattr(Image, 'BICUBIC'):
            Image.BICUBIC = Image.Resampling.BICUBIC
            print("✓ BICUBIC兼容性已修复")
        if not hasattr(Image, 'BILINEAR'):
            Image.BILINEAR = Image.Resampling.BILINEAR
            print("✓ BILINEAR兼容性已修复")
        if not hasattr(Image, 'NEAREST'):
            Image.NEAREST = Image.Resampling.NEAREST
            print("✓ NEAREST兼容性已修复")
        
        # 测试图像处理功能
        print("\n测试图像处理功能...")
        test_img = Image.new('RGB', (100, 100), color='white')
        
        # 测试resize功能
        try:
            resized_img = test_img.resize((50, 50), Image.ANTIALIAS)
            print("✓ resize功能正常")
        except Exception as e:
            print(f"✗ resize功能测试失败: {e}")
            return False
        
        # 测试其他图像处理功能
        try:
            gray_img = test_img.convert('L')
            print("✓ 图像模式转换正常")
        except Exception as e:
            print(f"✗ 图像模式转换失败: {e}")
            return False
        
        print("✓ PIL兼容性检查完成")
        return True
        
    except ImportError as e:
        print(f"错误：无法导入PIL库: {e}")
        print("请确保已安装Pillow库：pip install Pillow")
        return False
    except Exception as e:
        print(f"修复过程中出现错误: {e}")
        return False

def test_easyocr_compatibility():
    """测试easyocr兼容性"""
    print("\n正在测试easyocr兼容性...")
    
    try:
        import easyocr
        import numpy as np
        from PIL import Image
        
        # 创建测试图像
        test_img = Image.new('RGB', (200, 100), color='white')
        img_array = np.array(test_img)
        
        # 尝试创建OCR读取器（不下载模型）
        reader = easyocr.Reader(
            ['ch_sim', 'en'],
            gpu=False,
            download_enabled=False  # 不下载模型，只测试兼容性
        )
        print("✓ easyocr兼容性测试通过")
        
        # 测试图像处理
        results = reader.readtext(img_array)
        print("✓ easyocr图像处理正常")
        
        return True
        
    except Exception as e:
        print(f"✗ easyocr兼容性测试失败: {e}")
        if "ANTIALIAS" in str(e):
            print("  这是PIL兼容性问题，请运行此脚本修复")
        return False

def create_compatibility_patch():
    """创建兼容性补丁文件"""
    print("\n创建兼容性补丁文件...")
    
    patch_content = '''# -*- coding: utf-8 -*-
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
'''
    
    try:
        with open('pil_compatibility_patch.py', 'w', encoding='utf-8') as f:
            f.write(patch_content)
        print("✓ 兼容性补丁文件已创建: pil_compatibility_patch.py")
        return True
    except Exception as e:
        print(f"✗ 创建兼容性补丁文件失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("PIL兼容性修复工具")
    print("=" * 50)
    
    # 修复PIL兼容性
    if fix_pil_compatibility():
        print("\n" + "=" * 30)
        print("PIL兼容性修复成功！")
        print("=" * 30)
        
        # 创建兼容性补丁文件
        create_compatibility_patch()
        
        # 测试easyocr兼容性
        test_easyocr_compatibility()
        
        print("\n现在可以运行主脚本了：")
        print("python nju_electric_monitor_auto.py")
        
        print("\n如果其他脚本仍有PIL兼容性问题，请在其开头添加：")
        print("from pil_compatibility_patch import *")
    else:
        print("\n" + "=" * 30)
        print("PIL兼容性修复失败！")
        print("=" * 30)
        print("请检查Pillow安装或手动修复兼容性问题")
        sys.exit(1)

if __name__ == "__main__":
    main() 