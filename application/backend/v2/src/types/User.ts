export type User = {
  id: string;
  displayName?: string | null;
  jobTitle?: string | null;
  department?: string | null;
  createdDateTime?: string | null;
  accountEnabled?: boolean;
  onPremisesSyncEnabled?: boolean;
  preferredLanguage?: string | null;
  role: string;
};
