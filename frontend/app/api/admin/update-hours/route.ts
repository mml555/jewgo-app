import { updateRestaurantHours } from "@/db/sync/updateHours";

export async function POST(req: Request) {
  const { id, placeId } = await req.json();
  await updateRestaurantHours(id, placeId);
  return new Response("Updated", { status: 200 });
}