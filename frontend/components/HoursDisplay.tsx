interface Props {
  hoursOfOperation: string;
}

export default function HoursDisplay({ hoursOfOperation }: Props) {
  const weekday = new Date().getDay(); // 0 = Sunday
  const lines = hoursOfOperation.split("\n");
  const today = lines[weekday];

  return (
    <div className="text-sm text-gray-800">
      <p><strong>Today:</strong> {today}</p>
      <details className="mt-1">
        <summary className="cursor-pointer text-blue-600">View all hours</summary>
        <ul className="list-disc ml-4 mt-1">
          {lines.map((line, i) => (
            <li key={i}>{line}</li>
          ))}
        </ul>
      </details>
    </div>
  );
}