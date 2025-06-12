from wordcloud import WordCloud
import argparse
#ワードクラウドの作成

def get_args():
    parser = argparse.ArgumentParser(description='MeCab/GiNZAの解析結果を基にwordcloudを作成')
    parser.add_argument('-i',  '--file_input_path')
    parser.add_argument('-t', '--parser') 
    args = parser.parse_args()

    return args

#parseしたテキストから名詞・形容詞を取り出す
#Mecabバージョン
def extract_target_words_by_mecab(input_file):
    target_words = []
    target_pos = ('名詞', '形容詞')
    with open(input_file, 'r') as input_f:
        for line in input_f:
        
            if line != 'EOS\n':
                info = line.split('\t')
                surface = info[0]
                detail_infos = info[1].split(',')
                pos = detail_infos[0]
                
                if surface != 'ー' and pos in target_pos:
                    target_words.append(surface) 
                else:
                    pass
            else:
                pass
    target_words_str = ' '.join(target_words)
    return target_words_str

#GiNZAバージョン
def extract_target_words_by_ginza(input_file):
    target_words = []
    target_pos = ('NOUN','ADJ', 'PROPN') 

    with open(input_file, 'r') as f_input:
        for line in f_input: 
            try:
                infos = line.split(',')
                surface = infos[1]
                pos = infos[3]

                if pos in target_pos:
                    target_words.append(surface)
                else:
                    pass            
            except:
                pass

    target_words_str = ' '.join(target_words)
    return target_words_str

def make_wordcloud(text, thesis_type):

    #フォントとストップワードの設定
    #フォントは/System/Library/Fonts/に転がってます
    f_path = '/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc'

    #一般的に使われていそうな単語は除外
    #国名も除外
    stopwords = ['分析', '影響', '着目', '検討', '関連', '効果', '事例', '方法', \
                '研究', '的', '性', '要因', '者', '感', '実態', \
                'and', 'the', 'A', 'p', 'in', 'of', 'through', '利用','系', \
                '高', '間', '後', '別', '小', '中', '高', '化',  'こと', '論', \
                'at','考察', 'ため', '被', 'づくり', '児', '法', '観', 'つ', \
                '例', '会', '第', '課題', '分析', '関係', '中国', '日本', '日中', '中国人']
    custom_stopwords = set(stopwords)   

    #ワードクラウドを作成
    #中の詳しい引数は公式ドキュメント参照
    wordcloud = WordCloud(
        background_color = 'white',
        width = 1920, height=1080,
        font_path = f_path,
        stopwords = custom_stopwords,
    ).generate(text)

    #作成したワードクラウドをpng形式で保存
    wordcloud.to_file(f'word_cloud_png/word_cloud_{thesis_type}_5y_exclude_PROPN.png')

def main(args):
    input_file_name = args.file_input_path 
    parser = args.parser

    if parser == 'mecab':
        target_words = extract_target_words_by_mecab(input_file_name)
    elif parser== 'ginza':
        target_words = extract_target_words_by_ginza(input_file_name)
    else:
        assert AssertionError, 'plz put second arg; mecab or ginza' 

    make_wordcloud(target_words, args.thesis_type)

if __name__ == '__main__':
    args = get_args()
    main(args)