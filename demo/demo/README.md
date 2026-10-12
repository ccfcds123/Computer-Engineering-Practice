# XGO 机器狗智能巡检 Demo

基于 **XGO Mini 四足机器狗（树莓派 + 陆吾 `xgomini` 固件）** 的课程实践项目：机器狗沿方形路径自主巡线行走，在每个检查点调用 **YOLO 目标检测** 识别仪表读数、安全帽佩戴和区域标识，通过 **TTS 语音** 实时播报结果，最后识别并抓取桌面上的红色小球。

---

## 1. 系统架构

采用 **「狗端采集 + PC 端推理」** 的 C/S 架构，把算力需求高的 YOLO 推理放在 PC 上，树莓派只负责采图和执行动作。

```
        ┌─────────────────────────┐          ┌──────────────────────────┐
        │   树莓派 4B（机器狗端）  │          │      PC（推理服务器端）    │
        │                         │          │                          │
        │  camera1.py             │  TCP     │  dog_server.py           │
        │  └ Picamera2 全局单例    │ ───────► │  ├ 收图 → YOLO 推理       │
        │  dog_client.py          │  5555    │  ├ best.pt（10 类模型）   │
        │  ├ 采图/JPEG 编码        │ ◄─────── │  └ 返回 JSON 检测结果     │
        │  └ 语音播报 (edge-tts)   │  JSON    │                          │
        │  action_test.py         │          │  运行环境：yolo(conda)    │
        │  ├ 方形路径运动规划       │          └──────────────────────────┘
        │  ├ 检查点触发识别         │
        │  └ redball.py 抓取小球    │
        └─────────────────────────┘
```

**数据流：** 树莓派摄像头 → JPEG 编码 → TCP 发送 → PC 端 YOLO 推理 → JSON 结果回传 → 树莓派打印结果并 TTS 播报。

---

## 2. 文件说明

| 文件 | 运行端 | 说明 |
| --- | --- | --- |
| `dog_server.py` | **PC** | YOLO 推理服务器。TCP 监听 `0.0.0.0:5555`，多线程处理每个客户端连接，收到图片后推理并返回 JSON 结果 |
| `dog_client.py` | 狗 | 客户端核心。调用全局摄像头采图，按长度前缀协议发送帧、接收 JSON 结果，并调用语音模块播报检出的每一类目标；若检出安全帽相关类别（cls 5/6）会额外播报统计信息 |
| `camera1.py` | 狗 | 摄像头模块。`SingletonDogCamera` 全局单例封装 Picamera2，避免多模块重复 `open/close` 导致的资源冲突；对外提供 `get_global_camera()` |
| `action_test.py` | 狗 | **主程序入口**。完成「方形路径行走 → 检查点识别 → 红色小球抓取」的完整流程编排 |
| `redball.py` | 狗 | 红色小球识别与抓取。HSV 双区间阈值 + 形态学去噪 + 霍夫圆检测，按半径估算距离，闭环调整前后/左右位置后执行机械臂抓取 |
| `yuyin.py` | 狗 | 语音播报。基于 `edge-tts` 流式合成 + `mpg123` 直接播放，**无需落盘**；首次运行会尝试自动 `apt install mpg123` |
| `录制.py` | 狗 | 录制工具。让机器狗低头（`attitude('p', -12)`）后自动录制视频到 `/home/pi/xgoVideos/`，带 FPS 与剩余时间叠加显示，按 `q` / `Esc` 可提前退出 |
| `test.py` | PC | 离线单图测试脚本。对 `D_frame_240.jpg` 跑一次推理，打印类别/置信度并弹窗可视化，用于验证模型是否正常 |
| `best.pt` | PC | YOLO 权重文件（约 5.4 MB） |
| `D_frame_240.jpg` | PC | 测试用样例图片 |

> **与原 readme 的差异：** 旧 readme 中提到的 `action.py`、`action2.py`、`yuying.py` 在本仓库中并不存在，实际对应 `action_test.py`（完整流程）与 `yuyin.py`（语音播报）。

