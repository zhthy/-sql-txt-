import pymysql
import time
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties

# 指定字体，例如微软雅黑
font = FontProperties(fname=r'C:\Windows\Fonts\msyh.ttc', size=10)
matplotlib.rcParams['font.family'] = font.get_name()

def insql(v, speeds):
    db = pymysql.connect(host='数据库host', port=数据库端口, user='用户名', password='密码', db='数据库')
    cursor = db.cursor()

    with open('txt文件地址', 'r') as file:
        i = 0
        x = 0
        data_list = []
        consecutive_failures = 0  # 记录连续上传成功的次数
        while True:
            for line in file:
                data = line.strip().split('    ')
                data_list.append((data[0], data[1]))
                i += 1
                if i % v == 0:
                    try:
                        cursor.executemany("INSERT INTO wbdome(phone,uid) VALUES (%s, %s)", data_list)
                        db.commit()
                        print(f"已经上传 {i} 条，错误 {x} 条，当前速度：{v}")
                        speeds.append(v)
                        data_list = []  # 插入剩余的数据
                        consecutive_failures += 1
                        if consecutive_failures >= 3:  # 如果连续成功3次，增加速度
                            v = int(v * 2)
                            consecutive_failures = 0  # 重置连续上传成功的次数
                    except pymysql.Error as e:
                        print(f"Error while inserting data: {e}")
                        data_list = []  # 清空出错的数据，避免再次尝试插入出错的数据
                        x += v
                        consecutive_failures = 0
                        if v >10:
                            v = int(v / 2)
                        time.sleep(2)  # 等待一段时间再重试
            db.close()
            tu(v)

def tu(speeds):
    # 绘制速度变化图
    plt.plot(speeds)
    plt.xlabel('上传批次')
    plt.ylabel('上传速度')
    plt.title('sql数据上传速度变化图')
    plt.show()

if __name__ == "__main__":
    x = 10
    speeds = []
    while True:
        if x < 1:
            break
        else:
            insql(x, speeds)
