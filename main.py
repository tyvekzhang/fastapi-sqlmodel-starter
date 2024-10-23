from fastapi import FastAPI, Response, Query, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from jinja2 import Template
import zipfile
from io import BytesIO
import os

app = FastAPI()


# 加载模板函数
def load_template(template_name):
    template_path = f"templates/{template_name}"
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found")
    with open(template_path, 'r') as f:
        template = Template(f.read())
    return template


# 渲染模板函数
def render_template(template, **context):
    return template.render(**context)


# 生成文件并打包为ZIP
def generate_and_zip(name):
    template1 = load_template('template1.txt')
    template2 = load_template('template2.txt')
    template3 = load_template('template3.txt')  # 新增的模板文件

    file1_content = render_template(template1, name=name)
    file2_content = render_template(template2, name=name)
    file3_content = render_template(template3, name=name)  # 新增的模板文件内容

    # 在内存中创建ZIP文件
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        zip_file.writestr('generated_file1.txt', file1_content)
        zip_file.writestr('generated_file2.txt', file2_content)
        zip_file.writestr('folder/generated_file3.txt', file3_content)  # 添加到文件夹中

        # 添加一个空文件夹需要使用 writestr 方法写入一个空字符串
        zip_file.writestr('folder/', '')

    # 将指针回到起始位置
    buffer.seek(0)

    return buffer


# 下载接口
@app.get("/download/{name}")
async def download(name: str):
    zip_buffer = generate_and_zip(name)
    return StreamingResponse(iter([zip_buffer.read()]),
                             media_type="application/zip",
                             headers={"Content-Disposition": f"attachment; filename={name}_files.zip"})


# 新增的预览接口
@app.get("/preview/{template_name}")
async def preview_template(
        template_name: str,
        name: str = Query(None, description="The name to render in the template")
):
    try:
        template = load_template(template_name)
        rendered_content = render_template(template, name=name if name else "")
        return PlainTextResponse(rendered_content)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))