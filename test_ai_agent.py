from model.ai_agent import AiAgent

# AIモデルのテスト
def main():
	# 生成AIのロード
	ai_model = AiAgent()

	prompt = {
			"role" : "user",
			"content" : "{ 'enemies': [{'angle': 0, 'distance': 2}, {'angle': 10, 'distance': 10}], 'foods': [{'angle': 45, 'distance': 400}, {'angle': 5, 'distance': 500}] }"
	}

	# 生成AIでの生成
	ai_model.generate(prompt=prompt, is_add_prompts=True)


if __name__ == '__main__':
	main()