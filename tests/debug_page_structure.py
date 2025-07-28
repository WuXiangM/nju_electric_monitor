#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
页面结构调试脚本
用于分析页面HTML结构并查找电量信息
"""

import os
import re
from bs4 import BeautifulSoup

def analyze_page_structure(html_file="debug_page_source.html"):
    """分析页面结构"""
    if not os.path.exists(html_file):
        print(f"错误：找不到文件 {html_file}")
        print("请先运行主脚本生成页面源码文件")
        return
    
    print("=" * 60)
    print("页面结构分析工具")
    print("=" * 60)
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找所有包含"电量"的元素
        print("\n1. 查找包含'电量'的元素:")
        elements_with_electricity = soup.find_all(text=re.compile(r'电量'))
        for i, element in enumerate(elements_with_electricity[:10]):  # 只显示前10个
            parent = element.parent
            print(f"  {i+1}. 文本: '{element.strip()}'")
            print(f"     父元素: {parent.name} {parent.get('class', '')} {parent.get('id', '')}")
            print(f"     完整HTML: {parent}")
            print()
        
        # 查找所有包含"度"的元素
        print("\n2. 查找包含'度'的元素:")
        elements_with_degree = soup.find_all(text=re.compile(r'度'))
        for i, element in enumerate(elements_with_degree[:10]):  # 只显示前10个
            parent = element.parent
            print(f"  {i+1}. 文本: '{element.strip()}'")
            print(f"     父元素: {parent.name} {parent.get('class', '')} {parent.get('id', '')}")
            print(f"     完整HTML: {parent}")
            print()
        
        # 查找所有span.fl元素
        print("\n3. 查找所有span.fl元素:")
        span_fl_elements = soup.find_all('span', class_='fl')
        for i, element in enumerate(span_fl_elements):
            print(f"  {i+1}. {element}")
            print()
        
        # 查找所有i标签
        print("\n4. 查找所有i标签:")
        i_elements = soup.find_all('i')
        for i, element in enumerate(i_elements[:10]):  # 只显示前10个
            print(f"  {i+1}. {element}")
            print()
        
        # 使用正则表达式查找电量信息
        print("\n5. 使用正则表达式查找电量信息:")
        patterns = [
            r'剩余电量[：:]\s*<i>(\d+(?:\.\d+)?)度</i>',
            r'剩余电量[：:]\s*(\d+(?:\.\d+)?)\s*度',
            r'电量[：:]\s*(\d+(?:\.\d+)?)\s*度',
            r'<i>(\d+(?:\.\d+)?)度</i>',
            r'(\d+(?:\.\d+)?)\s*度'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html_content)
            if matches:
                print(f"  模式 '{pattern}' 找到匹配: {matches}")
        
        # 查找可能的电量信息容器
        print("\n6. 查找可能的电量信息容器:")
        possible_containers = soup.find_all(['div', 'span', 'p'], class_=re.compile(r'electric|power|energy|电量|电费'))
        for i, container in enumerate(possible_containers[:5]):
            print(f"  {i+1}. {container.name}.{container.get('class', '')}: {container.get_text()[:100]}...")
        
    except Exception as e:
        print(f"分析过程中出现错误: {e}")

def main():
    """主函数"""
    analyze_page_structure()
    
    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)
    print("\n建议:")
    print("1. 查看上面的输出，找到包含电量信息的元素")
    print("2. 根据找到的元素结构，调整主脚本中的选择器")
    print("3. 如果页面结构复杂，可能需要使用更精确的XPath或CSS选择器")

if __name__ == "__main__":
    main() 