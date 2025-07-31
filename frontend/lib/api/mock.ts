// Mock API functions for profile page

export const mockExportUserData = async (): Promise<any> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  // Return mock user data
  return {
    profile: {
      name: 'Sarah Cohen',
      email: 'sarah.cohen@email.com',
      phone: '(305) 555-0123',
      location: 'Miami, FL',
      dietaryPreferences: ['dairy', 'pareve'],
      favoriteCertifications: ['ORB', 'KM']
    },
    favorites: [
      { id: 1, name: 'Kosher Deli', addedAt: '2024-01-15' },
      { id: 2, name: 'Miami Kosher Market', addedAt: '2024-01-10' }
    ],
    reviews: [
      { id: 1, restaurantName: 'Miami Kosher Market', rating: 5, comment: 'Great food!', date: '2024-01-12' }
    ],
    activity: {
      restaurantsVisited: 12,
      reviewsWritten: 8,
      favoritesSaved: 15,
      dealsClaimed: 5
    },
    exportDate: new Date().toISOString()
  };
};

export const mockDeleteAccount = async (password: string): Promise<void> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  // Simulate password validation
  if (password !== 'password123') {
    throw new Error('Invalid password');
  }
  
  // Simulate successful deletion
  return Promise.resolve();
};

export const mockClaimDeal = async (dealId: number): Promise<any> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  // Simulate random success/failure
  const success = Math.random() > 0.1; // 90% success rate
  
  if (!success) {
    throw new Error('Failed to claim deal. Please try again.');
  }
  
  return {
    success: true,
    dealId,
    claimedAt: new Date().toISOString(),
    message: 'Deal claimed successfully!'
  };
}; 