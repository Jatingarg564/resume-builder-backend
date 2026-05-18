import '@testing-library/jest-dom';

// Mock React Router
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: () => ({ id: '1' }),
  useNavigate: () => jest.fn(),
}));

// Mock API
jest.mock('../api', () => ({
  resumeAPI: {
    getAll: jest.fn(),
    getOne: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
    addEducation: jest.fn(),
    updateEducation: jest.fn(),
    addExperience: jest.fn(),
    updateExperience: jest.fn(),
    addSkill: jest.fn(),
    updateSkill: jest.fn(),
    addProject: jest.fn(),
    updateProject: jest.fn(),
    generateShareLink: jest.fn(),
    revokeShareLink: jest.fn(),
  },
  publicAPI: {
    getResume: jest.fn(),
  },
  authAPI: {
    signup: jest.fn(),
    login: jest.fn(),
    getProfile: jest.fn(),
    updateProfile: jest.fn(),
  },
}));

// Mock Toast
jest.mock('../components/ToastProvider', () => ({
  useToast: () => ({
    addToast: jest.fn(),
  }),
}));

// Mock ResumeContext
jest.mock('../context/ResumeContext', () => ({
  useResume: () => ({
    fetchResume: jest.fn(),
    createResume: jest.fn(),
    currentResume: null,
    loading: false,
  }),
}));

// Suppress console errors during tests
global.console = {
  ...console,
  error: jest.fn(),
  warn: jest.fn(),
};
