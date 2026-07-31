# 南京大学电费监控系统 - 完整使用指南

## 📋 目录

1. [项目简介](#项目简介)
2. [系统架构](#系统架构)
3. [安装部署](#安装部署)
4. [配置说明](#配置说明)
5. [运行方式](#运行方式)
6. [验证机制](#验证机制)
7. [数据输出](#数据输出)
8. [故障排除](#故障排除)
9. [开发指南](#开发指南)

---

## 项目简介

南京大学电费监控系统是一个自动化工具，用于定期监控南京大学电费充值页面的剩余电量信息。系统支持自动登录、验证码识别、数据提取和可视化展示。

### 核心功能

- ✅ 自动登录南京大学电费充值系统
- ✅ 支持两种验证方式：传统验证码（OCR识别）和滑块验证（AI识别）
- ✅ 自动提取剩余电量信息
- ✅ 数据持久化存储（JSON/CSV）
- ✅ 可视化网页面板
- ✅ GitHub Actions 自动化运行
- ✅ 邮件预警通知

### 技术栈

- **爬虫框架**: Selenium WebDriver
- **验证码识别**: ddddocr (传统验证码) + captcha-recognizer (滑块验证)
- **数据处理**: pandas, numpy
- **可视化**: matplotlib, plotly, Flask
- **自动化**: GitHub Actions

---

## 系统架构

```
nju_electric_monitor/
├── src/                          # 源代码目录
│   ├── nju_electric_monitor_auto.py      # 本地自动版主脚本
│   ├── nju_electric_monitor_workflow.py  # GitHub Actions版主脚本
│   ├── web_panel.py                      # 可视化网页面板
│   ├── run_workflow_wrapper.py           # Workflow运行包装器
│   ├── fix_pil_compatibility.py          # PIL兼容性修复
│   └── pil_compatibility_patch.py        # PIL补丁
├── tests/                        # 测试脚本目录
│   ├── test_environment.py               # 环境检测
│   ├── test_verification_flow.py         # 验证流程测试
│   ├── test_captcha_recognizer_full.py   # 滑块验证测试
│   ├── test_captcha_recognition.py       # 验证码识别测试
│   └── debug_page_structure.py           # 页面结构调试
├── data/                         # 数据存储目录
│   ├── electricity_data.json             # 电量数据（JSON）
│   ├── electricity_data.csv              # 电量数据（CSV）
│   ├── electricity_trend.png             # 电量趋势图
│   └── test_verification_flow/           # 验证流程测试结果
├── logs/                         # 日志目录
├── chromedriver-win64/           # ChromeDriver
├── config.json                   # 本地版配置文件
├── config_workflow.json          # Workflow版配置文件
├── requirements.txt              # Python依赖
├── run_auto_monitor.bat          # 本地版启动脚本
├── run_auto_monitor_workflow.bat # Workflow版启动脚本
└── run_web_panel.bat             # 网页面板启动脚本
```

---

## 安装部署

### 环境要求

- **Python**: 3.9+ (推荐 3.11)
- **Chrome浏览器**: 最新稳定版
- **ChromeDriver**: 与Chrome版本匹配（已包含在项目中）
- **操作系统**: Windows 10/11, Linux, macOS

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/your-username/nju_electric_monitor.git
cd nju_electric_monitor
```

#### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

**主要依赖说明**：
- `selenium==4.15.2`: 浏览器自动化
- `ddddocr==1.4.11`: 传统验证码OCR识别
- `captcha-recognizer>=0.1.0`: 滑块验证AI识别
- `Pillow>=10.0.0`: 图像处理
- `pandas>=1.1.0`: 数据处理
- `matplotlib>=3.0.0`: 数据可视化
- `plotly>=5.0.0`: 交互式可视化
- `flask>=2.0.0`: Web服务

#### 4. 环境检测

```bash
python tests/test_environment.py
```

该脚本会检查：
- Python版本
- 依赖包安装情况
- ChromeDriver可用性
- 配置文件完整性

#### 5. PIL兼容性修复（如遇问题）

```bash
python src/fix_pil_compatibility.py
```

---

## 配置说明

### 本地版配置 (config.json)

```json
{
    "username": "你的学号",
    "password": "你的密码",
    "auto_login": true,
    "headless_mode": true,
    "captcha_retry_count": 5,
    "save_captcha_images": true,
    "log_level": "INFO",
    "test_mode": false
}
```

**参数说明**：
- `username`: 南京大学学号
- `password`: 统一认证密码
- `auto_login`: 是否自动登录（默认true）
- `headless_mode`: 是否无头模式运行（默认true，不显示浏览器窗口）
- `captcha_retry_count`: 验证码识别失败重试次数（默认5）
- `save_captcha_images`: 是否保存验证码图片用于调试（默认true）
- `log_level`: 日志级别（DEBUG/INFO/WARNING/ERROR）
- `test_mode`: 测试模式，保存更多调试信息（默认false）

### Workflow版配置 (config_workflow.json)

```json
{
    "username": "",
    "password": "",
    "auto_login": true,
    "headless_mode": true,
    "captcha_retry_count": 4,
    "save_captcha_images": true,
    "log_level": "INFO",
    "test_mode": false,
    "enable_email_alert": true,
    "alert_threshold_warn": 15,
    "alert_threshold_high": 10,
    "alert_threshold_critical": 5
}
```

**额外参数**：
- `enable_email_alert`: 是否启用邮件预警（默认true）
- `alert_threshold_warn`: 预警阈值（度），低于此值发送警告邮件
- `alert_threshold_high`: 高优先级阈值（度）
- `alert_threshold_critical`: 紧急阈值（度）

**注意**：Workflow版的username和password通过GitHub Secrets配置，不写在配置文件中。

### GitHub Secrets配置

在GitHub仓库的 Settings → Secrets and variables → Actions 中添加：

- `NJU_USERNAME`: 你的学号
- `NJU_PASSWORD`: 你的密码
- `EMAIL_SENDER`: 发件人邮箱（可选）
- `EMAIL_PASSWORD`: 邮箱授权码（可选）
- `EMAIL_RECEIVER`: 收件人邮箱（可选）

---

## 运行方式

### 方式一：本地批处理脚本（推荐新手）

#### 本地自动版

```bash
run_auto_monitor.bat
```

功能：
1. 加载虚拟环境
2. 运行环境检测
3. 执行主脚本
4. 自动提交数据到Git

#### Workflow版

```bash
run_auto_monitor_workflow.bat
```

功能：
1. 加载虚拟环境
2. 运行环境检测
3. 通过包装器运行主脚本（捕获崩溃信息）
4. 自动提交数据到Git

### 方式二：命令行运行

```bash
# 激活虚拟环境
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/macOS

# 运行本地版
python src/nju_electric_monitor_auto.py

# 运行Workflow版
python src/nju_electric_monitor_workflow.py

# 指定配置文件
python src/nju_electric_monitor_auto.py config.json
```

### 方式三：GitHub Actions自动化

项目已配置GitHub Actions工作流，会自动定时运行：

- **触发时间**: 每天UTC 00:00, 08:00, 16:00（北京时间08:00, 16:00, 24:00）
- **手动触发**: 在Actions页面点击 "Run workflow"
- **运行结果**: 在Actions页面查看日志

### 启动可视化网页面板

```bash
run_web_panel.bat
```

或手动启动：

```bash
python src/web_panel.py
```

访问 http://127.0.0.1:5000/ 查看电量数据和趋势图。

---

## 验证机制

系统支持两种登录验证方式，会自动检测并选择对应的处理方式。

### 验证方式检测流程

```
1. 打开登录页面
2. 填写用户名和密码
3. 点击登录按钮
4. 等待验证元素出现（2秒）
5. 检测验证类型：
   - 检查 captchaImg 元素 → 传统验证码
   - 检查 sliderDiv 元素 → 滑块验证
   - 检查 .sliderContainer 元素 → 滑块验证
   - 都未检测到 → 无需验证
6. 根据验证类型执行对应处理
```

### 传统验证码处理

**识别引擎**: ddddocr

**处理流程**:
1. 截取验证码图片（captchaImg元素）
2. 图像预处理（放大、增强对比度、去噪）
3. OCR识别（ddddocr分类器）
4. 结果清洗（仅保留字母数字，转大写）
5. 填写验证码并登录
6. 验证失败时自动重试（最多5轮，每轮3次OCR尝试）

**重试机制**:
- **外层重试**: 刷新页面，重新获取验证码（最多5次）
- **内层重试**: 同一张验证码图片，多次OCR识别（最多3次）
- **总计**: 最多15次识别机会

### 滑块验证处理

**识别引擎**: captcha-recognizer

**处理流程**:
1. 点击登录按钮触发滑块验证
2. 等待滑块验证弹窗出现（最多5秒）
3. 截取canvas图片（包含缺口）
4. AI识别缺口位置（captcha-recognizer模型）
5. 坐标缩放换算（截图坐标→DOM坐标）
6. 生成人类化拖拽轨迹（物理模型）
7. 执行拖拽操作
8. 验证失败时自动重试（最多3轮）

**关键技术**:
- **坐标缩放**: 截图尺寸与DOM尺寸可能不一致（通常1.5倍），需要换算
- **轨迹生成**: 加速-减速两段式物理模型，模拟人类拖拽
- **重试机制**: 每轮重新截取canvas、重新识别、重新拖拽

**成功率**: 测试显示约80-90%（单次），多轮重试后接近100%

### 验证方式对比

| 特性 | 传统验证码 | 滑块验证 |
|------|-----------|---------|
| 识别引擎 | ddddocr | captcha-recognizer |
| 识别方式 | OCR文字识别 | AI目标检测 |
| 处理时间 | 2-3秒 | 5-8秒 |
| 单次成功率 | 60-80% | 80-90% |
| 重试机制 | 外层×内层 | 多轮完整重试 |
| 最终成功率 | 95%+ | 98%+ |

---

## 数据输出

### 数据文件

#### electricity_data.json

JSON Lines格式，每行一条记录：

```json
{"time": "2026-07-28 12:00:00", "num": 125.5, "unit": "度"}
{"time": "2026-07-29 12:00:00", "num": 120.3, "unit": "度"}
```

#### electricity_data.csv

CSV格式，包含表头：

```csv
time,num,unit
2026-07-28 12:00:00,125.5,度
2026-07-29 12:00:00,120.3,度
```

### 可视化图表

#### electricity_trend.png

完整历史电量变化曲线图，包含：
- 时间轴（X轴）
- 电量值（Y轴）
- 数据点标记
- 趋势线

#### recent_20_changes.png

最近20次电量变化曲线图，用于快速查看近期用电情况。

### 日志文件

#### 主脚本日志

位置: `logs/nju_electric_monitor-YYYY-MM-DD-HH.log`

按小时滚动生成，包含：
- 登录过程
- 验证处理
- 数据提取
- 错误信息

#### Workflow包装器日志

位置: `logs/workflow_wrapper_YYYYMMDD_HHMMSS.log`

包含：
- 环境信息摘要
- 磁盘使用情况
- 字体诊断
- 完整运行日志
- 崩溃堆栈（如有）

### 调试文件

#### 验证码图片

位置: `data/captcha_auto/` (本地版) 或 `data/captcha_workflow/` (Workflow版)

- 每轮重试保存验证码截图
- 识别成功后按结果重命名（如 `PCET.png`）
- 用于调试OCR识别效果

#### 测试快照

位置: `data/test_snapshots-auto/` 或 `data/test_snapshots-workflow/`

仅在 `test_mode=true` 时生成，包含：
- 登录页加载后快照
- 表单填写后快照
- 验证码填写前后快照
- 登录成功后快照

---

## 故障排除

### 常见问题

#### 1. ChromeDriver版本不匹配

**错误信息**: 
```
SessionNotCreatedException: This version of ChromeDriver only supports Chrome version XX
```

**解决方案**:
1. 查看Chrome浏览器版本（设置→关于Chrome）
2. 下载对应版本的ChromeDriver: https://chromedriver.chromium.org/downloads
3. 替换 `chromedriver-win64/chromedriver.exe`

#### 2. PIL兼容性问题

**错误信息**: 
```
AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'
```

**解决方案**:
```bash
python src/fix_pil_compatibility.py
```

或手动降级Pillow:
```bash
pip install Pillow==9.5.0
```

#### 3. 验证码识别失败

**现象**: 多次重试后仍提示"验证码错误"

**排查步骤**:
1. 查看 `data/captcha_auto/` 中的验证码截图
2. 运行测试脚本:
   ```bash
   python tests/test_captcha_recognition.py
   ```
3. 增加重试次数:
   ```json
   {"captcha_retry_count": 10}
   ```
4. 临时关闭无头模式，手动输入验证码:
   ```json
   {"headless_mode": false}
   ```

#### 4. 滑块验证失败

**现象**: 滑块拖拽后未通过验证

**排查步骤**:
1. 运行滑块验证测试:
   ```bash
   python tests/test_verification_flow.py --rounds 5
   ```
2. 查看测试结果: `data/test_verification_flow/verification_flow_results.json`
3. 检查canvas截图: `data/test_verification_flow/slider_canvas_*.png`
4. 确认captcha-recognizer已安装:
   ```bash
   pip list | grep captcha-recognizer
   ```

#### 5. 无法提取电量信息

**现象**: 登录成功但未提取到电量数据

**排查步骤**:
1. 运行页面结构调试:
   ```bash
   python tests/debug_page_structure.py
   ```
2. 检查页面元素选择器是否变化
3. 查看日志中的错误信息
4. 临时开启test_mode查看详细快照:
   ```json
   {"test_mode": true}
   ```

#### 6. GitHub Actions运行失败

**排查步骤**:
1. 在Actions页面查看完整日志
2. 检查Secrets配置是否正确
3. 确认config_workflow.json格式正确
4. 手动触发一次workflow测试
5. 查看 `logs/workflow_wrapper_*.log` 日志

### 调试技巧

#### 开启调试模式

```json
{
    "test_mode": true,
    "log_level": "DEBUG",
    "save_captcha_images": true
}
```

#### 查看页面结构

```bash
python tests/debug_page_structure.py
```

会输出：
- 页面HTML结构
- 关键元素位置
- 表单字段信息

#### 测试验证流程

```bash
python tests/test_verification_flow.py --rounds 10
```

会统计：
- 验证方式分布（captcha/slider/none）
- 各验证方式成功率
- 失败原因分析

---

## 开发指南

### 代码结构

#### 主类: NJUElectricMonitor

**核心方法**:

```python
class NJUElectricMonitor:
    def __init__(self, config_file="config.json")
        # 初始化配置、浏览器、OCR引擎
    
    def run(self)
        # 主流程：登录→提取→保存
    
    def handle_captcha(self)
        # 验证方式检测和分发
    
    def detect_verification_type(self)
        # 检测验证类型：captcha/slider/none
    
    def _handle_captcha_ocr(self)
        # 处理传统验证码
    
    def handle_slider_verification(self, max_rounds=3)
        # 处理滑块验证（多轮重试）
    
    def detect_slider_gap(self, img, dom_width)
        # AI识别滑块缺口位置
    
    def perform_slider_drag(self, offset_x, max_retries=2)
        # 执行滑块拖拽
    
    def extract_remaining_electricity(self)
        # 提取电量信息
    
    def save_data(self, electricity)
        # 保存数据到JSON/CSV
```

### 添加新功能

#### 1. 修改数据提取逻辑

编辑 `src/nju_electric_monitor_auto.py`:

```python
def extract_remaining_electricity(self):
    # 修改选择器
    element = self.driver.find_element(By.CSS_SELECTOR, "new_selector")
    # 修改提取逻辑
    ...
```

#### 2. 添加新的验证方式

1. 在 `detect_verification_type()` 中添加检测逻辑
2. 创建对应的处理方法 `handle_xxx_verification()`
3. 在 `handle_captcha()` 中添加分发逻辑

#### 3. 自定义可视化

编辑 `src/web_panel.py`:

```python
@app.route('/custom_chart')
def custom_chart():
    # 添加自定义图表
    ...
```

### 测试开发

#### 创建新测试

在 `tests/` 目录创建测试文件:

```python
# tests/test_new_feature.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_new_feature():
    # 测试逻辑
    ...

if __name__ == "__main__":
    test_new_feature()
```

#### 运行测试

```bash
# 运行单个测试
python tests/test_new_feature.py

# 运行所有测试
pytest tests/
```

### 性能优化

#### 1. 减少等待时间

```python
# 使用显式等待替代固定等待
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "element_id"))
)
```

#### 2. 优化图像识别

```python
# 调整图像预处理参数
img = img.resize((img.width * 2, img.height * 2))
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.5)  # 调整对比度
```

#### 3. 缓存识别结果

```python
# 避免重复识别相同验证码
from functools import lru_cache

@lru_cache(maxsize=32)
def recognize_captcha(self, img_hash):
    ...
```

### 贡献代码

1. Fork项目
2. 创建特性分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送分支: `git push origin feature/amazing-feature`
5. 提交Pull Request

---

## 附录

### A. 相关资源

- **Selenium文档**: https://www.selenium.dev/documentation/
- **ddddocr项目**: https://github.com/sml2h3/ddddocr
- **captcha-recognizer**: https://pypi.org/project/captcha-recognizer/
- **GitHub Actions文档**: https://docs.github.com/en/actions

### B. 常见问题FAQ

**Q: 为什么有时验证码识别成功率低？**  
A: 验证码图片质量、噪声、扭曲程度都会影响OCR识别。系统已实现多轮重试机制，最终成功率可达95%+。

**Q: 滑块验证失败率高怎么办？**  
A: 检查captcha-recognizer是否正确安装，查看canvas截图是否清晰。系统已实现多轮重试，单次失败会自动重试。

**Q: 如何修改定时任务频率？**  
A: 编辑 `.github/workflows/schedule.yml`，修改 `schedule` 部分的cron表达式。

**Q: 数据文件太大怎么办？**  
A: 可以定期清理旧数据，或修改代码只保留最近N天的数据。

**Q: 如何禁用邮件通知？**  
A: 在config_workflow.json中设置 `"enable_email_alert": false`。

### C. 更新日志

**v2.0 (2026-07-28)**
- ✅ 新增滑块验证支持
- ✅ 优化验证方式自动检测
- ✅ 增加多轮重试机制
- ✅ 完善测试脚本

**v1.0 (2025-07-27)**
- ✅ 初始版本发布
- ✅ 支持传统验证码识别
- ✅ 数据可视化面板
- ✅ GitHub Actions自动化

---

## 许可证

MIT License

---

## 联系方式

如有问题或建议，请通过GitHub Issues提交。

**最后更新**: 2026-07-28
