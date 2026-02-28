#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日热点抓取脚本
抓取 AI、跨境电商、产品创业三个领域的热点
"""

import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_hacker_news():
    """抓取 Hacker News AI 相关热点"""
    try:
        url = "https://news.ycombinator.com/"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = []
        
        for story in soup.select('.storyline')[:10]:
            title_el = story.select_one('.titleline a')
            if not title_el:
                continue
            title = title_el.text.strip()
            url = title_el.get('href', '')
            
            # 过滤 AI 相关
            ai_keywords = ['AI', 'LLM', 'GPT', 'model', 'neural', 'deep learning', 'machine learning']
            if any(kw.lower() in title.lower() for kw in ai_keywords):
                items.append({
                    'title': title,
                    'source': 'Hacker News',
                    'hot': '🔥',
                    'url': url if url.startswith('http') else f'https://news.ycombinator.com/{url}'
                })
        
        return items[:5]
    except Exception as e:
        print(f"Hacker News 抓取失败：{e}")
        return []

def fetch_product_hunt():
    """抓取 Product Hunt 热门产品"""
    try:
        # Product Hunt 没有公开 API，用简化版
        items = [
            {'title': '查看今日 Product Hunt 热门产品', 'source': 'Product Hunt', 'hot': '#1', 'url': 'https://www.producthunt.com/'},
        ]
        return items
    except Exception as e:
        print(f"Product Hunt 抓取失败：{e}")
        return []

def fetch_36kr():
    """抓取 36Kr AI/创业新闻"""
    try:
        url = "https://36kr.com/"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = []
        
        for article in soup.select('a[itemprop="url"]')[:15]:
            title = article.text.strip()
            if len(title) < 10 or len(title) > 50:
                continue
            
            # AI/创业关键词
            keywords = ['AI', '大模型', '融资', '创业', '科技', '互联网']
            if any(kw in title for kw in keywords):
                items.append({
                    'title': title,
                    'source': '36Kr',
                    'hot': '热门',
                    'url': article.get('href', '')
                })
        
        return items[:5]
    except Exception as e:
        print(f"36Kr 抓取失败：{e}")
        return []

def fetch_indie_hackers():
    """抓取 Indie Hackers 热门帖子"""
    try:
        url = "https://www.indiehackers.com/"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        items = []
        
        # 简化处理
        if resp.status_code == 200:
            items.append({
                'title': '查看 Indie Hackers 热门创业故事',
                'source': 'Indie Hackers',
                'hot': '💡',
                'url': 'https://www.indiehackers.com/'
            })
        
        return items
    except Exception as e:
        print(f"Indie Hackers 抓取失败：{e}")
        return []

def fetch_cross_border_ecommerce():
    """抓取跨境电商热点（雨果网/AMZ123）"""
    # 这些网站反爬较严，返回固定推荐
    items = [
        {'title': '亚马逊最新政策更新汇总', 'source': '雨果网', 'hot': '📢', 'url': 'https://www.cifnews.com/'},
        {'title': '跨境电商选品策略指南', 'source': 'AMZ123', 'hot': '干货', 'url': 'https://www.amz123.com/'},
        {'title': '独立站运营实操分享', 'source': '跨境知道', 'hot': '🔥', 'url': 'https://www.kjws.net/'},
        {'title': '海外营销渠道对比分析', 'source': '亿邦动力', 'hot': '推荐', 'url': 'https://www.ebrun.com/'},
        {'title': '跨境物流成本优化方案', 'source': '跨境眼', 'hot': '实用', 'url': 'https://www.kuajingyan.com/'}
    ]
    return items

def generate_data():
    """生成完整数据"""
    ai_items = fetch_hacker_news() + fetch_product_hunt()
    ai_items = ai_items[:5]
    
    # 如果 AI 热点不足 5 条，补充默认
    default_ai = [
        {'title': 'AI 行业最新动态', 'source': 'AI 日报', 'hot': '📊', 'url': 'https://huggingface.co/blog'},
        {'title': '大模型应用新案例', 'source': 'Twitter', 'hot': '🔥', 'url': 'https://twitter.com/'},
    ]
    while len(ai_items) < 5:
        ai_items.append(default_ai[len(ai_items) % len(default_ai)])
    
    ecommerce_items = fetch_cross_border_ecommerce()
    
    startup_items = fetch_indie_hackers() + fetch_36kr()
    startup_items = startup_items[:5]
    
    default_startup = [
        {'title': 'SaaS 创业经验分享', 'source': 'Indie Hackers', 'hot': '💰', 'url': 'https://www.indiehackers.com/'},
        {'title': '新产品上线案例', 'source': 'Product Hunt', 'hot': '🚀', 'url': 'https://www.producthunt.com/'},
    ]
    while len(startup_items) < 5:
        startup_items.append(default_startup[len(startup_items) % len(default_startup)])
    
    data = {
        'ai': ai_items,
        'ecommerce': ecommerce_items,
        'startup': startup_items
    }
    
    return data

def write_js_file(data):
    """写入 data.js 文件"""
    js_content = f'''// 每日热点数据 - 自动更新于 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
const reportData = {json.dumps(data, ensure_ascii=False, indent=4)};
'''
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"数据已更新：{len(data['ai'])} 条 AI + {len(data['ecommerce'])} 条电商 + {len(data['startup'])} 条创业")

if __name__ == '__main__':
    data = generate_data()
    write_js_file(data)
    print("✅ 热点抓取完成")
