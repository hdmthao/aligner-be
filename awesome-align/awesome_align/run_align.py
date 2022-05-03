# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors and The HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
# Modifications copyright (C) 2020 Zi-Yi Dou
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import random
import itertools
from tqdm import trange
from typing import Union

import numpy as np
import torch
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader, IterableDataset

from awesome_align import modeling
from awesome_align.configuration_bert import BertConfig
from awesome_align.modeling import BertForMaskedLM
from awesome_align.tokenization_bert import BertTokenizer
from awesome_align.tokenization_utils import PreTrainedTokenizer
from awesome_align.modeling_utils import PreTrainedModel


def set_seed(seed):
    if seed >= 0:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

class LineByLineTextDataset(IterableDataset):
    def __init__(self, tokenizer: PreTrainedTokenizer, sentence_pairs, offsets=None):
        print('Loading the dataset...')
        self.examples = []
        self.tokenizer = tokenizer
        self.sentence_pairs = sentence_pairs
        self.offsets = offsets

    def process_line(self, worker_id, sentence_pair):
        
        sent_src, sent_tgt = sentence_pair
        token_src, token_tgt = [self.tokenizer.tokenize(word) for word in sent_src], [self.tokenizer.tokenize(word) for word in sent_tgt]
        wid_src, wid_tgt = [self.tokenizer.convert_tokens_to_ids(x) for x in token_src], [self.tokenizer.convert_tokens_to_ids(x) for x in token_tgt]

        ids_src, ids_tgt = self.tokenizer.prepare_for_model(list(itertools.chain(*wid_src)), return_tensors='pt', max_length=self.tokenizer.max_len)['input_ids'], self.tokenizer.prepare_for_model(list(itertools.chain(*wid_tgt)), return_tensors='pt', max_length=self.tokenizer.max_len)['input_ids']
        if len(ids_src[0]) == 2 or len(ids_tgt[0]) == 2:
            return None

        bpe2word_map_src = []
        for i, word_list in enumerate(token_src):
            bpe2word_map_src += [i for _ in word_list]
        bpe2word_map_tgt = []
        for i, word_list in enumerate(token_tgt):
            bpe2word_map_tgt += [i for _ in word_list]
        return (worker_id, ids_src[0], ids_tgt[0], bpe2word_map_src, bpe2word_map_tgt, sent_src, sent_tgt) 

    def __iter__(self):
        # if self.offsets is not None:
        #     worker_info = torch.utils.data.get_worker_info()
        #     worker_id = worker_info.id
        #     offset_start = self.offsets[worker_id]
        #     offset_end = self.offsets[worker_id+1] if worker_id+1 < len(self.offsets) else None
        # else:
        #     offset_start = 0
        #     offset_end = None
        #     worker_id = 0
        worker_id = 0

        for sentence_pair in self.sentence_pairs:
            processed = self.process_line(worker_id, sentence_pair)
            if processed is None:
                print(f'SentencePair "{sentence_pair[0] + " ||| " + sentence_pair[1]}" is not in the correct format. Skipping...')
                empty_tensor = torch.tensor([self.tokenizer.cls_token_id, 999, self.tokenizer.sep_token_id])
                empty_sent = ''
                yield (worker_id, empty_tensor, empty_tensor, [-1], [-1], empty_sent, empty_sent)
            else:
                yield processed
            # if offset_end is not None and offset_start + i >= offset_end:
            #     break

# def find_offsets(filename, num_workers):
#     if num_workers <= 1:
#         return None
#     with open(filename, "r", encoding="utf-8") as f:
#         size = os.fstat(f.fileno()).st_size
#         chunk_size = size // num_workers
#         offsets = [0]
#         for i in range(1, num_workers):
#             f.seek(chunk_size * i)
#             pos = f.tell()
#             while True:
#                 try:
#                     l=f.readline()
#                     break
#                 except UnicodeDecodeError:
#                     pos -= 1
#                     f.seek(pos)
#             offsets.append(f.tell())
#     return offsets

# def open_writer_list(filename, num_workers):
#     writer = open(filename, 'w+', encoding='utf-8')
#     writers = [writer]
#     if num_workers > 1:
#         writers.extend([tempfile.TemporaryFile(mode='w+', encoding='utf-8') for i in range(1, num_workers)])
#     return writers
#
# def merge_files(writers):
#     if len(writers) == 1:
#         writers[0].close()
#         return
#
#     for i, writer in enumerate(writers[1:], 1):
#         writer.seek(0)
#         shutil.copyfileobj(writer, writers[0])
#         writer.close()
#     writers[0].close()
#     return
#
#

def random_align(sentence_pairs):
    results = []

    for setence_pair in sentence_pairs:
        src_sent, tgt_sent = setence_pair
        alignments = []
        for _ in range(len(src_sent)):
            src_idx = random.randint(0, len(src_sent))
            tgt_idx = random.randint(0, len(tgt_sent))
            alignments.append(f'{src_idx}-{tgt_idx}')

        results.append(' '.join(alignments))

    return results

def word_align(model: Union[PreTrainedModel, None], tokenizer: PreTrainedTokenizer, sentence_pairs):
    if model is None:
        return random_align(sentence_pairs)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    align_layer = 8
    extraction = "softmax"
    softmax_threshold = 0.001

    def collate(examples):
        worker_ids, ids_src, ids_tgt, bpe2word_map_src, bpe2word_map_tgt, sents_src, sents_tgt = zip(*examples)
        ids_src = pad_sequence(ids_src, batch_first=True, padding_value=tokenizer.pad_token_id)
        ids_tgt = pad_sequence(ids_tgt, batch_first=True, padding_value=tokenizer.pad_token_id)
        return worker_ids, ids_src, ids_tgt, bpe2word_map_src, bpe2word_map_tgt, sents_src, sents_tgt

    # offsets = find_offsets(args.data_file, args.num_workers)
    dataset = LineByLineTextDataset(tokenizer, sentence_pairs=sentence_pairs)
    dataloader = DataLoader(
        dataset, batch_size=32, collate_fn=collate, num_workers=0
    )

    model.to(device)
    model.eval()

    results = []
    tqdm_iterator = trange(0, desc="Extracting")

    for batch in dataloader:
        with torch.no_grad():
            worker_ids, ids_src, ids_tgt, bpe2word_map_src, bpe2word_map_tgt, sents_src, sents_tgt = batch
            word_aligns_list = model.get_aligned_word(ids_src, ids_tgt, bpe2word_map_src, bpe2word_map_tgt, device, 0, 0, align_layer=align_layer, extraction=extraction, softmax_threshold=softmax_threshold, test=True, output_prob=False)
            for _, word_aligns, _, _ in zip(worker_ids, word_aligns_list, sents_src, sents_tgt):
                output_str = []
                for word_align in word_aligns:
                    if word_align[0] != -1:
                        output_str.append(f'{word_align[0]}-{word_align[1]}')
                results.append(' '.join(output_str))
            tqdm_iterator.update(len(ids_src))

    return results

if __name__ == '__main__':
    set_seed(1234)

    model_path = "../model"
    config = BertConfig.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)

    modeling.PAD_ID = tokenizer.pad_token_id
    modeling.CLS_ID = tokenizer.cls_token_id
    modeling.SEP_ID = tokenizer.sep_token_id

    model = BertForMaskedLM(config=config)

    sentence_pairs = []
    sentence_pairs.append([['My', 'name', 'is' ,'chicky'], ['toi', 'ten', 'la', 'chicky']])
    print(word_align(model, tokenizer, sentence_pairs))

