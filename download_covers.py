import pandas as pd
import requests
import os
import logging
import time
import uuid
from datetime import datetime
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_folder(folder_path):
    """
    创建文件夹
    
    Args:
        folder_path: 文件夹路径
    """
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logger.info(f"创建文件夹: {folder_path}")
    except Exception as e:
        logger.error(f"创建文件夹失败: {str(e)}")
        raise

def get_file_extension(url):
    """
    从URL中获取文件扩展名
    
    Args:
        url: 图片URL
        
    Returns:
        str: 文件扩展名
    """
    parsed = urlparse(url)
    path = parsed.path
    return os.path.splitext(path)[1] or '.jpg'  # 默认使用.jpg

def download_image(url, save_path):
    """
    下载图片
    
    Args:
        url: 图片URL
        save_path: 保存路径
        
    Returns:
        bool: 是否下载成功
    """
    try:
        # 发送HTTP请求
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # 保存图片
        with open(save_path, 'wb') as f:
            f.write(response.content)
            
        return True
        
    except Exception as e:
        logger.error(f"下载图片失败 {url}: {str(e)}")
        return False

def main():
    # 配置路径
    input_file = r"D:\Cursor\小红书爆款笔记抓取\结果_20241212_155052.xlsx"
    output_folder = r"D:\Cursor\小红书爆款笔记抓取\封面图片"
    
    try:
        # 创建保存文件夹
        create_folder(output_folder)
        
        # 读取Excel文件
        logger.info(f"正在读取文件: {input_file}")
        df = pd.read_excel(input_file)
        
        # 检查必要的列是否存在
        required_columns = ['粉丝数', '互动量', '封面地址']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Excel文件中未找到'{col}'列")
        
        # 筛选符合条件的数据
        filtered_df = df[
            (df['粉丝数'] < 1000) & 
            (df['互动量'] > 100)
        ]
        
        if filtered_df.empty:
            logger.info("没有找到符合条件的数据")
            return
            
        logger.info(f"找到 {len(filtered_df)} 条符合条件的数据")
        
        # 下载图片
        success_count = 0
        for idx, row in filtered_df.iterrows():
            url = row['封面地址']
            if pd.isna(url):
                continue
                
            # 生成唯一文件名
            extension = get_file_extension(url)
            filename = f"cover_{uuid.uuid4().hex[:8]}{extension}"
            save_path = os.path.join(output_folder, filename)
            
            logger.info(f"正在下载第 {success_count + 1}/{len(filtered_df)} 张图片: {url}")
            
            if download_image(url, save_path):
                success_count += 1
                
            # 添加延时
            time.sleep(1)
        
        logger.info(f"下载完成! 成功: {success_count}, 失败: {len(filtered_df) - success_count}")
        
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        raise

if __name__ == "__main__":
    main() 