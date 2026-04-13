import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useResume } from '../context/ResumeContext';
import Button from '../components/Button';
import Spinner from '../components/Spinner';
import Modal from '../components/Modal';
import { useToast } from '../components/ToastProvider';

export default function Dashboard() {
  const { user, loading: authLoading } = useAuth();
  const { resumes, loading: resumesLoading, fetchResumes, deleteResume } = useResume();
  const { addToast } = useToast();
  const navigate = useNavigate();
  const [deleteModal, setDeleteModal] = useState({ open: false, id: null });

  useEffect(() => {
    if (!authLoading && !user) {
      navigate('/login');
    } else if (user) {
      fetchResumes();
    }
  }, [user, authLoading]);

  const handleDelete = async () => {
    try {
      await deleteResume(deleteModal.id);
      addToast('Resume deleted successfully', 'success');
      setDeleteModal({ open: false, id: null });
    } catch (err) {
      addToast('Failed to delete resume', 'error');
    }
  };

  if (authLoading || resumesLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  return (
    <div className="p-6 lg:p-8">
      {/* Page Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Resumes</h1>
          <p className="text-gray-500 mt-1">Manage your resume collection</p>
        </div>
        <Button onClick={() => navigate('/create')}>Create New Resume</Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <p className="text-sm text-gray-500 mb-1">Total Resumes</p>
          <p className="text-3xl font-bold text-gray-900">{resumes.length}</p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <p className="text-sm text-gray-500 mb-1">Active Resumes</p>
          <p className="text-3xl font-bold text-gray-900">{resumes.length}</p>
        </div>
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <p className="text-sm text-gray-500 mb-1">Profile Views</p>
          <p className="text-3xl font-bold text-gray-900">0</p>
        </div>
      </div>

      {resumes.length === 0 ? (
        <div className="bg-white rounded-xl p-12 text-center shadow-sm">
          <div className="text-4xl mb-4">📄</div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No resumes yet</h3>
          <p className="text-gray-500 mb-6">Create your first resume to get started</p>
          <Button onClick={() => navigate('/create')}>Create Resume</Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {resumes.map((resume) => (
            <div key={resume.id} className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="font-semibold text-gray-900">{resume.title}</h3>
                  <p className="text-sm text-gray-500">
                    Created {new Date(resume.created_at).toLocaleDateString()}
                  </p>
                </div>
                <span className="text-2xl">📄</span>
              </div>

              {/* Stats */}
              <div className="flex gap-4 text-sm text-gray-500 mb-4">
                <span>{resume.educations?.length || 0} Education</span>
                <span>{resume.experiences?.length || 0} Experience</span>
                <span>{resume.skills?.length || 0} Skills</span>
              </div>

              {/* Actions */}
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="flex-1"
                  onClick={() => navigate(`/resume/${resume.id}`)}
                >
                  View
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => navigate(`/resume/${resume.id}/edit`)}
                >
                  Edit
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setDeleteModal({ open: true, id: resume.id })}
                >
                  🗑️
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={deleteModal.open}
        onClose={() => setDeleteModal({ open: false, id: null })}
        title="Delete Resume"
      >
        <p className="text-gray-600 mb-6">Are you sure you want to delete this resume? This action cannot be undone.</p>
        <div className="flex gap-3 justify-end">
          <Button variant="secondary" onClick={() => setDeleteModal({ open: false, id: null })}>
            Cancel
          </Button>
          <Button variant="danger" onClick={handleDelete}>
            Delete
          </Button>
        </div>
      </Modal>
    </div>
  );
}