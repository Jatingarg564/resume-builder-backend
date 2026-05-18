import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ResumeBuilder from '../pages/ResumeBuilder';
import { useResume } from '../context/ResumeContext';
import { useToast } from '../components/ToastProvider';

// Mock the hooks
jest.mock('../context/ResumeContext', () => ({
  useResume: jest.fn(),
}));

jest.mock('../components/ToastProvider', () => ({
  useToast: jest.fn(),
}));

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('ResumeBuilder', () => {
  const mockAddToast = jest.fn();
  const mockFetchResume = jest.fn();
  const mockCreateResume = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    useResume.mockReturnValue({
      fetchResume: mockFetchResume,
      createResume: mockCreateResume,
      currentResume: null,
      loading: false,
    });
    useToast.mockReturnValue({ addToast: mockAddToast });
  });

  describe('Basic Info Step', () => {
    test('should display resume title input on first step', () => {
      renderWithRouter(<ResumeBuilder />);

      expect(screen.getByLabelText(/resume title/i)).toBeInTheDocument();
      expect(screen.getByText('Basic Info')).toBeInTheDocument();
    });

    test('should show error when title is empty and clicking Next', () => {
      renderWithRouter(<ResumeBuilder />);

      const nextButton = screen.getByText('Next');
      fireEvent.click(nextButton);

      expect(mockAddToast).toHaveBeenCalledWith('Please enter a resume title', 'error');
    });

    test('should proceed to next step when title is entered', async () => {
      mockCreateResume.mockResolvedValue({ id: '1' });
      renderWithRouter(<ResumeBuilder />);

      const titleInput = screen.getByLabelText(/resume title/i);
      fireEvent.change(titleInput, { target: { value: 'Software Engineer Resume' } });

      const nextButton = screen.getByText('Next');
      fireEvent.click(nextButton);

      await waitFor(() => {
        expect(screen.getByText('Education')).toBeInTheDocument();
      });
    });
  });

  describe('Education Step', () => {
    test('should display education form fields', async () => {
      mockCreateResume.mockResolvedValue({ id: '1' });
      renderWithRouter(<ResumeBuilder />);

      // Fill title and go to next step
      const titleInput = screen.getByLabelText(/resume title/i);
      fireEvent.change(titleInput, { target: { value: 'Test Resume' } });
      fireEvent.click(screen.getByText('Next'));

      await waitFor(() => {
        expect(screen.getByLabelText(/degree/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/institution/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/start year/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/end year/i)).toBeInTheDocument();
      });
    });

    test('should add new education entry when clicking Add Education', async () => {
      mockCreateResume.mockResolvedValue({ id: '1' });
      renderWithRouter(<ResumeBuilder />);

      const titleInput = screen.getByLabelText(/resume title/i);
      fireEvent.change(titleInput, { target: { value: 'Test Resume' } });
      fireEvent.click(screen.getByText('Next'));

      await waitFor(() => {
        expect(screen.getByText('+ Add Education')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByText('+ Add Education'));

      // Should now have 2 education entries
      expect(screen.getAllByLabelText(/degree/i)).toHaveLength(2);
    });
  });

  describe('Experience Step', () => {
    test('should display experience form fields', async () => {
      mockCreateResume.mockResolvedValue({ id: '1' });
      renderWithRouter(<ResumeBuilder />);

      const titleInput = screen.getByLabelText(/resume title/i);
      fireEvent.change(titleInput, { target: { value: 'Test Resume' } });
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Next'));

      await waitFor(() => {
        expect(screen.getByLabelText(/company/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/role/i)).toBeInTheDocument();
      });
    });
  });

  describe('Skills Step', () => {
    test('should display skills form and allow adding multiple skills', async () => {
      mockCreateResume.mockResolvedValue({ id: '1' });
      renderWithRouter(<ResumeBuilder />);

      const titleInput = screen.getByLabelText(/resume title/i);
      fireEvent.change(titleInput, { target: { value: 'Test Resume' } });
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Next'));

      await waitFor(() => {
        expect(screen.getByPlaceholderText(/e\.g\., Python, JavaScript/i)).toBeInTheDocument();
      });

      fireEvent.click(screen.getByText('+ Add Skill'));

      expect(screen.getAllByPlaceholderText(/e\.g\., Python, JavaScript/i)).toHaveLength(2);
    });
  });

  describe('Projects Step', () => {
    test('should display projects form fields', async () => {
      mockCreateResume.mockResolvedValue({ id: '1' });
      renderWithRouter(<ResumeBuilder />);

      const titleInput = screen.getByLabelText(/resume title/i);
      fireEvent.change(titleInput, { target: { value: 'Test Resume' } });
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Next'));
      fireEvent.click(screen.getByText('Next'));

      await waitFor(() => {
        expect(screen.getByLabelText(/project title/i)).toBeInTheDocument();
      });
    });
  });

  describe('Navigation', () => {
    test('should navigate back to previous step', async () => {
      mockCreateResume.mockResolvedValue({ id: '1' });
      renderWithRouter(<ResumeBuilder />);

      // Go to Education step
      const titleInput = screen.getByLabelText(/resume title/i);
      fireEvent.change(titleInput, { target: { value: 'Test Resume' } });
      fireEvent.click(screen.getByText('Next'));

      await waitFor(() => {
        expect(screen.getByText('Education')).toBeInTheDocument();
      });

      // Go back
      fireEvent.click(screen.getByText('Back'));

      expect(screen.getByText('Basic Info')).toBeInTheDocument();
    });

    test('should disable Back button on first step', () => {
      renderWithRouter(<ResumeBuilder />);

      const backButton = screen.getByText('Back');
      expect(backButton).toBeDisabled();
    });
  });
});
