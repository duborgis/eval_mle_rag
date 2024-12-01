import requests
from bs4 import BeautifulSoup
import os

def extract_content_from_webpage(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        text = ' '.join([p.get_text(strip=True) for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
        
        images = []
        for img in soup.find_all('img'):
            img_url = img.get('src')
            if img_url:
                images.append(img_url)
        
        return {
            'text': text,
            'images': images
        }
    
    except Exception as e:
        print(f"Erro ao extrair conteúdo: {str(e)}")
        return None

def download_images(images, output_dir):
    """
    Faz o download das imagens encontradas
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    downloaded_images = []
    for i, img_url in enumerate(images):
        try:
            print(f"Baixando imagem {img_url}")
            response = requests.get(img_url)
            if response.status_code == 200:
                file_name = f"image_{i}.jpg"
                file_path = os.path.join(output_dir, file_name)
                
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                downloaded_images.append(file_path)
        
        except Exception as e:
            print(f"Erro ao baixar imagem {img_url}: {str(e)}")
    
    return downloaded_images

# Exemplo de uso
if __name__ == "__main__":
    url = "https://hotmart.com/pt-br/blog/como-funciona-hotmart"
    output_dir = "out"
    
    content = extract_content_from_webpage(url)
    
    if content:
        print("Texto extraído:")
        print(content['text'])
        with open(f'{output_dir}/output.txt', 'w') as f:
            f.write(content['text'])
        
        print("\nBaixando imagens...")
        downloaded_images = download_images(content['images'], output_dir)
        print(f"Imagens baixadas: {len(downloaded_images)}")

