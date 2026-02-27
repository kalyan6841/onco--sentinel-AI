import React, { useState, useEffect } from 'react';
import { Calculator, Activity, Pill, User, AlertCircle } from 'lucide-react';
import { cn } from '../utils';

export interface PatientData {
  patientId: string;
  age: string;
  gender: string;
  weight: string;
  height: string;
  bsa: string;
  diagnosis: string;
  labs: string;
  medications: string;
}

interface PatientFormProps {
  onSubmit: (data: PatientData) => void;
  isLoading: boolean;
}

export function PatientForm({ onSubmit, isLoading }: PatientFormProps) {
  const [formData, setFormData] = useState<PatientData>({
    patientId: '',
    age: '',
    gender: '',
    weight: '',
    height: '',
    bsa: '',
    diagnosis: '',
    labs: '',
    medications: '',
  });

  // Auto-calculate BSA using Mosteller formula: sqrt((height(cm) * weight(kg)) / 3600)
  useEffect(() => {
    const w = parseFloat(formData.weight);
    const h = parseFloat(formData.height);
    if (!isNaN(w) && !isNaN(h) && w > 0 && h > 0) {
      const bsa = Math.sqrt((w * h) / 3600).toFixed(2);
      setFormData((prev) => ({ ...prev, bsa }));
    } else {
      setFormData((prev) => ({ ...prev, bsa: '' }));
    }
  }, [formData.weight, formData.height]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const fillExample = () => {
    setFormData({
      patientId: 'PT-84920',
      age: '72',
      gender: 'Female',
      weight: '65',
      height: '160',
      bsa: '1.70',
      diagnosis: 'Metastatic Breast Cancer (ER+/PR+/HER2-)',
      labs: 'CrCl: 45 mL/min\\nAST: 42 U/L\\nALT: 38 U/L\\nT.Bili: 1.1 mg/dL',
      medications: 'Capecitabine 1250 mg/m2 PO BID\\nOndansetron 8mg PO BID\\nOmeprazole 40mg PO Daily\\nFluconazole 150mg PO (for recent thrush)',
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900 flex items-center gap-2">
          <User className="w-5 h-5 text-indigo-600" />
          Patient Profile
        </h2>
        <button
          type="button"
          onClick={fillExample}
          className="text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors"
        >
          Load Example Case
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Patient ID</label>
          <input
            required
            name="patientId"
            value={formData.patientId}
            onChange={handleChange}
            className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
            placeholder="e.g. PT-12345"
          />
        </div>
        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Age</label>
          <input
            required
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
            placeholder="Years"
          />
        </div>
        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Gender</label>
          <select
            required
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
          >
            <option value="">Select...</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Weight (kg)</label>
          <input
            required
            type="number"
            step="0.1"
            name="weight"
            value={formData.weight}
            onChange={handleChange}
            className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
            placeholder="65.0"
          />
        </div>
        <div className="space-y-1">
          <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Height (cm)</label>
          <input
            required
            type="number"
            step="0.1"
            name="height"
            value={formData.height}
            onChange={handleChange}
            className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
            placeholder="160.0"
          />
        </div>
        <div className="space-y-1 relative">
          <label className="text-xs font-medium text-slate-500 uppercase tracking-wider flex items-center gap-1">
            BSA (m²) <Calculator className="w-3 h-3" />
          </label>
          <input
            readOnly
            value={formData.bsa}
            className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm font-mono text-slate-600 cursor-not-allowed"
            placeholder="Auto-calc"
          />
        </div>
      </div>

      <div className="space-y-1">
        <label className="text-xs font-medium text-slate-500 uppercase tracking-wider">Diagnosis & Protocol</label>
        <input
          required
          name="diagnosis"
          value={formData.diagnosis}
          onChange={handleChange}
          className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
          placeholder="e.g. Diffuse Large B-Cell Lymphoma (R-CHOP)"
        />
      </div>

      <div className="space-y-1">
        <label className="text-xs font-medium text-slate-500 uppercase tracking-wider flex items-center gap-1">
          <Activity className="w-3 h-3" /> Labs (Renal/Hepatic)
        </label>
        <textarea
          required
          name="labs"
          value={formData.labs}
          onChange={handleChange}
          rows={3}
          className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-mono"
          placeholder="CrCl: 50 mL/min&#10;AST: 30 U/L&#10;ALT: 25 U/L&#10;T.Bili: 0.8 mg/dL"
        />
      </div>

      <div className="space-y-1">
        <label className="text-xs font-medium text-slate-500 uppercase tracking-wider flex items-center gap-1">
          <Pill className="w-3 h-3" /> Medications (Chemo, Supportive, Palliative)
        </label>
        <textarea
          required
          name="medications"
          value={formData.medications}
          onChange={handleChange}
          rows={4}
          className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-mono"
          placeholder="List all medications and proposed doses..."
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className={cn(
          "w-full py-3 px-4 rounded-xl text-sm font-semibold text-white shadow-sm transition-all flex items-center justify-center gap-2",
          isLoading 
            ? "bg-indigo-400 cursor-not-allowed" 
            : "bg-indigo-600 hover:bg-indigo-700 hover:shadow-md active:scale-[0.98]"
        )}
      >
        {isLoading ? (
          <>
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Running Zero-Error Audit...
          </>
        ) : (
          <>
            <AlertCircle className="w-4 h-4" />
            Run Safety Audit
          </>
        )}
      </button>
    </form>
  );
}
