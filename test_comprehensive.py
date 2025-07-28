#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Poe API 综合功能测试脚本
包括：创建新对话、发送消息、获取设置等功能
"""

from poe_api_wrapper import PoeApi
import sys
import json
from datetime import datetime

class PoeAPITester:
    def __init__(self, account_name, p_b_token, p_lat_token):
        self.account_name = account_name
        self.tokens = {
            'p-b': p_b_token,
            'p-lat': p_lat_token
        }
        self.client = None
        self.test_results = {
            'account': account_name,
            'init': {'success': False, 'error': None},
            'settings': {'success': False, 'data': None, 'error': None},
            'new_chat': {'success': False, 'chat_info': {}, 'response': '', 'error': None},
            'bot_info': {'success': False, 'data': None, 'error': None}
        }

    def init_client(self):
        """初始化API客户端"""
        try:
            print(f"🚀 初始化 {self.account_name} 的 PoeApi...")
            self.client = PoeApi(tokens=self.tokens)
            self.test_results['init']['success'] = True
            print(f"✅ {self.account_name} API 客户端初始化成功")
            return True
        except Exception as e:
            self.test_results['init']['error'] = str(e)
            print(f"❌ {self.account_name} 初始化失败: {str(e)}")
            return False

    def test_get_settings(self):
        """测试获取设置信息"""
        print(f"⚙️  测试 {self.account_name} 获取设置信息...")
        try:
            settings = self.client.get_settings()
            self.test_results['settings']['success'] = True
            self.test_results['settings']['data'] = settings
            
            # 显示关键信息
            subscription = settings.get('subscription', {})
            message_info = settings.get('messagePointInfo', {})
            
            print(f"✅ {self.account_name} 设置获取成功:")
            print(f"   订阅状态: {subscription.get('isActive', 'Unknown')}")
            print(f"   订阅类型: {subscription.get('subscriptionType', 'Unknown')}")
            print(f"   消息点数: {message_info.get('messagePointBalance', 'Unknown')}")
            print(f"   每日限制: {message_info.get('messagePointLimitRemaining', 'Unknown')}")
            
            return True
        except Exception as e:
            self.test_results['settings']['error'] = str(e)
            print(f"❌ {self.account_name} 获取设置失败: {str(e)}")
            return False

    def test_bot_info(self, bot_name="ChatGPT-4o-Latest"):
        """测试获取bot信息"""
        print(f"🤖 测试 {self.account_name} 获取 {bot_name} 信息...")
        try:
            bot_info = self.client.get_botInfo(bot_name)
            self.test_results['bot_info']['success'] = True
            self.test_results['bot_info']['data'] = bot_info
            
            print(f"✅ {self.account_name} Bot信息获取成功:")
            print(f"   Bot句柄: {bot_info.get('handle', 'Unknown')}")
            print(f"   模型: {bot_info.get('model', 'Unknown')}")
            print(f"   支持文件上传: {bot_info.get('supportsFileUpload', 'Unknown')}")
            print(f"   消息价格: {bot_info.get('displayMessagePointPrice', 'Unknown')}")
            print(f"   剩余消息数: {bot_info.get('numRemainingMessages', 'Unknown')}")
            
            return True
        except Exception as e:
            self.test_results['bot_info']['error'] = str(e)
            print(f"⚠️  {self.account_name} 获取Bot信息失败: {str(e)}")
            print(f"   (这可能是正常的，将使用默认参数)")
            return False

    def test_new_conversation(self, bot_name="ChatGPT-4o-Latest"):
        """测试创建新对话"""
        print(f"💬 测试 {self.account_name} 创建新对话...")
        try:
            message = f"你好！这是来自{self.account_name}的API测试消息，请简短回复确认收到。"
            print(f"向 {bot_name} 发送: {message}")
            
            response_text = ""
            chat_info = {}
            
            for chunk in self.client.send_message(bot=bot_name, message=message):
                if chunk['response']:
                    response_text += chunk['response']
                
                # 保存对话信息
                if 'chatId' in chunk:
                    chat_info = {
                        'chatId': chunk['chatId'],
                        'chatCode': chunk['chatCode'],
                        'title': chunk.get('title', ''),
                        'msgPrice': chunk.get('msgPrice', 0)
                    }
                
                # 收到完整响应
                if chunk.get('state') == 'complete':
                    self.test_results['new_chat']['success'] = True
                    self.test_results['new_chat']['chat_info'] = chat_info
                    self.test_results['new_chat']['response'] = response_text
                    
                    print(f"✅ {self.account_name} 新对话创建成功:")
                    print(f"   对话ID: {chat_info.get('chatId', 'N/A')}")
                    print(f"   对话码: {chat_info.get('chatCode', 'N/A')}")
                    print(f"   标题: {chat_info.get('title', 'N/A')}")
                    print(f"   AI回复: {response_text[:100]}{'...' if len(response_text) > 100 else ''}")
                    
                    return True
            
            return False
            
        except Exception as e:
            self.test_results['new_chat']['error'] = str(e)
            print(f"❌ {self.account_name} 创建新对话失败: {str(e)}")
            return False

    def cleanup(self):
        """清理资源"""
        if self.client:
            try:
                self.client.disconnect_ws()
                print(f"🔌 {self.account_name} WebSocket 连接已断开")
            except:
                pass

    def run_full_test(self):
        """运行完整测试"""
        print(f"\n{'='*60}")
        print(f"🧪 开始测试账号: {self.account_name}")
        print(f"{'='*60}")
        
        # 1. 初始化
        if not self.init_client():
            return self.test_results
        
        # 2. 测试获取设置
        self.test_get_settings()
        
        # 3. 测试获取Bot信息
        self.test_bot_info()
        
        # 4. 测试创建新对话
        self.test_new_conversation()
        
        # 5. 清理
        self.cleanup()
        
        return self.test_results

def print_summary(results_list):
    """打印测试总结"""
    print(f"\n{'='*80}")
    print("📊 测试结果总结")
    print(f"{'='*80}")
    
    total_tests = len(results_list)
    success_counts = {
        'init': 0,
        'settings': 0,
        'bot_info': 0,
        'new_chat': 0
    }
    
    for result in results_list:
        print(f"\n🏷️  {result['account']}:")
        
        # 初始化
        init_status = "✅ 成功" if result['init']['success'] else "❌ 失败"
        print(f"   初始化: {init_status}")
        if result['init']['success']:
            success_counts['init'] += 1
        
        # 设置
        settings_status = "✅ 成功" if result['settings']['success'] else "❌ 失败"
        print(f"   获取设置: {settings_status}")
        if result['settings']['success']:
            success_counts['settings'] += 1
            settings_data = result['settings']['data']
            if settings_data:
                subscription = settings_data.get('subscription', {})
                print(f"      订阅状态: {subscription.get('isActive', 'Unknown')}")
        
        # Bot信息
        bot_info_status = "✅ 成功" if result['bot_info']['success'] else "⚠️  失败(可能正常)"
        print(f"   Bot信息: {bot_info_status}")
        if result['bot_info']['success']:
            success_counts['bot_info'] += 1
        
        # 新对话
        chat_status = "✅ 成功" if result['new_chat']['success'] else "❌ 失败"
        print(f"   创建对话: {chat_status}")
        if result['new_chat']['success']:
            success_counts['new_chat'] += 1
            chat_info = result['new_chat']['chat_info']
            print(f"      对话ID: {chat_info.get('chatId', 'N/A')}")
        
        # 显示错误信息
        for test_name, test_result in result.items():
            if test_name != 'account' and isinstance(test_result, dict) and test_result.get('error'):
                print(f"      {test_name}错误: {test_result['error'][:100]}...")

    # 总体统计
    print(f"\n📈 成功率统计:")
    print(f"   初始化: {success_counts['init']}/{total_tests} = {success_counts['init']/total_tests*100:.0f}%")
    print(f"   获取设置: {success_counts['settings']}/{total_tests} = {success_counts['settings']/total_tests*100:.0f}%")
    print(f"   Bot信息: {success_counts['bot_info']}/{total_tests} = {success_counts['bot_info']/total_tests*100:.0f}%")
    print(f"   创建对话: {success_counts['new_chat']}/{total_tests} = {success_counts['new_chat']/total_tests*100:.0f}%")

    # 核心功能成功率
    core_success = success_counts['new_chat']
    print(f"\n🎯 核心功能(创建对话)成功率: {core_success}/{total_tests} = {core_success/total_tests*100:.0f}%")
    
    return core_success == total_tests

def main():
    print("🔍 Poe API 综合功能测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 定义测试账号
    accounts = [
        ("账号1", "rjVTy6Cnrbh_mgNJlcncTw==", "rjVTy6Cnrbh_mgNJlcncTw=="),
        ("账号2", "aA6YVvHUoVDmvP-9s6SFeA==", "aA6YVvHUoVDmvP-9s6SFeA==")
    ]
    
    results = []
    
    # 运行测试
    for account_name, p_b, p_lat in accounts:
        tester = PoeAPITester(account_name, p_b, p_lat)
        result = tester.run_full_test()
        results.append(result)
    
    # 打印总结
    all_success = print_summary(results)
    
    if all_success:
        print("\n🎉 所有核心功能测试通过！API修复完全成功！")
        return 0
    else:
        print("\n⚠️  部分功能存在问题，但这可能是正常的")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 