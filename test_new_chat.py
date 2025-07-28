#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试创建新对话 - 不使用现有chatId
"""

from poe_api_wrapper import PoeApi
import sys

def test_new_conversation(account_name, p_b_token, p_lat_token):
    """测试创建新对话"""
    print(f"\n{'='*50}")
    print(f"🧪 测试账号: {account_name} - 创建新对话")
    print(f"{'='*50}")
    
    tokens = {
        'p-b': p_b_token,
        'p-lat': p_lat_token
    }
    
    try:
        print(f"🚀 初始化 {account_name} 的 PoeApi...")
        client = PoeApi(tokens=tokens)
        print(f"✅ {account_name} API 客户端初始化成功")
        
        # 创建新对话（不指定chatId和chatCode）
        print(f"📝 测试 {account_name} 创建新对话并发送消息...")
        bot = "ChatGPT-4o-Latest"
        message = f"你好，这是来自{account_name}的测试消息"
        
        print(f"向 {bot} 发送消息创建新对话: {message}")
        
        success = False
        response_text = ""
        chat_info = {}
        
        try:
            for chunk in client.send_message(bot=bot, message=message):
                print(f"📦 {account_name} 收到数据块: {chunk.get('response', '')[:50]}...")
                
                if chunk['response']:
                    response_text += chunk['response']
                
                # 保存对话信息
                if 'chatId' in chunk:
                    chat_info = {
                        'chatId': chunk['chatId'],
                        'chatCode': chunk['chatCode'],
                        'title': chunk.get('title', '')
                    }
                
                # 如果收到完整响应就标记成功
                if chunk.get('state') == 'complete':
                    success = True
                    print(f"✅ {account_name} 收到完整响应")
                    break
                    
        except Exception as e:
            print(f"❌ {account_name} 发送消息失败: {str(e)}")
            success = False
        
        client.disconnect_ws()
        print(f"🔌 {account_name} WebSocket 连接已断开")
        
        return {
            'account': account_name,
            'init_success': True,
            'message_success': success,
            'response': response_text[:200] + "..." if len(response_text) > 200 else response_text,
            'chat_info': chat_info,
            'error': None
        }
        
    except Exception as e:
        print(f"❌ {account_name} 测试失败: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        
        return {
            'account': account_name,
            'init_success': False,
            'message_success': False,
            'response': "",
            'chat_info': {},
            'error': str(e)
        }

def main():
    print("🆕 Poe API 新对话创建测试")
    
    # 测试账号1
    account1_result = test_new_conversation(
        "账号1", 
        "rjVTy6Cnrbh_mgNJlcncTw==", 
        "rjVTy6Cnrbh_mgNJlcncTw=="
    )
    
    # 测试账号2
    account2_result = test_new_conversation(
        "账号2", 
        "aA6YVvHUoVDmvP-9s6SFeA==", 
        "aA6YVvHUoVDmvP-9s6SFeA=="
    )
    
    # 结果总结
    print(f"\n{'='*60}")
    print("📊 测试结果总结")
    print(f"{'='*60}")
    
    results = [account1_result, account2_result]
    success_count = 0
    
    for result in results:
        print(f"\n🏷️  {result['account']}:")
        print(f"   初始化: {'✅ 成功' if result['init_success'] else '❌ 失败'}")
        print(f"   创建对话: {'✅ 成功' if result['message_success'] else '❌ 失败'}")
        
        if result['message_success']:
            success_count += 1
            print(f"   对话ID: {result['chat_info'].get('chatId', 'N/A')}")
            print(f"   对话码: {result['chat_info'].get('chatCode', 'N/A')}")
            print(f"   响应: {result['response']}")
        
        if result['error']:
            print(f"   错误: {result['error']}")
    
    print(f"\n📈 成功率: {success_count}/2 = {success_count/2*100:.0f}%")
    
    if success_count == 2:
        print("🎉 两个账号都能成功创建新对话！SendMessageMutation修复完全成功！")
        return 0
    elif success_count == 1:
        print("⚠️  只有一个账号成功，可能存在账号特定的限制")
        return 1
    else:
        print("❌ 两个账号都失败，可能还有其他问题需要解决")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 