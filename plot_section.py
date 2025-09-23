
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ================== 从Excel读取速度限制数据 ==================
try:
    # 读取Excel文件，指定没有列名
    df = pd.read_excel('D:\Study\TTO\section_data.xlsx', header=None)
    
    # 提取距离和速度数据（第一列是距离，第二列是速度）
    distance_limit = df[0].tolist()  # 第一列
    speed_limit = df[1].tolist()     # 第二列
    
    # 确保数据是数值类型
    distance_limit = [float(x) for x in distance_limit]
    speed_limit = [float(x) for x in speed_limit]
    
    print("成功读取速度限制数据：")
    print(f"距离数据: {distance_limit}")
    print(f"速度数据: {speed_limit}")
    
except Exception as e:
    print(f"读取Excel文件时出错: {e}")
    # 如果读取失败，使用默认数据
    distance_limit = [0, 0, 20, 20, 50, 50]
    speed_limit = [0, 50, 50, 90, 90, 0]

# ================== 物理常数和参数 ==================
g = 9.8  # 重力加速度 (m/s^2)
M = 16.4e4  # 列车质量 (kg)
alpha = 1.36e-4  # 阻力系数
beta = 1.45e-2   # 阻力系数
gamma = 1.244    # 阻力系数
kappa = 1.36e-4  # 坡度 (弧度)

# ================== 定义多段运行参数 ==================
segments1 = [
   {'type': 'accel', 'v0': 0.0, 'v1': 47.0, 'F_max': 200000},    # 加速阶段（最大牵引力200kN）
    {'type': 'cruise', 'v0': 47.0, 'distance': 50},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 47.0, 'v1': 46.5},                      # 惰行阶段（仅受阻力影响）
       {'type': 'accel', 'v0': 46.5, 'v1': 50.0, 'F_max': 200000},
        {'type': 'cruise', 'v0': 50.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 50.0, 'v1': 49.4},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 49.4, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）


    {'type': 'accel', 'v0': 0.0, 'v1': 33.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 33.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 33.0, 'v1': 31.9},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 31.9, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
    
        {'type': 'accel', 'v0': 0.0, 'v1': 41.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 41.0, 'distance': 100},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 41.0, 'v1': 39.8},                      # 惰行阶段（仅受阻力影响）
     {'type': 'decel', 'v0': 39.8, 'v1': 30, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
 {'type': 'cruise', 'v0': 30.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 30.0, 'v1': 28.5},                      # 惰行阶段（仅受阻力影响）
     {'type': 'decel', 'v0': 28.5, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 160},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 38.0, 'v1': 36},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 36, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

  {'type': 'accel', 'v0': 0.0, 'v1': 27.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 27.0, 'distance': 130},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 27.0, 'v1': 25.8},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 25.8, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

      {'type': 'accel', 'v0': 0.0, 'v1': 37.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 37.0, 'distance': 100},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 37.0, 'v1': 36},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 36, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

          {'type': 'accel', 'v0': 0.0, 'v1': 32.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 32.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 32.0, 'v1': 30.5},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 30.5, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

              {'type': 'accel', 'v0': 0.0, 'v1': 32.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 32.0, 'distance': 220},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 32.0, 'v1': 31},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 31, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

 {'type': 'accel', 'v0': 0.0, 'v1': 36.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 36.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 36.0, 'v1': 35.5},                      # 惰行阶段（仅受阻力影响）
     {'type': 'decel', 'v0': 35, 'v1': 28, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
     {'type': 'cruise', 'v0': 28.0, 'distance': 100},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 28.0, 'v1': 26},                      # 惰行阶段（仅受阻力影响）
         {'type': 'accel', 'v0': 26.0, 'v1': 32.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 32.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 32.0, 'v1': 31.5},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 31.5, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

     {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 40.0, 'distance': 140},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 40.0, 'v1': 37.6},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 37.6, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

         {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 225},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 38.0, 'v1': 36},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 36, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

     {'type': 'accel', 'v0': 0.0, 'v1': 33.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 33.0, 'distance': 100},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 33.0, 'v1': 31.8},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 31.8, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 33.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 33.0, 'distance': 90},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 33.0, 'v1': 31.7},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 31.7, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
]

