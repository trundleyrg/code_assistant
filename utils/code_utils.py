"""
组装项目代码库为text
"""
import os


def create_repo_file(file_path, repo_dir):
    file_txt = f"""<|file_sep|>{os.path.relpath(file_path, repo_dir)}\n"""
    file_txt += open(file_path, 'r', encoding='utf-8').read()
    file_txt += "\n"
    return file_txt


def create_repo_text(repo_name, repo_dir):
    res = f'''<|repo_name|>{repo_name}\n'''
    file_list = []
    for root, dirs, path in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d not in ("debug", "logs", "test")]
        for p in path:
            _, ext = os.path.splitext(p)
            if ext in ('.py', ".md", ".sh"):
                res += create_repo_file(os.path.join(root, p), repo_dir)
                file_list.append(p)
    return res


if __name__ == '__main__':
    repo_dir = "/home/yinrigao/pkgs/txt2ppt"
    repo_name = "txt2ppt"
    repo_str = create_repo_text(repo_name, repo_dir)
