import os
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path

categorys = ['fake', 'real']
def calc_ms(humanNum):
    """
    根据所给人数计算每个人fake和true连续帧的均值和方差并返回

    Parameters
    ----------
    humanNum: int

    return
    ------
    result: dict
        返回数据字典，其格式为：
        {
            fake：{
                mean：[human1, human2,...,human*] (dtype=ndarray)
                std：[human1, human2,...,human*] (dtype=ndarray)
            }
            real：{
                mean：[human1, human2,...,human*] (dtype=ndarray)
                std：[human1, human2,...,human*] (dtype=ndarray)
            }
        }

        human*数据为ndarray， 其维度为(frame_num, 3), frame_num表示帧的数量, 3表示rgb通道
    """
    result = {}
    # 根据fake还是real进行区分
    for category in categorys:
        # 获取fake和real文明夹路径
        root_path = Path.cwd() / 'face' / category
        total_mean = []
        total_std = []
        # 根据人数进行遍历
        for i in range(humanNum):
            # 获取每个人的文件夹路径
            human_path = root_path / str(i+1)
            human_mean = []
            human_std = []
            # 对该文件夹下的图片进行遍历
            for _, file in enumerate(human_path.iterdir()):
                image = np.array(Image.open(file),dtype=np.uint8) # 先图片加载并保存为ndarray
                # 计算均值方差
                human_mean.append(list(image[i].mean() for i in range(3)))
                human_std.append(list(image[i].std() for i in range(3)))
            total_mean.append(human_mean)
            total_std.append(human_std)
        # 保存为上述格式的字典
        result[category] = {'mean': np.array(total_mean, dtype=np.uint8), 'std': np.array(total_std, dtype=np.uint8)}
    return result 

def save_csv(data):
    """
    将data保存为指定格式的excel文件
    """
    result_path = Path.cwd() / 'result'
    result_path.mkdir(exist_ok=True)
    # 拆分为fake和real
    for cate_key, cate_val in data.items():
        # 拆分为mean和std
        for mathdesc_key, mathdesc_val in cate_val.items():
            # 创建writer类型保存多个sheet页
            writer = pd.ExcelWriter(result_path / (cate_key + '_' + mathdesc_key +'.xlsx'), engine='openpyxl')
            # 按照不同的人进行分页
            for human_index, human_data in enumerate(mathdesc_val):
                df = pd.DataFrame(human_data, columns=('r', 'g', 'b'))
                # 重置索引
                df.index = df.index + 1
                df.to_excel(excel_writer=writer, sheet_name=str(human_index+1), encoding='gbk')
            writer.save()
            writer.close()

if __name__ == "__main__":
    res = calc_ms(4)
    save_csv(res)