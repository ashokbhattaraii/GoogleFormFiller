"use client";

import { useState } from 'react';

const FIRST_NAMES = ["Aarav", "Aashish", "Bikash", "Bishal", "Dipendra", "Gopal", "Hari", "Kamal", "Kiran", "Milan", "Nabin", "Prakash", "Rabin", "Rajan", "Rakesh", "Ramesh", "Sagar", "Sandeep", "Santosh", "Shyam", "Sujan", "Suman", "Sunil", "Suraj", "Suresh", "Umesh", "Anjali", "Asmita", "Bipana", "Bishnu", "Deepa", "Gita", "Kabita", "Kamala", "Kopila", "Laxmi", "Manju", "Maya", "Mina", "Nisha", "Pabitra", "Pooja", "Pratima", "Priyanka", "Radha", "Rekha", "Rita", "Sabita", "Sangita", "Saraswati", "Sarita", "Sharmila", "Shila", "Sita", "Srijana", "Sujata", "Sumina", "Sunita", "Sushma"];
const LAST_NAMES = ["Acharya", "Adhikari", "Aryal", "Banskota", "Baral", "Basnet", "Bhandari", "Bhattarai", "Bista", "Chaudhary", "Chettri", "Dahal", "Devkota", "Dhakal", "Gautam", "Ghimire", "Gurung", "Joshi", "Karki", "Khadka", "Khatri", "Koirala", "Lama", "Magar", "Maharjan", "Malla", "Neupane", "Ojha", "Pandey", "Parajuli", "Poudel", "Pradhan", "Rai", "Rana", "Regmi", "Rijal", "Sharma", "Shrestha", "Silwal", "Subedi", "Tamang", "Thapa", "Tiwari", "Upadhyay", "Yadav"];

function getRandomName() {
  return `${FIRST_NAMES[Math.floor(Math.random() * FIRST_NAMES.length)]} ${LAST_NAMES[Math.floor(Math.random() * LAST_NAMES.length)]}`;
}

