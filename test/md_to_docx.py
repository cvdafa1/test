#使用pypandoc进行markdown转docx
import os
import tempfile
from pathlib import Path
import pypandoc

def markdown_to_docx_file(params: any):
    success = 1
    try:
        with tempfile.NamedTemporaryFile(suffix='.docx',dir='./', delete=False) as temp_file:
                temp_path = temp_file.name
        # 模板路径（所有的公用内容均在automl/v1文件夹中）
        # 获取当前脚本所在目录
        current_script_path = os.path.dirname(os.path.abspath(__file__))
        template_file_path = os.path.join(current_script_path,"target_template.docx")
        #temp_path =  os.path.join(current_script_path,"report.docx")
        pypandoc.convert_text(
                params["mk_str"],
                'docx',
                format='md',
                outputfile= temp_path,  # 返回字节数据而不是文件
                extra_args=[f"--reference-doc={template_file_path}"]
            )
        with open(temp_path, 'rb') as f:
                docx_data = f.read()
        # 清理临时文件
        os.unlink(temp_path)
    except Exception as e:
        success = -1
        docx_data = str(e)
        if os.path.exists(temp_path):
             os.unlink(temp_path)


    with open(temp_path, 'wb') as f:
        f.write(docx_data)

    output_result  = {
        "success":success,
        "file_info":docx_data
    }
    return output_result

if __name__ == '__main__':
    print(markdown_to_docx_file({"mk_str":"""
    
    """}))




