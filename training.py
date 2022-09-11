
import os
from glob import glob
import re
import pickle
import numpy as np
import argparse


class TrainModel():
    def __init__(self) -> None:
        
        self.fileseparator = '||||||'
        self.n = 2
        self.encoding = 'utf-8'

    

    def _fill_input(self,input_dir) -> str:
        '''fills data with file content or user's stdin'''
        if input_dir == None:
            pass
        else:
            assert os.DirEntry.is_dir(input_dir), "Invalid value for argument 'input_dir'. Please, specify correct directory path"
            file_list = self._read_files_in_dir(self.input_dir)
            




    def _read_files_in_dir(self, input_dir) -> str:
        '''reads files in specified dir'''
        starred_path = os.path.join(input_dir,'**')
        file_list = glob(starred_path,recursive=True)
        output_file_list = []
        for filepath in file_list:
            if os.path.isfile(filepath):
                output_file_list.append(filepath)
        return output_file_list

    def _generate_filenames(self,input_dir):
        '''reads all files from folder recursively'''
        for folder_path, folder_names, file_names in os.walk(input_dir):
            for file_name in file_names:
                yield open(os.path.join(folder_path, file_name), encoding = self.encoding)

    def _get_file_rows(self,files)->str:
        '''lazy method to read file line by line and get normalized row'''
        for fileobject in files:
            
            line = fileobject.readline()
            while line:
                if line == self.fileseparator:
                    continue
                else:
                    yield re.sub(r'[^а-яa-zÀ-ÿ. ]','',line.lower().strip())
                line = fileobject.readline()
                
            yield self.fileseparator

    def _tokenize(self,lines)->str:
        '''splits lines to words'''
        for line in lines:
            for word in line.split(' '):
                yield word.strip()
    

    def _generate_key_value(self,words):
        n = self.n
        i = 0
        container = []
        for word in words:
            if word == '':
                continue
            elif word == self.fileseparator:
                i = 0
                container = []
            else:
                i +=1
                if i <= n:
                    container.append(word)
                else:
                    yield ( ' '.join(container) , word )
                    container = container[1:] + [word]

    def _lazy_reader(self, filepath = None):
        tokenized_words = []
        n = self.n
        tokenized_content = {}
        if filepath == None:
            filelines = self._lazy_words_from_input()
        else:
            filenames = self._generate_filenames(filepath)
            filelines = self._get_file_rows(filenames)
        words = self._tokenize(filelines)
        tuples = self._generate_key_value(words)
        for tpl in tuples:
            tpl_key = tpl[0]
            tpl_value = tpl[1]
            if tpl_key in tokenized_content.keys():
                if tpl_value in tokenized_content[tpl_key]:
                    continue
                else:
                    tokenized_content[tpl_key].append(tpl_value)
            else:
                tokenized_content.update({tpl_key:[tpl_value]})
            tokenized_words.append(tpl_value)
        return {'tokenized_content': tokenized_content, 'tokenized_words': tokenized_words}


    def _fit(self,model,input_dir = None):
        tokenized_content = self._lazy_reader(input_dir)
        with open(model,'wb') as pkl_file:
            pickle.dump(
                tokenized_content,
                pkl_file
                )

    def _generate_stdio(self,content:str):
        pass

    def fit(self, input_dir, model):
        self._fit(input_dir, model)

    def _load_pickle(self, model):
        with open(model,'rb') as pkl_file:
            tokenized_content = pickle.load(pkl_file)
        return tokenized_content
    
    def generator(self, length, start_sequence, model) -> str:
        tokenized_dict = self._load_pickle(model)
        tokenized_words = tokenized_dict['tokenized_words']
        tokenized_content = tokenized_dict['tokenized_content']
        if start_sequence == None:
            i=np.random.choice(len(tokenized_words)-self.n)
            curr_sequence = tokenized_words[i:i+self.n]
        else:
            curr_sequence = start_sequence.split(' ')
            
                
        output = curr_sequence
        curr_sequence_str = ' '.join(curr_sequence[-self.n:])
        if curr_sequence_str not in tokenized_content.keys():
            return 'По введенной последовательности не может быть ничего сгенерировано'
        for i in range(length-1):
            possible_words = tokenized_content[curr_sequence_str]
            next_word = possible_words[np.random.choice(len(possible_words))]
            output += [next_word]
            curr_sequence_str = ' '.join(output[-self.n:])
        output_str = ' '.join(output)
        return output_str

    def _lazy_words_from_input(self):
        print("Введите текст для обучения. Чтобы сохранить строку нажмите Enter после ввода. Для выхода из режима нажмите Enter повторно и подтвердите выход")
        while True:
            
            line = input()
            if line == '':
                print("Закончить вывод текста Y/N (по умолчанию [N])")
                inp = input()
                if inp.capitalize() == 'Y':
                    break
                else:
                    pass
            else:
                yield line.strip()
            
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='training model')
    parser.add_argument('--input-dir',type=str)
    parser.add_argument('--model',type=str)
    args = parser.parse_args()
    input_dir = args.input_dir
    model = args.model
    train_model = TrainModel()
    train_model.fit(model,input_dir)






## закомментить код

        