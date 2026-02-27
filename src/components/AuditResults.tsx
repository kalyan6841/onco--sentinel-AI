import React from 'react';
import Markdown from 'react-markdown';
import { ShieldCheck, AlertTriangle } from 'lucide-react';

interface AuditResultsProps {
  result: string | null;
}

export function AuditResults({ result }: AuditResultsProps) {
  if (!result) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-slate-400 p-8 text-center border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/50">
        <ShieldCheck className="w-12 h-12 mb-4 text-slate-300" />
        <h3 className="text-lg font-medium text-slate-600 mb-2">Awaiting Patient Data</h3>
        <p className="text-sm max-w-sm">
          Enter patient demographics, labs, and medications to run a Zero-Error Safety Audit.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col h-full">
      <div className="bg-slate-900 px-6 py-4 flex items-center gap-3">
        <ShieldCheck className="w-5 h-5 text-emerald-400" />
        <h2 className="text-white font-medium">Audit Results</h2>
      </div>
      
      <div className="p-6 overflow-y-auto flex-1 custom-scrollbar">
        <div className="prose prose-sm max-w-none prose-headings:font-semibold prose-h1:text-xl prose-h2:text-lg prose-p:text-slate-600 prose-li:text-slate-600">
          <Markdown
            components={{
              p: ({ children }) => {
                // Custom styling for specific alert types based on the text content
                const content = React.Children.toArray(children).join('');
                if (content.includes('🚨 CRITICAL ALERTS:')) {
                  return <div className="bg-red-50 border border-red-200 text-red-900 p-4 rounded-xl my-4 font-medium shadow-sm">{children}</div>;
                }
                if (content.includes('⚠️ MAJOR ALERTS:')) {
                  return <div className="bg-amber-50 border border-amber-200 text-amber-900 p-4 rounded-xl my-4 font-medium shadow-sm">{children}</div>;
                }
                if (content.includes('💡 CLINICAL REASONING:')) {
                  return <div className="bg-blue-50 border border-blue-200 text-blue-900 p-4 rounded-xl my-4 shadow-sm">{children}</div>;
                }
                if (content.includes('✅ RECOMMENDED ACTION:')) {
                  return <div className="bg-emerald-50 border border-emerald-200 text-emerald-900 p-4 rounded-xl my-4 shadow-sm">{children}</div>;
                }
                if (content.match(/^\\[.*\\]$/)) {
                  // Patient ID header
                  return <h3 className="text-lg font-bold text-slate-900 border-b border-slate-200 pb-2 mb-4">{children}</h3>;
                }
                return <p className="mb-4">{children}</p>;
              }
            }}
          >
            {result}
          </Markdown>
        </div>
      </div>
    </div>
  );
}
