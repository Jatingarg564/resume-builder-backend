import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { publicAPI } from '../api';
import Spinner from '../components/Spinner';

export default function PublicShareView() {
  const { shareCode } = useParams();
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedTemplate, setSelectedTemplate] = useState('classic');

  useEffect(() => {
    loadResume();
  }, [shareCode]);

  const loadResume = async () => {
    try {
      const response = await publicAPI.getResume(shareCode);
      setResume(response.data);
    } catch (err) {
      setError('Resume not found or has been made private');
    } finally {
      setLoading(false);
    }
  };

  const renderClassicTemplate = () => (
    <div className="bg-white p-8 font-serif max-w-[800px] mx-auto shadow-lg">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">{resume.title}</h1>
        <p className="text-gray-600">Professional Resume</p>
      </div>

      {resume.educations?.length > 0 && (
        <section className="mb-6">
          <h2 className="text-lg font-bold text-gray-900 mb-3 pb-1 border-b-2 border-gray-300 uppercase tracking-wide">
            Education
          </h2>
          {resume.educations.map((edu, i) => (
            <div key={i} className="mb-3">
              <h3 className="font-semibold text-gray-800">{edu.degree}</h3>
              <p className="text-gray-600">{edu.institution}</p>
              <p className="text-sm text-gray-500">{edu.start_year} - {edu.end_year || 'Present'}</p>
            </div>
          ))}
        </section>
      )}

      {resume.experiences?.length > 0 && (
        <section className="mb-6">
          <h2 className="text-lg font-bold text-gray-900 mb-3 pb-1 border-b-2 border-gray-300 uppercase tracking-wide">
            Experience
          </h2>
          {resume.experiences.map((exp, i) => (
            <div key={i} className="mb-3">
              <h3 className="font-semibold text-gray-800">{exp.role}</h3>
              <p className="text-gray-600">{exp.company}</p>
              <p className="text-sm text-gray-500 mb-1">{exp.start_date} - {exp.end_date || 'Present'}</p>
              <p className="text-gray-700 text-sm whitespace-pre-line">{exp.description}</p>
            </div>
          ))}
        </section>
      )}

      {resume.skills?.length > 0 && (
        <section className="mb-6">
          <h2 className="text-lg font-bold text-gray-900 mb-3 pb-1 border-b-2 border-gray-300 uppercase tracking-wide">
            Skills
          </h2>
          <div className="flex flex-wrap gap-2">
            {resume.skills.map((skill, i) => (
              <span key={i} className="px-3 py-1 bg-gray-100 text-gray-700 rounded text-sm border border-gray-300">
                {skill.name}
              </span>
            ))}
          </div>
        </section>
      )}

      {resume.projects?.length > 0 && (
        <section>
          <h2 className="text-lg font-bold text-gray-900 mb-3 pb-1 border-b-2 border-gray-300 uppercase tracking-wide">
            Projects
          </h2>
          {resume.projects.map((proj, i) => (
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
    <div className="bg-white p-8 font-sans max-w-[800px] mx-auto shadow-lg">
      <div className="grid grid-cols-[1fr_2fr] gap-6">
        <div className="bg-gradient-to-br from-slate-800 to-slate-700 text-white p-6 rounded-lg">
          <h1 className="text-2xl font-bold mb-1">{resume.title}</h1>
          <p className="text-slate-300 text-sm mb-6">Professional Resume</p>

          {resume.skills?.length > 0 && (
            <div className="mb-6">
              <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">Skills</h2>
              <div className="space-y-2">
                {resume.skills.map((skill, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                    <span className="text-sm">{skill.name}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {resume.educations?.length > 0 && (
            <div>
              <h2 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-3">Education</h2>
              {resume.educations.map((edu, i) => (
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
          {resume.experiences?.length > 0 && (
            <section className="mb-6">
              <h2 className="text-lg font-bold text-slate-800 mb-3 pb-2 border-b-2 border-blue-500">
                Experience
              </h2>
              {resume.experiences.map((exp, i) => (
                <div key={i} className="mb-4">
                  <h3 className="font-semibold text-gray-900">{exp.role}</h3>
                  <p className="text-blue-600 text-sm">{exp.company}</p>
                  <p className="text-gray-500 text-xs mb-2">{exp.start_date} - {exp.end_date || 'Present'}</p>
                  <p className="text-gray-700 text-sm whitespace-pre-line">{exp.description}</p>
                </div>
              ))}
            </section>
          )}

          {resume.projects?.length > 0 && (
            <section>
              <h2 className="text-lg font-bold text-slate-800 mb-3 pb-2 border-b-2 border-blue-500">
                Projects
              </h2>
              {resume.projects.map((proj, i) => (
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Resume Not Found</h1>
          <p className="text-gray-500">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="text-center mb-6">
          <div className="flex items-center justify-center gap-4">
            <select
              value={selectedTemplate}
              onChange={(e) => setSelectedTemplate(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
            >
              <option value="classic">Classic Template</option>
              <option value="modern">Modern Template</option>
            </select>
          </div>
        </div>

        <div className="bg-white shadow-xl rounded-lg overflow-hidden">
          {selectedTemplate === 'classic' ? renderClassicTemplate() : renderModernTemplate()}
        </div>

        <div className="text-center mt-6 text-sm text-gray-500">
          Created with Resume Builder
        </div>
      </div>
    </div>
  );
}
