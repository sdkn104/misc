from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredPDFLoader,
    MathpixPDFLoader,
    AmazonTextractPDFLoader,
)
from pprint import pprint

in_files = [
    'test.pdf',
    '04-1.pdf',
    '2021_theme137_2.pdf',
    'CorpStrategy2025.pdf',
    'generally_02.pdf',
    'nyumon6.pdf',
    'pdf_test.pdf',
    'pwhr2020_manual_ref_4_staff.pdf',
    'sdgs_miraikoshien_template-2021.pdf',
    'seiho_slides(2023)_2.pdf',
    'sinnkyouzai.pdf',
    '地方議会活性化シンポジウム.pdf',
]

for in_file in in_files:
    print(f'Processing {in_file}...')
    
    # PyPDFLoader
    print(f'  [PyPDFLoader]')
    try:
        loader = PyPDFLoader(in_file)
        documents = loader.load()
        
        with open(in_file + '.langchain.pypdf.doc', 'w', encoding='utf-8') as fout:
            for i, doc in enumerate(documents):
                fout.write(f"--- Page {i} ---\n")
                fout.write(f"Metadata: {doc.metadata}\n")
                fout.write(f"Content:\n{doc.page_content}\n\n")
        
        print(f'    Successfully processed {len(documents)} pages')
    except Exception as e:
        print(f'    Error: {e}')
    
    # UnstructuredPDFLoader
    print(f'  [UnstructuredPDFLoader]')
    try:
        loader = UnstructuredPDFLoader(in_file)
        documents = loader.load()
        
        with open(in_file + '.langchain.unstructured.doc', 'w', encoding='utf-8') as fout:
            for i, doc in enumerate(documents):
                fout.write(f"--- Document {i} ---\n")
                fout.write(f"Metadata: {doc.metadata}\n")
                fout.write(f"Content:\n{doc.page_content}\n\n")
        
        print(f'    Successfully processed {len(documents)} documents')
    except Exception as e:
        print(f'    Error: {e}')

    # UnstructuredPDFLoader (elements)
    print(f'  [UnstructuredPDFLoader]')
    try:
        loader = UnstructuredPDFLoader(in_file, mode="elements") #, infer_table_structure=True)
        documents = loader.load()
        
        with open(in_file + '.langchain.unstructured_ele.md', 'w', encoding='utf-8') as fout:
            for i, doc in enumerate(documents):
                category = doc.metadata.get("category", "")
                md_text = ""
                if category == "Title":
                    md_text = f"# {doc.page_content}\n\n"
                elif category == "ListItem":
                    md_text = f"- {doc.page_content}\n"
                elif category == "UncategorizedText":
                    md_text = f"\n{doc.page_content}\n"
                else:
                    md_text =  f"\n--- Document {i} cat={category} ---\n"
                    #md_text += f"Metadata: {doc.metadata}\n"
                    md_text += f"Content:\n{doc.page_content}\n\n"
                fout.write(md_text)
                
        print(f'    Successfully processed {len(documents)} documents')
    except Exception as e:
        print(f'    Error: {e}')

print('All files processed.')
exit()
