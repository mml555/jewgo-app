'use client';

import React from 'react';
import { RestaurantSpecial } from '@/types/restaurant';

interface SpecialsCardProps {
  specials: RestaurantSpecial[];
  maxDisplay?: number;
}

export default function SpecialsCard({ specials, maxDisplay = 3 }: SpecialsCardProps) {
  // Only show paid specials
  const paidSpecials = specials.filter(special => special.is_paid && special.is_active);
  
  if (paidSpecials.length === 0) {
    return null;
  }

  // Limit to maxDisplay
  const displaySpecials = paidSpecials.slice(0, maxDisplay);

  const formatDiscount = (special: RestaurantSpecial) => {
    if (special.discount_percent) {
      return `${special.discount_percent}% OFF`;
    }
    if (special.discount_amount) {
      return `$${special.discount_amount} OFF`;
    }
    return '';
  };

  return (
    <div className="mt-4">
      <div className="flex items-center space-x-2 mb-3">
        <span className="text-lg">🎯</span>
        <h3 className="text-lg font-bold text-gray-900">Our Specials</h3>
      </div>
      <div className="flex space-x-4 overflow-x-auto pb-2">
        {displaySpecials.map((special) => (
          <div
            key={special.id}
            className="bg-white border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow flex-shrink-0 w-48"
          >
            {/* Food Image - Better visuals with fallback icons */}
            <div className="h-32 bg-gray-200 relative">
              <div className="w-full h-full bg-gradient-to-br from-orange-100 to-red-100 flex items-center justify-center">
                {/* Better food icons based on special type */}
                {special.special_type === 'discount' && (
                  <div className="text-center">
                    <div className="text-4xl mb-2">🍔</div>
                    <div className="text-2xl">🍟</div>
                  </div>
                )}
                {special.special_type === 'promotion' && (
                  <div className="text-center">
                    <div className="text-4xl mb-2">🍣</div>
                    <div className="text-2xl">🥒</div>
                  </div>
                )}
                {special.special_type === 'event' && (
                  <div className="text-center">
                    <div className="text-4xl mb-2">🍹</div>
                    <div className="text-2xl">🍋</div>
                  </div>
                )}
              </div>
            </div>
            <div className="p-3">
              <h4 className="font-semibold text-sm text-gray-900 mb-1 line-clamp-1 leading-tight">
                {special.title}
              </h4>
              {formatDiscount(special) && (
                <p className="text-red-600 font-bold text-xs">{formatDiscount(special)}</p>
              )}
              {special.description && (
                <p className="text-gray-600 text-xs mt-1 line-clamp-2">
                  {special.description}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
} 