import gymnasium as gym
env = gym.make("CartPole-v1", render_mode="human") # 若改用這個，會畫圖
# env = gym.make("CartPole-v1", render_mode="rgb_array")
observation, info = env.reset(seed=42)
position, velocity, angle, angle_velocity = observation
score = 0
for _ in range(10000):
   env.render()
   if position > 2.25 : 
      action = 0
      #print('>')
   elif position < -2.25 : 
      action = 1
      #print('<')
   elif angle_velocity < 0 : action = 0
   elif angle_velocity > 0 : action = 1

   #if angle_velocity > 0 : action = 1
   #elif angle_velocity < 0 : action = 0
   observation, reward, terminated, truncated, info = env.step(action)
   position, velocity, angle, angle_velocity = observation
   score += reward
   #print('observation=', observation)
   if terminated or truncated:
      #if angle > 0.2095 or angle < -0.2095 :
      #   print('angle dead')
      #if position > 2.4 or position < -2.4 :
      #   print('position dead')
      observation, info = env.reset()
      print('done, score=',score)
      score = 0
env.close()