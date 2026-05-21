import asyncio
import edge_tts
import subprocess
import sys

# ===================== 核心配置区（只需改这里！） =====================
TEXT = "我自己写的文本，无需保存文件直接播放"  # 自定义要朗读的文本
VOICE = "zh-CN-XiaoyiNeural"  # 可选音色：zh-CN-XiaochenNeural/zh-CN-XiaohanNeural等
# =====================================================================

def install_dependency() -> None:
    """自动检测并安装mpg123依赖（仅首次运行）"""
    try:
        subprocess.run(["mpg123", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  检测到未安装mpg123，正在自动安装...")
        try:
            subprocess.run(["sudo", "apt", "install", "-y", "mpg123"], check=True)
            print("✅ 依赖安装完成")
        except subprocess.CalledProcessError as e:
            raise RuntimeError("依赖安装失败，请手动执行：sudo apt install -y mpg123") from e

async def play_speech_directly(text: str, voice: str = VOICE) -> None:
    """
    无需保存文件，直接流式播放语音
    :param text: 要转换的文本
    :param voice: 语音音色
    """
    if not text.strip():
        raise ValueError("要朗读的文本不能为空！")
    
    # 初始化TTS并获取音频流
    communicate = edge_tts.Communicate(text, voice)
    # 启动mpg123作为音频播放器（标准输入接收音频流）
    player = subprocess.Popen(
        ["mpg123", "-q", "-"],  # -q静默模式，-表示从标准输入读取
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        print("🔊 正在播放语音...")
        # 流式读取音频数据并写入播放器
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                player.stdin.write(chunk["data"])
                player.stdin.flush()
        # 关闭标准输入，等待播放器结束
        player.stdin.close()
        player.wait()
        if player.returncode == 0:
            print("✅ 语音播放完成")
        else:
            print(f"⚠️  播放异常，退出码：{player.returncode}")
    except Exception as e:
        print(f"❌ 播放失败：{e}")
    finally:
        # 确保播放器进程终止
        if player.poll() is None:
            player.terminate()

if __name__ == "__main__":
    # 1. 自动安装依赖
    install_dependency()
    
    # 2. 直接播放文本（无需保存文件）
    asyncio.run(play_speech_directly(TEXT))