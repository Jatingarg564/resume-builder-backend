import { useNavigate } from 'react-router-dom';
import Button from '../components/Button';

const PLANS = [
  {
    name: 'Free',
    price: '$0',
    period: 'forever',
    features: [
      'Create up to 3 resumes',
      'Basic templates',
      'PDF export (watermark)',
      'Email support',
    ],
    buttonText: 'Get Started',
    popular: false,
  },
  {
    name: 'Pro',
    price: '$9',
    period: 'per month',
    features: [
      'Unlimited resumes',
      'All templates',
      'No watermark',
      'Priority support',
      'Custom colors',
    ],
    buttonText: 'Upgrade to Pro',
    popular: true,
  },
  {
    name: 'Premium',
    price: '$19',
    period: 'per month',
    features: [
      'Everything in Pro',
      'AI resume enhancement',
      'Multiple share links',
      'Analytics dashboard',
      'Cover letter builder',
      '24/7 support',
    ],
    buttonText: 'Go Premium',
    popular: false,
  },
];

export default function Pricing() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-gray-800">Pricing</h1>
          <Button variant="ghost" onClick={() => navigate('/dashboard')}>Back to Dashboard</Button>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">Simple, Transparent Pricing</h2>
          <p className="text-xl text-gray-500">Choose the plan that fits your needs</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {PLANS.map((plan) => (
            <div
              key={plan.name}
              className={`
                bg-white rounded-2xl p-8 shadow-sm
                ${plan.popular ? 'ring-2 ring-blue-500 relative' : ''}
              `}
            >
              {plan.popular && (
                <span className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-blue-500 text-white text-xs font-medium px-3 py-1 rounded-full">
                  Most Popular
                </span>
              )}

              <div className="text-center mb-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{plan.name}</h3>
                <div className="flex items-baseline justify-center">
                  <span className="text-4xl font-bold text-gray-900">{plan.price}</span>
                  <span className="text-gray-500 ml-1">/{plan.period}</span>
                </div>
              </div>

              <ul className="space-y-3 mb-8">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-center text-gray-600">
                    <svg className="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>

              <Button
                variant={plan.popular ? 'primary' : 'outline'}
                className="w-full"
                onClick={() => {
                  if (plan.name === 'Free') {
                    navigate('/signup');
                  } else {
                    // Would open payment modal in production
                    alert('Payment integration would go here');
                  }
                }}
              >
                {plan.buttonText}
              </Button>
            </div>
          ))}
        </div>

        {/* FAQ */}
        <div className="mt-16">
          <h3 className="text-2xl font-bold text-center mb-8">Frequently Asked Questions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            <div className="bg-white rounded-xl p-6">
              <h4 className="font-semibold text-gray-900 mb-2">Can I cancel anytime?</h4>
              <p className="text-gray-500">Yes, you can cancel your subscription at any time. Your data will be preserved.</p>
            </div>
            <div className="bg-white rounded-xl p-6">
              <h4 className="font-semibold text-gray-900 mb-2">Is my data secure?</h4>
              <p className="text-gray-500">Absolutely. We use industry-standard encryption to protect your data.</p>
            </div>
            <div className="bg-white rounded-xl p-6">
              <h4 className="font-semibold text-gray-900 mb-2">Do you offer refunds?</h4>
              <p className="text-gray-500">Yes, we offer a 30-day money-back guarantee on all paid plans.</p>
            </div>
            <div className="bg-white rounded-xl p-6">
              <h4 className="font-semibold text-gray-900 mb-2">Can I upgrade later?</h4>
              <p className="text-gray-500">Of course! You can upgrade or downgrade your plan at any time.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}