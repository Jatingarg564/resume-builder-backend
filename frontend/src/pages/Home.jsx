import { Link } from 'react-router-dom';
import Button from '../components/Button';

export default function Home() {
  const features = [
    { icon: '✨', title: 'Easy Resume Creation', desc: 'Build professional resumes in minutes with our intuitive interface.' },
    { icon: '🎨', title: 'Multiple Templates', desc: 'Choose from a variety of beautifully designed templates.' },
    { icon: '🔒', title: 'Secure Storage', desc: 'Your data is safe with us. Access it anywhere, anytime.' },
    { icon: '📥', title: 'Download PDF', desc: 'Export your resume as a polished PDF document.' },
  ];

  const templates = ['classic', 'modern', 'minimal', 'professional'];

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 bg-white/80 backdrop-blur-sm border-b border-gray-100 z-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <span className="text-xl font-bold text-gray-800">ResumeBuilder</span>
          <div className="flex items-center gap-4">
            <Link to="/login">
              <Button variant="ghost">Sign In</Button>
            </Link>
            <Link to="/signup">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 leading-tight mb-6">
            Build Your Resume<br />
            <span className="text-blue-600">Effortlessly</span>
          </h1>
          <p className="text-xl text-gray-500 mb-10 max-w-2xl mx-auto">
            Create a professional resume that stands out. Our easy-to-use builder helps you showcase your skills and land your dream job.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link to="/signup">
              <Button size="lg">Get Started</Button>
            </Link>
            <Link to="/templates">
              <Button size="lg" variant="outline">View Templates</Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Why Choose Us</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((f, i) => (
              <div key={i} className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow">
                <span className="text-3xl mb-4 block">{f.icon}</span>
                <h3 className="font-semibold text-gray-900 mb-2">{f.title}</h3>
                <p className="text-gray-500 text-sm">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Template Preview */}
      <section className="py-20">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-4">Professional Templates</h2>
          <p className="text-gray-500 text-center mb-12">Choose from our collection of carefully crafted templates</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {templates.map((t, i) => (
              <div key={i} className="group cursor-pointer">
                <div className={`aspect-[3/4] rounded-xl border-2 border-gray-200 group-hover:border-blue-500 transition-colors flex items-center justify-center bg-gray-50 ${t === 'classic' ? 'bg-white' : t === 'modern' ? 'bg-gradient-to-br from-blue-50 to-purple-50' : t === 'minimal' ? 'bg-gray-100' : 'bg-slate-50'}`}>
                  <div className="text-center p-4">
                    <div className="w-16 h-2 bg-gray-400 mx-auto mb-2 rounded"></div>
                    <div className="w-12 h-1 bg-gray-300 mx-auto mb-1 rounded"></div>
                    <div className="w-10 h-1 bg-gray-200 mx-auto rounded"></div>
                  </div>
                </div>
                <p className="mt-2 text-center font-medium text-gray-700 capitalize">{t}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-blue-600">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Build Your Resume?</h2>
          <p className="text-blue-100 mb-8">Join thousands of job seekers who have created professional resumes with us.</p>
          <Link to="/signup">
            <Button size="lg" className="bg-blue-700 text-white hover:bg-blue-800">Create Your Resume Now</Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-gray-200">
        <div className="max-w-6xl mx-auto px-4 text-center text-gray-500">
          <p>&copy; 2026 ResumeBuilder. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}