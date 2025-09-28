
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_whole_line1():
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

    {'type': 'accel', 'v0': 0.0, 'v1': 37.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 37.0, 'distance': 360},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 37.0, 'v1': 37},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 37, 'v1': 33, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
        {'type': 'cruise', 'v0': 33.0, 'distance': 500},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 33.0, 'v1': 33},                      # 惰行阶段（仅受阻力影响）
            {'type': 'accel', 'v0': 33.0, 'v1': 36.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 36.0, 'distance': 240},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 36.0, 'v1': 36},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 36, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

        {'type': 'accel', 'v0': 0.0, 'v1': 47, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 47, 'distance': 500},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 47, 'v1': 47},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 47, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 40.0, 'distance': 800},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 40.0, 'v1': 40},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 40, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

        {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 35.0, 'distance': 320},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 35.0, 'v1': 35},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 35, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

                {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 35.0, 'distance': 400},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 35.0, 'v1': 35},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 35, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
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
    plt.xlabel('Location (m)', fontsize=14)
    plt.ylabel('Speed (km/h)', fontsize=14)
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
    plt.legend(loc='lower right', fontsize=12)

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
        plt.text(pos, tick_label_y-3, label, 
                ha='center', va='center', 
                color='gray', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.show()



def plot_whole_line2():
    # ================== 从Excel读取速度限制数据 ==================
    try:
        # 读取Excel文件，指定没有列名
        df = pd.read_excel('D:\Study\TTO\section_data.xlsx', header=None)
        
        # 提取距离和速度数据（第一列是距离，第二列是速度）
        distance_limit = df[3].tolist()  # 第一列
        speed_limit = df[4].tolist()     # 第二列
        
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
    {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000},    # 加速阶段（最大牵引力200kN）
        {'type': 'cruise', 'v0': 35.0, 'distance': 50},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 35.0, 'v1': 34},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 34, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）


        {'type': 'accel', 'v0': 0.0, 'v1': 33.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 33.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 33.0, 'v1': 31.9},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 31.9, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
        
            {'type': 'accel', 'v0': 0.0, 'v1': 39.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 39.0, 'distance': 120},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 39.0, 'v1': 36.8},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 36.8, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

    {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 35.0, 'distance': 60},              # 巡航阶段（给定距离）  
        {'type': 'coast', 'v0': 35.0, 'v1': 34.8},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 34.8, 'v1': 30, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
         {'type': 'cruise', 'v0': 30.0, 'distance': 160},              # 巡航阶段（给定距离）
        {'type': 'accel', 'v0': 30.0, 'v1': 38.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 38.0, 'distance': 60},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 38.0, 'v1': 36.5},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 36.5, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

    {'type': 'accel', 'v0': 0.0, 'v1': 32.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 32.0, 'distance': 200},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 32.0, 'v1': 32},                      # 惰行阶段（仅受阻力影响）
            {'type': 'accel', 'v0': 32, 'v1': 38.0, 'F_max': 200000}, 
          {'type': 'cruise', 'v0': 38.0, 'distance': 200},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 38.0, 'v1': 37.7},         
        {'type': 'decel', 'v0': 37.7, 'v1': 18.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
          {'type': 'cruise', 'v0': 18.0, 'distance': 200},              # 巡航阶段（给定距离）
            {'type': 'accel', 'v0': 18, 'v1': 25.0, 'F_max': 200000}, 
              {'type': 'cruise', 'v0': 25.0, 'distance': 100},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 25.0, 'v1': 24.5},         
        {'type': 'decel', 'v0': 24.5, 'v1': 0.0, 'F_max': -200000}, 

        {'type': 'accel', 'v0': 0.0, 'v1': 34.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 34.0, 'distance': 50},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 34.0, 'v1': 33.5},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 33.5, 'v1': 20.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
          {'type': 'cruise', 'v0': 20.0, 'distance': 50},    
            {'type': 'coast', 'v0': 20.0, 'v1':19.8},               # 巡航阶段（给定距离）
            {'type': 'accel', 'v0': 19.8, 'v1': 22, 'F_max': 200000}, 
              {'type': 'cruise', 'v0': 22.0, 'distance': 50},              # 巡航阶段（给定距离）     
                {'type': 'coast', 'v0': 22.0, 'v1':21.8},   
        {'type': 'decel', 'v0': 22, 'v1': 0.0, 'F_max': -200000}, 

            {'type': 'accel', 'v0': 0.0, 'v1': 32.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 32.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 32.0, 'v1': 31.5},          
         {'type': 'decel', 'v0': 31.5, 'v1': 18.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
          {'type': 'cruise', 'v0': 18.0, 'distance': 150},                # 惰行阶段（仅受阻力影响） 
            {'type': 'accel', 'v0': 18, 'v1': 20.0, 'F_max': 200000}, 
        {'type': 'coast', 'v0': 20.0, 'v1': 19.6},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 19.6, 'v1': 0, 'F_max': -200000}, 

            {'type': 'accel', 'v0': 0.0, 'v1': 32.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 32.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 32.0, 'v1': 31.5},          
         {'type': 'decel', 'v0': 31.5, 'v1': 20.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
          {'type': 'cruise', 'v0': 20.0, 'distance': 150},                # 惰行阶段（仅受阻力影响） 
            {'type': 'accel', 'v0': 20, 'v1': 23.0, 'F_max': 200000}, 
        {'type': 'coast', 'v0': 23.0, 'v1': 22},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 22, 'v1': 0, 'F_max': -200000}, 


                {'type': 'accel', 'v0': 0.0, 'v1': 30.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 30.0, 'distance': 50},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 30.0, 'v1': 29.3},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 29.3, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

    {'type': 'accel', 'v0': 0.0, 'v1': 32.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 32.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 32.0, 'v1': 31.5},                      # 惰行阶段（仅受阻力影响）
        {'type': 'accel', 'v0': 31.5, 'v1': 35.0, 'F_max': 200000},      # 减速阶段（最大制动力200kN）
        {'type': 'cruise', 'v0': 35.0, 'distance': 100},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 35, 'v1': 35},                      # 惰行阶段（仅受阻力影响）
         {'type': 'decel', 'v0': 35, 'v1': 26, 'F_max': -200000},
        {'type': 'cruise', 'v0': 26.0, 'distance': 80},  
             {'type': 'coast', 'v0': 26, 'v1': 25.8},               # 巡航阶段（给定距离）
      {'type': 'accel', 'v0': 25.8, 'v1': 30.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 30.0, 'distance': 180},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 30.0, 'v1': 28.9},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 28.9, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 36.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 36.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 36.0, 'v1': 35},                      # 惰行阶段（仅受阻力影响）
         {'type': 'decel', 'v0': 35, 'v1': 26, 'F_max': -200000},
        {'type': 'cruise', 'v0': 26.0, 'distance': 80},  
             {'type': 'coast', 'v0': 26, 'v1': 25.8},               # 巡航阶段（给定距离）
      {'type': 'accel', 'v0': 25.8, 'v1': 33.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 33.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 33.0, 'v1': 32},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 32, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 33.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 33.0, 'distance': 225},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 33.0, 'v1': 32.3},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 32.3, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

        {'type': 'accel', 'v0': 0.0, 'v1': 37.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 37, 'distance': 100},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 37.0, 'v1': 36.2},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 36.2, 'v1': 33, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
        {'type': 'cruise', 'v0': 33.0, 'distance': 90},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 33.0, 'v1': 32.5},                      # 惰行阶段（仅受阻力影响）
          {'type': 'accel', 'v0': 32.5, 'v1': 42.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 42, 'distance': 150},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 42.0, 'v1': 41.3},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 41.3, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

    ]

    segments2 = [
    {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000},    # 加速阶段（最大牵引力200kN）
        {'type': 'cruise', 'v0': 40.0, 'distance': 50},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 40.0, 'v1': 39.8},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 39.8, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）


        {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 38.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 38.0, 'v1': 37.9},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 37.9, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
        
            {'type': 'accel', 'v0': 0.0, 'v1': 45.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 45.0, 'distance': 420},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 45.0, 'v1': 44.8},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 44.8, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

    {'type': 'accel', 'v0': 0.0, 'v1': 50.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 50.0, 'distance': 200},              # 巡航阶段（给定距离）  
        {'type': 'coast', 'v0': 50.0, 'v1': 49.9},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 49.9, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

    {'type': 'accel', 'v0': 0.0, 'v1': 50.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 50.0, 'distance': 150},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 50.0, 'v1': 49.5},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 49.5, 'v1': 0.0, 'F_max': -200000}, 

        {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 40.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 40.0, 'v1':40},                      # 惰行阶段（仅受阻力影响）     
        {'type': 'decel', 'v0': 40, 'v1': 0.0, 'F_max': -200000}, 

            {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 40.0, 'distance': 20},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 40.0, 'v1': 39.9},          
         {'type': 'decel', 'v0': 39.9, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 42.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 42.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 42.0, 'v1': 42},          
        {'type': 'decel', 'v0': 42, 'v1': 0, 'F_max': -200000}, 


                {'type': 'accel', 'v0': 0.0, 'v1': 34.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 34.0, 'distance': 20},              # 巡航阶段（给定距离）
        {'type': 'decel', 'v0': 34, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
    {'type': 'accel', 'v0': 0.0, 'v1': 42.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 42.0, 'distance': 100},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 42.0, 'v1': 42},                      # 惰行阶段（仅受阻力影响）
         {'type': 'decel', 'v0': 42, 'v1': 36.0, 'F_max': -200000},    # 减速阶段（最大制动力200kN）
        {'type': 'cruise', 'v0': 36.0, 'distance': 100},              # 巡航阶段（给定距离）
      {'type': 'accel', 'v0': 36, 'v1': 41.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 41.0, 'distance': 120},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 41.0, 'v1': 40.9},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 40.9, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 41.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 41.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 41.0, 'v1': 40},                      # 惰行阶段（仅受阻力影响）
         {'type': 'decel', 'v0': 40, 'v1': 36, 'F_max': -200000},
        {'type': 'cruise', 'v0': 36.0, 'distance': 80},  
             {'type': 'coast', 'v0':36, 'v1': 35.9},               # 巡航阶段（给定距离）
      {'type': 'accel', 'v0': 35.9, 'v1': 40.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 40.0, 'distance': 150},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 40.0, 'v1': 39.8},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 39.8, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 37.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 37.0, 'distance': 100},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 37.0, 'v1': 36.7},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 36.7, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

        {'type': 'accel', 'v0': 0.0, 'v1': 50.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 50, 'distance': 100},              # 巡航阶段（给定距离）                     # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 50, 'v1': 47, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
        {'type': 'cruise', 'v0': 47.0, 'distance': 80},              # 巡航阶段（给定距离）               
          {'type': 'accel', 'v0': 47, 'v1': 52, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 52, 'distance': 52},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 52, 'v1': 51.9},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 51.9, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

    ]
    segments3 = [
    {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000},    # 加速阶段（最大牵引力200kN）
        {'type': 'cruise', 'v0': 38, 'distance': 220},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 38, 'v1': 38},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 38, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）


        {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 35.0, 'distance': 280},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 35.0, 'v1': 35},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 35, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
        
            {'type': 'accel', 'v0': 0.0, 'v1': 42.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 42.0, 'distance': 350},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 42, 'v1': 41},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 41, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

    {'type': 'accel', 'v0': 0.0, 'v1': 46.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 46.0, 'distance': 560},              # 巡航阶段（给定距离）  
        {'type': 'decel', 'v0': 46, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

    {'type': 'accel', 'v0': 0.0, 'v1': 48.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 48.0, 'distance': 500},              # 巡航阶段（给定距离）
        {'type': 'decel', 'v0': 48, 'v1': 0.0, 'F_max': -200000}, 

        {'type': 'accel', 'v0': 0.0, 'v1': 38.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 38.0, 'distance': 50},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 38.0, 'v1': 37.8},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 37.8, 'v1': 20.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
          {'type': 'cruise', 'v0': 20.0, 'distance': 50},   
            {'type': 'accel', 'v0': 20, 'v1': 22, 'F_max': 200000}, 
              {'type': 'cruise', 'v0': 22.0, 'distance': 20},              # 巡航阶段（给定距离）        
        {'type': 'decel', 'v0': 22, 'v1': 0.0, 'F_max': -200000}, 

            {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 35.0, 'distance': 180},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 35.0, 'v1': 35},          
         {'type': 'decel', 'v0': 35, 'v1': 20.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
          {'type': 'cruise', 'v0': 20.0, 'distance': 100},                # 惰行阶段（仅受阻力影响） 
            {'type': 'accel', 'v0': 20, 'v1': 20.0, 'F_max': 200000}, 
        {'type': 'coast', 'v0': 20.0, 'v1': 19.9},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 19.9, 'v1': 0, 'F_max': -200000}, 

            {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 35.0, 'distance': 80},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 35.0, 'v1': 34.5},          
         {'type': 'decel', 'v0': 34.5, 'v1': 20.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
          {'type': 'cruise', 'v0': 20.0, 'distance': 50},                # 惰行阶段（仅受阻力影响） 
            {'type': 'accel', 'v0': 20, 'v1': 23.0, 'F_max': 200000}, 
        {'type': 'coast', 'v0': 23.0, 'v1': 22.2},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 22.2, 'v1': 0, 'F_max': -200000}, 


                {'type': 'accel', 'v0': 0.0, 'v1': 31.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 31.0, 'distance': 100},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 31.0, 'v1': 31},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 31, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

    {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 40.0, 'distance': 200},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 40.0, 'v1': 39.9},    
        {'type': 'decel', 'v0': 39.9, 'v1': 34, 'F_max': -200000},    
         {'type': 'cruise', 'v0': 34.0, 'distance': 100},                # 惰行阶段（仅受阻力影响）
        {'type': 'accel', 'v0': 34, 'v1': 36.0, 'F_max': 200000},      # 减速阶段（最大制动力200kN）
     {'type': 'cruise', 'v0': 36.0, 'distance': 360},              # 巡航阶段（给定距离）
        {'type': 'decel', 'v0': 36, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 40.0, 'distance': 280},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 40.0, 'v1': 39.6},                      # 惰行阶段（仅受阻力影响）
         {'type': 'decel', 'v0': 39.6, 'v1': 30, 'F_max': -200000},
        {'type': 'cruise', 'v0': 30, 'distance': 120},             # 巡航阶段（给定距离）
      {'type': 'accel', 'v0': 30, 'v1': 35.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 35.0, 'distance': 280},              # 巡航阶段（给定距离）             
        {'type': 'decel', 'v0': 35, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

            {'type': 'accel', 'v0': 0.0, 'v1': 35.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0':35.0, 'distance': 325},              # 巡航阶段（给定距离）
        {'type': 'decel', 'v0': 35, 'v1': 0.0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

        {'type': 'accel', 'v0': 0.0, 'v1': 40.0, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 40, 'distance': 200},              # 巡航阶段（给定距离）
        {'type': 'coast', 'v0': 40.0, 'v1': 39.7},                      # 惰行阶段（仅受阻力影响）
        {'type': 'decel', 'v0': 39.7, 'v1': 29, 'F_max': -200000},      # 减速阶段（最大制动力200kN）
        {'type': 'cruise', 'v0': 29, 'distance': 190},              # 巡航阶段（给定距离）
          {'type': 'accel', 'v0': 29, 'v1': 35, 'F_max': 200000}, 
        {'type': 'cruise', 'v0': 35, 'distance': 600},              # 巡航阶段（给定距离）
        {'type': 'decel', 'v0': 35, 'v1': 0, 'F_max': -200000},      # 减速阶段（最大制动力200kN）

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
    plt.xlabel('Location (m)', fontsize=14)
    plt.ylabel('Speed (km/h)', fontsize=14)
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
    plt.legend(loc='lower right', fontsize=12)

    # 在指定位置添加标记（S1, S2等）
    markers = {
        0: 'S1',
        1334: 'S2',
        2620: 'S3',
        4706: 'S4',
        6971: 'S5',
        9309: 'S6',
        10663: 'S7',
        11943: 'S8',
        13481: 'S9',
        14374:'S10',
        16456:'S11',
        18822:'S12',
        20097:'S13',
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
        plt.text(pos, tick_label_y-3, label, 
                ha='center', va='center', 
                color='gray', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def plot_multiple_trains():
    # 车站位置信息（距离，米）
    station_positions = {
        'S1': 0,
        'S2': 1334,
        'S3': 2620,
        'S4': 4706,
        'S5': 6971,
        'S6': 9309,
        'S7': 10663,
        'S8': 11943,
        'S9': 13481,
        'S10': 14374,
        'S11': 16456,
        'S12': 18822,
        'S13': 20097,
        'S14': 22728
    }
    
    # 车站名称列表（按距离排序）
    station_names = list(station_positions.keys())
    station_distances = list(station_positions.values())
    
    # Schedule1: 节能方案的时刻表
    schedule1 = {
        'S1': {'arrival': '00:00:00', 'departure': '00:00:40'},
        'S2': {'arrival': '00:01:30', 'departure': '00:02:10'},
        'S3': {'arrival': '00:03:00', 'departure': '00:03:40'},
        'S4': {'arrival': '00:04:45', 'departure': '00:05:25'},
        'S5': {'arrival': '00:07:00', 'departure': '00:07:40'},
        'S6': {'arrival': '00:09:15', 'departure': '00:09:55'},
        'S7': {'arrival': '00:10:30', 'departure': '00:11:10'},
        'S8': {'arrival': '00:12:00', 'departure': '00:12:40'},
        'S9': {'arrival': '00:13:45', 'departure': '00:14:25'},
        'S10': {'arrival': '00:15:00', 'departure': '00:15:40'},
        'S11': {'arrival': '00:17:30', 'departure': '00:18:10'},
        'S12': {'arrival': '00:20:15', 'departure': '00:20:55'},
        'S13': {'arrival': '00:22:00', 'departure': '00:22:40'},
        'S14': {'arrival': '00:24:30', 'departure': 'N/A'}
    }
    
    # 将时间字符串转换为秒数
    def time_to_seconds(time_str):
        if time_str == 'N/A':
            return None
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    
    # 将秒数转换为时间字符串
    def seconds_to_time(seconds):
        if seconds is None:
            return 'N/A'
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f'{h:02d}:{m:02d}:{s:02d}'
    
    # 计算列车数量（4577秒内，间隔180秒发车）
    departure_time_range = 4577  # 发车时间范围（秒）
    headway = 180                 # 发车间隔（秒）
    num_trains = departure_time_range // headway + 1  # 列车数量
    
    # 计算第一班列车从S1到S14的总行程时间（秒）
    first_train_total_time = time_to_seconds(schedule1['S14']['arrival'])  # 24分30秒 = 1470秒
    
    # 计算最后一班列车到达S14的时间
    last_train_departure = (num_trains - 1) * headway
    last_train_arrival = last_train_departure + first_train_total_time
    
    # 设置图形时间范围（从0到最后一班列车到达S14的时间）
    plot_time_range = last_train_arrival
    
    # 创建图形
    plt.figure(figsize=(18, 12))
    
    # 绘制车站位置参考线
    for station, distance in station_positions.items():
        plt.axhline(y=distance, color='lightgray', linestyle='--', alpha=0.7)

    
    # 为每列列车绘制运行轨迹
    for train_id in range(num_trains):
        # 计算当前列车的发车时间（秒）
        departure_time = train_id * headway
        
        # 为当前列车创建偏移后的时刻表
        current_schedule = {}
        for station, times in schedule1.items():
            arrival_sec = time_to_seconds(times['arrival'])
            departure_sec = time_to_seconds(times['departure'])
            
            # 应用时间偏移（相对于第一班列车）
            if arrival_sec is not None:
                arrival_sec += departure_time
            if departure_sec is not None:
                departure_sec += departure_time
                
            current_schedule[station] = {
                'arrival': seconds_to_time(arrival_sec),
                'departure': seconds_to_time(departure_sec),
                'arrival_sec': arrival_sec,
                'departure_sec': departure_sec
            }
        
        # 绘制当前列车的运行轨迹（所有车站）
        for i in range(len(station_names)):
            station = station_names[i]
            
            # 获取当前车站的到达和出发时间（秒）
            arrival_sec = current_schedule[station]['arrival_sec']
            departure_sec = current_schedule[station]['departure_sec']
            
            # 绘制停站时间（水平线）
            # 修改：S1车站不绘制停站时间
            if departure_sec is not None and station != 'S1':
                plt.plot([arrival_sec, departure_sec], 
                        [station_positions[station], station_positions[station]], 
                        'b-', linewidth=2, alpha=0.7)
            
            # 绘制到下一个车站的运行轨迹（斜线）
            if i < len(station_names) - 1:
                next_station = station_names[i+1]
                next_arrival_sec = current_schedule[next_station]['arrival_sec']
                
                if departure_sec is not None and next_arrival_sec is not None:
                    plt.plot([departure_sec, next_arrival_sec], 
                            [station_positions[station], station_positions[next_station]], 
                            'b-', linewidth=1.5, alpha=0.6)
    
    # 设置坐标轴
    plt.xlabel('Time (seconds)', fontsize=14)
    plt.ylabel('Station', fontsize=14)
    plt.title(f'Multiple Trains Schedule - Energy Saving Scheme\n'
              f'Headway: {headway}s, Departure Range: 0-{departure_time_range}s, '
              f'Last Train Arrival: {last_train_arrival}s', 
              fontsize=16, fontweight='bold')
    
    # 设置y轴范围和刻度
    plt.ylim(-1000, max(station_distances))
    plt.yticks(station_distances, station_names, fontsize=12)
    
    # 设置x轴范围（0到最后一班列车到达S14的时间）
    plt.xlim(0, plot_time_range)
    
    # 添加网格
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # 横轴间隔为1000秒
    x_ticks = np.arange(0, plot_time_range + 1, 1000)  # 每1000秒一个刻度
    plt.xticks(x_ticks, [f'{t}s' for t in x_ticks], rotation=45)


    
    # 调整布局
    plt.tight_layout()
    plt.show()


# 运行函数绘制多列列车时刻表
plot_multiple_trains()






# 运行函数生成时刻表
#generate_train_timetable()



#plot_whole_line1()
#plot_whole_line2()
#procedure_data()