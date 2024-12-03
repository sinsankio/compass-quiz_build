from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document


def load_pages(file_path: str) -> list[Document]:
    loader = PyMuPDFLoader(file_path)
    return loader.load()


def load_requested_pages(file_path: str, requested_page_nos: list[int], na_pages: bool = False) \
        -> list[Document] | tuple:
    pages = load_pages(file_path)
    avb_pages = []
    for doc in pages:
        current_page_no = doc.metadata['page']
        if current_page_no in requested_page_nos:
            avb_pages.append(doc)
            requested_page_nos.remove(current_page_no)
    if na_pages:
        return avb_pages, requested_page_nos
    return avb_pages
