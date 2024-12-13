import pygame
import random
from model.bird import Bird
from model.food import Food
from model.enemy import Enemy
from model.ai_agent import AiAgent

# 群れの総数
BIRD_NUM = 1

# 餌の総数
FOOD_NUM = 10

# 敵の総数
ENEMY_NUM = 5

# カラー定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# メイン実行
def main():
	pygame.init()
	# 画面サイズの設定
	width, height = 800, 600
	step = 0
	screen = pygame.display.set_mode((width, height))
	pygame.display.set_caption("Boid Simulation")

	# ゲームの状態
	clear_flag = False  # クリア画面を表示するフラグ

	# 鳥の総数の初期化
	bird_num = BIRD_NUM
	# 体力が尽きた鳥の総数
	health_point_over_number = 0

	# 生成AIのロード
	ai_model = AiAgent()

	# 鳥の生成
	bird_list = []
	for i in range(bird_num):
		# 初期パラメータをランダムで生成します。
		bird_list.append(Bird(
			bird_id=i,
			width=width,
			height=height,
			ai_model=ai_model
		))

	# 餌の生成
	food_list = []
	for i in range(FOOD_NUM):
		food_list.append(
			Food(
				id=i,
				x=random.uniform(0, width),
				y=random.uniform(0, height)
			)
		)

	# 敵の生成
	enemy_list = []
	for i in range(ENEMY_NUM):
		enemy_list.append(
			Enemy(
				id=i,
				x=random.uniform(0, width),
				y=random.uniform(0, height)
			)
		)

	clock = pygame.time.Clock()

	# 実行
	while True:
		# 死亡予定の鳥のリスト
		over_bird_list = []

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				exit()

		# クリア画面
		if clear_flag:
			game_clear(
				screen=screen,
				width=width,
				height=height
			)
			continue  # シミュレーションを停止

		# それぞれの鳥の動き
		for bird in bird_list:
			# 死んだ鳥の中に、対象の鳥がいるかチェックする
			targets_in_over_bird_list = [over_bird for over_bird in over_bird_list if bird.bird_id == over_bird.bird_id]
			# 餌の探索
			bird.search_food(food_list)
			# 敵の探索
			bird.search_enemy(enemy_list)
			# AIによる動作指示
			if step % 100 == 0:
				bird.generate_ai_operation()
			# 行動
			bird.move()
			# 食事
			bird.eat_food(food_list)
			# 敵との衝突
			bird.clash_enemy(enemy_list)

			# 鳥の体力がなくなると死亡する
			if bird.health_point <= 0 and len(targets_in_over_bird_list) <= 0:
				print("health point over: %s" % bird.bird_id)
				over_bird_list.append(bird)
				health_point_over_number += 1

		screen.fill((0, 0, 0))

		# 死んだ鳥を削除する
		for over_bird in over_bird_list:
			bird_list = [bird for bird in bird_list if not bird.bird_id == over_bird.bird_id]

		# 食べられた餌の数
		eaten_food_num = 0
		# 食べられた餌を削除する
		for food in food_list:
			if food.eaten:
				food_list.remove(food)
				eaten_food_num += 1
		
		if len(food_list) == 0:
			print("クリア！　餌を全て食べることができました！")
			clear_flag = True
			# pygame.quit()
			# break

		# ランダムで餌を生む
		if len(bird_list) == 0:
			print("鳥が絶滅しましたので、プログラムを終了します。")
			pygame.quit()
			break

		# 鳥を描画する
		for bird in bird_list:
			bird.display(screen)
		
		# 餌を描画する
		for food in food_list:
			food.display(screen)

		# 敵を描画する
		for enemy in enemy_list:
			enemy.display(screen)

		# 画面に設定を表示
		display_rendered_text(
			screen=screen,
			bird_list=bird_list,
			food_list=food_list,
			enemy_list=enemy_list,
			health_point_over_number=health_point_over_number)

		pygame.display.flip()
		clock.tick(30)
		step +=1

# 画面に設定を表示する
def display_rendered_text(
		screen, 
		bird_list, 
		food_list, 
		enemy_list,
		health_point_over_number
	):
	font = pygame.font.Font(None, 15)
	text_lines = [
		"bird number: %s" % len(bird_list),
		"food number: %s" % len(food_list),
		"enemy number: %s" % len(enemy_list),
		"health point over: %s" % health_point_over_number,
	]
	rendered_lines = [font.render(line, True, (255, 255, 255)) for line in text_lines]
	text_position = (10, 10)
	for rendered_line in rendered_lines:
		screen.blit(rendered_line, text_position)
		text_position =(text_position[0], text_position[1] + rendered_line.get_height())

def game_clear(
		screen,
		width,
		height
	):
	font = pygame.font.Font(None, 74)
	# screen.fill(BLACK)
	text = font.render("GAME CLEAR", True, RED)
	screen.blit(text, (width // 2 - 200, height // 2))
	pygame.display.flip()


if __name__ == '__main__':
	main()