import requests
import json

BASE_URL = 'https://anuneko.ai/api/v1'
DEFAULT_HEADERS = {
    'accept': '*/*',
    'content-type': 'application/json',
    'origin': 'https://anuneko.ai',
    'referer': 'https://anuneko.ai/',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'sec-fetch-site': 'same-origin',
    'x-app_id': 'com.anuttacon.neko',
    'x-client_type': '4',
}
# 可用模型列表
LIST_MODELS = {
    "1": "Orange Cat",
    "2": "Exotic Shorthair"
}

def get_credentials():
    """获取用户认证信息"""
    print("--- AnuNeko聊天 ---")
    print("请先输入您的认证信息以开始聊天。\n")
    x_token = input("请输入您的请求头 'x-token' 的值: ").strip()

    if not x_token:
        print("\n❌ 错误：认证信息不能为空！")
        return None
    
    return x_token

# 用户选择模型
def get_model_choice():
    """让用户选择聊天模型"""
    print("\n请选择您想对话的模型：")
    for key, value in LIST_MODELS.items():
        print(f"  {key}. {value}")
    
    while True:
        choice = input("请输入选项数字 (例如 1): ").strip()
        if choice in LIST_MODELS:
            return LIST_MODELS[choice]
        else:
            print("❌ 无效的选项，请重新输入。")


def create_chat_session(x_token, model):
    """创建新的聊天会话并返回 chat_id"""
    url = f'{BASE_URL}/chat'
    
    headers = DEFAULT_HEADERS.copy()
    headers['x-token'] = x_token
    
    # 传入的 model 参数
    payload = {"model": model, "is_chose_persona": True}

    print(f"\n正在使用模型 '{model}' 创建新的聊天会话...")
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() 
        data = response.json()

        chat_id = data.get('chat_id') or data.get('data', {}).get('chat_id')
        
        if chat_id:
            print(f"✅ 成功创建聊天会话，ID: {chat_id}")
            return chat_id
        else:
            print("❌ 错误：创建失败，未能从响应中获取 chat_id")
            print("服务器原始响应:", json.dumps(data, indent=2, ensure_ascii=False))
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求错误: {e}")
        if e.response is not None:
            print("错误响应内容:", e.response.text)
        return None
    except json.JSONDecodeError:
        print("❌ 错误：服务器返回的不是有效的 JSON 格式")
        print("服务器响应:", response.text)
        return None


def send_message_and_get_stream(chat_id, x_token, question):
    """向指定的 chat_id 发送消息并处理流式响应"""
    url = f'{BASE_URL}/msg/{chat_id}/stream'
    
    headers = DEFAULT_HEADERS.copy()
    headers['x-token'] = x_token

    payload = {"contents": [question]}

    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)
        response.raise_for_status()
        response.encoding = 'utf-8' # 防止中文乱码

        full_response = ""
        
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    json_str = decoded_line[6:]
                    if json_str.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(json_str)
                        if 'v' in data:
                            content = data['v']
                            print(content, end='', flush=True)
                            full_response += content
                    except json.JSONDecodeError:
                        pass
        
        print() 
        return full_response

    except requests.exceptions.RequestException as e:
        print(f"\n❌ 网络请求错误: {e}")
        if e.response is not None:
            print("错误响应内容:", e.response.text)
        return None


def main():
    """主函数，控制程序流程"""
    x_token = get_credentials()
    if not x_token:
        print("程序因缺少认证信息而退出。")
        return
        
    # 获取用户选择的模型
    model_name = get_model_choice()

    # 将 model_name 传递给 create_chat_session
    chat_id = create_chat_session(x_token, model_name)
    
    if chat_id:
        print(f"\n🚀 与模型 '{model_name}' 的聊天已准备就绪！您可以开始提问了。")
        print("输入 'exit' 或 'quit' 可随时退出程序。\n")
        
        while True:
            try:
                question = input("用户：").strip()
                
                if question.lower() in ['exit', 'quit']:
                    print("👋 主人再见喵~")
                    break
                
                if not question:
                    print("（主人好像没有输入问题喵！）")
                    continue

                print("AnuNeko：", end='')
                send_message_and_get_stream(chat_id, x_token, question)
                print() 

            except KeyboardInterrupt:
                print("\n\n👋 检测到主人强行打断了喵，主人坏坏喵！~~")
                break
    else:
        print("❌ 无法启动聊天，请检查您的网络和认证信息。")


if __name__ == "__main__":
    main()
