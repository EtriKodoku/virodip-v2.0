import * as process from "process";
import { MongoClient } from "mongodb";

const uri = process.env.MONGO_DB_URL;
const dbName = process.env.MONGO_DB_DATABASE_NAME;

let client: MongoClient;

if (!globalThis.mongoClientPromise) {
  client = new MongoClient(uri);
  globalThis.mongoClientPromise = client.connect();
}

export const getDb = async () => {
  const connectedClient = await globalThis.mongoClientPromise;
  return connectedClient.db(dbName);
};
