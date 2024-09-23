from utils.code_utils import create_repo_text
from utils.vllm_utils import *


class CodeAssistant():
    def __init__(self, model_name="qwen25_coder_7b", model_path=r"/home/yinrigao/models/qwen25_coder_7b"):
        self.tokenizer = tokenizer_initial(model_path)
        self.model_name = model_name
        self.model = model_initial(model_path)
        self.param = param_initial()

    @staticmethod
    def get_repo_str(repo_name, repo_dir):
        return create_repo_text(repo_name, repo_dir)

    def inference(self, sys_promt, user_input):
        msg = [
            {"role": "system", "content": sys_promt},
            {"role": "user", "content": user_input}
        ]
        res = model_inference(msg, self.tokenizer, self.model, self.param)
        return res

    def review_code(self, repo_str):
        review_prompt = "请根据已有的代码情况，检查代码中可能存在问题的代码，标记出来并给出修改样例。"
        res = self.inference(review_prompt, repo_str)
        return res

    def __call__(self, repo_name, repo_dir):
        repo_str = self.get_repo_str(repo_name, repo_dir)
        response = self.review_code(repo_str)
        return response


if __name__ == '__main__':
    repo_dir = "/home/yinrigao/pkgs/txt2ppt"
    repo_name = "txt2ppt"
    ca = CodeAssistant()
    res = ca(repo_name, repo_dir)
    print(res)
