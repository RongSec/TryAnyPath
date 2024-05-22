import json
import csv
import requests
import argparse
import os
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def print_large_findany():
    findany_text = """
    \033[1;31m
    _______           _____               ________    _            
   / ____(_)___  ____/ /   |  ____  __  _/_  __/ /_  (_)___  ____ _
  / /_  / / __ \/ __  / /| | / __ \/ / / // / / __ \/ / __ \/ __ `/
 / __/ / / / / / /_/ / ___ |/ / / / /_/ // / / / / / / / / / /_/ / 
/_/   /_/_/ /_/\__,_/_/  |_/_/ /_/\__, //_/ /_/ /_/_/_/ /_/\__, /  
                                 /____/                   /____/   
    \033[0m 
            很高兴认识了你 允许我先介绍我自己
            作者：人间体佐菲
    """
    print(findany_text)


def extract_paths(json_data):
    paths = []
    for record in json_data["records"]:
        if record["id"] == "path":
            content = record["content"]
            source = record["source"]
            if not content.startswith("/"):
                content = "/" + content
            paths.append((content, source))
    return paths

def generate_csv(json_files, output_file):
    headers = ["类型", "域名", "接口", "来源", "HTTP", "HTTPS", "HTTP响应码", "HTTP长度", "HTTPS响应码", "HTTPS长度"]
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for json_file in json_files:
            with open(json_file, "r") as file:
                json_data = json.load(file)
                domain = json_data["target"].replace("http://", "").replace("https://", "")
                paths = extract_paths(json_data)

                for path in paths:
                    content, source = path
                    row = ["", domain, content, source, "", "", "", "", "", ""]
                    if "?" in content:
                        row[0] = "含参数源路径"
                    else:
                        row[0] = "不含参数源路径"
                    writer.writerow(row)

                root_paths = set([path[0].split("/")[1] for path in paths])
                for path in root_paths:
                    # 1. 当提取出的根目录为任意后缀的文件时，忽略这个结果
                    if os.path.splitext(path)[1] != '':
                        continue
                    root_row = ["根目录", domain, path, "", "", "", "", "", "", ""]
                    writer.writerow(root_row)

                    for path2 in paths:
                        content2, _ = path2
                        if content2 != path and not content2.startswith(path + "/"):
                            new_path = os.path.join(path, content2[1:])
                            # 1. 当提取出的根目录为任意后缀的文件时，忽略这个结果
                            if os.path.splitext(path)[1] != '' or os.path.splitext(content2.split("/")[0])[1] != '':
                                continue
                            # 2. 当前半部分的根目录与后半部分的两种源数据的第一级目录相同时，忽略这条拼接数据
                            if os.path.basename(path.split("/")[0]) == os.path.basename(content2.split("/")[0]):
                                continue
                            if "?" in new_path:
                                row = ["含参数拼接路径", domain, new_path, "", "", "", "", "", "", ""]
                                writer.writerow(row)
                            else:
                                row = ["不含参数拼接路径", domain, new_path, "", "", "", "", "", "", ""]
                                writer.writerow(row)

def append_http_domain(row):
    if row[4] == "":
        row[4] = "http://" + row[1] + "/" + row[2].lstrip("/")
    return row

def append_https_domain(row):
    if row[5] == "":
        row[5] = "https://" + row[1] + "/" + row[2].lstrip("/")
    return row

def process_csv(csv_file):
    rows = []
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    rows = [append_http_domain(row) for row in rows]
    rows = [append_https_domain(row) for row in rows]

    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def make_web_requests(csv_file, threads):
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    for row in rows[1:]:
        http_url = row[4]
        https_url = row[5]
        try:
            http_response = requests.get(http_url, verify=False)
            row[6] = http_response.status_code
            row[7] = len(http_response.content)
            print("HTTP请求详情：", http_url, "响应码：",http_response.status_code, "返回长度：",len(http_response.content))
        except Exception as e:
            print("HTTP请求异常：", str(e))

        try:
            https_response = requests.get(https_url, verify=False)
            row[8] = https_response.status_code
            row[9] = len(https_response.content)
            print("HTTPS请求详情：", https_url, "响应码：",https_response.status_code, "返回长度：",len(https_response.content))
        except Exception as e:
            print("HTTPS请求异常：", str(e))

    with open(csv_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def main():
    print_large_findany()
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target_dir", help="json文件目录 eg:target")
    parser.add_argument("-o", "--output_file", help="输出文件路径 eg:result/1.csv")
    args = parser.parse_args()

    json_files = [os.path.join(args.target_dir, file) for file in os.listdir(args.target_dir) if file.endswith(".json")]
    output_file = args.output_file

    if not output_file:
        output_file = "output.csv"

    generate_csv(json_files, output_file)
    print("CSV文件总行数：", sum(1 for line in open(output_file)))

    process_csv(output_file)

    while True:
        choice = input("想要继续web请求吗？ (y/n): ")
        if choice.lower() == "n":
            print("CSV写入完毕，文件路径：", os.path.abspath(output_file))
            break
        elif choice.lower() == "y":
            threads = int(input("请输入web请求的线程数： "))
            make_web_requests(output_file, threads)

if __name__ == "__main__":
    main()
