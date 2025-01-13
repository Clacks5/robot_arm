import time
from math import radians,degrees,sin,cos,atan2,sqrt,pi,acos
import traceback
import numpy as np

print("mode select:")
print("* 0 -> value check")
print("* 1 -> simulation")
print("* 2 -> move mode")
move_mode = int(input())


# ----- メイン関数 ----- #
def main():

	print("start program")

	try:    # try内で何らかのエラーが発生 -> 処理中断してexceptに移動

		# --- メインループ （実験内容に応じてここを変更）--- #
		while True:

			J = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # 角度値の初期化（単位：degree）
			# J = [-12.08, -51.17, -123.8, 84.96, 0.0, -12.08]
			# J = [-34.7, -63.36, -119.18, 92.54, 0.0, -34.7]
			# J = [26.27, -26.46, -146.28, 82.74, 0.0, 26.27]
			# J = [55.30, -51.17, -123.80, 84.96, 0.0, 55.30]
			J = [77.92, -63.36, -119.18, 92.54, 0.0, 77.92]

			# for i in range(6):
			# 	print(f"input J[{i}]:")
			# 	J[i] = float(input())               # 角度値をキーボード入力

			for i in range(6):                  # 6つの角度値を表示
				print("J"+str(i+1)+": ",J[i])

			# moveto(J=J, marker_pos=[100, 100, 100])
			moveto(J=J, marker_pos=calc_minions_pos(J))

	except:
		traceback.print_exc()                   # try内で発生したエラーを表示
# -------------------- #


# ----- 学生定義のサブ関数（実験内容に応じてここに関数を追加する） ----- #
def calc_minions_pos(J):
	# thetaのオフセット
	theta = np.array(J)/180*np.pi + [0, np.pi/2, 0, np.pi/2, -np.pi/2, 0]

	T1 = np.array([
		[np.cos(theta[0]), 0, np.sin(theta[0]), 0],
		[np.sin(theta[0]), 0, -np.cos(theta[0]), 0],
		[0, 1, 0, d1],
		[0, 0, 0, 1]
	])
	T2 = np.array([
		[np.cos(theta[1]), -np.sin(theta[1]), 0, a2*np.cos(theta[1])],
		[np.sin(theta[1]), np.cos(theta[1]), 0, a2*np.sin(theta[1])],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])
	T3 = np.array([
		[np.cos(theta[2]), -np.sin(theta[2]), 0, a3*np.cos(theta[2])],
		[np.sin(theta[2]), np.cos(theta[2]), 0, a3*np.sin(theta[2])],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])
	T4 = np.array([
		[np.cos(theta[3]), 0, np.sin(theta[3]), 0],
		[np.sin(theta[3]), 0, -np.cos(theta[3]), 0],
		[0, 1, 0, d4],
		[0, 0, 0, 1]
	])
	T5 = np.array([
		[np.cos(theta[4]), 0, np.sin(theta[4]), 0],
		[np.sin(theta[4]), 0, -np.cos(theta[4]), 0],
		[0, 1, 0, d5],
		[0, 0, 0, 1]
	])
	T6 = np.array([
		[np.cos(theta[5]), -np.sin(theta[5]), 0, 0],
		[np.sin(theta[5]), np.cos(theta[5]), 0, 0],
		[0, 0, 1, d6],
		[0, 0, 0, 1]
	])

	pos = T1@T2@T3@T4@T5@T6@np.array([0, 0, 0, 1])
	print(pos)
	return pos[:3].tolist()

# ------------------------------------------------------------ #

# ----- 【！変更しないこと！】mycobotライブラリの初期化 ----- #

if move_mode==1:
	from mycobot_sim import send_angles_sim

elif move_mode==2:
	print("load mycobot library...", end=" ")
	from pymycobot.mycobot import MyCobot
	from pymycobot.genre import Angle
	from pymycobot import PI_PORT, PI_BAUD

	mycobot = MyCobot(PI_PORT, PI_BAUD)
	time.sleep(1)
	mycobot.set_gripper_ini()
	time.sleep(1)
	print("OK")


# - 【！変更しないこと！】リンク長の定義 [mm] - #
d1 = 140
a2 = 110.4
a3 = 96.0
d4 = 66.39
d5 = 73.18
d6 = 43.6


# ----- 【！変更しないこと！】mycobot6軸関節確度制御----- #
def moveto(J, marker_pos):

	angle_check(J)  # 角度が動作範囲内かチェック

	if move_mode == 2:
		print("move")
		mycobot.send_angles([J[0]-90, J[1], J[2], J[3], J[4], J[5]], 20)
		time.sleep(5)

	elif move_mode == 1:
		send_angles_sim(J=J, marker_pos=marker_pos)


# ----- 【！変更しないこと！】角度リミットエラー用 ----- #
class AngleError(Exception):
	pass


# ----- 【！変更しないこと！】関節角度範囲チェック ----- #
def angle_check(J):

	print("angle_check...", end=" ")

	if J[0] < -90 or J[0] > 90:
		raise AngleError('J1 angle error')

	if J[1] < -120 or J[1] > 120:
		raise AngleError('J2 angle error')

	if J[2] < -150 or J[2] > 150:
		raise AngleError('J3 angle error')

	if J[3] < -120 or J[3] > 120:
		raise AngleError('J4 angle error')

	if J[4] < -120 or J[4] > 120:
		raise AngleError('J5 angle error')

	if J[5] < -90 or J[5] > 90:
		raise AngleError('J6 angle error')

	print("OK\n")

# ----- 【！変更しないこと！】メイン処理 ----- #
if __name__ == "__main__":
	main()
