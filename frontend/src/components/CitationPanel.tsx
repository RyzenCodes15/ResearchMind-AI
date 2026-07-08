'use client';

import React from 'react';
import { useChat } from '../lib/ChatContext';

export default function CitationPanel() {
  const { selectedCitations } = useChat();

  return (
    <div className="w-80 bg-gray-50 border-l border-gray-200 flex flex-col h-full overflow-hidden">
      <div className="p-4 border-b border-gray-200 bg-white">
        <h2 className="text-sm font-semibold text-gray-800 flex items-center gap-2">
          <svg className="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Citations
        </h2>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {!selectedCitations || selectedCitations.length === 0 ? (
          <div className="text-center text-gray-500 mt-10">
            <svg className="w-12 h-12 text-gray-300 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            <p className="text-sm">Click on citations in the chat to view details.</p>
          </div>
        ) : (
          selectedCitations.map((citation, index) => (
            <div key={index} className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
              <div className="flex items-start justify-between mb-2">
                <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded font-medium">
                  {index + 1}
                </span>
                <span className="text-xs font-medium text-gray-400">
                  {Math.round(citation.similarity_score * 100)}% match
                </span>
              </div>
              <h3 className="text-sm font-semibold text-gray-800 truncate mb-1" title={citation.document_name}>
                {citation.document_name}
              </h3>
              {citation.page_start !== null && (
                <p className="text-xs text-gray-500 mb-2 font-medium">
                  Page {citation.page_start}
                  {citation.page_end && citation.page_end !== citation.page_start ? ` - ${citation.page_end}` : ''}
                </p>
              )}
              <div className="text-xs text-gray-600 leading-relaxed bg-gray-50 p-2 rounded border border-gray-100 whitespace-pre-wrap">
                "{citation.content}"
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
