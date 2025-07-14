import requests
import json
import time
from pathlib import Path
import urllib.parse
import urllib.request
from fake_useragent import UserAgent

def search_images(keywords, max_results=100):
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }
    
    # DuckDuckGo検索のためのパラメータ
    params = {
        'q': keywords,
        'iax': 'images',
        'ia': 'images'
    }
    
    search_url = f"https://duckduckgo.com/?{urllib.parse.urlencode(params)}"
    
    # VQD値を取得
    res = requests.get(search_url, headers=headers)
    vqd = res.text.split('vqd=\'')[1].split('\'')[0]
    
    # 画像検索API用のURL
    api_url = "https://duckduckgo.com/i.js"
    images = []
    current = 0
    
    while current < max_results:
        params = {
            'l': 'jp-jp',
            'o': 'json',
            'q': keywords,
            'vqd': vqd,
            's': current,
            'p': '1',
            'v7exp': 'a'
        }
        
        try:
            res = requests.get(api_url, headers=headers, params=params)
            data = res.json()
            
            if 'results' not in data:
                break
                
            images.extend(data['results'])
            
            if not data.get('next'):
                break
                
            current = len(images)
            time.sleep(0.5)  # APIへの負荷を抑えるため
            
        except Exception as e:
            print(f"Error during search: {e}")
            break
    
    return images[:max_results]

def download_image(url, save_dir):
    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            image_data = response.read()
            
        # URLからファイル名を生成
        filename = f"image_{hash(url)}.jpg"
        save_path = Path(save_dir) / filename
        
        with open(save_path, 'wb') as f:
            f.write(image_data)
            
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main(queries, max_results=100):
    save_dir = Path('maitake_images')
    save_dir.mkdir(exist_ok=True)
    
    for query in queries:
        print(f"\nSearching for: {query}")
        images = search_images(query, max_results)
        
        print(f"Found {len(images)} images")
        for img in images:
            if 'image' in img:
                download_image(img['image'], save_dir)
            time.sleep(0.2)  # ダウンロード間隔を設定

if __name__ == "__main__":
    queries = ['hogehoge', 'fugafuga']
    main(queries)