segments2 = [

       {'type': 'accel', 'v0': 0.0, 'v1': 52.0, 'F_max': 200000},    # 加速阶段（最大牵引力200kN）
    {'type': 'cruise', 'v0': 52.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 52.0, 'v1': 51.6},                      # 惰行阶段（仅受阻力影响）
       {'type': 'accel', 'v0': 51.6, 'v1': 53, 'F_max': 200000},
        {'type': 'cruise', 'v0': 53.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 53.0, 'v1': 52.9},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 52.9, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

        {'type': 'accel', 'v0': 0.0, 'v1': 36.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 36.0, 'distance': 40},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 36.0, 'v1': 35.4},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 35.4, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

        {'type': 'accel', 'v0': 0.0, 'v1': 46.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 46.0, 'distance': 200},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 46.0, 'v1': 45.5},                      # 惰行阶段（仅受阻力影响）
     {'type': 'decel', 'v0': 45.5, 'v1': 35, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
 {'type': 'cruise', 'v0': 35.0, 'distance': 300},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 35.0, 'v1': 35},                      # 惰行阶段（仅受阻力影响）
     {'type': 'decel', 'v0': 35, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

      {'type': 'accel', 'v0': 0.0, 'v1': 44.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 44.0, 'distance': 170},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 44.0, 'v1': 43.4},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 43.4, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

 {'type': 'accel', 'v0': 0.0, 'v1': 33.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 33.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 33.0, 'v1': 32.7},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 32.7, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

      {'type': 'accel', 'v0': 0.0, 'v1': 41.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 41.0, 'distance': 180},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 41.0, 'v1': 41},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 41, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

          {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 170},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 38.0, 'v1': 38},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 38, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

              {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 50},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 38.0, 'v1': 37.6},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 37.6, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

 {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 40.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 40.0, 'v1': 39.7},                      # 惰行阶段（仅受阻力影响）
     {'type': 'decel', 'v0': 39.7, 'v1': 36, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
     {'type': 'cruise', 'v0': 36.0, 'distance': 250},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 36.0, 'v1': 35},                      # 惰行阶段（仅受阻力影响）
         {'type': 'accel', 'v0': 35.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 140},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 38.0, 'v1': 38},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 38, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

     {'type': 'accel', 'v0': 0.0, 'v1': 50.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 50.0, 'distance': 150},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 50.0, 'v1': 49.7},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 49.7, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

         {'type': 'accel', 'v0': 0.0, 'v1': 44.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 44.0, 'distance': 125},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 44.0, 'v1': 43},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 43, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

     {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 100},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 38.0, 'v1': 37.8},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 37.8, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 210},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 38.0, 'v1': 38},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 38, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
]

segments3 = [

       {'type': 'accel', 'v0': 0.0, 'v1': 48.0, 'F_max': 200000},    # 加速阶段（最大牵引力200kN）
    {'type': 'cruise', 'v0': 48.0, 'distance': 400},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 48.0, 'v1': 48},                      # 惰行阶段（仅受阻力影响）
       {'type': 'accel', 'v0': 48, 'v1': 52, 'F_max': 200000},
        {'type': 'cruise', 'v0': 52.0, 'distance': 100},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 52.0, 'v1': 52},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 52, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

        {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 35.0, 'distance': 280},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 35.0, 'v1': 35},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 35, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

        {'type': 'accel', 'v0': 0.0, 'v1': 44.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 44.0, 'distance': 450},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 44.0, 'v1': 44},                      # 惰行阶段（仅受阻力影响）
     {'type': 'decel', 'v0': 44, 'v1': 32, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
 {'type': 'cruise', 'v0': 32.0, 'distance': 400},              # 巡航阶段（给定距离）
     {'type': 'decel', 'v0': 32, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

      {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 40.0, 'distance': 720},              # 巡航阶段（给定距离）
    {'type': 'decel', 'v0': 40, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

 {'type': 'accel', 'v0': 0.0, 'v1': 30.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 30.0, 'distance': 320},              # 巡航阶段（给定距离）
    {'type': 'decel', 'v0': 30, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

      {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 400},              # 巡航阶段（给定距离）
    {'type': 'decel', 'v0': 38, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

          {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 35.0, 'distance': 300},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 35.0, 'v1': 35},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 35, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

              {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 35.0, 'distance': 400},              # 巡航阶段（给定距离）                 # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 35, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

 {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 40.0, 'distance': 80},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 40.0, 'v1': 39.7},                      # 惰行阶段（仅受阻力影响）
     {'type': 'decel', 'v0': 39.7, 'v1': 36, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
     {'type': 'cruise', 'v0': 36.0, 'distance': 250},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 36.0, 'v1': 35},                      # 惰行阶段（仅受阻力影响）
         {'type': 'accel', 'v0': 35.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 140},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 38.0, 'v1': 38},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 38, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

     {'type': 'accel', 'v0': 0.0, 'v1': 50.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 50.0, 'distance': 150},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 50.0, 'v1': 49.7},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 49.7, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

         {'type': 'accel', 'v0': 0.0, 'v1': 44.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 44.0, 'distance': 125},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 44.0, 'v1': 43},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 43, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

     {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 100},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 38.0, 'v1': 37.8},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 37.8, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
     {'type': 'cruise', 'v0': 38.0, 'distance': 210},              # 巡航阶段（给定距离）
    {'type': 'coast', 'v0': 38.0, 'v1': 38},                      # 惰行阶段（仅受阻力影响）
    {'type': 'decel', 'v0': 38, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
]

