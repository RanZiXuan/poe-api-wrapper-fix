#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
对比测试两个 Poe 账号的行为
"""

from poe_api_wrapper import PoeApi
import sys
import traceback

def test_account(account_name, p_b_token, p_lat_token):
    """测试单个账号"""
    print(f"\n{'='*50}")
    print(f"🧪 测试账号: {account_name}")
    print(f"{'='*50}")
    
    tokens = {
        'p-b': p_b_token,
        'p-lat': p_lat_token
    }
    
    try:
        print(f"🚀 初始化 {account_name} 的 PoeApi...")
        client = PoeApi(tokens=tokens)
        print(f"✅ {account_name} API 客户端初始化成功")
        
        # 尝试发送消息
        print(f"📝 测试 {account_name} 发送消息...")
        bot = "ChatGPT-4o-Latest"
        message = f"测试消息 - {account_name}"
        chatId = 1220251558  # 使用原来的chatId
        
        print(f"向 {account_name} 的chatId {chatId} 发送消息: {message}")
        
        success = False
        response_text = ""
        
        try:
            for chunk in client.send_message(bot=bot, message=message, chatId=chatId):
                if chunk['response']:
                    response_text = chunk['response'][:100]
                    print(f"📦 {account_name} 收到响应: {response_text}...")
                    success = True
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
            'response': response_text,
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
            'error': str(e)
        }

def main():
    print("🔍 Poe API 双账号对比测试")
    
    # 账号1 - 工作的
    account1_result = test_account(
        "账号1(工作)", 
        "rjVTy6Cnrbh_mgNJlcncTw==", 
        "rjVTy6Cnrbh_mgNJlcncTw=="
    )
    
    # 账号2 - 新的
    account2_result = test_account(
        "账号2(新)", 
        "aA6YVvHUoVDmvP-9s6SFeA==", 
        "aA6YVvHUoVDmvP-9s6SFeA=="
    )
    
    # 对比结果
    print(f"\n{'='*60}")
    print("📊 对比结果")
    print(f"{'='*60}")
    
    results = [account1_result, account2_result]
    
    for result in results:
        print(f"\n🏷️  {result['account']}:")
        print(f"   初始化: {'✅ 成功' if result['init_success'] else '❌ 失败'}")
        print(f"   发送消息: {'✅ 成功' if result['message_success'] else '❌ 失败'}")
        if result['response']:
            print(f"   响应: {result['response']}")
        if result['error']:
            print(f"   错误: {result['error']}")
    
    # 分析差异
    print(f"\n🔍 差异分析:")
    if account1_result['init_success'] != account2_result['init_success']:
        print("❗ 初始化结果不同 - 可能是账号权限或状态差异")
    
    if account1_result['message_success'] != account2_result['message_success']:
        print("❗ 消息发送结果不同 - 可能需要特定的session或cookie")
    
    if account1_result['init_success'] and account2_result['init_success']:
        if account1_result['message_success'] and not account2_result['message_success']:
            print("💡 建议: 账号1可以发送消息但账号2不行，可能需要:")
            print("   1. 完整的Cloudflare cookie (cf_clearance, __cf_bm)")
            print("   2. 特定的账号验证状态")
            print("   3. 会话相关的其他cookie")
    
    # 总结
    all_success = all(r['init_success'] and r['message_success'] for r in results)
    if all_success:
        print("\n🎉 所有账号测试成功！API修复完全正常！")
        return 0
    else:
        print(f"\n⚠️  部分账号存在问题，需要进一步调试")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 