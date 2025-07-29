import dayjs from 'dayjs';
import isToday from 'dayjs/plugin/isToday';
import isTomorrow from 'dayjs/plugin/isTomorrow';
import relativeTime from 'dayjs/plugin/relativeTime';

dayjs.extend(isToday);
dayjs.extend(isTomorrow);
dayjs.extend(relativeTime);

export interface HoursStatus {
  badge: string;
  label: string;
  type: 'open' | 'opensToday' | 'opensTomorrow' | 'opensLater' | 'closed' | 'unknown';
  tooltip: string;
  icon: string;
  isOpenNow: boolean;
  isClosedForToday: boolean;
  nextOpenTime?: string;
  closingTime?: string;
  subtext?: string;
}

export interface OpeningHours {
  day: string;
  open: string;
  close: string;
}

// Helper to convert time string to minutes
const timeToMinutes = (timeStr: string): number => {
  const match = timeStr.match(/(\d{1,2}):?(\d{2})?\s*(AM|PM)/i);
  if (match) {
    let hours = parseInt(match[1]);
    const minutes = match[2] ? parseInt(match[2]) : 0;
    const period = match[3].toUpperCase();

    if (period === 'PM' && hours !== 12) hours += 12;
    if (period === 'AM' && hours === 12) hours = 0;

    return hours * 60 + minutes;
  }
  return 0;
};

// Helper to format time for display
const formatTimeDisplay = (timeStr: string): string => {
  const match = timeStr.match(/(\d{1,2}):?(\d{2})?\s*(AM|PM)/i);
  if (match) {
    const hours = parseInt(match[1]);
    const minutes = match[2] ? parseInt(match[2]) : 0;
    const period = match[3].toUpperCase();
    return `${hours}:${minutes.toString().padStart(2, '0')} ${period}`;
  }
  return timeStr;
};

// Parse hours from various formats
const parseHoursData = (hoursData: any): OpeningHours[] | null => {
  if (!hoursData) return null;

  try {
    // Try to parse as JSON first
    const hours = typeof hoursData === 'string' ? JSON.parse(hoursData) : hoursData;
    
    if (typeof hours === 'object' && hours !== null) {
      const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
      const parsed: OpeningHours[] = [];
      
      days.forEach((day, index) => {
        const dayHours = hours[day];
        if (dayHours && dayHours.open && dayHours.close) {
          parsed.push({
            day: day,
            open: dayHours.open,
            close: dayHours.close
          });
        }
      });
      
      return parsed.length > 0 ? parsed : null;
    }
  } catch (error) {
    // Handle human-readable string format
    if (typeof hoursData === 'string') {
      const dayMatches = [
        { day: 'monday', pattern: /Mon\s+([^-–]+)[-–]([^,]+)/i },
        { day: 'tuesday', pattern: /Tue\s+([^-–]+)[-–]([^,]+)/i },
        { day: 'wednesday', pattern: /Wed\s+([^-–]+)[-–]([^,]+)/i },
        { day: 'thursday', pattern: /Thu\s+([^-–]+)[-–]([^,]+)/i },
        { day: 'friday', pattern: /Fri\s+([^-–]+)[-–]([^,]+)/i },
        { day: 'saturday', pattern: /Sat\s+([^-–]+)[-–]([^,]+)/i },
        { day: 'sunday', pattern: /Sun\s+([^-–]+)[-–]([^,]+)/i }
      ];
      
      const parsed: OpeningHours[] = [];
      
      dayMatches.forEach(({ day, pattern }) => {
        const match = hoursData.match(pattern);
        if (match && !match[1].toLowerCase().includes('closed')) {
          parsed.push({
            day: day,
            open: match[1].trim(),
            close: match[2].trim()
          });
        }
      });
      
      return parsed.length > 0 ? parsed : null;
    }
  }
  
  return null;
};

