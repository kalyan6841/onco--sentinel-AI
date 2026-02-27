import React, { useState } from 'react';
import { Shield, Activity } from 'lucide-react';
import { PatientForm, type PatientData } from './components/PatientForm';
import { AuditResults } from './components/AuditResults';
import { runSafetyAudit } from './services/gemini';

export default function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [auditResult, setAuditResult] = useState<string | null>(null);

  const handleAudit = async (data: PatientData) => {
    setIsLoading(true);
    setAuditResult(null);
    
    try {
      // Format patient data for the prompt
      const formattedData = `
Patient ID: ${data.patientId}
Age: ${data.age}
Gender: ${data.gender}
Weight: ${data.weight} kg
Height: ${data.height} cm
BSA: ${data.bsa} m²
Diagnosis: ${data.diagnosis}

Labs:
${data.labs}

Medications:
${data.medications}
      `.trim();

      const result = await runSafetyAudit(formattedData);
      setAuditResult(result);
    } catch (error) {
      console.error(error);
      setAuditResult("🚨 **Error:** Failed to generate audit. Please check your connection and try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans selection:bg-indigo-100 selection:text-indigo-900">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-sm">
              <Shield className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-slate-900 leading-tight">Onco-Sentinel AI</h1>
              <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">Zero-Error Safety Audit</p>
            </div>
          </div>
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-emerald-50 text-emerald-700 rounded-full text-xs font-semibold border border-emerald-200">
            <Activity className="w-3.5 h-3.5" />
            System Active
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          {/* Left Column: Input Form */}
          <div className="lg:col-span-5 xl:col-span-4">
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
              <PatientForm onSubmit={handleAudit} isLoading={isLoading} />
            </div>
          </div>

          {/* Right Column: Results */}
          <div className="lg:col-span-7 xl:col-span-8 h-[calc(100vh-8rem)] min-h-[600px]">
            <AuditResults result={auditResult} />
          </div>

        </div>
      </main>
    </div>
  );
}