# ================== 封装模拟函数 ==================
def simulate_train_profile(segments, dt=0.01, max_time_per_segment=500):
    """模拟列车运行曲线"""
    # 初始化总历史记录
    total_time = [0]
    total_velocity = [segments[0]['v0']]
    total_distance = [0]
    
    # 模拟每一段
    current_distance = 0
    current_time = 0
    
    for i, seg in enumerate(segments):
        print(f"\n=== 模拟第 {i+1} 段 ({seg['type']}) ===")
        
        # 初始化当前段变量
        v = seg['v0']
        l = current_distance
        t = current_time
        
        # 当前段历史记录
        segment_time = [t]
        segment_velocity = [v]
        segment_distance = [l]
        
        # 模拟循环
        while t < current_time + max_time_per_segment:
            # 计算基本阻力 (修正：乘以M*g)
            f_r = alpha * v**2 + beta * v + gamma
            
            # 计算重力分量 (坡度阻力)
            f_g = M * g * kappa
            
            # 根据阶段类型计算加速度
            if seg['type'] == 'accel':
                # 加速阶段：使用最大牵引力计算加速度
                F = seg['F_max']  # 最大牵引力 (200kN)
                # 计算实际加速度 (牛顿第二定律)
                a = (F - f_r - f_g) / M
                # 更新速度
                v_new = v + a * dt
                # 终止条件：达到目标速度
                if v_new >= seg['v1']:
                    v_new = seg['v1']
                    
            elif seg['type'] == 'cruise':
                # 巡航阶段：速度保持不变，加速度为0
                a = 0
                # 牵引力等于阻力
                F = f_r + f_g
                # 速度不变
                v_new = v
                # 终止条件：达到目标距离
                if l - current_distance >= seg['distance']:
                    break
                    
            elif seg['type'] == 'coast':
                # 惰行阶段：无牵引力，仅受阻力影响
                F = 0
                # 加速度由阻力决定
                #a = -(f_r + f_g) / M
                a = -0.1
                # 更新速度
                v_new = v + a * dt
                # 终止条件：达到目标速度
                if v_new <= seg['v1']:
                    v_new = seg['v1']
                    
            elif seg['type'] == 'decel':
                # 减速阶段：使用最大制动力计算加速度
                F = seg['F_max']  # 最大制动力 (-200kN)
                # 计算实际减速度 (牛顿第二定律)
                a = F  / M -0.1
                # 更新速度
                v_new = v + a * dt
                # 终止条件：达到目标速度
                if v_new <= seg['v1']:
                    v_new = seg['v1']
            
            # 更新距离 (使用梯形法积分)
            l_new = l + 0.5 * (v + v_new) * dt
            
            # 更新时间
            t += dt
            
            # 更新状态
            v = v_new
            l = l_new
            
            # 记录历史数据
            segment_time.append(t)
            segment_velocity.append(v)
            segment_distance.append(l)
            
            # 检查终止条件（加速、惰行、减速阶段）
            if seg['type'] in ['accel', 'coast', 'decel']:
                if (seg['type'] == 'accel' and v >= seg['v1']) or \
                   (seg['type'] == 'coast' and v <= seg['v1']) or \
                   (seg['type'] == 'decel' and v <= seg['v1']):
                    break
        
        # 更新当前状态为下一段的初始状态
        current_distance = l
        current_time = t
        
        # 将当前段数据追加到总历史记录（跳过第一个点以避免重复）
        total_time.extend(segment_time[1:])
        total_velocity.extend(segment_velocity[1:])
        total_distance.extend(segment_distance[1:])
        
        print(f"段结束: 速度={v:.2f} m/s, 距离={l:.2f} m, 时间={t:.2f} s")
    
    # 转换为numpy数组便于绘图
    distance_sim = np.array(total_distance)
    velocity_sim = np.array(total_velocity)
    
    return distance_sim, velocity_sim

