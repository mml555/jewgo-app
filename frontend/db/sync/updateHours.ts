export async function updateRestaurantHours(restaurantId: number) {
  try {
    // Call the backend API to fetch and update hours
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://jewgo.onrender.com';
    const response = await fetch(`${backendUrl}/api/restaurants/${restaurantId}/fetch-hours`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Backend API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error updating restaurant hours:', error);
    throw error;
  }
}