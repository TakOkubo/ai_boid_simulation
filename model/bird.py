import pygame
import random
import json
import numpy as np

BIRD_COLORS = [
	'#FFA5CC',  # pink
	'#80FF25',  # green
	'#A0D4FF',  # skyblue
]

# 食事ルール
RADIUS_OF_FOOD = 300
# 敵ルール
RADIUS_OF_ENEMY = 300
# HP
HEALTH_POINT = 500

# 鳥モデル
class Bird:
	def __init__(self,
			bird_id,
			width,
			height,
			ai_model
	):
		self.bird_id = bird_id
		self.width = width
		self.height = height
		# 生成AIモデル
		self.ai_model = ai_model
		# 初期値
		self.food_param = RADIUS_OF_FOOD
		self.food_positions = []
		self.enemy_param = RADIUS_OF_ENEMY
		self.enemy_positions = []
		# 位置
		self.position = np.array([random.uniform(0, width), random.uniform(0, height)])
		# 速度と角度
		self.velocity = 0.0
		self.angle = np.radians(0)
		self.direction = np.array([np.cos(self.angle), np.sin(self.angle)])
		# 鳥のHP
		self.health_point = HEALTH_POINT
		# 鳥の形状
		self.polygon = np.array([(20, 0), (0, 5), (0, -5)])
		self.type_id = self.bird_id % 3
		self.color = BIRD_COLORS[self.type_id]

	# 行動
	def move(self):
		self.direction = np.array([np.cos(self.angle), np.sin(self.angle)])
		# 速度ベクトルから進行方向を求める。
		vector = self.velocity * (self.direction)
		if np.linalg.norm(vector) != 0:
			self.position += vector

		# 鳥が壁にぶつかったら反対側に通り抜ける
		if self.position[0] > self.width or self.position[0] < 0:
			self.position[0] = np.abs(self.position[0] - self.width)
		if self.position[1] > self.height or self.position[1] < 0:
			self.position[1] = np.abs(self.position[1] - self.height)

	# 生成AIによる動作指示
	def generate_ai_operation(self):
		data = {
			"enemies": list(self.enemy_positions),
			"foods": list(self.food_positions)
		}

		prompt = {
			"role" : "user",
			"content" : f'{json.dumps(data)}'
		}

		output = self.ai_model.generate(
			prompt=prompt,
			is_add_prompts=True)
		# 行ごとに処理
		for line in output.splitlines():
			if "angle" in line:
				output = line
				break

		try:
			output_json = json.loads(output)

			angle_degrees = output_json["angle"] if "angle" in output_json else None
			self.angle = np.radians(angle_degrees) if angle_degrees is not None else self.angle
			self.velocity = output_json["velocity"] if "velocity" in output_json else self.velocity

			print(f'angle: {angle_degrees}, velocity: {self.velocity}')
		except json.JSONDecodeError as e:
			return

	# 餌の探索ルール
	def search_food(self, food_list):
		# 探索範囲
		radius = self.food_param
		# 自分の位置
		x = self.position[0]
		y = self.position[1]

		# 鳥の近くにある餌を取得する。
		near_food = [food for food in food_list
			if np.linalg.norm(np.array([food.x, food.y]) - np.array([x, y])) < radius
				and not food.eaten
		]

		# 鳥と餌の相対位置を計算する。
		relative_food_positions = []
		if len(near_food) > 0 :
			for food in near_food:
				food_position = np.array([food.x, food.y]) - np.array([x, y])

				# 極座標変換
				r = np.linalg.norm(food_position)
				theta = np.degrees(np.arctan2(food_position[1], food_position[0]))

				relative_food_positions.append({
						"angle" : theta,
						"distance" : r
				})
		self.food_positions = relative_food_positions
	
	# 食事ルール
	def eat_food(self, food_list):
		# 餌を食べる
		x = self.position[0]
		y = self.position[1]

		# 鳥の近くにある餌を取得する。
		near_foods = [food for food in food_list
			if np.linalg.norm(np.array([food.x, food.y]) - np.array([x, y])) < food.radius
				and not food.eaten
		]

		# 餌がある場合、食べる。
		if len(near_foods) > 0:
			first_near_food = near_foods[0]
			self.health_point += first_near_food.power
			first_near_food.eaten = True
			print(f'餌を食べました。HP:{self.health_point}')

	# 敵の探索ルール
	def search_enemy(self, enemy_list):
		# 探索範囲
		radius = self.enemy_param
		# 自分の位置
		x = self.position[0]
		y = self.position[1]

		# 鳥の近くにある敵を取得する。
		near_enemy = [enemy for enemy in enemy_list
			if np.linalg.norm(np.array([enemy.x, enemy.y]) - np.array([x, y])) < radius
		]

		# 鳥と敵の相対位置を計算する。
		relative_enemy_positions = []
		if len(near_enemy) > 0 :
			for enemy in near_enemy:
				enemy_position = np.array([enemy.x, enemy.y]) - np.array([x, y])

				# 極座標変換
				r = np.linalg.norm(enemy_position)
				theta = np.degrees(np.arctan2(enemy_position[1], enemy_position[0]))

				relative_enemy_positions.append({
						"angle" : theta,
						"distance" : r
				})
		self.enemy_positions = relative_enemy_positions
	
	# 敵に衝突する。
	def clash_enemy(self, enemy_list):
		x = self.position[0]
		y = self.position[1]

		# 鳥の近くにいる敵を取得する。
		near_enemies = [enemy for enemy in enemy_list
			if np.linalg.norm(np.array([enemy.x, enemy.y]) - np.array([x, y])) < enemy.radius
		]

		# 敵に衝突した場合、HPを下げる。
		if len(near_enemies) > 0:
			# 衝突をしたことがない敵を抽出する。
			not_clash_near_enemies = [enemy for enemy in near_enemies if not enemy.clashed]
			if len(not_clash_near_enemies) > 0:
				first_near_enemy = not_clash_near_enemies[0]
				self.health_point -= first_near_enemy.power
				first_near_enemy.clashed = True
				print(f'敵に当たりました。HP:{self.health_point}')
		else:
			for enemy in enemy_list:
				enemy.clashed = False

	def display(self, screen):
		# 回転行列を形成
		rotation_matrix = np.array([[np.cos(self.angle), -np.sin(self.angle)],
									[np.sin(self.angle), np.cos(self.angle)]])
		# 頭を進行方向にするように回転させる。
		rotated_polygon = np.dot(self.polygon, rotation_matrix.T) + self.position
		pygame.draw.polygon(screen, self.color, rotated_polygon, 0)