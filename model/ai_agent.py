from llama_cpp import Llama
import json
import time

Gemma2 = {
	"model_path" : "./ai_model/mmnga/gemma-2-2b-it-gguf/gemma-2-2b-it-Q4_K_M.gguf",
	"chat_format" : "gemma"
}

Llama3 = {
	"model_path" : "./ai_model/bartowski/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
	"chat_format" : "llama-3"
}

# 使用するAIモデル
# use_model = Gemma2
use_model = Llama3

prompts = [
		{
			"role": "user",
			"content":
				"I want to determine the angle and velocity of an agent on a 2D plane based on the following rules:\n" + 
				"・The agent moves away from enemies based on their relative distances.\n" + 
				"・The agent moves toward foods based on their relative distances.\n" + 
				"・The agent prioritizes the closest food. However, if a food is close to an enemy, the agent avoids that food and moves to another.\n" + 
				"・Based on these conditions, calculate the angle and velocity.\n" + 
				"・The distances and angles of enemies and foods will be provided in JSON format.\n" + 
				"・The agent's angle and velocity should also be returned in JSON format.\n" + 
				"・Do not include any extra text or explanations.\n" +
				"Input example:{ 'enemies': [{'angle': 0, 'distance': 2}, {'angle': 10, 'distance': 10}], 'foods': [{'angle': 45, 'distance': 400}, {'angle': 5, 'distance': 500}] }\n"
				"Output example:{'angle': 45, 'velocity': 4.5}\n" +
				"------------------------------------------\n" +
				'{ "enemies": [], "foods": [] }'
		},
		{
			"role": "assistant",
			"content": '{"angle": 10, "velocity": 2.5}'
		},
		{
			"role": "user", 
			"content" : '{ "enemies": [{"angle": 45, "distance": 800}], "foods": [{"angle": -45, "distance": 210.5}] }'
		},
		{
			"role": "assistant",
			"content": '{"angle": -45, "velocity": 3.01}'
		},
		{
			"role": "user",
			"content": '{ "enemies": [{"angle": 0, "distance": 2}, {"angle": 10, "distance": 10}], "foods": [{"angle": 10, "distance": 40},{"angle": 5, "distance": 5}] }'
		},
		{
			"role" : "assistant",
			"content" : '{"angle": 5, "velocity": 1.5}'
		},
	]


class AiAgent:
	def __init__(self):
		start_time_1 = time.time()

		llm = Llama(
			model_path=use_model["model_path"],
			chat_format=use_model["chat_format"],
			n_gpu_layers=-1, 
			# n_ctx=512
			n_ctx=2048
		)
		end_time_1 = time.time()
		print("------------------------------")
		print("モデルロード時間　", end_time_1 - start_time_1)
		print("------------------------------")

		self.model = llm
		self.prompts = prompts
	
	# 生成
	def generate(self, prompt, is_add_prompts):
		start_time_2 = time.time()
		print("------------------------------")
		print("プロンプト: ", prompt)
		print("------------------------------")

		if is_add_prompts:
			messages = list(self.prompts)
		else:
			messages = []

		messages.append(prompt)
		outputs = self.model.create_chat_completion(
			messages=messages,
			max_tokens=100, 
			temperature=0.7
		)

		output = outputs["choices"][0]["message"]["content"]
		end_time_2 = time.time()
		print("------------------------------")
		print("回答時間　", end_time_2 - start_time_2)
		print(output)
		print("------------------------------")

		return output