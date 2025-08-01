'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import BottomNavigation from '@/components/BottomNavigation';
import ImageUpload from '@/components/ImageUpload';

interface FormData {
  // Basic Info
  name: string;
  short_description: string;
  description: string;
  certifying_agency: string;
  kosher_category: 'meat' | 'dairy' | 'pareve' | '';
  
  // Kosher Info
  is_cholov_yisroel?: boolean;
  is_pas_yisroel?: boolean;
  kosher_cert_link: string;
  
  // Contact & Location
  phone: string;
  email: string;
  address: string;
  website: string;
  google_listing_url: string;
  
  // Business Info
  hours_open: string;
  price_range: string;
  
  // Images
  image_url: string;
  
  // Owner Info
  owner_name: string;
  owner_email: string;
  owner_phone: string;
}

interface FormErrors {
  [key: string]: string;
}

export default function AddEateryPage() {
  const router = useRouter();
  const [userType, setUserType] = useState<'owner' | 'community' | ''>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  
  const [formData, setFormData] = useState<FormData>({
    name: '',
    short_description: '',
    description: '',
    certifying_agency: '',
    kosher_category: '',
    kosher_cert_link: '',
    phone: '',
    email: '',
    address: '',
    website: '',
    google_listing_url: '',
    hours_open: '',
    price_range: '',
    image_url: '',
    owner_name: '',
    owner_email: '',
    owner_phone: ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    
    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData(prev => ({
        ...prev,
        [name]: checked
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    // Required fields
    if (!formData.name.trim()) newErrors.name = 'Restaurant name is required';
    if (!formData.short_description.trim()) newErrors.short_description = 'Short description is required';
    if (formData.short_description.length > 80) newErrors.short_description = 'Short description must be 80 characters or less';
    if (!formData.certifying_agency) newErrors.certifying_agency = 'Certifying agency is required';
    if (!formData.kosher_category) newErrors.kosher_category = 'Kosher category is required';
    if (!formData.phone.trim()) newErrors.phone = 'Phone number is required';
    if (!formData.address.trim()) newErrors.address = 'Address is required';
    if (!formData.hours_open.trim()) newErrors.hours_open = 'Hours are required';
    if (!formData.image_url) newErrors.image_url = 'Restaurant image is required';

    // Conditional validation
    if (formData.kosher_category === 'dairy' && formData.is_cholov_yisroel === undefined) {
      newErrors.is_cholov_yisroel = 'Please specify if this is Chalav Yisrael or Chalav Stam';
    }
    if (['meat', 'pareve'].includes(formData.kosher_category) && formData.is_pas_yisroel === undefined) {
      newErrors.is_pas_yisroel = 'Please specify if this is Pas Yisroel';
    }

    // Owner info validation
    if (userType === 'owner') {
      if (!formData.owner_name.trim()) newErrors.owner_name = 'Owner name is required';
      if (!formData.owner_email.trim()) newErrors.owner_email = 'Owner email is required';
      if (!formData.owner_phone.trim()) newErrors.owner_phone = 'Owner phone is required';
    }

    // URL validation
    if (formData.website && !isValidUrl(formData.website)) {
      newErrors.website = 'Please enter a valid website URL';
    }
    if (formData.google_listing_url && !isValidUrl(formData.google_listing_url)) {
      newErrors.google_listing_url = 'Please enter a valid Google Maps URL';
    }
    if (formData.kosher_cert_link && !isValidUrl(formData.kosher_cert_link)) {
      newErrors.kosher_cert_link = 'Please enter a valid certification URL';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const isValidUrl = (url: string): boolean => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!userType) {
      alert('Please select whether you own this establishment or are adding it to the community.');
      return;
    }
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const submissionData = {
        ...formData,
        user_type: userType,
        category: 'restaurant',
        owner_info: userType === 'owner' ? {
          name: formData.owner_name,
          email: formData.owner_email,
          phone: formData.owner_phone
        } : undefined
      };

      const response = await fetch('/api/restaurants', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(submissionData),
      });

      const result = await response.json();

      if (result.success) {
        // Show success message
        alert(userType === 'owner' 
          ? 'Thank you! Your establishment has been submitted for review. We will contact you soon to verify your ownership and complete the listing process.'
          : 'Thank you! Your submission has been received and will be reviewed by our team. We will verify the information before adding it to the directory.'
        );
        
        // Redirect to home page
        router.push('/');
      } else {
        // Handle validation errors from API
        if (result.errors) {
          const apiErrors: FormErrors = {};
          result.errors.forEach((error: { path: string[]; message: string }) => {
            apiErrors[error.path[0]] = error.message;
          });
          setErrors(apiErrors);
        } else {
          alert('Failed to submit restaurant. Please try again.');
        }
      }
    } catch (error) {
      console.error('Submission error:', error);
      alert('An error occurred while submitting. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getErrorClass = (fieldName: string) => {
    return errors[fieldName] ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 focus:ring-jewgo-primary';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header />
      
      {/* Content */}
      <div className="px-4 py-6 pb-24">
        <div className="max-w-2xl mx-auto">
          {/* Page Header */}
          <div className="text-center mb-8">
            <div className="text-4xl mb-4">🏪</div>
            <h1 className="text-2xl font-bold text-gray-800 mb-2">Add a New Eatery</h1>
            <p className="text-gray-600">Help the community by adding a kosher establishment</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6 space-y-6">
            {/* User Type Selection */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Who are you?</h3>
              <div className="space-y-3">
                <label className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                  <input
                    type="radio"
                    name="userType"
                    value="owner"
                    checked={userType === 'owner'}
                    onChange={(e) => setUserType(e.target.value as 'owner')}
                    className="mr-3 text-jewgo-primary focus:ring-jewgo-primary"
                  />
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">👨‍💼</span>
                      <div>
                        <div className="font-medium text-gray-900">I own this establishment</div>
                        <div className="text-sm text-gray-600">I&apos;m the owner or manager and want to list my business</div>
                      </div>
                    </div>
                  </div>
                </label>

                <label className="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
                  <input
                    type="radio"
                    name="userType"
                    value="community"
                    checked={userType === 'community'}
                    onChange={(e) => setUserType(e.target.value as 'community')}
                    className="mr-3 text-jewgo-primary focus:ring-jewgo-primary"
                  />
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">🤝</span>
                      <div>
                        <div className="font-medium text-gray-900">I want to add it to the community</div>
                        <div className="text-sm text-gray-600">I found a kosher establishment that should be listed</div>
                      </div>
                    </div>
                  </div>
                </label>
              </div>
              
              {userType && (
                <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <div className="flex items-start space-x-2">
                    <span className="text-blue-500 mt-0.5">ℹ️</span>
                    <div className="text-sm text-blue-800">
                      {userType === 'owner' ? (
                        <>
                          <strong>Owner submission:</strong> We&apos;ll contact you to verify ownership and help you set up your listing with additional features like menu updates and special announcements.
                        </>
                      ) : (
                        <>
                          <strong>Community submission:</strong> We&apos;ll review and verify the information before adding it to our directory. Thank you for helping the community!
                        </>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Owner Information (only show if user is owner) */}
            {userType === 'owner' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Owner Information</h3>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Your Name *
                      </label>
                      <input
                        type="text"
                        name="owner_name"
                        value={formData.owner_name}
                        onChange={handleInputChange}
                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('owner_name')}`}
                        placeholder="Your full name"
                      />
                      {errors.owner_name && <p className="text-red-500 text-sm mt-1">{errors.owner_name}</p>}
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Your Email *
                      </label>
                      <input
                        type="email"
                        name="owner_email"
                        value={formData.owner_email}
                        onChange={handleInputChange}
                        className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('owner_email')}`}
                        placeholder="your@email.com"
                      />
                      {errors.owner_email && <p className="text-red-500 text-sm mt-1">{errors.owner_email}</p>}
                    </div>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Your Phone Number *
                    </label>
                    <input
                      type="tel"
                      name="owner_phone"
                      value={formData.owner_phone}
                      onChange={handleInputChange}
                      className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('owner_phone')}`}
                      placeholder="(555) 123-4567"
                    />
                    {errors.owner_phone && <p className="text-red-500 text-sm mt-1">{errors.owner_phone}</p>}
                  </div>
                </div>
              </div>
            )}

            {/* Image Upload */}
            <ImageUpload
              onImageUpload={(imageUrl) => setFormData(prev => ({ ...prev, image_url: imageUrl }))}
              currentImageUrl={formData.image_url}
            />
            {errors.image_url && <p className="text-red-500 text-sm mt-1">{errors.image_url}</p>}

            {/* Basic Information */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Establishment Information</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Restaurant Name *
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('name')}`}
                    placeholder="Enter restaurant name"
                  />
                  {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Short Description * (max 80 characters)
                  </label>
                  <input
                    type="text"
                    name="short_description"
                    value={formData.short_description}
                    onChange={handleInputChange}
                    maxLength={80}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('short_description')}`}
                    placeholder="Brief description for mobile display"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>{errors.short_description}</span>
                    <span>{formData.short_description.length}/80</span>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Full Description (optional)
                  </label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    placeholder="Tell us about this establishment..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Address *
                  </label>
                  <input
                    type="text"
                    name="address"
                    value={formData.address}
                    onChange={handleInputChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('address')}`}
                    placeholder="Full street address"
                  />
                  {errors.address && <p className="text-red-500 text-sm mt-1">{errors.address}</p>}
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number *</label>
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('phone')}`}
                      placeholder="(555) 123-4567"
                    />
                    {errors.phone && <p className="text-red-500 text-sm mt-1">{errors.phone}</p>}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Email (optional)</label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('email')}`}
                      placeholder="contact@restaurant.com"
                    />
                    {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Website (optional)</label>
                    <input
                      type="url"
                      name="website"
                      value={formData.website}
                      onChange={handleInputChange}
                      className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('website')}`}
                      placeholder="https://example.com"
                    />
                    {errors.website && <p className="text-red-500 text-sm mt-1">{errors.website}</p>}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Google Maps Link (optional)</label>
                    <input
                      type="url"
                      name="google_listing_url"
                      value={formData.google_listing_url}
                      onChange={handleInputChange}
                      className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('google_listing_url')}`}
                      placeholder="https://maps.google.com/..."
                    />
                    {errors.google_listing_url && <p className="text-red-500 text-sm mt-1">{errors.google_listing_url}</p>}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Hours Open *</label>
                    <input
                      type="text"
                      name="hours_open"
                      value={formData.hours_open}
                      onChange={handleInputChange}
                      className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('hours_open')}`}
                      placeholder="Mon-Fri 11AM-10PM, Sat-Sun 12PM-11PM"
                    />
                    {errors.hours_open && <p className="text-red-500 text-sm mt-1">{errors.hours_open}</p>}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Price Range (optional)</label>
                    <select
                      name="price_range"
                      value={formData.price_range}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-jewgo-primary focus:border-transparent"
                    >
                      <option value="">Select price range</option>
                      <option value="$">$ (Under $15)</option>
                      <option value="$$">$$ ($15-$30)</option>
                      <option value="$$$">$$$ ($30-$60)</option>
                      <option value="$$$$">$$$$ (Over $60)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>

            {/* Kosher Information */}
            <div>
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Kosher Information</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Certifying Agency *
                  </label>
                  <select
                    name="certifying_agency"
                    value={formData.certifying_agency}
                    onChange={handleInputChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('certifying_agency')}`}
                  >
                    <option value="">Select certifying agency</option>
                    <option value="ORB">ORB</option>
                    <option value="KM">KM (Cholov Yisroel)</option>
                    <option value="KDM">KDM (Mixed)</option>
                    <option value="Diamond K">Diamond K</option>
                    <option value="OU">OU</option>
                    <option value="Other">Other</option>
                  </select>
                  {errors.certifying_agency && <p className="text-red-500 text-sm mt-1">{errors.certifying_agency}</p>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Kosher Category *
                  </label>
                  <select
                    name="kosher_category"
                    value={formData.kosher_category}
                    onChange={handleInputChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('kosher_category')}`}
                  >
                    <option value="">Select category</option>
                    <option value="meat">Meat</option>
                    <option value="dairy">Dairy</option>
                    <option value="pareve">Pareve</option>
                  </select>
                  {errors.kosher_category && <p className="text-red-500 text-sm mt-1">{errors.kosher_category}</p>}
                </div>

                {/* Conditional Kosher Fields */}
                {formData.kosher_category === 'dairy' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      Dairy Type *
                    </label>
                    <div className="space-y-2">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="is_cholov_yisroel"
                          value="true"
                          checked={formData.is_cholov_yisroel === true}
                          onChange={handleInputChange}
                          className="mr-2 text-jewgo-primary focus:ring-jewgo-primary"
                        />
                        Chalav Yisrael (Supervised milking)
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="is_cholov_yisroel"
                          value="false"
                          checked={formData.is_cholov_yisroel === false}
                          onChange={handleInputChange}
                          className="mr-2 text-jewgo-primary focus:ring-jewgo-primary"
                        />
                        Chalav Stam (Regular supervision)
                      </label>
                    </div>
                    {errors.is_cholov_yisroel && <p className="text-red-500 text-sm mt-1">{errors.is_cholov_yisroel}</p>}
                  </div>
                )}

                {['meat', 'pareve'].includes(formData.kosher_category) && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-3">
                      Pas Yisroel *
                    </label>
                    <div className="space-y-2">
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="is_pas_yisroel"
                          value="true"
                          checked={formData.is_pas_yisroel === true}
                          onChange={handleInputChange}
                          className="mr-2 text-jewgo-primary focus:ring-jewgo-primary"
                        />
                        Yes - Pas Yisroel (Jewish-owned bakery)
                      </label>
                      <label className="flex items-center">
                        <input
                          type="radio"
                          name="is_pas_yisroel"
                          value="false"
                          checked={formData.is_pas_yisroel === false}
                          onChange={handleInputChange}
                          className="mr-2 text-jewgo-primary focus:ring-jewgo-primary"
                        />
                        No - Regular supervision
                      </label>
                    </div>
                    {errors.is_pas_yisroel && <p className="text-red-500 text-sm mt-1">{errors.is_pas_yisroel}</p>}
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Certification Link (optional)
                  </label>
                  <input
                    type="url"
                    name="kosher_cert_link"
                    value={formData.kosher_cert_link}
                    onChange={handleInputChange}
                    className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:border-transparent ${getErrorClass('kosher_cert_link')}`}
                    placeholder="https://example.com/certification.pdf"
                  />
                  {errors.kosher_cert_link && <p className="text-red-500 text-sm mt-1">{errors.kosher_cert_link}</p>}
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-4">
              <button
                type="submit"
                disabled={isSubmitting || !userType}
                className="w-full bg-jewgo-primary text-white py-3 px-6 rounded-lg font-medium hover:bg-jewgo-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Submitting...</span>
                  </div>
                ) : (
                  userType === 'owner' ? 'Submit as Owner' : 'Submit for Review'
                )}
              </button>
            </div>

            {/* Note */}
            <div className="text-center text-sm text-gray-500">
              <p>
                {userType === 'owner' 
                  ? 'As an owner, you\'ll receive priority review and additional listing features.'
                  : 'All community submissions are reviewed before being added to the directory.'
                }
              </p>
            </div>
          </form>
        </div>
      </div>

      {/* Bottom Navigation */}
      <BottomNavigation />
    </div>
  );
} 