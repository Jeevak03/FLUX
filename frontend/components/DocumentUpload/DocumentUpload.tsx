// components/DocumentUpload/DocumentUpload.tsx
import React, { useState, useRef, useCallback } from 'react';
import { UploadedFile } from '../../types/agents';

interface DocumentUploadProps {
  onFilesUploaded: (files: UploadedFile[]) => void;
  maxFiles?: number;
  maxFileSize?: number; // in bytes
  className?: string;
}

const SUPPORTED_FORMATS = {
  // Text Documents
  'application/pdf': { extension: 'PDF', icon: '📄', color: 'text-red-600' },
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': { extension: 'DOCX', icon: '📝', color: 'text-blue-600' },
  'text/plain': { extension: 'TXT', icon: '📄', color: 'text-gray-600' },
  'text/html': { extension: 'HTML', icon: '🌐', color: 'text-orange-600' },
  'application/vnd.oasis.opendocument.text': { extension: 'ODT', icon: '📝', color: 'text-blue-600' },
  'application/rtf': { extension: 'RTF', icon: '📝', color: 'text-purple-600' },
  'application/epub+zip': { extension: 'EPUB', icon: '📚', color: 'text-green-600' },
  'text/markdown': { extension: 'MD', icon: '📝', color: 'text-gray-600' },
  
  // Data Files
  'text/csv': { extension: 'CSV', icon: '📊', color: 'text-green-600' },
  'application/json': { extension: 'JSON', icon: '🔧', color: 'text-yellow-600' },
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': { extension: 'XLSX', icon: '📊', color: 'text-green-600' },
  'application/vnd.openxmlformats-officedocument.presentationml.presentation': { extension: 'PPTX', icon: '📊', color: 'text-orange-600' },
  'text/tab-separated-values': { extension: 'TSV', icon: '📊', color: 'text-green-600' },
  
  // Image Formats
  'image/jpeg': { extension: 'JPEG', icon: '🖼️', color: 'text-pink-600' },
  'image/jpg': { extension: 'JPG', icon: '🖼️', color: 'text-pink-600' },
  'image/png': { extension: 'PNG', icon: '🖼️', color: 'text-purple-600' },
  'image/gif': { extension: 'GIF', icon: '🎞️', color: 'text-blue-600' },
  'image/webp': { extension: 'WEBP', icon: '🖼️', color: 'text-teal-600' },
};

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
  onFilesUploaded,
  maxFiles = 10,
  maxFileSize = 30 * 1024 * 1024, // 30MB
  className = ''
}) => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<{ [key: string]: number }>({});
  const [errors, setErrors] = useState<string[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (file: File): string | null => {
    // Check file size
    if (file.size > maxFileSize) {
      return `File "${file.name}" exceeds maximum size of ${Math.round(maxFileSize / (1024 * 1024))}MB`;
    }

    // Check file type
    const fileType = file.type || getTypeFromExtension(file.name);
    if (!SUPPORTED_FORMATS[fileType as keyof typeof SUPPORTED_FORMATS]) {
      return `File "${file.name}" has unsupported format. Supported formats: ${Object.values(SUPPORTED_FORMATS).map(f => f.extension).join(', ')}`;
    }

    return null;
  };

  const getTypeFromExtension = (filename: string): string => {
    const ext = filename.toLowerCase().split('.').pop();
    const extensionMap: { [key: string]: string } = {
      'pdf': 'application/pdf',
      'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'txt': 'text/plain',
      'html': 'text/html',
      'htm': 'text/html',
      'odt': 'application/vnd.oasis.opendocument.text',
      'rtf': 'application/rtf',
      'epub': 'application/epub+zip',
      'md': 'text/markdown',
      'csv': 'text/csv',
      'json': 'application/json',
      'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
      'tsv': 'text/tab-separated-values',
      'jpeg': 'image/jpeg',
      'jpg': 'image/jpeg',
      'png': 'image/png',
      'gif': 'image/gif',
      'webp': 'image/webp',
    };
    return extensionMap[ext || ''] || 'application/octet-stream';
  };

  const processFile = async (file: File): Promise<UploadedFile> => {
    const fileId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const fileType = file.type || getTypeFromExtension(file.name);
    
    // Update progress
    setUploadProgress(prev => ({ ...prev, [fileId]: 0 }));

    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onprogress = (e) => {
        if (e.lengthComputable) {
          const progress = Math.round((e.loaded / e.total) * 100);
          setUploadProgress(prev => ({ ...prev, [fileId]: progress }));
        }
      };

      reader.onload = () => {
        const uploadedFile: UploadedFile = {
          id: fileId,
          name: file.name,
          type: fileType,
          size: file.size,
          content: reader.result as string,
          uploadedAt: new Date().toISOString()
        };
        
        setUploadProgress(prev => ({ ...prev, [fileId]: 100 }));
        resolve(uploadedFile);
      };

      reader.onerror = () => {
        setUploadProgress(prev => {
          const newProgress = { ...prev };
          delete newProgress[fileId];
          return newProgress;
        });
        reject(new Error(`Failed to read file: ${file.name}`));
      };

      // Read file based on type
      if (fileType.startsWith('text/') || fileType === 'application/json') {
        reader.readAsText(file);
      } else {
        reader.readAsDataURL(file);
      }
    });
  };

  const handleFiles = async (files: FileList | File[]) => {
    const fileArray = Array.from(files);
    const newErrors: string[] = [];

    // Check total file count
    if (uploadedFiles.length + fileArray.length > maxFiles) {
      newErrors.push(`Cannot upload more than ${maxFiles} files total`);
    }

    // Validate each file
    const validFiles: File[] = [];
    fileArray.forEach(file => {
      const error = validateFile(file);
      if (error) {
        newErrors.push(error);
      } else {
        validFiles.push(file);
      }
    });

    setErrors(newErrors);

    if (validFiles.length === 0) return;

    setIsUploading(true);
    
    try {
      const processedFiles = await Promise.all(
        validFiles.map(file => processFile(file))
      );

      const newUploadedFiles = [...uploadedFiles, ...processedFiles];
      setUploadedFiles(newUploadedFiles);
      onFilesUploaded(newUploadedFiles);

      // Clear progress after a short delay
      setTimeout(() => {
        setUploadProgress({});
      }, 1000);

    } catch (error) {
      console.error('Upload error:', error);
      setErrors(prev => [...prev, 'Upload failed. Please try again.']);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFiles(files);
    }
  }, [uploadedFiles, maxFiles]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFiles(files);
    }
  };

  const removeFile = (fileId: string) => {
    const newFiles = uploadedFiles.filter(f => f.id !== fileId);
    setUploadedFiles(newFiles);
    onFilesUploaded(newFiles);
  };

  const clearErrors = () => setErrors([]);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (type: string) => {
    const formatInfo = SUPPORTED_FORMATS[type as keyof typeof SUPPORTED_FORMATS];
    return formatInfo ? formatInfo.icon : '📄';
  };

  const getFileColor = (type: string) => {
    const formatInfo = SUPPORTED_FORMATS[type as keyof typeof SUPPORTED_FORMATS];
    return formatInfo ? formatInfo.color : 'text-gray-600';
  };

  return (
    <div className={`bg-white rounded-xl shadow-lg border border-gray-100 ${className}`}>
      {/* Header */}
      <div className="bg-gradient-to-r from-cyan-500 to-blue-600 p-4 rounded-t-xl">
        <div className="flex items-center justify-between text-white">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
              📎
            </div>
            <div>
              <h3 className="font-semibold text-lg">Upload Project Documents</h3>
              <p className="text-sm text-white/80">
                {uploadedFiles.length}/{maxFiles} files • {Math.round(maxFileSize / (1024 * 1024))}MB max per file
              </p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm text-white/80">Supported Formats</div>
            <div className="text-xs text-white/60">
              PDF, DOCX, TXT, HTML, CSV, JSON, Images, etc.
            </div>
          </div>
        </div>
      </div>

      {/* Upload Area */}
      <div className="p-6">
        {/* Drag & Drop Zone */}
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ${
            isDragOver
              ? 'border-blue-400 bg-blue-50'
              : uploadedFiles.length > 0
                ? 'border-gray-200 bg-gray-50'
                : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
          }`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <div className="space-y-4">
            <div className={`text-6xl ${isDragOver ? 'animate-bounce' : ''}`}>
              {isDragOver ? '📥' : '📁'}
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {isDragOver ? 'Drop your files here!' : 'Upload Project Documents'}
              </h3>
              <p className="text-gray-600 mb-4">
                Drag and drop files here, or click to select files
              </p>
              
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={isUploading || uploadedFiles.length >= maxFiles}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isUploading ? 'Uploading...' : 'Choose Documents'}
              </button>
            </div>

            <div className="text-sm text-gray-500">
              <div className="flex flex-wrap justify-center gap-2 mb-2">
                {Object.values(SUPPORTED_FORMATS).slice(0, 8).map((format, index) => (
                  <span key={index} className={`px-2 py-1 bg-gray-100 rounded text-xs ${format.color}`}>
                    {format.icon} {format.extension}
                  </span>
                ))}
                <span className="px-2 py-1 bg-gray-100 rounded text-xs text-gray-600">
                  +{Object.keys(SUPPORTED_FORMATS).length - 8} more
                </span>
              </div>
              <p>Maximum {maxFiles} files, {Math.round(maxFileSize / (1024 * 1024))}MB each</p>
            </div>
          </div>
        </div>

        {/* File Input */}
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept={Object.keys(SUPPORTED_FORMATS).join(',')}
          onChange={handleFileInput}
          className="hidden"
        />

        {/* Error Messages */}
        {errors.length > 0 && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-2">
                <span className="text-red-500">⚠️</span>
                <h4 className="font-medium text-red-800">Upload Errors</h4>
              </div>
              <button
                onClick={clearErrors}
                className="text-red-600 hover:text-red-800"
              >
                ✕
              </button>
            </div>
            <ul className="mt-2 space-y-1">
              {errors.map((error, index) => (
                <li key={index} className="text-sm text-red-700">
                  • {error}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Upload Progress */}
        {Object.keys(uploadProgress).length > 0 && (
          <div className="mt-4 space-y-2">
            {Object.entries(uploadProgress).map(([fileId, progress]) => (
              <div key={fileId} className="bg-gray-100 rounded-lg p-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm text-gray-600">Uploading...</span>
                  <span className="text-sm font-medium text-gray-900">{progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Uploaded Files List */}
        {uploadedFiles.length > 0 && (
          <div className="mt-6">
            <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
              <span className="mr-2">📋</span>
              Uploaded Files ({uploadedFiles.length})
            </h4>
            
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {uploadedFiles.map((file) => (
                <div
                  key={file.id}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-center space-x-3 flex-1 min-w-0">
                    <div className={`text-2xl ${getFileColor(file.type)}`}>
                      {getFileIcon(file.type)}
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-gray-900 truncate">{file.name}</p>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span>{formatFileSize(file.size)}</span>
                        <span>
                          {SUPPORTED_FORMATS[file.type as keyof typeof SUPPORTED_FORMATS]?.extension || 'Unknown'}
                        </span>
                        <span>{new Date(file.uploadedAt).toLocaleTimeString()}</span>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => removeFile(file.id)}
                    className="ml-4 p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors"
                    title="Remove file"
                  >
                    🗑️
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};