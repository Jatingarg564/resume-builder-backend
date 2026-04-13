import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useResume } from '../context/ResumeContext';
import { resumeAPI } from '../api';
import Button from '../components/Button';
import Input from '../components/Input';
import Spinner from '../components/Spinner';
import { useToast } from '../components/ToastProvider';

const STEPS = ['Basic Info', 'Education', 'Experience', 'Skills', 'Projects'];

export default function ResumeBuilder() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { fetchResume, createResume } = useResume();
  const { addToast } = useToast();
  const isEditing = Boolean(id);

  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [resumeId, setResumeId] = useState(id || null);

  const [formData, setFormData] = useState({
    title: '',
    educations: [{ degree: '', institution: '', start_year: '', end_year: '' }],
    experiences: [{ company: '', role: '', start_date: '', end_date: '', description: '' }],
    skills: [{ name: '' }],
    projects: [{ title: '', description: '', tech_stack: '', project_link: '' }],
  });

  useEffect(() => {
    if (isEditing && id) {
      loadResume(id);
    }
  }, [id]);

  const loadResume = async (resumeId) => {
    setLoading(true);
    try {
      const data = await fetchResume(resumeId);
      if (data) {
        setFormData({
          title: data.title || '',
          educations: data.educations?.length > 0 ? data.educations : [{ degree: '', institution: '', start_year: '', end_year: '' }],
          experiences: data.experiences?.length > 0 ? data.experiences : [{ company: '', role: '', start_date: '', end_date: '', description: '' }],
          skills: data.skills?.length > 0 ? data.skills : [{ name: '' }],
          projects: data.projects?.length > 0 ? data.projects : [{ title: '', description: '', tech_stack: '', project_link: '' }],
        });
        setResumeId(data.id);
      }
    } catch (err) {
      addToast('Failed to load resume', 'error');
    } finally {
      setLoading(false);
    }
  };

  const updateFormData = (section, index, field, value) => {
    setFormData(prev => ({
      ...prev,
      [section]: prev[section].map((item, i) =>
        i === index ? { ...item, [field]: value } : item
      ),
    }));
  };

  const addItem = (section, template) => {
    setFormData(prev => ({
      ...prev,
      [section]: [...prev[section], { ...template }],
    }));
  };

  const removeItem = (section, index) => {
    if (formData[section].length > 1) {
      setFormData(prev => ({
        ...prev,
        [section]: prev[section].filter((_, i) => i !== index),
      }));
    }
  };

  const handleNext = async () => {
    if (currentStep === 0) {
      if (!formData.title.trim()) {
        addToast('Please enter a resume title', 'error');
        return;
      }
      setLoading(true);
      try {
        if (!resumeId) {
          const resume = await createResume({ title: formData.title });
          setResumeId(resume.id);
        }
        setCurrentStep(1);
      } catch (err) {
        addToast('Failed to save resume', 'error');
      } finally {
        setLoading(false);
      }
    } else {
      setCurrentStep(prev => Math.min(prev + 1, STEPS.length - 1));
    }
  };

  const handleBack = () => {
    setCurrentStep(prev => Math.max(prev - 1, 0));
  };

  const handleSaveSection = async () => {
    if (!resumeId) {
      addToast('Please save basic info first', 'error');
      return;
    }

    setLoading(true);
    try {
      const section = STEPS[currentStep].toLowerCase();
      const data = formData[`${section}`];

      for (const item of data) {
        const hasData = Object.values(item).some(v => v && v.trim());
        if (!hasData) continue;

        if (item.id) {
          if (section === 'education') await resumeAPI.updateEducation(item.id, item);
          else if (section === 'experience') await resumeAPI.updateExperience(item.id, item);
          else if (section === 'projects') await resumeAPI.updateProject(item.id, item);
        } else {
          if (section === 'education') await resumeAPI.addEducation(resumeId, item);
          else if (section === 'experience') await resumeAPI.addExperience(resumeId, item);
          else if (section === 'skills') {
            if (item.name?.trim()) await resumeAPI.addSkill(resumeId, { name: item.name });
          }
          else if (section === 'projects') await resumeAPI.addProject(resumeId, item);
        }
      }

      addToast('Section saved successfully', 'success');
      if (currentStep === STEPS.length - 1) {
        navigate('/dashboard');
      }
    } catch (err) {
      addToast('Failed to save section', 'error');
    } finally {
      setLoading(false);
    }
  };

  const renderStep = () => {
    switch (currentStep) {
      case 0:
        return (
          <div className="space-y-6">
            <Input
              label="Resume Title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="e.g., Software Engineer Resume"
              required
            />
          </div>
        );

      case 1:
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Education</h3>
            {formData.educations.map((edu, i) => (
              <div key={i} className="bg-gray-50 rounded-lg p-4 space-y-4">
                <div className="flex justify-between items-center">
                  <span className="font-medium text-gray-700">Education {i + 1}</span>
                  {formData.educations.length > 1 && (
                    <button onClick={() => removeItem('educations', i)} className="text-red-500 hover:text-red-700">Remove</button>
                  )}
                </div>
                <Input
                  label="Degree"
                  value={edu.degree}
                  onChange={(e) => updateFormData('educations', i, 'degree', e.target.value)}
                  placeholder="e.g., Bachelor of Science"
                />
                <Input
                  label="Institution"
                  value={edu.institution}
                  onChange={(e) => updateFormData('educations', i, 'institution', e.target.value)}
                  placeholder="e.g., MIT"
                />
                <div className="grid grid-cols-2 gap-4">
                  <Input
                    label="Start Year"
                    type="number"
                    value={edu.start_year}
                    onChange={(e) => updateFormData('educations', i, 'start_year', e.target.value)}
                    placeholder="2020"
                  />
                  <Input
                    label="End Year"
                    type="number"
                    value={edu.end_year}
                    onChange={(e) => updateFormData('educations', i, 'end_year', e.target.value)}
                    placeholder="2024"
                  />
                </div>
              </div>
            ))}
            <Button variant="outline" onClick={() => addItem('educations', { degree: '', institution: '', start_year: '', end_year: '' })}>
              + Add Education
            </Button>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Experience</h3>
            {formData.experiences.map((exp, i) => (
              <div key={i} className="bg-gray-50 rounded-lg p-4 space-y-4">
                <div className="flex justify-between items-center">
                  <span className="font-medium text-gray-700">Experience {i + 1}</span>
                  {formData.experiences.length > 1 && (
                    <button onClick={() => removeItem('experiences', i)} className="text-red-500 hover:text-red-700">Remove</button>
                  )}
                </div>
                <Input
                  label="Company"
                  value={exp.company}
                  onChange={(e) => updateFormData('experiences', i, 'company', e.target.value)}
                  placeholder="e.g., Google"
                />
                <Input
                  label="Role"
                  value={exp.role}
                  onChange={(e) => updateFormData('experiences', i, 'role', e.target.value)}
                  placeholder="e.g., Software Engineer"
                />
                <div className="grid grid-cols-2 gap-4">
                  <Input
                    label="Start Date"
                    value={exp.start_date}
                    onChange={(e) => updateFormData('experiences', i, 'start_date', e.target.value)}
                    placeholder="Jan 2020"
                  />
                  <Input
                    label="End Date"
                    value={exp.end_date}
                    onChange={(e) => updateFormData('experiences', i, 'end_date', e.target.value)}
                    placeholder="Present"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={exp.description}
                    onChange={(e) => updateFormData('experiences', i, 'description', e.target.value)}
                    placeholder="Describe your responsibilities and achievements..."
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            ))}
            <Button variant="outline" onClick={() => addItem('experiences', { company: '', role: '', start_date: '', end_date: '', description: '' })}>
              + Add Experience
            </Button>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Skills</h3>
            <p className="text-gray-500 text-sm">Add skills relevant to your resume</p>
            {formData.skills.map((skill, i) => (
              <div key={i} className="flex gap-4 items-end">
                <div className="flex-1">
                  <Input
                    label={i === 0 ? 'Skill Name' : ''}
                    value={skill.name}
                    onChange={(e) => updateFormData('skills', i, 'name', e.target.value)}
                    placeholder="e.g., Python, JavaScript, React"
                  />
                </div>
                {formData.skills.length > 1 && (
                  <button onClick={() => removeItem('skills', i)} className="text-red-500 hover:text-red-700 pb-2">Remove</button>
                )}
              </div>
            ))}
            <Button variant="outline" onClick={() => addItem('skills', { name: '' })}>
              + Add Skill
            </Button>
          </div>
        );

      case 4:
        return (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold">Projects</h3>
            {formData.projects.map((proj, i) => (
              <div key={i} className="bg-gray-50 rounded-lg p-4 space-y-4">
                <div className="flex justify-between items-center">
                  <span className="font-medium text-gray-700">Project {i + 1}</span>
                  {formData.projects.length > 1 && (
                    <button onClick={() => removeItem('projects', i)} className="text-red-500 hover:text-red-700">Remove</button>
                  )}
                </div>
                <Input
                  label="Project Title"
                  value={proj.title}
                  onChange={(e) => updateFormData('projects', i, 'title', e.target.value)}
                  placeholder="e.g., E-commerce Platform"
                />
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={proj.description}
                    onChange={(e) => updateFormData('projects', i, 'description', e.target.value)}
                    placeholder="Describe what the project does and your contribution..."
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <Input
                    label="Tech Stack"
                    value={proj.tech_stack}
                    onChange={(e) => updateFormData('projects', i, 'tech_stack', e.target.value)}
                    placeholder="e.g., React, Node.js, MongoDB"
                  />
                  <Input
                    label="Project Link"
                    value={proj.project_link}
                    onChange={(e) => updateFormData('projects', i, 'project_link', e.target.value)}
                    placeholder="https://github.com/..."
                  />
                </div>
              </div>
            ))}
            <Button variant="outline" onClick={() => addItem('projects', { title: '', description: '', tech_stack: '', project_link: '' })}>
              + Add Project
            </Button>
          </div>
        );

      default:
        return null;
    }
  };

  if (loading && isEditing && !formData.title) {
    return <div className="flex items-center justify-center min-h-screen"><Spinner size="lg" /></div>;
  }

  return (
    <div className="p-6 lg:p-8">
      {/* Page Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          {isEditing ? 'Edit Resume' : 'Create Resume'}
        </h1>
        <p className="text-gray-500 mt-1">Fill in the details for your resume</p>
      </div>

      {/* Progress Steps */}
      <div className="mb-8">
        <div className="flex items-center justify-between max-w-xl">
          {STEPS.map((step, i) => (
            <div key={step} className="flex items-center">
              <div className={`
                w-8 h-8 rounded-full flex items-center justify-center font-medium text-sm
                ${i <= currentStep ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'}
              `}>
                {i + 1}
              </div>
              {i < STEPS.length - 1 && (
                <div className={`w-12 sm:w-16 h-1 ${i < currentStep ? 'bg-blue-600' : 'bg-gray-200'}`} />
              )}
            </div>
          ))}
        </div>
        <div className="flex justify-between mt-2 max-w-xl text-xs sm:text-sm">
          {STEPS.map((step, i) => (
            <span key={step} className={`${i === currentStep ? 'text-blue-600 font-medium' : 'text-gray-400'}`}>
              {step}
            </span>
          ))}
        </div>
      </div>

      {/* Form */}
      <div className="bg-white rounded-xl shadow-sm p-6 max-w-2xl">
        <h2 className="text-xl font-semibold mb-6">{STEPS[currentStep]}</h2>
        {renderStep()}

        {/* Navigation */}
        <div className="flex justify-between mt-8 pt-6 border-t border-gray-100">
          <Button
            variant="outline"
            onClick={handleBack}
            disabled={currentStep === 0}
          >
            Back
          </Button>
          <div className="flex gap-3">
            {currentStep > 0 && (
              <Button variant="secondary" onClick={handleSaveSection} loading={loading}>
                Save & Continue
              </Button>
            )}
            <Button onClick={handleNext} loading={loading}>
              {currentStep === STEPS.length - 1 ? 'Complete' : 'Next'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}