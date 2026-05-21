import qrcode

# 二维码内容
content = "https://b23.tv/givtd6V"

# 生成二维码
qr = qrcode.QRCode(
    version=1,  # 控制二维码大小，1为最小
    error_correction=qrcode.constants.ERROR_CORRECT_M,  # 纠错级别
    box_size=10,  # 每个小格子的像素大小
    border=4,  # 边框宽度
)
qr.add_data(content)
qr.make(fit=True)

# 生成并保存图片
img = qr.make_image(fill_color="black", back_color="white")
img.save("qrcode_20251223.png")
print("二维码已保存为 qrcode_20251223.png")