# ================== 模拟多个分段曲线 ==================
# 时间步长和模拟参数
dt = 0.01   # 时间步长 (s)
max_time_per_segment = 500  # 每段最大模拟时间 (s)

# 模拟所有分段曲线
all_segments = {
    "Energy saving scheme with preference [1,0,0]": segments1,
    "Shortest driving scheme with preference [0,1,0]": segments2,
    " Comfort-focused scheme with preference [0,0,1]": segments3,
    # 可以添加更多分段曲线，例如：
    # "Profile 3": segments3,
}

# 存储所有模拟结果
simulation_results = {}

for name, segments in all_segments.items():
    print(f"\n{'='*50}")
    print(f"开始模拟: {name}")
    print(f"{'='*50}")
    
    distance_sim, velocity_sim = simulate_train_profile(segments, dt, max_time_per_segment)
    simulation_results[name] = {
        'distance': distance_sim,
        'velocity': velocity_sim
    }
    
    # 打印关键结果
    print(f"\n=== {name} 总体模拟结果 ===")
    print(f"初始速度: {velocity_sim[0]} m/s")
    print(f"最终速度: {velocity_sim[-1]:.2f} m/s")
    print(f"总行驶距离: {distance_sim[-1]:.2f} m")
    print(f"总行驶时间: {len(distance_sim)*dt:.2f} s")

# ================== 创建组合图形 ==================
plt.figure(figsize=(18, 8))

# 绘制速度限制阶梯图 (where='pre' 表示在距离点之前变化)
plt.step(distance_limit, speed_limit, where='pre', 
         color='blue', linewidth=2, 
         label='Speed Limit')

# 定义不同曲线的颜色
colors = ['red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'olive', 'cyan']

# 绘制所有模拟的速度-距离曲线
for i, (name, result) in enumerate(simulation_results.items()):
    color = colors[i % len(colors)]  # 循环使用颜色
    plt.plot(result['distance'], result['velocity'], 
             color=color, linewidth=2, 
             label=name)

# 设置坐标轴和标题
plt.title('Multi-segment Train Velocity-Distance Profiles with Speed Limits', fontsize=16)
plt.xlabel('Distance (m)', fontsize=14)
plt.ylabel('Velocity (m/s)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)

# 自动设置坐标轴范围（基于所有数据）
all_distances = distance_limit.copy()
all_speeds = speed_limit.copy()
for result in simulation_results.values():
    all_distances.extend(result['distance'])
    all_speeds.extend(result['velocity'])

plt.xlim(0, max(all_distances) + 100)
plt.ylim(0, max(all_speeds) + 5)

# 添加图例
plt.legend(loc='upper right', fontsize=12)

# 在指定位置添加标记（S1, S2等）
markers = {
    0: 'S1',
    2631: 'S2',
    3906: 'S3',
    6272: 'S4',
    8254: 'S5',
    9247: 'S6',
    10785: 'S7',
    12065: 'S8',
    13419: 'S9',
    15757:'S10',
    18022:'S11',
    20108:'S12',
    21394:'S13',
    22728:'S14',
}

# 获取当前坐标轴
ax = plt.gca()

# 获取x轴刻度标签的位置信息
first_tick_label = ax.get_xticklabels()[0]
tick_label_y = first_tick_label.get_position()[1]

# 在指定位置添加垂直参考线和标记
for pos, label in markers.items():
    # 添加垂直参考线
    plt.axvline(x=pos, color='gray', linestyle='--', alpha=0.7, linewidth=1.5)
    
    # 在x轴下方添加标记文本，与刻度标签在同一水平线上
    plt.text(pos, tick_label_y-1.5, label, 
             ha='center', va='center', 
             color='gray', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()


