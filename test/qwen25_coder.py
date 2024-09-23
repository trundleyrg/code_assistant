import os
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

os.environ['CUDA_VISIBLE_DEVICES'] = '1'

tokenizer = AutoTokenizer.from_pretrained('/home/yinrigao/models/qwen25_coder_7b')
sampling_params = SamplingParams(temperature=0.7, top_p=0.8, repetition_penalty=1.05, max_tokens=512)
llm = LLM(model="/home/yinrigao/models/qwen25_coder_7b")

# Prepare your prompts
prompt = "使用python实现：python pptx设置add_textbox添加的文本为有序列表。"
messages = [
    {"role": "system", "content": "根据user的需求，实现对应的代码。"},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# generate outputs
outputs = llm.generate([text], sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

"""
from :\n    
# 打开Word文档\n
    doc = Document(doc_path)\n
        \n    
        # 遍历文档中的所有段落\n    
        for para in doc.paragraphs:\n        
        # 检查段落是否是标题（H1, H2, H3 等）\n        
        if para.style.name.startsw     
        # 将标题字体设置为黑体\n            
        for run in para.runs:\n                
        run.font.bold = True\n
            \n    # 保存修改后的文档\n
                doc.save(\'modified_\' + doc_path)\n\n
                # 示例用法\ndoc_path = \'exset_heading_font_to_bold(doc_path)\n
"""
