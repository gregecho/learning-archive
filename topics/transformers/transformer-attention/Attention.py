"""
通过 Pytorch 来手工实现注意力机制。
首先需要将文本分词为词元序列，然后将每一个词元转换为对应的词嵌入。
Pytorch 提供了 torch.nn.Embedding 层来完成该操作，即构建一个从词元 ID 到词元嵌入的映射表。
This demo shows how to manually implement attention mechanism using Pytorch.
First, we need to tokenize the text into a sequence of word tokens, and then convert each word token to its corresponding word embedding.
Pytorch provides the torch.nn.Embedding layer to perform this task, which builds a mapping table from word token ID to word embedding.
"""

from torch import nn
from transformers import AutoConfig
from transformers import AutoTokenizer

model_ckpt = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)

text = "time flies like an arrow"
inputs = tokenizer(text, return_tensors="pt", add_special_tokens=False)
print(inputs.input_ids)


config = AutoConfig.from_pretrained(model_ckpt)
token_emb = nn.Embedding(config.vocab_size, config.hidden_size)
print(token_emb)

inputs_embeds = token_emb(inputs.input_ids)
print(inputs_embeds.size())
print(inputs_embeds)
print(type(inputs_embeds))
