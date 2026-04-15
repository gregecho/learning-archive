from langchain_community.embeddings import DashScopeEmbeddings

model = DashScopeEmbeddings()

# 使用例子
vector = model.embed_query("我喜欢你")  # 生成文本的向量表示
vectors = model.embed_documents(
    ["我喜欢你", "我稀饭你", "今天天气不错"]
)  # 生成文本列表的向量表示
print(f"向量长度: {len(vector)}")
print(f"前五位数据: {vector[:5]}")
print(f"向量列表长度: {len(vectors)}")
print(f"第一个向量长度: {len(vectors[0])}")
