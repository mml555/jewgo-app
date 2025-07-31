import { getTodayHours, formatHours, isOpenNow, formatTime } from '@/lib/utils/hours';

interface Props {
  hoursOfOperation?: string;
  hoursJson?: any[];
  hoursLastUpdated?: string;
}

export default function HoursDisplay({ hoursOfOperation, hoursJson, hoursLastUpdated }: Props) {
  if (!hoursOfOperation) {
    return <div className="text-sm text-gray-500">Hours not available</div>;
  }

  const todayHours = getTodayHours(hoursOfOperation);
  const allHours = formatHours(hoursOfOperation);
  const isOpen = hoursJson ? isOpenNow(hoursJson) : null;

  return (
    <div className="text-sm text-gray-800">
      <div className="flex items-center gap-2">
        <p><strong>Today:</strong> {todayHours}</p>
        {isOpen !== null && (
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
            isOpen ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            {isOpen ? 'Open' : 'Closed'}
          </span>
        )}
      </div>
      
      <details className="mt-1">
        <summary className="cursor-pointer text-blue-600 hover:text-blue-800">
          View all hours
        </summary>
        <ul className="list-disc ml-4 mt-1 space-y-1">
          {allHours.map((line, i) => (
            <li key={i} className="text-gray-700">{line}</li>
          ))}
        </ul>
      </details>
      
      {hoursLastUpdated && (
        <p className="text-xs text-gray-500 mt-2">
          Last updated: {new Date(hoursLastUpdated).toLocaleDateString()}
        </p>
      )}
    </div>
  );
}