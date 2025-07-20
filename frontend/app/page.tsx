"use client"

import React, { useState } from "react"
import { Sidebar } from "./components/sidebar"
import { ChatArea } from "./components/chat-area"
import { useDocuments } from "@/hooks/use-documents"
import { useChat } from "@/hooks/use-chat"
import type { Document } from "@/lib/api"

export default function KnowledgeAssistant() {
  const [searchQuery, setSearchQuery] = useState("")
  const [chatInput, setChatInput] = useState("")
  
  // Use custom hooks for backend integration
  const { documents, loading: documentsLoading, error: documentsError, isUploading, uploadProgress, uploadDocument, deleteDocument } = useDocuments()
  const { messages, loading: chatLoading, error: chatError, sendMessage, clearChat } = useChat()

  // Transform documents to match the expected format for the sidebar
  const transformedDocuments = documents.map((doc: Document) => ({
    id: parseInt(doc.id) || Math.random(),
    name: doc.name,
    addedDate: doc.modified,
    type: doc.type,
  }))

  const handleSendMessage = async () => {
    if (chatInput.trim()) {
      const message = chatInput
      setChatInput("") // Clear input immediately
      await sendMessage(message) // Send message after clearing input
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar 
        documents={transformedDocuments} 
        searchQuery={searchQuery} 
        onSearchChange={setSearchQuery}
        onUpload={(files) => {
          if (files && files.length > 0) {
            uploadDocument(files[0])
          }
        }}
        onDelete={(id) => deleteDocument(id.toString())}
        loading={documentsLoading}
        error={documentsError || undefined}
        isUploading={isUploading}
        uploadProgress={uploadProgress}
      />
      <ChatArea
        messages={messages}
        chatInput={chatInput}
        onChatInputChange={setChatInput}
        onSendMessage={handleSendMessage}
        onKeyPress={handleKeyPress}
        documentCount={transformedDocuments.length}
      />
    </div>
  )
}
