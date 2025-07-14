import requests
import os
from urllib.parse import urlparse
from pathlib import Path

def setup_pixabay_api():
    # Pixabay APIキーを設定
    # https://pixabay.com/api/docs/ からAPIキーを取得してください
    PIXABAY_API_KEY = "hogehoge"
    return PIXABAY_API_KEY

def search_images(query, api_key, per_page=100):
    # Pixabay APIのエンドポイント
    url = "https://pixabay.com/api/"
    
    # パラメータの設定
    params = {
        'key': api_key,
        'q': query,
        'image_type': 'photo',
        'per_page': per_page
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching images: {e}")
        return None

def download_image(url, save_dir):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # URLからファイル名を取得
        filename = os.path.basename(urlparse(url).path)
        if not filename:
            filename = f"image_{hash(url)}.jpg"
            
        # 保存パスの作成
        save_path = Path(save_dir) / filename
        
        # 画像の保存
        with open(save_path, 'wb') as f:
            f.write(response.content)
            
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main(queries):
    # APIキーの設定
    api_key = setup_pixabay_api()
    
    # 画像の保存先ディレクトリ
    save_dir = Path('maitake_images')
    save_dir.mkdir(exist_ok=True)
    
    for query in queries:
        print(f"\nSearching for: {query}")
        # 画像の検索
        result = search_images(query, api_key)
        
        if result and 'hits' in result:
            print(f"Found {len(result['hits'])} images")
            
            # 各画像のダウンロード
            for hit in result['hits']:
                download_image(hit['largeImageURL'], save_dir)
        else:
            print(f"No results found for {query}")

if __name__ == "__main__":

    # 検索クエリを使用
    queries = ['fugafuga']
    
    main(queries)