import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useResume } from '../context/ResumeContext';
import { resumeAPI } from '../api';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import { useToast } from '../components/ToastProvider';
import { publicAPI } from '../api';

export default function ResumeView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { fetchResume, currentResume, loading } = useResume();
  const { addToast } = useToast();
  const [shareLink, setShareLink] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState('classic');
  const [downloading, setDownloading] = useState(false);
  const resumeRef = useRef(null);

  useEffect(() => {
    if (id) {
      fetchResume(id);
    }
  }, [id]);

  const handleGenerateShareLink = async () => {
    try {
      const response = await resumeAPI.generateShareLink(id);
      setShareLink(`${window.location.origin}/share/${response.data.share_code}`);
      addToast('Share link generated!', 'success');
    } catch (err) {
      addToast('Failed to generate share link', 'error');
    }
  };

  const handleDownloadPDF = async () => {
    setDownloading(true);
    try {
      // Use browser's print-to-pdf functionality for better compatibility
      const printWindow = window.open('', '_blank');
      if (!printWindow) {
        throw new Error('Could not open print window. Please allow popups for this site.');
      }

      // Get the resume HTML content
      const resumeContent = resumeRef.current.innerHTML;

      // Create a clean HTML document for printing
      printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
          <title>${currentResume?.title || 'Resume'}</title>
          <style>
            @page { margin: 0.5in; size: A4; }
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
            * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
          </style>
        </head>
        <body>${resumeContent}</body>
        </html>
      `);
      printWindow.document.close();

      // Wait for content to load
      printWindow.onload = () => {
        printWindow.print();
        setDownloading(false);
        addToast('Use the print dialog to save as PDF', 'success');
      };
    } catch (err) {
      console.error('PDF generation failed:', err);
      addToast('Failed to generate PDF: ' + err.message, 'error');
      setDownloading(false);
    }
  };

  const renderClassicTemplate = () => (
    <div className="bg-white p-8 font-serif">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{currentResume.title}</h1>
        <p className="text-gray-600">Professional Resume</p>
      </div>

      {currentResume.educations?.length > 0 && (
        <section className="mb-6">
          <h2 className="text-lg font-bold text-gray-900 mb-3 pb-1 border-b-2 border-gray-300 uppercase tracking-wide">
            Education
          </h2>
          {currentResume.educations.map((edu, i) => (
            <div key={i} className="mb-3">
              <h3 className="font-semibold text-gray-800">{edu.degree}</h3>
              <p className="text-gray-600">{edu.institution}</p>
              <p className="text-sm text-gray-500">{edu.start_year} - {edu.end_year || 'Present'}</p>
            </div>
          ))}
        </section>
      )}

      {currentResume.experiences?.length > 0 && (
        <section className="mb-6">
          <h2 className="text-lg font-bold text-gray-900 mb-3 pb-1 border-b-2 border-gray-300 uppercase tracking-wide">
            Experience
          </h2>
          {currentResume.experiences.map((exp, i) => (
            <div key={i} className="mb-3">
              <h3 className="font-semibold text-gray-800">{exp.role}</h3>
              <p className="text-gray-600">{exp.company}</p>
              <p className="text-sm text-gray-500 mb-1">{exp.start_date} - {exp.end_date || 'Present'}</p>
              <p className="text-gray-700 text-sm whitespace-pre-line">{exp.description}</p>
            </div>
          ))}
        </section>
      )}

      {currentResume.skills?.length > 0 && (
        <section className="mb-6">
          <h2 className="text-lg font-bold text-gray-900 mb-3 pb-1 border-b-2 border-gray-300 uppercase tracking-wide">
            Skills
          </h2>
          <div className="flex flex-wrap gap-2">
            {currentResume.skills.map((skill, i) => (
              <span key={i} className="px-3 py-1 bg-gray-100 text-gray-700 rounded text-sm border border-gray-300">
                {skill.name}
              </span>
            ))}
          </div>
        </section>
      )}

      {currentResume.projects?.length > 0 && (
        <section>
          <h2 className="text-lg font-bold text-gray-900 mb-3 pb-1 border-b-2 border-gray-300 uppercase tracking-wide">
            Projects
          </h2>
          {currentResume.projects.map((proj, i) => (
            <div key={i} className="mb-3">
              <h3 className="font-semibold text-gray-800">{proj.title}</h3>
              <p className="text-gray-700 text-sm whitespace-pre-line">{proj.description}</p>
              {proj.tech_stack && <p className="text-sm text-gray-500 mt-1">Tech: {proj.tech_stack}</p>}
              {proj.project_link && (
                <a href={proj.project_link} target="_blank" rel="noopener noreferrer" className="text-blue-600 text-sm hover:underline mt-1 block">
                  {proj.project_link}
                </a>
              )}
            </div>
          ))}
        </section>
      )}
    </div>
  );

  const renderModernTemplate = () => (
    <div className="bg-white p-8 font-sans">
      <div className="grid grid-cols-[1fr_2fr] gap-6">
        <div className="bg-gradient-to-br from-slate-800 to-slate-700 text-white p-6 rounded-lg">
          <h1 className="text-2xl font-bold mb-1">{currentResume.title}</h1>
          <p className="text-slate-300 text-sm mb-6">Professional Resume</p>

          {currentResume.skills?.length > 0 && (
            <div className="mb-6">
              <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">Skills</h2>
              <div className="space-y-2">
                {currentResume.skills.map((skill, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                    <span className="text-sm">{skill.name}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {currentResume.educations?.length > 0 && (
            <div>
              <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">Education</h2>
              {currentResume.educations.map((edu, i) => (
                <div key={i} className="mb-3">
                  <p className="font-medium text-sm">{edu.degree}</p>
                  <p className="text-slate-300 text-xs">{edu.institution}</p>
                  <p className="text-slate-400 text-xs">{edu.start_year} - {edu.end_year || 'Present'}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        <div>
          {currentResume.experiences?.length > 0 && (
            <section className="mb-6">
              <h2 className="text-lg font-bold text-slate-800 mb-3 pb-2 border-b-2 border-blue-500">
                Experience
              </h2>
              {currentResume.experiences.map((exp, i) => (
                <div key={i} className="mb-4">
                  <h3 className="font-semibold text-gray-900">{exp.role}</h3>
                  <p className="text-blue-600 text-sm">{exp.company}</p>
                  <p className="text-gray-500 text-xs mb-2">{exp.start_date} - {exp.end_date || 'Present'}</p>
                  <p className="text-gray-700 text-sm whitespace-pre-line">{exp.description}</p>
                </div>
              ))}
            </section>
          )}

          {currentResume.projects?.length > 0 && (
            <section>
              <h2 className="text-lg font-bold text-slate-800 mb-3 pb-2 border-b-2 border-blue-500">
                Projects
              </h2>
              {currentResume.projects.map((proj, i) => (
                <div key={i} className="mb-3">
                  <h3 className="font-semibold text-gray-900">{proj.title}</h3>
                  <p className="text-gray-700 text-sm whitespace-pre-line">{proj.description}</p>
                  {proj.tech_stack && <p className="text-blue-600 text-xs mt-1">Tech: {proj.tech_stack}</p>}
                  {proj.project_link && (
                    <a href={proj.project_link} target="_blank" rel="noopener noreferrer" className="text-blue-500 text-xs hover:underline mt-1 block">
                      {proj.project_link}
                    </a>
                  )}
                </div>
              ))}
            </section>
          )}
        </div>
      </div>
    </div>
  );

  if (loading || !currentResume) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800">{currentResume.title}</h1>
          <div className="flex gap-3 items-center">
            <select
              value={selectedTemplate}
              onChange={(e) => setSelectedTemplate(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="classic">Classic Template</option>
              <option value="modern">Modern Template</option>
            </select>
            <Button variant="outline" onClick={() => navigate(`/resume/${id}/edit`)}>
              Edit
            </Button>
            <Button variant="outline" onClick={handleGenerateShareLink}>
              Share
            </Button>
            <Button onClick={handleDownloadPDF} loading={downloading}>
              {downloading ? 'Generating...' : 'Download PDF'}
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <div className="bg-white shadow-xl rounded-lg overflow-hidden">
          <div ref={resumeRef}>
            {selectedTemplate === 'classic' ? renderClassicTemplate() : renderModernTemplate()}
          </div>
        </div>

        {shareLink && (
          <div className="bg-blue-50 rounded-xl p-4 mt-8">
            <p className="text-sm text-blue-800 mb-2">Share Link:</p>
            <div className="flex gap-2">
              <input
                type="text"
                value={shareLink}
                readOnly
                className="flex-1 px-3 py-2 bg-white border border-blue-200 rounded-lg"
              />
              <Button
                variant="outline"
                onClick={() => {
                  navigator.clipboard.writeText(shareLink);
                  addToast('Copied to clipboard!', 'success');
                }}
              >
                Copy
              </Button>
            </div>
          </div>
        )}

        <div className="flex justify-center gap-4 mt-8">
          <Button variant="outline" onClick={() => navigate('/dashboard')}>
            Back to Dashboard
          </Button>
          <Button onClick={() => navigate(`/resume/${id}/edit`)}>
            Edit Resume
          </Button>
        </div>
      </div>
    </div>
  );
}
