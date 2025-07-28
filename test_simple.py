#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简化的 Poe API 测试 - 直接发送消息
"""

from poe_api_wrapper import PoeApi
import sys

def test_direct_message():
    """直接发送消息测试，绕过bot信息获取"""
    
    tokens = {
        'p-b': 'rjVTy6Cnrbh_mgNJlcncTw==',
        'p-lat': 'rjVTy6Cnrbh_mgNJlcncTw=='
    }
    
    try:
        print("🚀 初始化 PoeApi...")
        client = PoeApi(tokens=tokens)
        print("✅ API 客户端初始化成功")
        
        # 直接使用已知的chatId发送消息，绕过bot信息获取
        print("📝 测试发送消息到现有对话...")
        
        bot = "ChatGPT-4o-Latest"
        message = "简单测试消息"
        chatId = 1220251558  # 从你的curl请求中获取的chatId
        
        print(f"向chatId {chatId} 发送消息: {message}")
        
        # 直接向已存在的对话发送消息
        for chunk in client.send_message(bot=bot, message=message, chatId=chatId):
            if chunk['response']:
                print(f"📦 收到响应: {chunk['response'][:100]}...")
                break
        
        print("✅ 消息发送测试成功！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        try:
            if 'client' in locals():
                client.disconnect_ws()
                print("🔌 WebSocket 连接已断开")
        except:
            pass

if __name__ == "__main__":
    print("=" * 50)
    print("🧪 Poe API 简化测试")
    print("=" * 50)
    
    success = test_direct_message()
    
    print("=" * 50)
    if success:
        print("🎉 测试通过！SendMessageMutation 修复成功！")
        sys.exit(0)
    else:
        print("💥 测试失败")
        sys.exit(1) 