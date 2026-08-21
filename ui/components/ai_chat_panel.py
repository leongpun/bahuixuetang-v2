"""
AI答疑面板 - 聊天式答疑界面
"""
import customtkinter as ctk
import tkinter as tk
from pathlib import Path
import threading
from typing import Optional


class AIChatPanel(ctk.CTkFrame):
    """AI答疑面板"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # 导入AI服务
        self.ai_service = None
        self._loading_widgets = {}
        try:
            from core.api.ai_service import AIService
            self.ai_service = AIService()
            print(f"AI服务初始化成功, api_key={bool(self.ai_service.api_key)}")
        except Exception as e:
            print(f"AI服务初始化失败: {e}")
        
        # 聊天历史
        self.chat_history = []
        
        # 构建UI
        self._build_ui()
    
    def _build_ui(self):
        """构建UI"""
        # 主框架
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # 标题栏
        title_frame = ctk.CTkFrame(main_frame, fg_color="#f8f9fa", height=50)
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            title_frame,
            text="🤖 AI答疑助手",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2c3e50"
        ).pack(side="left", padx=15, pady=10)
        
        ctk.CTkLabel(
            title_frame,
            text="✅ 已连接",
            font=ctk.CTkFont(size=11),
            text_color="#27ae60"
        ).pack(side="right", padx=15, pady=10)
        
        # 聊天消息区域
        chat_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        chat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 消息滚动区域
        self.messages_frame = ctk.CTkScrollableFrame(chat_frame, fg_color="transparent")
        self.messages_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 添加欢迎消息
        self._add_message("assistant", "你好！我是柏慧学堂AI答疑助手。\n\n你可以问我任何关于初中课程的问题，我会尽力帮助你！\n\n例如：\n• 数学：勾股定理是什么？\n• 物理：牛顿第一定律怎么理解？\n• 化学：什么是化合价？")
        
        # 输入区域
        input_frame = ctk.CTkFrame(main_frame, fg_color="#f8f9fa", height=80)
        input_frame.pack(fill="x", padx=10, pady=10)
        input_frame.pack_propagate(False)
        
        # 文本输入框
        self.input_text = ctk.CTkTextbox(
            input_frame,
            height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
            border_color="#cccccc"
        )
        self.input_text.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        self.input_text.bind("<Return>", self._on_enter)
        self.input_text.bind("<Shift-Return>", lambda e: None)  # 允许换行
        
        # 发送按钮
        send_btn = ctk.CTkButton(
            input_frame,
            text="发送",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="white",
            width=80,
            command=self._send_message
        )
        send_btn.pack(side="right", padx=10, pady=10)
    
    def _on_enter(self, event):
        """处理回车键"""
        if not event.state & 0x1:  # 非Shift
            self._send_message()
    
    def _send_message(self):
        """发送消息"""
        message = self.input_text.get("1.0", "end-1c").strip()
        if not message:
            return
        
        # 检查API密钥
        if not self.ai_service or not self.ai_service.api_key:
            self._add_message("system", "请先在设置中配置AI API密钥。")
            return
        
        # 清空输入框
        self.input_text.delete("1.0", "end")
        
        # 添加用户消息
        self._add_message("user", message)
        
        # 添加loading指示
        loading_id = self._add_loading_message()
        
        # 在后台线程中获取AI回复
        def get_reply():
            try:
                reply = self._get_ai_reply(message)
                # 在主线程中更新UI
                self.after(0, lambda lid=loading_id: self._remove_loading_message(lid))
                self.after(0, lambda: self._add_message("assistant", reply))
            except Exception as e:
                self.after(0, lambda: self._show_error(f"❌ 错误: {str(e)}"))
        
        threading.Thread(target=get_reply, daemon=True).start()
    
    def _show_reply(self, reply: str):
        """显示AI回复（兼容旧方法）"""
        self._add_message("assistant", reply)
    
    def _show_error(self, error: str):
        """显示错误信息"""
        self._add_message("system", error)
    
    def _get_ai_reply(self, question: str) -> str:
        """获取AI回复（非流式，保留兼容）"""
        if not self.ai_service or not self.ai_service.api_key:
            return "请先在设置中配置AI API密钥。"
        
        # 构建系统提示
        system_prompt = "你是一位经验丰富的初中辅导老师，善于用通俗易懂的方式解释知识点，并给出学习建议。请用中文回答。"
        
        try:
            import requests
            import json
            
            headers = {
                "Authorization": f"Bearer {self.ai_service.api_key}",
                "Content-Type": "application/json",
            }
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
            
            payload = {
                "model": self.ai_service.model,
                "messages": messages,
                "temperature": 0.7,
            }
            
            resp = requests.post(
                self.ai_service.base_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            resp.raise_for_status()
            
            reply = resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            return reply
            
        except Exception as e:
            return f"获取回复失败: {str(e)}"
    
    def _add_message(self, role: str, content: str) -> str:
        """添加消息到聊天区域"""
        msg_frame = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        msg_frame.pack(fill="x", pady=5)
        
        # 头像
        avatar = ctk.CTkLabel(
            msg_frame,
            text="👤" if role == "user" else "🤖",
            font=ctk.CTkFont(size=20),
            width=40,
            height=40
        )
        avatar.pack(side="left", padx=5)
        
        # 消息气泡 - 使用Label避免内建滚动条
        bubble = ctk.CTkLabel(
            msg_frame,
            text=content,
            font=ctk.CTkFont(size=12),
            wraplength=450,
            justify="left",
            anchor="w",
            fg_color="#f0f0f0" if role == "user" else "#e8f4fc",
            corner_radius=15,
            padx=12,
            pady=8,
            border_width=0
        )
        bubble.pack(side="left", fill="x", expand=True, padx=5)
        
        # 滚动到底部 - 使用tkinter的see方法
        try:
            self.messages_frame.canvas.yview_moveto(1.0)
        except:
            pass
        
        # 保存消息ID
        msg_id = f"msg_{len(self.chat_history)}"
        self.chat_history.append({"role": role, "content": content})
        
        return msg_id
    
    def _add_loading_message(self) -> str:
        """添加加载中的消息"""
        msg_frame = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        msg_frame.pack(fill="x", pady=5)
        
        # 加载指示器
        loading_label = ctk.CTkLabel(
            msg_frame,
            text="⏳ AI正在思考中...",
            font=ctk.CTkFont(size=12),
            text_color="#888888",
            anchor="w"
        )
        loading_label.pack(side="left", padx=15, pady=8)
        
        loading_id = f"loading_{len(self.chat_history)}"
        self.chat_history.append({"role": "loading", "content": "thinking"})
        self._loading_widgets[loading_id] = loading_label
        
        return loading_id
    
    def _update_loading_message(self, loading_id: str, content: str):
        """更新loading消息内容"""
        if loading_id in self._loading_widgets:
            widget = self._loading_widgets[loading_id]
            widget.configure(text=f"⏳ AI正在思考中...\n{content}")
    
    def _remove_loading_message(self, loading_id: str):
        """移除loading消息"""
        if loading_id in self._loading_widgets:
            widget = self._loading_widgets.pop(loading_id)
            widget.destroy()
    
    def _update_reply(self, loading_id: str, reply: str):
        """更新回复消息（已废弃）"""
        self._add_message("assistant", reply)
    
    def set_api_key(self, key: str):
        """设置API密钥"""
        if self.ai_service:
            self.ai_service.set_api_key(key)
    
    def clear_chat(self):
        """清空聊天历史"""
        self.chat_history = []
        self._loading_widgets = {}
        # 清空消息区域
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        # 重新添加欢迎消息
        self._add_message("assistant", "你好！我是柏慧学堂AI答疑助手。\n\n你可以问我任何关于初中课程的问题，我会尽力帮助你！\n\n例如：\n• 数学：勾股定理是什么？\n• 物理：牛顿第一定律怎么理解？\n• 化学：什么是化合价？")
