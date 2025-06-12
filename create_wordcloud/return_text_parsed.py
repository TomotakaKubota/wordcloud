import MeCab
import argparse
import os 
import spacy

def get_args():
    parser = argparse.ArgumentParser(description='Mecab/GiNZAで文書に形態素解析して保存する')
    parser.add_argument('-i', '--file_input_path', required=True)
    parser.add_argument('-o', '--file_output_path', required=True)
    parser.add_argument('-p', '--parser')
    args = parser.parse_args()

    return args

def parse_and_save_by_mecab(target_file, parsed_file):
    #利用した辞書はIPA
    tagger = MeCab.Tagger()
    with open(target_file, 'r') as f_input, open(parsed_file, 'w') as f_output:
        for line in f_input:
            parse_result = tagger.parse(line)
            f_output.write(parse_result)

    return parsed_file

def parse_and_save_by_ginza(target_file, parsed_file):
    tagger = spacy.load('ja_ginza')

    with open(target_file, 'r') as f_input, open(parsed_file, 'w') as f_output:
        for line in f_input:
            parsed_result = tagger(line)
            for token in parsed_result:
                result_info  = f"{str(token.i)},{token.text},{token.lemma_},{token.pos_},{token.tag_}\n"
                f_output.write(result_info)

def main(args):
    input_file = args.file_input_path
    file_output_path = os.path.join(args.file_output_path, 'parsed_test.txt')
    parser = args.parser
    
    if parser == 'mecab':
        parse_and_save_by_mecab(input_file, file_output_path)
    elif parser == 'ginza':
        parse_and_save_by_ginza(input_file, file_output_path)

if __name__ == "__main__":
    args= get_args()
    main(args)



