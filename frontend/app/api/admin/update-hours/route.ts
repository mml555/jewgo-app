import { updateRestaurantHours } from "@/db/sync/updateHours";

export async function POST(req: Request) {
  const { id } = await req.json();
  await updateRestaurantHours(id);
  return new Response("Updated", { status: 200 });
}