"use client"

import React, { useRef } from "react"
import { Search, FileText, RotateCcw, Upload } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"

interface Document {
  id: number
  name: string
  addedDate: string
  type: string
}

interface SidebarProps {
  documents: Document[]
  searchQuery: string
  onSearchChange: (query: string) => void
  onUpload?: (files: FileList) => void
  onDelete?: (id: number) => void
  loading?: boolean
  error?: string
  isUploading?: boolean
  uploadProgress?: number
}

export function Sidebar({ 
  documents, 
  searchQuery, 
  onSearchChange, 
  onUpload, 
  onDelete, 
  loading, 
  error, 
  isUploading, 
  uploadProgress 
}: SidebarProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleUploadClick = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && onUpload) {
      onUpload(files)
    }
  }

  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center gap-2">
          <h1 className="text-lg font-semibold text-gray-900">Knowledge Assistant</h1>
          <div className="flex items-center gap-1">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-sm text-gray-600">Online</span>
          </div>
        </div>
      </div>

      {/* Documents Section */}
      <div className="flex-1 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-medium text-gray-900">Documents</h2>
            <div className="flex gap-1">
              <Button 
                variant="ghost" 
                size="sm" 
                className="h-8 w-8 p-0" 
                onClick={handleUploadClick}
                title="Upload document"
              >
                <Upload className="h-4 w-4" />
              </Button>
              <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Refresh">
                <RotateCcw className="h-4 w-4" />
              </Button>
            </div>
          </div>
          
          {/* Hidden file input */}
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.txt,.docx,.md"
            multiple
            onChange={handleFileChange}
            className="hidden"
          />

          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Search documents..."
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* Document List */}
        <div className="flex-1 overflow-y-auto max-h-96">
          {loading ? (
            <div className="p-4 text-center text-gray-500">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-gray-900 mx-auto mb-2"></div>
              Loading documents...
            </div>
          ) : error ? (
            <div className="p-4 text-center text-red-500">
              <p className="text-sm">{error}</p>
            </div>
          ) : documents.length === 0 ? (
            <div className="p-4 text-center text-gray-500">
              <FileText className="h-8 w-8 mx-auto mb-2 text-gray-300" />
              <p className="text-sm">No documents uploaded yet</p>
            </div>
          ) : (
            documents.map((doc) => (
              <div key={doc.id} className="p-3 border-b border-gray-100 hover:bg-gray-50 cursor-pointer">
                <div className="flex items-start gap-3">
                  <div className="mt-1">
                    <FileText className="h-4 w-4 text-red-500" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{doc.name}</p>
                    <p className="text-xs text-gray-500 mt-1">Added: {doc.addedDate}</p>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Reindexing Status - Only show when uploading */}
        {isUploading && (
          <div className="p-4 border-t border-gray-200 bg-gray-50">
            <div className="flex items-center gap-2 mb-2">
              <RotateCcw className="h-4 w-4 text-gray-500 animate-spin" />
              <span className="text-sm text-gray-700">Processing documents</span>
            </div>
            <Progress value={uploadProgress || 0} className="h-2 mb-1" />
            <p className="text-xs text-gray-500">Indexing for search...</p>
          </div>
        )}
      </div>
    </div>
  )
}
