export async function fetchPlaceDetails(place_id: string): Promise<{
  hoursText: string,
  hoursJson: any[],
  timezone: string
}> {
  const res = await fetch(
    `https://maps.googleapis.com/maps/api/place/details/json?place_id=${place_id}&fields=opening_hours,utc_offset_minutes&key=${process.env.GOOGLE_API_KEY}`
  );
  const data = await res.json();
  const periods = data.result.opening_hours?.periods || [];
  const weekdayText = data.result.opening_hours?.weekday_text || [];
  const offset = data.result.utc_offset_minutes;

  return {
    hoursText: weekdayText.join("\n"),
    hoursJson: periods,
    timezone: offsetToTimezone(offset)
  };
}

function offsetToTimezone(offset: number): string {
  // Simple mapping for common US timezones
  switch (offset) {
    case -300: return 'America/New_York';
    case -360: return 'America/Chicago';
    case -420: return 'America/Denver';
    case -480: return 'America/Los_Angeles';
    default: return 'UTC';
  }
}