---

## 3. 检测类别

代码中的类别表共 **11 项（class_id 0~10）**，`dog_server.py` 的 `LABELS_CN` 与 `dog_client.py` 的 `CLASS_NAMES` / `CLASS_CN_MAP` 三个列表必须按同一顺序保持一一对应：

| ID | 英文名 | 中文含义 | 播报内容 |
| --- | --- | --- | --- |
| 0 | low | 偏低 | 偏低为异常状态 |
| 1 | normal | 正常 | 正常为正常状态 |
| 2 | higher | 较高 | 较高为异常状态 |
| 3 | three | 35212 | 35212 偏高变压器过压 |
| 4 | six | 10561 | 10561 偏低变压器欠压 |
| 5 | No helmet | 未佩戴安全帽 | 未佩戴安全帽 |
| 6 | helmet | 佩戴安全帽 | 佩戴安全帽 |
| 7 | B | B 区域 | B 区域 |
| 8 | D | D 区域 | D 区域 |
| 9 | A | A 区域 | A 区域 |
| 10 | C | C 区域 | C 区域 |

> ⚠️ 模型实际类别数以 `best.pt` 内 `model.names` 为准（可用 `test.py` 打印核对）。三个类别列表的长度与顺序必须一致，否则会出现「A 区域」播报成「C 区域」这类错位问题。

---

## 4. 环境依赖

### 4.1 PC 端（推理服务器）

```bash
conda create -n yolo python=3.10 -y
conda activate yolo

pip install ultralytics opencv-python numpy
```

### 4.2 机器狗端（树莓派）

```bash
# 系统依赖（语音播放）
sudo apt install -y mpg123

# Python 依赖
pip install opencv-python numpy edge-tts
```

此外需使用官方 **xgo-python-lib** 提供 `xgolib`（机器狗固件已内置），以及树莓派原生的 `picamera2`。

> 注意：`xgolib`、`picamera2` 仅能在机器狗本体 / 树莓派上运行，在 PC 上 import 会失败，因此 `action_test.py`、`camera1.py`、`redball.py`、`录制.py` 无法在 PC 上直接调试。

---

## 5. 快速开始

### 步骤 1：PC 端启动推理服务器

```bash
conda activate yolo
python dog_server.py
```

出现 `🚀 机器狗YOLO推理服务器已启动 | 监听地址: 0.0.0.0:5555` 即成功。启动时会一次性加载 `best.pt`。

> 首次运行前，把 `dog_server.py` 中的 `MODEL_PATH` 改成本机 `best.pt` 的实际路径。
> 并确认 PC 防火墙放行 5555 端口，且 PC 与机器狗在 **同一局域网**。

### 步骤 2：机器狗端运行主程序

```bash
python action_test.py
```

程序会依次执行：

1. 连接机器狗，读取固件版本（返回 `Null` 表示连接失败）
2. 初始化全局摄像头（320×240）与 `DogClient`
3. **方形路径行走** —— 前进/转向分段执行（210 → 40 → 80 → 40 → 110 → 40 → 80 → 40 cm），途中在 4 个检查点完成原地转向
4. **检查点识别** —— 低头姿态（`attitude('p', -12)`）下连续识别两轮，每轮持续 15 秒
5. **红色小球抓取** —— 调用 `redball.redball_catch_main(dog)`
6. 释放摄像头与 socket，`dog.reset()` 复位

单独测试某个模块：

```bash
python test.py        # PC：单张图片验证 YOLO 模型
python redball.py     # 狗：只跑小球识别抓取
python 录制.py         # 狗：只跑视频录制
python yuyin.py       # 狗：只跑语音播报
```

---

## 6. 通信协议

自定义 TCP 长连接协议，**大端 4 字节长度前缀** 解决 TCP 粘包问题。

**请求（狗 → PC）：** `[4 字节帧长度][JPEG 图像数据]`

