"use client"

import type React from "react"

import { Send, MoreVertical, User, Bot } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"

interface Message {
  id: number
  type: "user" | "assistant"
  content: string
  source?: string
  timestamp: Date
}

interface ChatAreaProps {
  messages: Message[]
  chatInput: string
  onChatInputChange: (value: string) => void
  onSendMessage: () => void
  onKeyPress: (e: React.KeyboardEvent) => void
  documentCount: number
}

export function ChatArea({
  messages,
  chatInput,
  onChatInputChange,
  onSendMessage,
  onKeyPress,
  documentCount,
}: ChatAreaProps) {
  const formatMessageContent = (content: string) => {
    // Simple markdown-like formatting
    const lines = content.split("\n")
    return lines.map((line, index) => {
      if (line.startsWith("• ")) {
        return (
          <li key={index} className="ml-4">
            {line.substring(2)}
          </li>
        )
      }
      if (line.includes("**")) {
        const parts = line.split("**")
        return (
          <p key={index} className="mb-2">
            {parts.map((part, i) => (i % 2 === 1 ? <strong key={i}>{part}</strong> : part))}
          </p>
        )
      }
      return line ? (
        <p key={index} className="mb-2">
          {line}
        </p>
      ) : (
        <br key={index} />
      )
    })
  }

  return (
    <div className="flex-1 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 bg-white">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-semibold text-gray-900">Chat with Knowledge Assistant</h1>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <MoreVertical className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex gap-3 ${message.type === "user" ? "justify-end" : "justify-start"}`}>
            {message.type === "assistant" && (
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <Bot className="h-4 w-4 text-blue-600" />
              </div>
            )}

            <div className={`max-w-2xl ${message.type === "user" ? "order-1" : ""}`}>
              <div
                className={`rounded-lg p-3 ${
                  message.type === "user" ? "bg-blue-600 text-white" : "bg-white border border-gray-200"
                }`}
              >
                <div className={`text-sm ${message.type === "user" ? "text-white" : "text-gray-900"}`}>
                  {message.type === "assistant" ? (
                    <div>{formatMessageContent(message.content)}</div>
                  ) : (
                    <p className="font-medium">{message.content}</p>
                  )}
                </div>
              </div>

              {message.source && <p className="text-xs text-gray-500 mt-2 px-3">Source: {message.source}</p>}
            </div>

            {message.type === "user" && (
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                <User className="h-4 w-4 text-white" />
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-200 bg-white">
        <div className="flex gap-2">
          <div className="flex-1">
            <Textarea
              placeholder="Ask a question about your documents..."
              value={chatInput}
              onChange={(e) => onChatInputChange(e.target.value)}
              onKeyPress={onKeyPress}
              className="min-h-[44px] max-h-32 resize-none"
              rows={1}
            />
          </div>
          <Button
            onClick={onSendMessage}
            disabled={!chatInput.trim()}
            className="h-11 w-11 p-0 bg-blue-600 hover:bg-blue-700"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>

        <div className="flex justify-between items-center mt-2 text-xs text-gray-500">
          <span>Searching in {documentCount} documents</span>
          <span>Press Enter to send, Shift+Enter for new line</span>
        </div>
      </div>
    </div>
  )
}
