import random
import matplotlib.pyplot as plt
import cv2
import os

# 文明类定义
class Civilization:
    def __init__(self, mark, attitude, isPositive, id):
        self.mark = mark
        self.attitude = attitude  # 0: 友善, 1: 中立, 2: 好斗
        self.isPositive = isPositive  # 1: 积极探索, 0: 消极保守
        self.state = 1  # 1: 存活, 0: 死亡
        self.id = id

def activeCv(cv1, cv2):
    """模拟两个文明的互动"""
    if cv1.attitude == 2 or cv2.attitude == 2:  # 如果任一方好斗，则战斗
        if cv1.mark > cv2.mark:
            delta = (cv1.mark + cv2.mark) * 0.2
            cv1.mark += delta
            cv2.mark -= delta
        else:
            delta = (cv1.mark + cv2.mark) * 0.2
            cv2.mark += delta
            cv1.mark -= delta
    elif cv1.attitude == 0 or cv2.attitude == 0:  # 友善合作
        delta = (cv1.mark + cv2.mark) * 0.1
        cv1.mark += delta
        cv2.mark += delta
    return cv1, cv2

def checkDead(cv):
    """检查文明是否灭亡"""
    if cv.mark <= 0:
        cv.state = 0
    return cv

def simulate_universe(max_frames=36000, fps=30, record_interval=60):
    """模拟宇宙演化，每2秒记录一次数据"""
    universe = [Civilization(random.randint(8000, 12000), random.randint(0, 2), random.randint(0, 1), i) for i in range(200)]
    data_frames = []

    for frame in range(max_frames):
        if sum(1 for cv in universe if cv.state == 1) <= 1:  # 只剩下一个文明
            break

        pos_cvs = [cv for cv in universe if cv.isPositive == 1 and cv.state == 1]
        for cv in pos_cvs:
            other = random.choice([c for c in universe if c != cv and c.state == 1])
            cv, other = activeCv(cv, other)
            cv = checkDead(cv)
            other = checkDead(other)

        # 每2秒（60帧）记录一次统计数据
        if frame % record_interval == 0:
            alive = sum(1 for cv in universe if cv.state == 1)
            marks = [cv.mark for cv in universe if cv.state == 1]
            data_frames.append((frame, alive, sum(marks) / len(marks) if marks else 0))

    return data_frames
    
def save_frames_to_video(data_frames, output_file="simulation.mp4", fps=30, start_index=0, keyframe_interval=10):
    """将每一帧数据绘制成图像并保存为视频（引入关键帧优化）"""
    if not os.path.exists("frames"):
        os.mkdir("frames")

    img_array = []
    for i, (frame, alive, avg_mark) in enumerate(data_frames):
        # 每隔keyframe_interval帧保存一次图像
        if i % keyframe_interval == 0:
            plt.figure(figsize=(8, 6))
            plt.title(f"Frame {frame}: Civilizations Alive = {alive}, Avg Mark = {avg_mark:.2f}")
            plt.bar(["Alive Civilizations", "Average Mark"], [alive, avg_mark], color=["blue", "green"])
            plt.savefig(f"frames/frame_{start_index + i:04d}.png")
            plt.close()
        
        # 将图片添加到视频列表
        if i % keyframe_interval == 0 or i == len(data_frames) - 1:  # 只添加关键帧
            img = cv2.imread(f"frames/frame_{start_index + i:04d}.png")
            height, width, _ = img.shape
            img_array.append(img)

    # 使用 OpenCV 将关键帧合成为视频
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for img in img_array:
        out.write(img)
    out.release()

    # 清理临时图片
    for filename in os.listdir("frames"):
        os.remove(os.path.join("frames", filename))
    os.rmdir("frames")

def manage_video_files(max_files=50):
    """管理视频文件，循环生成并删除"""
    file_index = 0
    while True:
        data_frames = simulate_universe(max_frames=36000)  # 模拟20分钟（fps=30时，36000帧）
        video_file = f"{file_index:02d}_res.mp4"
        save_frames_to_video(data_frames, output_file=video_file, fps=30, start_index=0)
        
        # 删除超出最大数量的视频文件
        if file_index >= max_files:
            old_video_file = f"{(file_index - max_files):02d}_res.mp4"
            if os.path.exists(old_video_file):
                os.remove(old_video_file)
        
        file_index += 1

# 主程序
if __name__ == "__main__":
    manage_video_files(max_files=50)  # 管理最多50个视频文件
