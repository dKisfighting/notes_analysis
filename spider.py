import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
import os
import re
import time
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 请求头配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Cookie': '__51uvsct__JitdmDK2c2fJCl6J=947; a1=1918cb5ece1zeyp5wff4sbt8q7xjnicn0c7o6znyd50000427058; webId=eeefd26a92fda357b54c40a842d5b4b2; gid=yjyYSDK8488YyjyYSD2dSSuIdyudvU2Eii4MWvfD9YAWCl28VI3SIK8884JW82Y8DKdiD2fq; x-user-id-creator.xiaohongshu.com=576273fb6a6a695354a9d003; customerClientId=488224448514091; web_session=0400697362ec7ba98055781304354bffcf2e7b; x-user-id-pro.xiaohongshu.com=576273fb6a6a695354a9d003; x-user-id-ad.xiaohongshu.com=576273fb6a6a695354a9d003; access-token-creator.xiaohongshu.com=customer.creator.AT-68c5174369823183461107449fprm4nz6ft80ryu; galaxy_creator_session_id=VYIL2j0AMDZz0kRVnPz0N4KhIfr73VQVcl95; galaxy.creator.beaker.session.id=1731557380782046166199; xsecappid=xhs-pc-web; acw_tc=0a00dbf117339894717607554ebe659dad5af19ac41ec360979745cfdcade5; abRequestId=eeefd26a92fda357b54c40a842d5b4b2; webBuild=4.47.1; websectiga=984412fef754c018e472127b8effd174be8a5d51061c991aadd200c69a2801d6; sec_poison_id=3e44bf82-2dc7-4a03-9bf7-b05f7073f3f3; unread={%22ub%22:%22674827730000000008006bc1%22%2C%22ue%22:%226754a1d8000000000402aace%22%2C%22uc%22:24}'  # 需要替换为实际的cookie
}

def get_note_content(url):
    """
    获取笔记内容和话题标签
    
    Args:
        url: 笔记URL
    
    Returns:
        tuple: (笔记内容, 话题标签字符串)
    """
    try:
        # 发送HTTP请求
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 获取笔记内容
        desc_elem = soup.find(id='detail-desc')
        content = desc_elem.text.strip() if desc_elem else ''
        
        # 获取话题标签
        tags_elem = soup.find(id='hash-tag')
        tags = []
        if tags_elem:
            tag_items = tags_elem.find_all('a')
            tags = [tag.text.strip() for tag in tag_items]
        
        # 如果内容仅包含话题标签,则将内容置空
        if content and all(tag in content for tag in tags) and len(''.join(tags)) >= len(content) * 0.8:
            content = ''
            
        return content, ' '.join(tags)
        
    except Exception as e:
        logger.error(f"处理URL时出错: {url}, 错��信息: {str(e)}")
        return '', ''

def main():
    # 输入输出文件路径
    input_file = r"D:\Cursor\小红书爆款笔记抓取\demo.xlsx"
    output_file = f"D:\Cursor\小红书爆款笔记抓取\结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    try:
        # 读取Excel文件
        logger.info(f"开始读取文件: {input_file}")
        df = pd.read_excel(input_file)
        
        # 检查是否存在URL列
        if df.empty or len(df.columns) == 0:
            raise ValueError("Excel文件为空或格式不正确")
            
        # 获取URL列
        url_column = df.iloc[:, 0]
        
        # 存储结果
        contents = []
        tags = []
        
        # 处理每个URL
        total = len(url_column)
        for idx, url in enumerate(url_column, 1):
            logger.info(f"正在处理第 {idx}/{total} 个URL: {url}")
            content, tag = get_note_content(url)
            contents.append(content)
            tags.append(tag)
            
            # 添加3秒延时
            if idx < total:  # 如果不是最后一个URL
                logger.info("等待3秒后继续...")
                time.sleep(3)
            
        # 添加新列
        df['笔记内容'] = contents
        df['话题标签'] = tags
        
        # 保存结果
        logger.info(f"正在保存结果到: {output_file}")
        df.to_excel(output_file, index=False)
        logger.info("处理完成!")
        
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        raise

if __name__ == "__main__":
    main() 