export default function Home() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [schema, setSchema] = useState<any>(null);
  const [error, setError] = useState('');
  
  const [targetCount, setTargetCount] = useState<number | string>(10);
  const [progress, setProgress] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [delayMs, setDelayMs] = useState<number | string>(200);

  const addLog = (msg: string) => {
    setLogs(prev => [msg, ...prev].slice(0, 10));
  };

  const parseForm = async () => {
    try {
      setLoading(true);
      setError('');
      setSchema(null);
      
      const res = await fetch('/api/parse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to parse form');
      
      setSchema(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateRandomPayload = () => {
    const params = new URLSearchParams();
    
    // Core parameters
    params.append('fvv', '1');
    params.append('pageHistory', schema.pageHistory || '0');
    params.append('fbzx', schema.fbzx || '');
    params.append('draftResponse', '[]');
    
    // Field answers
    schema.fields.forEach((field: any) => {
      const entryId = `entry.${field.id}`;
      const title = field.title.toLowerCase();
      let answer = '';
      
      if (field.type === 0 || field.type === 1) { // Text / Paragraph
        if (title.includes('name') || title.includes('नाम')) {
          answer = getRandomName();
        } else if (title.includes('email') || title.includes('इमेल')) {
          answer = `user${Math.floor(Math.random()*99999)}@example.com`;
        } else if (field.required) {
          answer = "N/A";
        }
        if (answer) params.append(entryId, answer);
      } 
      else if (field.type === 2 || field.type === 3 || field.type === 5) { // Radio, Dropdown, Scale
        if (field.options && field.options.length > 0) {
          answer = field.options[Math.floor(Math.random() * field.options.length)];
          params.append(entryId, answer);
        }
      }
      else if (field.type === 4) { // Checkbox
        if (field.options && field.options.length > 0) {
          // pick 1 to 3 random options
          const numChoices = Math.floor(Math.random() * 3) + 1;
          const shuffled = [...field.options].sort(() => 0.5 - Math.random());
          const choices = shuffled.slice(0, numChoices);
          choices.forEach(c => params.append(entryId, c));
        }
      }
    });
    
    return params;
  };

  const startSubmitting = async () => {
    setSubmitting(true);
    setProgress(0);
    setLogs([]);
    
    const target = Number(targetCount) || 1;
    for (let i = 1; i <= target; i++) {
      if (!submitting && i > 1) { // if cancelled
        break;
      }
      
      const payload = generateRandomPayload();
      
      try {
        await fetch(schema.postUrl, {
          method: 'POST',
          mode: 'no-cors',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: payload
        });
        
        setProgress(i);
        addLog(`Successfully sent response ${i}/${target}`);
      } catch (err: any) {
        addLog(`Error on response ${i}: ${err.message}`);
      }
      
      // Delay
      if (i < target) {
        await new Promise(r => setTimeout(r, Number(delayMs) || 200));
      }
    }
    
    setSubmitting(false);
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-8 font-sans selection:bg-purple-500/30">
      <div className="max-w-3xl mx-auto space-y-8">
        
        {/* Header */}
        <div className="text-center space-y-4 pt-12 pb-8">
          <div className="inline-block p-4 rounded-full bg-purple-500/10 mb-2">
            <svg className="w-10 h-10 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h1 className="text-5xl font-extrabold tracking-tight bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent">
            FormFlow Engine
          </h1>
          <p className="text-gray-400 text-lg">Automated Google Form responses at scale, directly from your browser.</p>
        </div>

        {/* Input Card */}
        <div className="bg-gray-900/50 backdrop-blur-xl border border-gray-800 rounded-3xl p-8 shadow-2xl relative overflow-hidden group">
          <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-pink-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          
          <div className="relative space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Google Form URL</label>
              <input
                type="url"
                value={url}
                onChange={e => setUrl(e.target.value)}
                placeholder="https://docs.google.com/forms/d/e/.../viewform"
                className="w-full px-6 py-4 bg-gray-950/50 border border-gray-800 rounded-2xl focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500 transition-all text-gray-200 placeholder-gray-600"
                disabled={submitting}
              />
            </div>
            
            <button
              onClick={parseForm}
              disabled={loading || !url || submitting}
              className="w-full py-4 bg-white hover:bg-gray-100 text-gray-900 rounded-2xl font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_40px_-10px_rgba(255,255,255,0.3)] hover:shadow-[0_0_60px_-15px_rgba(255,255,255,0.5)] active:scale-[0.98]"
            >
              {loading ? 'Analyzing Form Structure...' : 'Analyze Form'}
            </button>
            
            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 text-red-400 rounded-2xl text-sm">
                {error}
              </div>
            )}
          </div>
        </div>

        {/* Configuration Card */}
        {schema && (
          <div className="bg-gray-900/50 backdrop-blur-xl border border-gray-800 rounded-3xl p-8 shadow-2xl space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
            <div>
              <h2 className="text-2xl font-bold text-white mb-2">{schema.title}</h2>
              <p className="text-gray-400 text-sm">Found {schema.fields.length} configurable fields ready for automation.</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Target Responses</label>
                <input
                  type="number"
                  min="1"
                  max="1000"
                  value={targetCount}
                  onChange={e => setTargetCount(e.target.value === '' ? '' : parseInt(e.target.value))}
                  className="w-full px-6 py-4 bg-gray-950/50 border border-gray-800 rounded-2xl focus:outline-none focus:ring-2 focus:ring-purple-500/50 text-white"
                  disabled={submitting}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Delay Between Posts (ms)</label>
                <input
                  type="number"
                  min="0"
                  step="100"
                  value={delayMs}
                  onChange={e => setDelayMs(parseInt(e.target.value))}
                  className="w-full px-6 py-4 bg-gray-950/50 border border-gray-800 rounded-2xl focus:outline-none focus:ring-2 focus:ring-purple-500/50 text-white"
                  disabled={submitting}
                />
              </div>
            </div>

            {/* Actions & Progress */}
            <div className="pt-4 space-y-6">
              {!submitting ? (
                <button
                  onClick={startSubmitting}
                  disabled={Number(targetCount) < 1}
                  className="w-full py-4 bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-400 hover:to-pink-500 text-white rounded-2xl font-semibold transition-all shadow-[0_0_40px_-10px_rgba(168,85,247,0.4)] hover:shadow-[0_0_60px_-15px_rgba(168,85,247,0.6)] active:scale-[0.98]"
                >
                  Ignite Submission Engine
                </button>
              ) : (
                <div className="space-y-4">
                  <div className="flex justify-between text-sm font-medium">
                    <span className="text-purple-400">Processing Sequence</span>
                    <span className="text-gray-400">{progress} / {targetCount}</span>
                  </div>
                  <div className="w-full h-4 bg-gray-950 rounded-full overflow-hidden border border-gray-800 relative">
                    <div 
                      className="absolute top-0 left-0 h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-300"
                      style={{ width: `${(progress / (Number(targetCount) || 1)) * 100}%` }}
                    />
                    {/* Animated shine effect */}
                    <div className="absolute top-0 left-0 w-full h-full bg-white/20 blur-md translate-x-[-100%] animate-[shimmer_2s_infinite]" />
                  </div>
                  <button
                    onClick={() => setSubmitting(false)}
                    className="w-full py-3 bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20 rounded-xl font-medium transition-colors"
                  >
                    Abort Sequence
                  </button>
                </div>
              )}
            </div>

            {/* Logs */}
            {logs.length > 0 && (
              <div className="pt-6 border-t border-gray-800">
                <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-4">Live Telemetry</h3>
                <div className="space-y-2 font-mono text-sm">
                  {logs.map((log, i) => (
                    <div key={i} className="flex items-center space-x-3 text-gray-400 opacity-80 animate-in fade-in slide-in-from-left-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-green-500" />
                      <span>{log}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            
          </div>
        )}
      </div>
    </div>
  );
}
