import { fetchPlaceDetails } from "@/lib/google/places";
import { db } from "@/lib/db";

export async function updateRestaurantHours(restaurantId: number, placeId: string) {
  const { hoursText, hoursJson, timezone } = await fetchPlaceDetails(placeId);

  await db.restaurant.update({
    where: { id: restaurantId },
    data: {
      hours_of_operation: hoursText,
      hours_json: hoursJson,
      hours_last_updated: new Date(),
      timezone
    }
  });
}