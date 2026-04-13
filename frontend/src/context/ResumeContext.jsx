import { createContext, useContext, useState, useEffect } from 'react';
import { resumeAPI } from '../api';

const ResumeContext = createContext(null);

export const ResumeProvider = ({ children }) => {
  const [resumes, setResumes] = useState([]);
  const [currentResume, setCurrentResume] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchResumes = async () => {
    setLoading(true);
    try {
      const response = await resumeAPI.getAll();
      setResumes(response.data);
    } catch (error) {
      console.error('Failed to fetch resumes:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchResume = async (id) => {
    setLoading(true);
    try {
      const response = await resumeAPI.getOne(id);
      setCurrentResume(response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch resume:', error);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const createResume = async (data) => {
    try {
      const response = await resumeAPI.create(data);
      setResumes(prev => [...prev, response.data]);
      return response.data;
    } catch (error) {
      console.error('Failed to create resume:', error);
      throw error;
    }
  };

  const updateResume = async (id, data) => {
    try {
      const response = await resumeAPI.update(id, data);
      setResumes(prev => prev.map(r => r.id === id ? response.data : r));
      if (currentResume?.id === id) {
        setCurrentResume(response.data);
      }
      return response.data;
    } catch (error) {
      console.error('Failed to update resume:', error);
      throw error;
    }
  };

  const deleteResume = async (id) => {
    try {
      await resumeAPI.delete(id);
      setResumes(prev => prev.filter(r => r.id !== id));
      if (currentResume?.id === id) {
        setCurrentResume(null);
      }
    } catch (error) {
      console.error('Failed to delete resume:', error);
      throw error;
    }
  };

  return (
    <ResumeContext.Provider value={{
      resumes,
      currentResume,
      loading,
      fetchResumes,
      fetchResume,
      createResume,
      updateResume,
      deleteResume,
      setCurrentResume
    }}>
      {children}
    </ResumeContext.Provider>
  );
};

export const useResume = () => {
  const context = useContext(ResumeContext);
  if (!context) {
    throw new Error('useResume must be used within ResumeProvider');
  }
  return context;
};