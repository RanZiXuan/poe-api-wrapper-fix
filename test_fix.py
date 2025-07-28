#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 Poe API 修复是否有效
"""

from poe_api_wrapper import PoeApi
import sys

def test_poe_api():
    """测试 Poe API 是否工作正常"""
    
    # 使用用户提供的tokens
    tokens = {
        'p-b': 'rjVTy6Cnrbh_mgNJlcncTw==',  # URL解码后的值
        'p-lat': 'rjVTy6Cnrbh_mgNJlcncTw=='  # URL解码后的值
    }
    
    try:
        print("🚀 初始化 PoeApi...")
        client = PoeApi(tokens=tokens)
        
        print("✅ API 客户端初始化成功")
        
        # 测试发送消息
        print("📝 测试发送消息...")
        
        bot = "ChatGPT-4o-Latest"  # 使用你curl中的bot
        message = "你是什么模型。"  # 使用你curl中的消息
        
        print(f"向 {bot} 发送消息: {message}")
        
        # 发送消息并获取响应
        for chunk in client.send_message(bot=bot, message=message):
            if chunk['response']:
                print(f"📦 收到响应: {chunk['response'][:100]}...")
                break
        
        print("✅ 消息发送和接收测试成功！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
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
    print("🧪 Poe API 修复测试")
    print("=" * 50)
    
    success = test_poe_api()
    
    print("=" * 50)
    if success:
        print("🎉 所有测试通过！API 修复成功！")
        sys.exit(0)
    else:
        print("💥 测试失败，需要进一步调试")
        sys.exit(1) 