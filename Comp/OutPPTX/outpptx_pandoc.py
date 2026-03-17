
import sys
import os
import pypandoc
# pip install pypandoc_binary
# https://js2iiu.com/2025/09/14/pandoc-powerpoint/
# https://note.com/fujisao_i/n/nb311ef035bc3

def main():
    # pandocのパスをPATHに追加
    #pandoc_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pandoc-3.9-windows-x86_64', 'pandoc-3.9')
    #os.environ["PATH"] = pandoc_dir + os.pathsep + os.environ.get("PATH", "")

    if len(sys.argv) < 2:
        print("使い方: python outpptx.py <入力ファイル>")
        sys.exit(1)
    input_file = sys.argv[1]
    pdoc_args = ['--reference-doc=template.pptx', '--verbose', '--slide-level=2']
    output_file = input_file.rsplit('.', 1)[0] + '.pptx'
    output = pypandoc.convert_file(
        input_file,
        'pptx',
        outputfile=output_file,
        extra_args=pdoc_args,
    )
    print(f"Done: {output_file}")

if __name__ == "__main__":
    main()