**响应（PC → 狗）：** `[4 字节 JSON 长度][UTF-8 JSON]`

返回 JSON 结构：

```json
{
  "status": "success",
  "inference_ms": 42.3,
  "object_count": 2,
  "detected_objects": [
    { "xyxy": [12.5, 30.1, 88.0, 140.2],
      "confidence": 0.871,
      "class_id": 6 }
  ]
}
```

失败时返回：

```json
{ "status": "error", "msg": "图片解码失败" }
```

| 参数 | 位置 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `SERVER_PORT` | `dog_server.py` | `5555` | 监听端口，需与客户端一致 |
| `CONFIDENCE_THRESHOLD` | `dog_server.py` | `0.3` | 置信度过滤阈值 |
| `host` | `dog_client.py` / `action_test.py` | `172.18.17.47` | **PC 端 IP，换网络后必须修改** |
| `timeout` | `DogClient` | `10` | socket 超时（秒） |
| `IMWRITE_JPEG_QUALITY` | `dog_client.py` | `80` | 上传图像 JPEG 质量 |

> `dog_client.py` 结尾的 `__main__` 测试块里 `host='192.168.79.157'` 是遗留的旧地址；以主程序 `action_test.py` 中的 `172.18.17.47` 为准，两者需按实际网络环境统一修改。

---

## 7. 关键实现说明

- **摄像头单例**：`camera1.py` 用 `__new__` + 类锁实现单例并做打开状态标记。三个模块（客户端、录制、小球抓取）共享同一个 Picamera2 实例，避免反复 open/close 造成资源泄漏或 `device busy`；只有主程序 `finally` 里才真正释放。
- **距离估算**：`redball.py` 用 `distance_cm = 600 / radius` 的经验公式把像素半径换算成距离，`>17cm` 前进、`<12cm` 后退、`12~17cm` 视为可抓取区间，并做左右居中微调（图像中心 x = 160）。
- **抓取姿态**：抓取前先 `translation('z', 75)` 降到最低身高、`attitude('p', 30)` 低头，机械臂下降到 `arm(120, -15)` 后再闭合夹爪，确保末端足够低。
- **语音零落盘**：`edge_tts.Communicate().stream()` 的音频分片直接写进 `mpg123 -q -` 的标准输入，边合成边播放。
- **识别期间静止**：每次识别前调用 `dog.stop()`，识别结束再恢复运动，避免行进抖动影响检测。

---

## 8. 已知问题与注意事项

- **颜色通道**：Picamera2 输出 `RGB888`，而 OpenCV 的 `imencode` / `cvtColor(COLOR_BGR2HSV)` 默认按 BGR 处理。若发现保存的图片色彩异常或红色小球检测不稳定，需在编码前做 `cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)`。`redball.py` 中图像中心 x 取 160 也是按 320 宽度设定，换分辨率时需同步调整。
- **硬编码路径**：`best.pt` 路径写死在 `dog_server.py` 和 `test.py` 中（Windows 绝对路径），换机器后必须修改。
- **录制时长**：`录制.py` 的注释写「10 秒」，实际 `__record_duration = 60`（60 秒）；`cv.imshow` 需要本地桌面或 MobaXterm 开启 X11 转发才能实时查看。
- **运动误差累积**：路径靠 `time.sleep()` 开环控制，长时间运行会有里程误差，`angle_time`、`x40/x80/x110/x210` 等标定系数需按实车微调。
- **网络依赖**：`edge-tts` 需要联网，离线环境语音播报会失败。

---

## 9. 可改进方向

- 用里程计 / IMU 闭环替代 `sleep` 开环控制，降低路径累积误差
- 把 `host`、端口、模型路径、类别表抽到统一的 `config.py` 或 YAML
- 推理结果结构化落盘（JSON/CSV），支持巡检报告导出
- 服务端增加心跳与断线重连，以及请求队列避免多狗并发争抢
