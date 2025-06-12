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

    #フォントの設定(for mac)
    #フォントは/System/Library/Fonts/に転がってます
    f_path = '/System/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc'


    #ワードクラウドを作成
    #中の詳しい引数は公式ドキュメント参照
    wordcloud = WordCloud(
        background_color = 'white',
        width = 1920, height=1080,
        font_path = f_path,
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