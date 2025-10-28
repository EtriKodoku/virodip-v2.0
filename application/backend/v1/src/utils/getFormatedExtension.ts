import { AZURE_CONFIG } from "../config";

const { extensionAppId } = AZURE_CONFIG;

export const getFormatedExtension = (extensionName: string) => {
  return `extension_${extensionAppId}_${extensionName}`;
};
