export const formatInGmt5 = (
  date: string | Date | null | undefined,
  options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }
): string => {
  if (!date) return '—';

  const dateObj = typeof date === 'string' ? new Date(date) : date;


  const formatter = new Intl.DateTimeFormat('ru-RU', {
    ...options,
    timeZone: 'Asia/Yekaterinburg',
  });

  return formatter.format(dateObj);
};


export const dateOnlyInGmt5 = (date: string | Date | null | undefined): string => {
  return formatInGmt5(date, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
};


export const timeOnlyInGmt5 = (date: string | Date | null | undefined): string => {
  return formatInGmt5(date, {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
};