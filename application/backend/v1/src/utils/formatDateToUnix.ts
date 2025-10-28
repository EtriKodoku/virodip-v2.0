export const formatDateToUnix = (date: string | number | Date) => {
  return new Date(date).getTime();
};
