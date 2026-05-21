# hello.py

小型示例工具，包含：

- `greet(name, uppercase=False)`：生成问候字符串。
- `save_greeting(text, path)`：将问候保存到文件。
- `fetch_url(url)`：从指定 URL 获取内容并返回字符串（使用标准库）。

运行示例：

```bash
python hello.py --name Alice
python hello.py --name Bob --save greeting.txt
python hello.py --url https://example.com
```

运行测试：

```bash
python -m unittest discover -v
```
