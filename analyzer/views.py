from django.shortcuts import render
from django.views.generic import TemplateView
from collections import Counter #Python標準ライブラリの Counter を使って、リスト内の要素（単語）の頻度を簡単にカウン
import spacy
import os

#英語モデルをダウンロード
nlp = spacy.load("en_core_web_sm")

# ストップワードファイルのパス(親ディレクトリにあるtextファイルとこのファイルをつなぐ)
STOPWORDS_PATH = os.path.join(os.path.dirname(__file__), '..', 'stopwords_up_to_A1.txt')

# ストップワードを読み込む関数（再利用性の為に作成）
def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(word.strip().lower() for word in file)

# ストップワードリストをロード
custom_stopwords = load_stopwords(STOPWORDS_PATH)

def upload(request):
    # http://127.0.0.1:8000/ で表示されるページ
    return render(request, 'analyzer/upload.html')

def result(request):
    if request.method == 'POST':  # POSTリクエストの場合
        input_text = request.POST.get('name', '').strip()  # フォームデータを取得、空白を除去     
        # --- spacyを使ってストップワードを除外 ---
        doc = nlp(input_text) #入力されたテキストをトークナイズして、基本形を取得したり、ストップワードの判断を行う
        # 文字列を取得し、ストップワードとアルファベットのみで構成されてない単語を除去
        filtered_words = [token.text for token in doc 
                          if not token.is_stop and token.is_alpha and not token.is_punct #token.is_punctは記号をTrue
                          and token.text.lower() not in custom_stopwords] 
        word_count = dict(Counter(filtered_words))
        #word_countという辞書から特定のキー"items"を取り除く
        word_count = {key: value for key, value in word_count.items() if key != "items"}

        # 結果をテンプレートに渡す
        return render(request, 'analyzer/result.html', {
            'input_text': input_text,
            'word_count': word_count
        })
    else:
        # GETリクエストの場合(ユーザーがブラウザで直接/result/にアクセスした時)
        return render(request, 'analyzer/result.html', {
            'input_text': '',
            'word_count': {}
        })