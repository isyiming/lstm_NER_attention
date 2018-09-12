import sys, pickle, os, random
import numpy as np

## tags, BIO 将训练数据中的tag转为标签
tag2label = {"o": 0,
             "B-PER": 1, "I-PER": 2,"E-PER": 3,
             "B-LOC": 4, "I-LOC": 5,"E-LOC": 6,
             "B-ORG": 7, "I-ORG": 8,"E-ORG": 9
             }


def read_corpus(corpus_path):
    """
    读取语料库返回list
    read corpus and return the list of samples
    :param corpus_path:
    :return: data
    """
    data = []
    with open(corpus_path, encoding='utf-8') as fr:
        lines = fr.readlines()
    sent_, tag_, vec_ = [], [], []
    for line in lines:
        # if line != '\n':
        if len(line)>2:
            # [char, label] = line.strip().split()
            char_label_vec=line.strip().split()
            char=char_label_vec[0]
            label=char_label_vec[1]
            vector=[]
            for index in range(2,len(char_label_vec)):#去除前两个是文本和标签，后面的都是向量，不限大小，直接读到末尾
                vector.append(float(char_label_vec[index]))
            sent_.append(char)
            tag_.append(label)
            vec_.append(vector)
        else:
            data.append((sent_, tag_,vec_))
            sent_, tag_ , vec_= [], [],[]

    return data


def vocab_build(vocab_path, corpus_path, min_count):
    """
    根据训练集构建词汇表，存储
    :param vocab_path:存储的词汇表地址
    :param corpus_path:语料库
    :param min_count:
    :return:
    """
    data = read_corpus(corpus_path)
    word2id = {}
    for sent_, tag_ ,vec_ in data:
        for word in sent_:
            if word.isdigit():
                word = '<NUM>'
            elif ('\u0041' <= word <='\u005a') or ('\u0061' <= word <='\u007a'):
                word = '<ENG>'
            if word not in word2id:
                word2id[word] = [len(word2id)+1, 1]
            else:
                word2id[word][1] += 1
    low_freq_words = []
    for word, [word_id, word_freq] in word2id.items():
        if word_freq < min_count and word != '<NUM>' and word != '<ENG>':
            low_freq_words.append(word)
    for word in low_freq_words:
        del word2id[word]

    new_id = 1
    for word in word2id.keys():
        word2id[word] = new_id
        new_id += 1
    word2id['<UNK>'] = new_id
    word2id['<PAD>'] = 0

    print(len(word2id))
    with open(vocab_path, 'wb') as fw:
        pickle.dump(word2id, fw)


def sentence2id(sent, word2id):
    """
    将训练数据中的字转为id
    :param sent:
    :param word2id:
    :return:
    """
    sentence_id = []
    for word in sent:
        if word.isdigit():
            word = '<NUM>'
        elif ('\u0041' <= word <= '\u005a') or ('\u0061' <= word <= '\u007a'):
            word = '<ENG>'
        if word not in word2id:
            word = '<UNK>'
        sentence_id.append(word2id[word])
    return sentence_id


def read_dictionary(vocab_path):
    """
    读取字典
    :param vocab_path:
    :return:
    """
    vocab_path = os.path.join(vocab_path)
    with open(vocab_path, 'rb') as fr:
        word2id = pickle.load(fr)
    print('vocab_size:', len(word2id))
    return word2id


def random_embedding(vocab, embedding_dim):
    """ 
    乱序
    :param vocab:
    :param embedding_dim:
    :return:
    """
    embedding_mat = np.random.uniform(-0.25, 0.25, (len(vocab), embedding_dim))
    embedding_mat = np.float32(embedding_mat)
    return embedding_mat


def pad_sequences(sequences, pad_mark=0):
    """
    
    :param sequences:
    :param pad_mark:
    :return:
    """
    #map为将操作平均地映射到sequence中，求得len(x),取最大值
    max_len = max(map(lambda x : len(x), sequences))
    if max_len<500:
        max_len=500
    seq_list, seq_len_list = [], []
    for seq in sequences:
        seq = list(seq)
        #seq[:max_len]将原句子打出，只能打到
        seq_ = seq[:max_len] + [pad_mark] * max(max_len - len(seq), 0)
        seq_list.append(seq_)
        seq_len_list.append(min(len(seq), max_len))
    return seq_list, seq_len_list

def batch_yield(data, batch_size, vocab, tag2label, shuffle=False):
    """

    :param data:
    :param batch_size:
    :param vocab:
    :param tag2label:
    :param shuffle:
    :return:
    """
    if shuffle:
        random.shuffle(data)

    seqs, labels, vectors= [], [], []
    for (sent_, tag_, vec_) in data:

        sent_ = sentence2id(sent_, vocab)
        label_ = [tag2label[tag] for tag in tag_]
        # vector_= 
        if len(seqs) == batch_size:
            yield seqs, labels, vectors
            seqs, labels, vectors = [], [],[]
        # print(len(sent_))
        # print(len(label_))
        # print(len(vec_))
        seqs.append(sent_)
        labels.append(label_)
        vectors.append(vec_)
    if len(seqs) != 0:
        yield seqs, labels, vectors

