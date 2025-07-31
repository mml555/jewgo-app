export function formatHours(hoursText: string): string[] {
  return hoursText.split('\n').filter(line => line.trim() !== '');
}

export function getTodayHours(hoursText: string): string {
  const lines = formatHours(hoursText);
  const weekday = new Date().getDay(); // 0 = Sunday
  return lines[weekday] || 'Hours not available';
}

export function isOpenNow(hoursJson: any[]): boolean {
  if (!hoursJson || hoursJson.length === 0) return false;
  
  const now = new Date();
  const currentDay = now.getDay(); // 0 = Sunday
  const currentTime = now.getHours() * 100 + now.getMinutes(); // HHMM format
  
  const todayPeriods = hoursJson.filter(period => period.open.day === currentDay);
  
  return todayPeriods.some(period => {
    const openTime = period.open.time;
    const closeTime = period.close?.time || '2359';
    
    const openMinutes = parseInt(openTime.slice(0, 2)) * 60 + parseInt(openTime.slice(2));
    const closeMinutes = parseInt(closeTime.slice(0, 2)) * 60 + parseInt(closeTime.slice(2));
    const currentMinutes = now.getHours() * 60 + now.getMinutes();
    
    return currentMinutes >= openMinutes && currentMinutes <= closeMinutes;
  });
}

export function formatTime(time: string): string {
  // Convert "1430" to "2:30 PM"
  const hours = parseInt(time.slice(0, 2));
  const minutes = time.slice(2);
  const ampm = hours >= 12 ? 'PM' : 'AM';
  const displayHours = hours > 12 ? hours - 12 : hours === 0 ? 12 : hours;
  return `${displayHours}:${minutes} ${ampm}`;
} 