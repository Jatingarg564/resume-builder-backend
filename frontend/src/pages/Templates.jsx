import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { resumeAPI } from '../api';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import { useToast } from '../components/ToastProvider';

const TEMPLATES = [
  {
    id: 1,
    name: 'Classic',
    description: 'Traditional single-column layout',
    style: 'bg-white',
    preview: 'classic'
  },
  {
    id: 2,
    name: 'Modern',
    description: 'Two-column with colored accents',
    style: 'bg-gradient-to-br from-blue-50 to-purple-50',
    preview: 'modern'
  },
  {
    id: 3,
    name: 'Minimal',
    description: 'Clean and simple design',
    style: 'bg-gray-100',
    preview: 'minimal'
  },
  {
    id: 4,
    name: 'Professional',
    description: 'Executive style resume',
    style: 'bg-slate-50',
    preview: 'professional'
  },
];

export default function Templates() {
  const navigate = useNavigate();
  const { addToast } = useToast();
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const response = await resumeAPI.getTemplates();
      if (response.data.length > 0) {
        setTemplates(response.data);
      } else {
        setTemplates(TEMPLATES);
      }
    } catch (err) {
      setTemplates(TEMPLATES);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800">Templates</h1>
          <Button variant="ghost" onClick={() => navigate('/dashboard')}>Back to Dashboard</Button>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Choose Your Template</h2>
          <p className="text-gray-500 max-w-2xl mx-auto">
            Select a template that best represents your professional style. You can change it anytime.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {templates.map((template) => (
            <div
              key={template.id}
              onClick={() => setSelectedTemplate(template)}
              className={`
                cursor-pointer rounded-xl border-2 transition-all duration-200
                ${selectedTemplate?.id === template.id
                  ? 'border-blue-500 shadow-lg'
                  : 'border-gray-200 hover:border-gray-300 hover:shadow-md'
                }
              `}
            >
              {/* Preview */}
              <div className={`aspect-[3/4] ${template.style} rounded-t-xl flex items-center justify-center p-4`}>
                <div className="w-full max-w-[120px]">
                  <div className="h-4 bg-gray-400 rounded mb-2 mx-auto w-3/4"></div>
                  <div className="h-2 bg-gray-300 rounded mb-1 mx-auto w-1/2"></div>
                  <div className="h-2 bg-gray-200 rounded mb-1 mx-auto w-2/3"></div>
                  <div className="h-2 bg-gray-200 rounded mb-3 mx-auto w-1/3"></div>
                  <div className="h-3 bg-gray-400 rounded mb-2 w-1/3"></div>
                  <div className="h-2 bg-gray-300 rounded mb-1 mx-auto w-3/4"></div>
                  <div className="h-2 bg-gray-200 rounded mb-1 mx-auto w-2/3"></div>
                </div>
              </div>

              {/* Info */}
              <div className="p-4 bg-white rounded-b-xl">
                <h3 className="font-semibold text-gray-900">{template.name}</h3>
                <p className="text-sm text-gray-500">{template.description}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Selected Template Info */}
        {selectedTemplate && (
          <div className="mt-8 bg-blue-50 rounded-xl p-6 text-center">
            <h3 className="font-semibold text-gray-900 mb-2">
              Selected: {selectedTemplate.name}
            </h3>
            <p className="text-gray-600 mb-4">{selectedTemplate.description}</p>
            <Button onClick={() => navigate('/create')}>
              Create Resume with {selectedTemplate.name}
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}