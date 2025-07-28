#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证码识别测试脚本
用于测试和改进验证码识别功能
"""

# 导入PIL兼容性补丁
try:
    from pil_compatibility_patch import *
except ImportError:
    pass

import os
import re
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import easyocr

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

def test_captcha_recognition(image_path="captcha_debug.png"):
    """测试验证码识别"""
    if not os.path.exists(image_path):
        print(f"错误：找不到验证码图片 {image_path}")
        print("请先运行主脚本生成验证码图片")
        return
    
    print("=" * 60)
    print("验证码识别测试工具")
    print("=" * 60)
    
    try:
        # 加载验证码图片
        original_img = Image.open(image_path)
        print(f"验证码图片尺寸: {original_img.size}")
        print(f"验证码图片模式: {original_img.mode}")
        
        # 初始化OCR读取器
        print("\n初始化OCR读取器...")
        ocr_reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        print("✓ OCR读取器初始化成功")
        
        # 测试不同的图像处理方法
        test_methods = [
            ("原始图像", original_img),
            ("灰度图像", original_img.convert('L')),
            ("放大图像", original_img.resize((original_img.width * 2, original_img.height * 2), Image.ANTIALIAS)),
            ("高对比度", ImageEnhance.Contrast(original_img).enhance(2.0)),
            ("锐化图像", original_img.filter(ImageFilter.SHARPEN)),
            ("二值化", original_img.convert('L').point(lambda x: 0 if x < 128 else 255, '1')),
            ("降噪", original_img.filter(ImageFilter.MedianFilter(size=3))),
        ]
        
        print(f"\n开始测试 {len(test_methods)} 种图像处理方法...")
        
        best_result = None
        best_confidence = 0
        
        for method_name, processed_img in test_methods:
            print(f"\n--- 测试方法: {method_name} ---")
            
            try:
                # 保存处理后的图像
                debug_filename = f"captcha_{method_name.replace(' ', '_')}.png"
                processed_img.save(debug_filename)
                print(f"已保存到: {debug_filename}")
                
                # 转换为numpy数组
                img_array = np.array(processed_img)
                
                # 使用OCR识别
                results = ocr_reader.readtext(img_array)
                
                if results:
                    print(f"识别结果: {results}")
                    
                    # 提取文本和置信度
                    for (bbox, text, prob) in results:
                        cleaned_text = re.sub(r'[^a-zA-Z0-9]', '', text.strip())
                        if cleaned_text and prob > best_confidence:
                            best_result = cleaned_text
                            best_confidence = prob
                            print(f"  ✓ 最佳结果: '{cleaned_text}' (置信度: {prob:.3f})")
                        else:
                            print(f"  - 结果: '{cleaned_text}' (置信度: {prob:.3f})")
                else:
                    print("  ✗ 未识别到任何内容")
                    
            except Exception as e:
                print(f"  ✗ 处理失败: {e}")
        
        # 显示最佳结果
        print("\n" + "=" * 40)
        print("测试结果总结")
        print("=" * 40)
        
        if best_result:
            print(f"最佳识别结果: '{best_result}'")
            print(f"置信度: {best_confidence:.3f}")
            
            if best_confidence > 0.5:
                print("✓ 识别结果可信度较高")
            elif best_confidence > 0.3:
                print("⚠ 识别结果可信度中等，建议人工确认")
            else:
                print("✗ 识别结果可信度较低，建议手动输入")
        else:
            print("✗ 未能识别出任何有效内容")
        
        # 提供建议
        print("\n建议:")
        print("1. 查看生成的调试图片，选择最清晰的处理方法")
        print("2. 如果识别效果不好，可以调整图像处理参数")
        print("3. 考虑使用其他OCR库或手动输入验证码")
        
    except Exception as e:
        print(f"测试过程中出现错误: {e}")

def main():
    """主函数"""
    test_captcha_recognition()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    main() 