# ローカルLLMを用いたボイドシミュレーション（llama.cpp、llama-cpp-python）
## 概要
ボイドモデルの動きをローカルLLMで生成して動かすシミュレーションを実施しました。

詳細はブログ記事にあげますので、そちらを参照してください。  
[ローカルLLMを使ったボイドシミュレーション（llama.cpp、llama-cpp-python）｜豆蔵デベロッパーサイト](https://developer.mamezou-tech.com/blogs/2024/12/19/ai_boid_simulation/)

## 実行について
### 前準備
- Hugging Faceの下記リンクからLLMをダウンロードし`./ai_model`内に格納してください。
	- ※ `./model/ai_ageng.py`に冒頭にある使用モデルのリンクを参照して格納するようにしてください。

| モデル | リンク | 使用モデル |
| --- | --- | --- |
| Gemma2 | [https://huggingface.co/mmnga/gemma-2b-it-gguf](https://huggingface.co/mmnga/gemma-2b-it-gguf) | gemma-2-2b-it-Q4_K_M.gguf |
| LLaMA3 | [https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF](https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF) | Llama-3.2-1B-Instruct-Q4_K_M.gguf |


- `./model/ai_agent.py`では下記のようにパスを定義しています。使用するAIモデルについては、`use_model`にて選択してください。
```python:./model/ai_agent.py
Gemma2 = {
	"model_path" : "./ai_model/mmnga/gemma-2-2b-it-Q4_K_M.gguf",
	"chat_format" : "gemma"
}

Llama3 = {
	"model_path" : "./ai_model/bartowski/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
	"chat_format" : "llama-3"
}

# 使用するAIモデル
# use_model = Gemma2
use_model = Llama3
```


### 実行
main.pyを実行すると、PyGameによるシミュレーションが実施できます。
※ Anacondaをインストールしていることが前提です。  
※ 実行するためのライブラリはrequirements.txtにありますので、適宜インストールしてください。
```powershell
python main.py
```

### 生成AIモデルのみ試したい場合
test_ai_agent.pyを実行すると、生成AIモデルのみ実施できます。
```powershell
python test_ai_agent.py
```