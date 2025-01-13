import time
# from math import radians,degrees,sin,cos,atan2,sqrt,pi,acos
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
			# 座標を入力
			print(f"input x:")
			x = float(input())
			print(f"input y:")
			y = float(input())
			print(f"input z:")
			z = float(input())
			print(f"x = {x}")
			print(f"y = {y}")
			print(f"z = {z}")


			J = calc_inverse_kinematics(x, y, z)
			for i in range(6):                  # 6つの角度値を表示
				print("J"+str(i+1)+": ",J[i])

			moveto(J=J, marker_pos=[x, y, z])

	except:
		traceback.print_exc()                   # try内で発生したエラーを表示
# -------------------- #


# ----- 学生定義のサブ関数（実験内容に応じてここに関数を追加する） ----- #
def calc_inverse_kinematics(x, y, z):
	d1 = 140
	a2 = 110.4
	a3 = 96.0
	d4 = 66.39
	d5 = 73.18
	d6 = 43.6

	theta = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

	# 逆運動学の計算
	zero_division_check(x*x + y*y)
	if y > 0:
		theta[0] = np.pi - np.atan2(x, y) - np.acos(d4 / np.sqrt(x*x + y*y))
	else:
		theta[0] = -(np.pi/2 - np.atan2(x, -y) - np.asin(d4 / np.sqrt(x*x + y*y)))
	
	X = (x - d5*np.cos(theta[0]) - d4*np.sin(theta[0])) / np.cos(theta[0])
	Z = z + d6 - d1

	sqrt_check(1 - ((X*X + Z*Z - a2*a2 - a3*a3)/(2*a2*a3))**2)
	theta[2] = -np.atan2(np.sqrt(1 - ((X*X + Z*Z - a2*a2 - a3*a3)/(2*a2*a3))**2), (X*X + Z*Z - a2*a2 - a3*a3)/(2*a2*a3))

	alpha = np.atan2(Z, X)
	beta = np.atan2(a3*np.sin(theta[2]), a3*np.cos(theta[2]) + a2)
	theta[1] = alpha - beta

	theta[3] = np.pi/2 - theta[1] - theta[2]
	theta[4] = -np.pi/2
	theta[5] = theta[0]

	J = 180/np.pi*(theta - np.array([0, np.pi/2, 0, np.pi/2, -np.pi/2, 0]))

	return J.tolist()

def z_check(pos):
	print("z_check...", end=" ")
	
	if pos[2] < 15.0:
		raise ZError("z error")

	print("OK\n")
def zero_division_check(val):
	print("zero_division_check...", end=" ")
	
	if np.abs(val) < 0.001:
		raise ZeroDivisionError("zero_division error")

	print("OK\n")
def sqrt_check(val):
	print("sqrt_check...", end=" ")
	
	if val < 0:
		raise SqrtError("sqrt error")

	print("OK\n")

class ZError(Exception):
	pass
class ZeroDivisionError(Exception):
	pass
class SqrtError(Exception):
	pass

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
	z_check(pos=marker_pos)	# z手先位置が小さすぎないことをチェック

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
