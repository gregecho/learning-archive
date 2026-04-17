import os
from typing import Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils.config_handler import chroma_conf
from model.factory import embed_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.path_tool import get_absolute_path
from utils.file_handler import (
    pdf_loader,
    txt_loader,
    listdir_with_allowed_type,
    get_file_md5_hex,
)
from utils.logger_handler import logger


class VectorStoreService(object):
    def __init__(self) -> None:
        self.vector_store = Chroma(
            embedding_function=embed_model,
            collection_name=chroma_conf["collection_name"],
            persist_directory=chroma_conf["persist_directory"],
        )
        self.spliter = RecursiveCharacterTextSplitter(
            separators=chroma_conf["separators"],
            chunk_size=chroma_conf["chunk_size"],
            chunk_overlap=chroma_conf["chunk_overlap"],
            length_function=len,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self):
        """从数据文件夹内读取数据文件，转为向量存到向量数据库"""

        def check_md5_hex(md5_for_check: str):
            if not os.path.exists(get_absolute_path(chroma_conf["md5_hex_store"])):
                # 创建文件
                open(
                    get_absolute_path(chroma_conf["md5_hex_store"]),
                    "w",
                    encoding="utf-8",
                ).close()
                return False  # md5 没处理过

            with open(
                get_absolute_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8"
            ) as f:
                for line in f.readlines():
                    line = line.strip()
                    if line == md5_for_check:
                        return True  # md5 处理过

                return False  # md5 没处理过

        def save_md5_hex(md5_for_check: Optional[str]):
            if not md5_hex or not isinstance(md5_hex, str):
                logger.warning(
                    f"[MD5存储] 接收到无效的 MD5 值: {type(md5_hex)}，跳过记录"
                )
                return False
            with open(
                get_absolute_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8"
            ) as f:
                f.write(f"{md5_for_check}\n")

        def get_file_documents(read_path: str):
            if read_path.endswith("txt"):
                return txt_loader(read_path)

            if read_path.endswith("pdf"):
                return pdf_loader(read_path)

            return []

        allowed_files_path: tuple[str] = listdir_with_allowed_type(
            path=get_absolute_path(chroma_conf["data_path"]),
            allowed_types=tuple(chroma_conf["allow_knowledge_file_type"]),
        )

        for path in allowed_files_path:
            # 获取文件的MD5
            md5_hex = get_file_md5_hex(path)

            if md5_hex and check_md5_hex(md5_hex):
                logger.info(f"[加载知识库]{path}内容已经存在知识库内，跳过")
                continue

            try:
                documents: list[Document] = get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}内没有有效文本内容，跳过")
                    continue

                split_document: list[Document] = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效文本内容，跳过")
                    continue

                # 将内容存入向量库
                self.vector_store.add_documents(split_document)

                # 记录这个已经处理好的文件的md5，避免下次重复加载
                save_md5_hex(md5_hex)

                logger.info(f"[加载知识库]{path} 内容加载成功")
            except Exception as e:
                # exc_info为True会记录详细的报错堆栈，如果为False仅记录报错信息本身
                logger.error(f"[加载知识库]{path}加载失败：{str(e)}", exc_info=True)
                continue


if __name__ == "__main__":
    vs = VectorStoreService()

    vs.load_document()

    retriever = vs.get_retriever()

    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-" * 20)
