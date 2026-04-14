import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { resumeAPI } from '../api';
import Button from '../components/Button';
import Spinner from '../components/Spinner';

const TEMPLATES = [
  {
    id: 1,
    name: 'Classic',
    description: 'Traditional single-column layout with serif fonts. Perfect for conservative industries like law, finance, or government.',
    style: 'classic',
    preview: 'classic'
  },
  {
    id: 2,
    name: 'Modern',
    description: 'Two-column design with colored accents. Ideal for tech, creative, and startup roles.',
    style: 'modern',
    preview: 'modern'
  },
];

export default function Templates() {
  const navigate = useNavigate();
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTemplate, setSelectedTemplate] = useState(null);

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const response = await resumeAPI.getTemplates();
      if (response.data.length > 0) {
        setTemplates(TEMPLATES);
      } else {
        setTemplates(TEMPLATES);
      }
    } catch (err) {
      setTemplates(TEMPLATES);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTemplate = (template) => {
    setSelectedTemplate(template);
    localStorage.setItem('selectedTemplate', template.style);
  };

  const handleCreateResume = () => {
    if (selectedTemplate) {
      navigate('/create');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800">Choose a Template</h1>
          <Button variant="ghost" onClick={() => navigate('/dashboard')}>
            Back to Dashboard
          </Button>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Select Your Resume Template</h2>
          <p className="text-gray-500 max-w-2xl mx-auto">
            Choose a template that matches your professional style. You can change it anytime.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {templates.map((template) => (
            <div
              key={template.id}
              onClick={() => handleSelectTemplate(template)}
              className={`
                cursor-pointer rounded-2xl border-4 transition-all duration-300 overflow-hidden
                ${selectedTemplate?.id === template.id
                  ? 'border-blue-500 shadow-2xl ring-4 ring-blue-200'
                  : 'border-gray-200 hover:border-gray-300 hover:shadow-lg'
                }
              `}
            >
              {/* Template Preview */}
              <div className="bg-white p-6 min-h-[400px]">
                {template.style === 'classic' ? (
                  <div className="font-serif">
                    <div className="text-center mb-4">
                      <div className="h-6 bg-gray-800 rounded w-2/3 mx-auto mb-2"></div>
                      <div className="h-2 bg-gray-400 rounded w-1/3 mx-auto"></div>
                    </div>
                    <div className="space-y-3">
                      <div>
                        <div className="h-3 bg-gray-700 rounded w-1/4 mb-1"></div>
                        <div className="h-2 bg-gray-300 rounded w-full mb-1"></div>
                        <div className="h-2 bg-gray-200 rounded w-3/4"></div>
                      </div>
                      <div>
                        <div className="h-3 bg-gray-700 rounded w-1/4 mb-1"></div>
                        <div className="h-2 bg-gray-300 rounded w-full mb-1"></div>
                        <div className="h-2 bg-gray-200 rounded w-5/6"></div>
                      </div>
                      <div>
                        <div className="h-3 bg-gray-700 rounded w-1/4 mb-1"></div>
                        <div className="flex gap-1 mt-2">
                          <span className="px-2 py-0.5 bg-gray-200 text-xs rounded">Skill</span>
                          <span className="px-2 py-0.5 bg-gray-200 text-xs rounded">Skill</span>
                          <span className="px-2 py-0.5 bg-gray-200 text-xs rounded">Skill</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="flex gap-4 font-sans">
                    <div className="w-1/3 bg-gradient-to-b from-gray-800 to-gray-700 text-white p-4 rounded-lg">
                      <div className="h-4 bg-white/20 rounded w-2/3 mb-4"></div>
                      <div className="h-2 bg-white/10 rounded w-full mb-2"></div>
                      <div className="h-2 bg-white/10 rounded w-4/5 mb-2"></div>
                      <div className="h-2 bg-white/10 rounded w-3/5 mb-4"></div>
                      <div className="h-2 bg-white/10 rounded w-full mb-2"></div>
                      <div className="h-2 bg-white/10 rounded w-3/4"></div>
                    </div>
                    <div className="flex-1 space-y-3">
                      <div className="h-4 bg-blue-600 rounded w-1/3"></div>
                      <div className="space-y-2">
                        <div className="h-2 bg-gray-300 rounded w-full"></div>
                        <div className="h-2 bg-gray-200 rounded w-5/6"></div>
                      </div>
                      <div className="h-4 bg-blue-600 rounded w-1/4 mt-4"></div>
                      <div className="space-y-2">
                        <div className="h-2 bg-gray-300 rounded w-full"></div>
                        <div className="h-2 bg-gray-200 rounded w-4/5"></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Template Info */}
              <div className="bg-gray-50 p-6 border-t border-gray-200">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-bold text-lg text-gray-900">{template.name}</h3>
                    <p className="text-sm text-gray-500 mt-1">{template.description}</p>
                  </div>
                  <div className={`
                    w-6 h-6 rounded-full border-2 flex items-center justify-center
                    ${selectedTemplate?.id === template.id
                      ? 'border-blue-500 bg-blue-500 text-white'
                      : 'border-gray-300'
                    }
                  `}>
                    {selectedTemplate?.id === template.id && (
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Selected Template Action */}
        {selectedTemplate && (
          <div className="mt-8 text-center">
            <p className="text-gray-600 mb-4">
              Selected: <span className="font-semibold text-gray-900">{selectedTemplate.name}</span> template
            </p>
            <Button onClick={handleCreateResume} size="lg">
              Create Resume with {selectedTemplate.name} Template
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
