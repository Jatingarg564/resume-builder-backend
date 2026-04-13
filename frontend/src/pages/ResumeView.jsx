import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useResume } from '../context/ResumeContext';
import { resumeAPI } from '../api';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import { useToast } from '../components/ToastProvider';

export default function ResumeView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { fetchResume, currentResume, loading } = useResume();
  const { addToast } = useToast();
  const [shareLink, setShareLink] = useState('');

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

  if (loading || !currentResume) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  const resume = currentResume;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800">{resume.title}</h1>
          <div className="flex gap-3">
            <Button variant="outline" onClick={() => navigate(`/resume/${id}/edit`)}>
              Edit Resume
            </Button>
            <Button onClick={handleGenerateShareLink}>
              Share
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-8">
        {/* Resume Preview */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          {/* Header */}
          <div className="text-center mb-8 pb-6 border-b border-gray-200">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{resume.title}</h1>
            <p className="text-gray-500">Resume Preview</p>
          </div>

          {/* Education */}
          {resume.educations?.length > 0 && (
            <section className="mb-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">Education</h2>
              {resume.educations.map((edu, i) => (
                <div key={i} className="mb-4">
                  <h3 className="font-medium text-gray-800">{edu.degree}</h3>
                  <p className="text-gray-600">{edu.institution}</p>
                  <p className="text-sm text-gray-500">{edu.start_year} - {edu.end_year || 'Present'}</p>
                </div>
              ))}
            </section>
          )}

          {/* Experience */}
          {resume.experiences?.length > 0 && (
            <section className="mb-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">Experience</h2>
              {resume.experiences.map((exp, i) => (
                <div key={i} className="mb-4">
                  <h3 className="font-medium text-gray-800">{exp.role} at {exp.company}</h3>
                  <p className="text-sm text-gray-500">{exp.start_date} - {exp.end_date || 'Present'}</p>
                  <p className="text-gray-600 mt-2">{exp.description}</p>
                </div>
              ))}
            </section>
          )}

          {/* Skills */}
          {resume.skills?.length > 0 && (
            <section className="mb-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">Skills</h2>
              <div className="flex flex-wrap gap-2">
                {resume.skills.map((skill, i) => (
                  <span key={i} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
                    {skill.name}
                  </span>
                ))}
              </div>
            </section>
          )}

          {/* Projects */}
          {resume.projects?.length > 0 && (
            <section>
              <h2 className="text-lg font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">Projects</h2>
              {resume.projects.map((proj, i) => (
                <div key={i} className="mb-4">
                  <h3 className="font-medium text-gray-800">{proj.title}</h3>
                  <p className="text-gray-600">{proj.description}</p>
                  {proj.tech_stack && <p className="text-sm text-gray-500 mt-1">Tech: {proj.tech_stack}</p>}
                  {proj.project_link && (
                    <a href={proj.project_link} target="_blank" rel="noopener noreferrer" className="text-blue-600 text-sm hover:underline mt-1 block">
                      View Project
                    </a>
                  )}
                </div>
              ))}
            </section>
          )}
        </div>

        {/* Share Link */}
        {shareLink && (
          <div className="bg-blue-50 rounded-xl p-4 mb-8">
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

        {/* Actions */}
        <div className="flex justify-center gap-4">
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