"""
AIQ&APanel - ChatTypeQ&AInterfacePage
"""
import customtkinter as ctk
import tkinter as tk
from pathlib import Path
import threading
from typing import Optional


class AIChatPanel(ctk.CTkFrame):
    """AIQ&APanel"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # ImportAIService
        self.ai_service = None
        self._loading_widgets = {}
        try:
            from core.api.ai_service import AIService
            self.ai_service = AIService()
            print(f"AIServiceInitializeSuccess, api_key={bool(self.ai_service.api_key)}")
        except Exception as e:
            print(f"AIServiceInitializeFailed: {e}")
        
        # ChatHistory
        self.chat_history = []
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build UI"""
        # Main Frame
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)
        
        # TitleBar
        title_frame = ctk.CTkFrame(main_frame, fg_color="#f8f9fa", height=50)
        title_frame.pack(fill="x", padx=10, pady=(10, 5))
        title_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            title_frame,
            text="🤖 AIQ&AAssistant",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#2c3e50"
        ).pack(side="left", padx=15, pady=10)
        
        ctk.CTkLabel(
            title_frame,
            text="✅ AlreadyConnect",
            font=ctk.CTkFont(size=11),
            text_color="#27ae60"
        ).pack(side="right", padx=15, pady=10)
        
        # ChatMessageArea
        chat_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
        chat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Message ScrollArea
        self.messages_frame = ctk.CTkScrollableFrame(chat_frame, fg_color="transparent")
        self.messages_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add Welcome Message
        self._add_message("assistant", "Hello！IYes柏慧学堂AIQ&AAssistant。\n\nYouCan AskIAnyAboutJuniorHighCourseAskQuestion，I Will Try My BestHelpYou！\n\nExampleSuch As：\n• Math：Pythagorean TheoremYesWhat？\n• Physics：Newton First Law？\n• Chemistry：WhatYesizeCombined Price？")
        
        # InputArea
        input_frame = ctk.CTkFrame(main_frame, fg_color="#f8f9fa", height=80)
        input_frame.pack(fill="x", padx=10, pady=10)
        input_frame.pack_propagate(False)
        
        # Text InputBox
        self.input_text = ctk.CTkTextbox(
            input_frame,
            height=50,
            corner_radius=10,
            font=ctk.CTkFont(size=12),
            border_color="#cccccc"
        )
        self.input_text.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        self.input_text.bind("<Return>", self._on_enter)
        self.input_text.bind("<Shift-Return>", lambda e: None)  # Allow Line Break
        
        # SendByButton
        send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="white",
            width=80,
            command=self._send_message
        )
        send_btn.pack(side="right", padx=10, pady=10)
    
    def _on_enter(self, event):
        """ProcessEnter Key"""
        if not event.state & 0x1:  # NonShift
            self._send_message()
    
    def _send_message(self):
        """SendMessage"""
        message = self.input_text.get("1.0", "end-1c").strip()
        if not message:
            return
        
        # CheckAPISecret Key
        if not self.ai_service or not self.ai_service.api_key:
            self._add_message("system", "Please firstInSettingsInConfigureAI APISecret Key。")
            return
        
        # ClearInputBox
        self.input_text.delete("1.0", "end")
        
        # AddUserMessage
        self._add_message("user", message)
        
        # AddloadingIndicator
        loading_id = self._add_loading_message()
        
        # InFetch in Background ThreadAIReply
        def get_reply():
            try:
                reply = self._get_ai_reply(message)
                # InIn Main ThreadMoreNewUI
                self.after(0, lambda lid=loading_id: self._remove_loading_message(lid))
                self.after(0, lambda: self._add_message("assistant", reply))
            except Exception as e:
                self.after(0, lambda: self._show_error(f"❌ Error: {str(e)}"))
        
        threading.Thread(target=get_reply, daemon=True).start()
    
    def _show_reply(self, reply: str):
        """ShowAIReply（Compatible with Old Method）"""
        self._add_message("assistant", reply)
    
    def _show_error(self, error: str):
        """ShowErrorInfo"""
        self._add_message("system", error)
    
    def _get_ai_reply(self, question: str) -> str:
        """GetAIReply（NonStreamType，Retain Compatibility）"""
        if not self.ai_service or not self.ai_service.api_key:
            return "Please firstInSettingsInConfigureAI APISecret Key。"
        
        # Build SystemTip
        system_prompt = "YouYesExperiencedJuniorHighTutor，Good AtUseEasy to UnderstandTypeExplain Knowledge Point，And ProvideStudySuggestion。PleaseAnswer in Chinese。"
        
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
            return f"GetReplyFailed: {str(e)}"
    
    def _add_message(self, role: str, content: str) -> str:
        """Add Message ToChatArea"""
        msg_frame = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        msg_frame.pack(fill="x", pady=5)
        
        # Avatar
        avatar = ctk.CTkLabel(
            msg_frame,
            text="👤" if role == "user" else "🤖",
            font=ctk.CTkFont(size=20),
            width=40,
            height=40
        )
        avatar.pack(side="left", padx=5)
        
        # MessageBubble - UseLabelAvoidInsideBuild Scrollbar
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
        
        # Scroll ToBottom - UsetkinterseeMethod
        try:
            self.messages_frame.canvas.yview_moveto(1.0)
        except:
            pass
        
        # SaveMessageID
        msg_id = f"msg_{len(self.chat_history)}"
        self.chat_history.append({"role": role, "content": content})
        
        return msg_id
    
    def _add_loading_message(self) -> str:
        """AddLoading's Message"""
        msg_frame = ctk.CTkFrame(self.messages_frame, fg_color="transparent")
        msg_frame.pack(fill="x", pady=5)
        
        # LoadIndicator
        loading_label = ctk.CTkLabel(
            msg_frame,
            text="⏳ AIProcessingThinkIn...",
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
        """MoreNewloadingMessage Content"""
        if loading_id in self._loading_widgets:
            widget = self._loading_widgets[loading_id]
            widget.configure(text=f"⏳ AIProcessingThinkIn...\n{content}")
    
    def _remove_loading_message(self, loading_id: str):
        """RemoveloadingMessage"""
        if loading_id in self._loading_widgets:
            widget = self._loading_widgets.pop(loading_id)
            widget.destroy()
    
    def _update_reply(self, loading_id: str, reply: str):
        """MoreNewReply Message（AlreadyDeprecated）"""
        self._add_message("assistant", reply)
    
    def set_api_key(self, key: str):
        """SettingsAPISecret Key"""
        if self.ai_service:
            self.ai_service.set_api_key(key)
    
    def clear_chat(self):
        """ClearChatHistory"""
        self.chat_history = []
        self._loading_widgets = {}
        # Clear MessagesArea
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        # AgainNewAdd Welcome Message
        self._add_message("assistant", "Hello！IYes柏慧学堂AIQ&AAssistant。\n\nYouCan AskIAnyAboutJuniorHighCourseAskQuestion，I Will Try My BestHelpYou！\n\nExampleSuch As：\n• Math：Pythagorean TheoremYesWhat？\n• Physics：Newton First Law？\n• Chemistry：WhatYesizeCombined Price？")
