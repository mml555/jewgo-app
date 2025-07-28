'use client';

import React, { useState } from 'react';
import { Restaurant } from '../types/restaurant';

interface Review {
  author_name?: string;
  author_url?: string;
  language?: string;
  profile_photo_url?: string;
  rating?: number;
  relative_time_description?: string;
  text: string;
  time: number;
  translated?: boolean;
  user?: {
    id: string;
    profile_url: string;
    image_url: string;
    name: string;
  };
}

interface ReviewsProps {
  restaurant: Restaurant;
  onWriteReview?: () => void;
}

const Reviews: React.FC<ReviewsProps> = ({ restaurant, onWriteReview }) => {
  const [showAllReviews, setShowAllReviews] = useState(false);

  // Parse review JSON strings
  const googleReviews: Review[] = restaurant.google_reviews 
    ? JSON.parse(restaurant.google_reviews) 
    : [];

  const hasGoogleReviews = googleReviews.length > 0;
  const hasAnyReviews = hasGoogleReviews;

  if (!hasAnyReviews) {
    return (
      <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">Reviews & Ratings</h2>
          {onWriteReview && (
            <button
              onClick={onWriteReview}
              className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors"
            >
              Write Review
            </button>
          )}
        </div>
        <div className="text-center text-gray-500">
          <p>No reviews available yet.</p>
          <p className="text-sm mt-2">Check back later for customer reviews!</p>
          {onWriteReview && (
            <button
              onClick={onWriteReview}
              className="mt-4 bg-green-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-green-700 transition-colors"
            >
              Be the first to review!
            </button>
          )}
        </div>
      </div>
    );
  }

  const renderStars = (rating: number) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <svg key={i} className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      );
    }

    if (hasHalfStar) {
      stars.push(
        <svg key="half" className="w-4 h-4 text-yellow-400 fill-current" viewBox="0 0 20 20">
          <defs>
            <linearGradient id="halfStar">
              <stop offset="50%" stopColor="currentColor" />
              <stop offset="50%" stopColor="#e5e7eb" />
            </linearGradient>
          </defs>
          <path fill="url(#halfStar)" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      );
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(
        <svg key={`empty-${i}`} className="w-4 h-4 text-gray-300 fill-current" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
      );
    }

    return stars;
  };

  const renderReview = (review: Review, index: number) => (
    <div key={index} className="border-b border-gray-100 last:border-b-0 pb-4 last:pb-0">
      <div className="flex items-start space-x-3">
        {/* Profile Image */}
        <div className="flex-shrink-0">
          <img
            src={review.profile_photo_url || review.user?.image_url || '/default-avatar.svg'}
            alt={review.author_name || review.user?.name || 'Reviewer'}
            className="w-10 h-10 rounded-full object-cover"
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.src = '/default-avatar.svg';
            }}
          />
        </div>
        
        {/* Review Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2 mb-1">
            <span className="font-medium text-gray-900 truncate">
              {review.author_name || review.user?.name || 'Anonymous'}
            </span>
            <div className="flex items-center">
              {renderStars(review.rating || 0)}
            </div>
          </div>
          
          {review.relative_time_description && (
            <p className="text-sm text-gray-500 mb-2">
              {review.relative_time_description}
            </p>
          )}
          
          <p className="text-gray-700 leading-relaxed">
            {review.text}
          </p>
        </div>
      </div>
    </div>
  );

  const displayedReviews = showAllReviews ? googleReviews : googleReviews.slice(0, 3);

  return (
    <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-900">Reviews & Ratings</h2>
        {onWriteReview && (
          <button
            onClick={onWriteReview}
            className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition-colors"
          >
            Write Review
          </button>
        )}
      </div>
      
      <div className="space-y-4">
        {displayedReviews.map((review, index) => renderReview(review, index))}
      </div>
      
      {googleReviews.length > 3 && (
        <div className="mt-4 text-center">
          <button
            onClick={() => setShowAllReviews(!showAllReviews)}
            className="text-green-600 hover:text-green-700 font-medium text-sm"
          >
            {showAllReviews ? 'Show less' : `Show all ${googleReviews.length} reviews`}
          </button>
        </div>
      )}
    </div>
  );
};

export default Reviews; 