export function getHoursStatus(hoursData: any): HoursStatus {
  const now = dayjs();
  const currentTime = now.hour() * 60 + now.minute();
  const today = now.format('dddd').toLowerCase();
  const todayIndex = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'].indexOf(today);
  
  const parsedHours = parseHoursData(hoursData);
  
  if (!parsedHours || parsedHours.length === 0) {
    return {
      badge: 'text-gray-500',
      label: 'Hours not available',
      type: 'unknown',
      tooltip: 'Hours information not available',
      icon: '⏰',
      isOpenNow: false,
      isClosedForToday: true
    };
  }
  
  // Find today's hours
  const todayHours = parsedHours.find(h => h.day === today);
  
  if (todayHours) {
    const openMins = timeToMinutes(todayHours.open);
    const closeMins = timeToMinutes(todayHours.close);
    
    if (currentTime >= openMins && currentTime < closeMins) {
      return {
        badge: 'text-green-600',
        label: `Open now • Closes ${formatTimeDisplay(todayHours.close)}`,
        type: 'open',
        tooltip: `${todayHours.open} - ${todayHours.close}`,
        icon: '🟢',
        isOpenNow: true,
        isClosedForToday: false,
        closingTime: formatTimeDisplay(todayHours.close)
      };
    } else if (currentTime < openMins) {
      return {
        badge: 'text-red-600',
        label: `Opens ${formatTimeDisplay(todayHours.open)}`,
        type: 'opensToday',
        tooltip: `Opens ${todayHours.open}`,
        icon: '🔴',
        isOpenNow: false,
        isClosedForToday: false,
        nextOpenTime: formatTimeDisplay(todayHours.open)
      };
    }
  }
  
  // Closed for today, find next opening
  for (let i = 1; i <= 7; i++) {
    const nextDayIndex = (todayIndex + i) % 7;
    const nextDay = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][nextDayIndex];
    const nextDayHours = parsedHours.find(h => h.day === nextDay);
    
    if (nextDayHours) {
      const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
      const dayName = dayNames[nextDayIndex];
      
      if (i === 1) {
        return {
          badge: 'text-red-600',
          label: `Opens ${formatTimeDisplay(nextDayHours.open)} tomorrow`,
          type: 'opensTomorrow',
          tooltip: `Opens ${nextDayHours.open} tomorrow`,
          icon: '🔴',
          isOpenNow: false,
          isClosedForToday: true,
          nextOpenTime: formatTimeDisplay(nextDayHours.open)
        };
      } else {
        return {
          badge: 'text-red-600',
          label: `Opens ${formatTimeDisplay(nextDayHours.open)} ${dayName}`,
          type: 'opensLater',
          tooltip: `Opens ${nextDayHours.open} ${dayName}`,
          icon: '🔴',
          isOpenNow: false,
          isClosedForToday: true,
          nextOpenTime: formatTimeDisplay(nextDayHours.open)
        };
      }
    }
  }
  
  // If no next opening found, show closed
  return {
    badge: 'text-red-600',
    label: 'Closed',
    type: 'closed',
    tooltip: 'Currently closed',
    icon: '🔴',
    isOpenNow: false,
    isClosedForToday: true
  };
}

// Format full weekly hours for display (string format)
export function formatWeeklyHours(hoursData: any): string {
  const parsedHours = parseHoursData(hoursData);
  
  if (!parsedHours) {
    return 'Hours not available';
  }
  
  const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
  
  return days.map((day, index) => {
    const dayHours = parsedHours.find(h => h.day === day);
    if (dayHours) {
      return `${dayNames[index]} ${dayHours.open}–${dayHours.close}`;
    }
    return `${dayNames[index]} Closed`;
  }).join(', ');
}

// Format weekly hours as array of objects for card display
export function formatWeeklyHoursArray(hoursData: any): Array<{day: string, hours: string}> | null {
  const parsedHours = parseHoursData(hoursData);
  
  if (!parsedHours) {
    return null;
  }
  
  const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
  
  return days.map((day, index) => {
    const dayHours = parsedHours.find(h => h.day === day);
    if (dayHours) {
      return {
        day: dayNames[index],
        hours: `${dayHours.open}–${dayHours.close}`
      };
    }
    return {
      day: dayNames[index],
      hours: 'Closed'
    };
  });
} 